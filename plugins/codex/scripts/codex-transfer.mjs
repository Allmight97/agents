#!/usr/bin/env node

import crypto from "node:crypto";
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import readline from "node:readline";

const TRANSCRIPT_PATH_ENV = "CODEX_PLUGIN_TRANSCRIPT_PATH";
const CLAUDE_PROJECTS_DIR = path.join(os.homedir(), ".claude", "projects");
const CODEX_HOME = path.resolve(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"));
const IMPORT_COMPLETED_METHOD = "externalAgentConfig/import/completed";
const IMPORT_TIMEOUT_MS = 2 * 60 * 1000;
const PLUGIN_VERSION = "0.3.0";

function shellEscape(value) {
  return `'${String(value).replace(/'/g, `'\"'\"'`)}'`;
}

function appendEnvVar(name, value) {
  if (!process.env.CLAUDE_ENV_FILE || value == null || value === "") {
    return;
  }
  fs.appendFileSync(process.env.CLAUDE_ENV_FILE, `export ${name}=${shellEscape(value)}\n`, "utf8");
}

function readHookInput() {
  const raw = fs.readFileSync(0, "utf8").trim();
  return raw ? JSON.parse(raw) : {};
}

function handleSessionStart() {
  const input = readHookInput();
  appendEnvVar(TRANSCRIPT_PATH_ENV, input.transcript_path);
}

function usage() {
  return [
    "Usage:",
    "  node scripts/codex-transfer.mjs [--source <claude-jsonl>]",
    "  node scripts/codex-transfer.mjs session-start"
  ].join("\n");
}

function parseArgs(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--source") {
      const next = argv[index + 1];
      if (!next) {
        throw new Error("Missing value for --source.");
      }
      options.source = next;
      index += 1;
      continue;
    }
    if (token.startsWith("--source=")) {
      options.source = token.slice("--source=".length);
      continue;
    }
    if (token === "--help" || token === "-h") {
      options.help = true;
      continue;
    }
    throw new Error(`Unknown argument: ${token}`);
  }
  return options;
}

function resolveUserPath(cwd, value) {
  if (value === "~") {
    return os.homedir();
  }
  if (String(value).startsWith("~/")) {
    return path.join(os.homedir(), String(value).slice(2));
  }
  return path.isAbsolute(value) ? value : path.resolve(cwd, value);
}

function resolveClaudeSessionPath(cwd, options = {}) {
  const requestedPath = options.source || process.env[TRANSCRIPT_PATH_ENV];
  if (!requestedPath) {
    throw new Error("Could not identify the current Claude transcript. Retry with --source <path-to-claude-jsonl>.");
  }

  const sourcePath = resolveUserPath(cwd, requestedPath);
  if (path.extname(sourcePath) !== ".jsonl") {
    throw new Error(`Claude session source must be a JSONL file: ${sourcePath}`);
  }

  let source;
  try {
    source = fs.realpathSync(sourcePath);
  } catch {
    throw new Error(`Claude session file not found: ${sourcePath}`);
  }

  let projects;
  try {
    projects = fs.realpathSync(CLAUDE_PROJECTS_DIR);
  } catch {
    throw new Error(`Claude projects directory not found: ${CLAUDE_PROJECTS_DIR}`);
  }

  const relative = path.relative(projects, source);
  if (relative === "" || relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new Error(`Codex can import Claude sessions only from ${CLAUDE_PROJECTS_DIR}: ${source}`);
  }
  return source;
}

function externalAgentSessionMigration(sourcePath, cwd) {
  return {
    migrationItems: [
      {
        itemType: "SESSIONS",
        description: `Transfer Claude session ${path.basename(sourcePath)}`,
        cwd: null,
        details: {
          plugins: [],
          sessions: [{ path: sourcePath, cwd, title: null }],
          mcpServers: [],
          hooks: [],
          subagents: [],
          commands: []
        }
      }
    ]
  };
}

function sourceContentSha256(sourcePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(sourcePath)).digest("hex");
}

function readJsonFile(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function importedThreadIdForSource(sourcePath) {
  const ledgerPath = path.join(CODEX_HOME, "external_agent_session_imports.json");
  if (!fs.existsSync(ledgerPath)) {
    return null;
  }

  const ledger = readJsonFile(ledgerPath);
  const canonicalSource = fs.realpathSync(sourcePath);
  const contentSha256 = sourceContentSha256(canonicalSource);
  const records = Array.isArray(ledger?.records) ? ledger.records : [];
  const match = records
    .filter(
      (record) =>
        record?.source_path === canonicalSource &&
        record?.content_sha256 === contentSha256 &&
        typeof record?.imported_thread_id === "string"
    )
    .at(-1);
  if (match?.imported_thread_id) {
    return match.imported_thread_id;
  }

  const sourcePathMatch = records
    .filter((record) => record?.source_path === canonicalSource && typeof record?.imported_thread_id === "string")
    .at(-1);
  return sourcePathMatch?.imported_thread_id ?? null;
}

class AppServerClient {
  constructor(cwd) {
    this.cwd = cwd;
    this.nextId = 1;
    this.pending = new Map();
    this.stderr = "";
    this.notificationHandler = null;
  }

  async connect() {
    this.proc = spawn("codex", ["app-server"], {
      cwd: this.cwd,
      env: process.env,
      stdio: ["pipe", "pipe", "pipe"],
      shell: false,
      windowsHide: true
    });

    this.proc.stderr.setEncoding("utf8");
    this.proc.stderr.on("data", (chunk) => {
      this.stderr += chunk;
    });

    this.proc.on("error", (error) => {
      this.rejectAll(error);
    });
    this.proc.on("exit", (code, signal) => {
      if (code === 0 && this.pending.size === 0) {
        return;
      }
      const detail = this.stderr.trim();
      const message =
        code === 0
          ? "codex app-server exited before replying to all pending requests."
          : `codex app-server exited unexpectedly (${signal ? `signal ${signal}` : `exit ${code}`}).${detail ? `\n${detail}` : ""}`;
      this.rejectAll(new Error(message));
    });

    const lines = readline.createInterface({ input: this.proc.stdout });
    lines.on("line", (line) => this.handleLine(line));
    this.lines = lines;

    await this.request("initialize", {
      clientInfo: {
        title: "Personal Codex Plugin",
        name: "Claude Code",
        version: PLUGIN_VERSION
      },
      capabilities: {
        experimentalApi: false,
        requestAttestation: false,
        optOutNotificationMethods: [
          "item/agentMessage/delta",
          "item/reasoning/summaryTextDelta",
          "item/reasoning/summaryPartAdded",
          "item/reasoning/textDelta"
        ]
      }
    });
    this.notify("initialized", {});
  }

  rejectAll(error) {
    for (const pending of this.pending.values()) {
      pending.reject(error);
    }
    this.pending.clear();
  }

  handleLine(line) {
    if (!line.trim()) {
      return;
    }

    let message;
    try {
      message = JSON.parse(line);
    } catch (error) {
      this.rejectAll(new Error(`Failed to parse codex app-server JSONL: ${error.message}`));
      return;
    }

    if (message.id !== undefined && message.method) {
      this.send({
        id: message.id,
        error: {
          code: -32601,
          message: `Unsupported server request: ${message.method}`
        }
      });
      return;
    }

    if (message.id !== undefined) {
      const pending = this.pending.get(message.id);
      if (!pending) {
        return;
      }
      this.pending.delete(message.id);
      if (message.error) {
        const error = new Error(message.error.message || `codex app-server ${pending.method} failed.`);
        error.rpcCode = message.error.code;
        error.data = message.error;
        pending.reject(error);
      } else {
        pending.resolve(message.result || {});
      }
      return;
    }

    if (message.method && this.notificationHandler) {
      this.notificationHandler(message);
    }
  }

  send(message) {
    this.proc.stdin.write(`${JSON.stringify(message)}\n`);
  }

  request(method, params) {
    const id = this.nextId;
    this.nextId += 1;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { method, resolve, reject });
      this.send({ id, method, params });
    });
  }

  notify(method, params = {}) {
    this.send({ method, params });
  }

  async close() {
    if (this.lines) {
      this.lines.close();
    }
    if (this.proc && !this.proc.killed) {
      this.proc.stdin.end();
      this.proc.kill("SIGTERM");
    }
  }
}

async function requestImport(client, params) {
  let timeout;
  let resolveCompleted;
  let rejectCompleted;
  const completed = new Promise((resolve, reject) => {
    resolveCompleted = resolve;
    rejectCompleted = reject;
  });
  void completed.catch(() => {});

  client.notificationHandler = (message) => {
    if (message.method === IMPORT_COMPLETED_METHOD) {
      resolveCompleted();
    }
  };

  timeout = setTimeout(() => {
    rejectCompleted(new Error("Timed out waiting for Codex to finish importing the Claude session."));
  }, IMPORT_TIMEOUT_MS);

  try {
    await client.request("externalAgentConfig/import", params);
    await completed;
  } catch (error) {
    if (error?.rpcCode === -32601) {
      throw new Error("This Codex version does not support Claude session transfer. Update Codex, then retry.");
    }
    throw error;
  } finally {
    clearTimeout(timeout);
    client.notificationHandler = null;
  }
}

async function transfer(options) {
  const cwd = process.cwd();
  const sourcePath = resolveClaudeSessionPath(cwd, options);
  const client = new AppServerClient(cwd);

  await client.connect();
  try {
    await requestImport(client, externalAgentSessionMigration(sourcePath, cwd));
  } finally {
    await client.close();
  }

  const threadId = importedThreadIdForSource(sourcePath);
  if (!threadId) {
    throw new Error("Codex reported that import completed, but no imported thread was recorded.");
  }

  process.stdout.write(
    [
      "Transferred the Claude session into a Codex thread with visible turn history.",
      `Codex session ID: ${threadId}`,
      `Resume in Codex: codex resume ${threadId}`,
      ""
    ].join("\n")
  );
}

async function main() {
  if (process.argv[2] === "session-start") {
    handleSessionStart();
    return;
  }

  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write(`${usage()}\n`);
    return;
  }
  await transfer(options);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
});
