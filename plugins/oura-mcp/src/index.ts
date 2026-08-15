import { DurableObject } from "cloudflare:workers";
import { createMcpHandler, McpServer } from "@modelcontextprotocol/server";
import { createRemoteJWKSet, jwtVerify } from "jose";
import { z } from "zod";
import {
  catalogPayload,
  collectionNames,
  collectionSpec,
  type CollectionSpec
} from "./catalog";

type Env = {
  AUTH0_ISSUER: string;
  AUTH0_AUDIENCE: string;
  OURA_CLIENT_ID: string;
  OURA_CLIENT_SECRET: string;
  OURA_REDIRECT_URI: string;
  SETUP_KEY: string;
  OURA_CREDENTIAL: DurableObjectNamespace<OuraCredential>;
};

type OuraToken = {
  access_token: string;
  refresh_token: string;
  expires_at: number;
  scope?: string;
  [key: string]: unknown;
};

type Query = {
  collection: string;
  start?: string;
  end?: string;
  cursor?: string;
  latest?: boolean;
};

const jwks = new Map<string, ReturnType<typeof createRemoteJWKSet>>();

export class OuraCredential extends DurableObject<Env> {
  private refreshInFlight?: Promise<OuraToken>;

  async catalog(): Promise<Record<string, unknown>> {
    const token = await this.ctx.storage.get<OuraToken>("token");
    return {
      ...catalogPayload(),
      oura_authorized: Boolean(token),
      granted_scopes: token?.scope?.split(/\s+/).filter(Boolean) ?? []
    };
  }

  async authorizationUrl(): Promise<string> {
    const state = crypto.randomUUID();
    await this.ctx.storage.put("oauth_state", { state, issuedAt: Date.now() });
    const url = new URL("https://cloud.ouraring.com/oauth/authorize");
    url.search = new URLSearchParams({
      response_type: "code",
      client_id: this.env.OURA_CLIENT_ID,
      redirect_uri: this.env.OURA_REDIRECT_URI,
      state
    }).toString();
    return url.toString();
  }

  async completeAuthorization(code: string, state: string, grantedScope?: string): Promise<void> {
    const saved = await this.ctx.storage.get<{ state: string; issuedAt: number }>("oauth_state");
    await this.ctx.storage.delete("oauth_state");
    if (!saved || saved.state !== state || Date.now() - saved.issuedAt > 10 * 60 * 1000) {
      throw new Error("Oura authorization state is invalid or expired.");
    }
    const token = await this.exchangeToken({
      grant_type: "authorization_code",
      code,
      client_id: this.env.OURA_CLIENT_ID,
      client_secret: this.env.OURA_CLIENT_SECRET,
      redirect_uri: this.env.OURA_REDIRECT_URI
    });
    if (grantedScope) token.scope = grantedScope;
    await this.ctx.storage.put("token", token);
  }

  async query(input: Query): Promise<Record<string, unknown>> {
    const spec = collectionSpec(input.collection);
    validateQuery(spec, input);
    let token = await this.accessToken();
    let response = await this.fetchCollection(spec, input, token);
    if (response.status === 401) {
      token = await this.accessToken(true);
      response = await this.fetchCollection(spec, input, token);
    }
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(`Oura ${response.status} for ${spec.name}: ${detail.slice(0, 300)}`);
    }
    const body = (await response.json()) as Record<string, unknown>;
    return {
      collection: spec.name,
      provenance: {
        provider: "oura",
        api_version: "v2",
        endpoint: `/v2/usercollection/${spec.path}`,
        retrieved_at: new Date().toISOString()
      },
      request: input,
      next_cursor: body.next_token ?? null,
      oura_response: body
    };
  }

  private async accessToken(force = false): Promise<string> {
    const token = await this.ctx.storage.get<OuraToken>("token");
    if (!token) throw new Error("Oura is not authorized yet.");
    if (!force && token.expires_at > Date.now() / 1000 + 60) return token.access_token;
    this.refreshInFlight ??= this.refresh(token).finally(() => {
      this.refreshInFlight = undefined;
    });
    return (await this.refreshInFlight).access_token;
  }

  private async refresh(previous: OuraToken): Promise<OuraToken> {
    const token = await this.exchangeToken({
      grant_type: "refresh_token",
      refresh_token: previous.refresh_token,
      client_id: this.env.OURA_CLIENT_ID,
      client_secret: this.env.OURA_CLIENT_SECRET
    }, previous.refresh_token);
    await this.ctx.storage.put("token", token);
    return token;
  }

  private async exchangeToken(
    values: Record<string, string>,
    priorRefreshToken?: string
  ): Promise<OuraToken> {
    const response = await fetch("https://api.ouraring.com/oauth/token", {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(values)
    });
    if (!response.ok) throw new Error(`Oura token exchange failed with ${response.status}.`);
    const raw = (await response.json()) as Record<string, unknown>;
    const accessToken = raw.access_token;
    const refreshToken = raw.refresh_token ?? priorRefreshToken;
    const expiresIn = raw.expires_in;
    if (typeof accessToken !== "string" || typeof refreshToken !== "string" || typeof expiresIn !== "number") {
      throw new Error("Oura returned an invalid token response.");
    }
    return {
      ...raw,
      access_token: accessToken,
      refresh_token: refreshToken,
      expires_at: Math.floor(Date.now() / 1000) + expiresIn
    };
  }

  private fetchCollection(spec: CollectionSpec, input: Query, accessToken: string) {
    const url = new URL(`https://api.ouraring.com/v2/usercollection/${spec.path}`);
    if (spec.rangeKind === "date") {
      url.searchParams.set("start_date", input.start!);
      url.searchParams.set("end_date", input.end!);
    } else if (spec.rangeKind === "datetime" && !input.latest) {
      url.searchParams.set("start_datetime", input.start!);
      url.searchParams.set("end_datetime", input.end!);
    }
    if (input.cursor) url.searchParams.set("next_token", input.cursor);
    if (input.latest) url.searchParams.set("latest", "true");
    return fetch(url, { headers: { authorization: `Bearer ${accessToken}` } });
  }
}

function createServer(env: Env) {
  const server = new McpServer({ name: "oura-private-data", version: "1.0.0" });
  const credential = env.OURA_CREDENTIAL.getByName("owner");

  server.registerTool(
    "oura_catalog",
    {
      description: "List every mapped Oura API v2 collection and its native query shape.",
      inputSchema: {},
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
    },
    async () => toolResult(await credential.catalog())
  );

  server.registerTool(
    "oura_query",
    {
      description: "Retrieve live Oura API v2 data without summarizing or interpreting it.",
      inputSchema: {
        collection: z.enum(collectionNames),
        start: z.string().optional(),
        end: z.string().optional(),
        cursor: z.string().optional(),
        latest: z.boolean().optional()
      },
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: true }
    },
    async (input) => toolResult(await credential.query(input))
  );

  return server;
}

function toolResult(value: Record<string, unknown>) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(value) }],
    structuredContent: value
  };
}

function validateQuery(spec: CollectionSpec, input: Query) {
  if (input.cursor && !spec.supportsCursor) throw new Error(`${spec.name} does not accept a cursor.`);
  if (input.latest && !spec.supportsLatest) throw new Error(`${spec.name} does not accept latest=true.`);
  if (input.latest && (input.start || input.end)) throw new Error("latest cannot be combined with bounds.");
  if (spec.rangeKind === "none") {
    if (input.start || input.end || input.latest) throw new Error(`${spec.name} does not accept bounds.`);
    return;
  }
  if (input.latest) return;
  if (!input.start || !input.end) throw new Error(`${spec.name} requires start and end.`);
  const start = parseBoundary(input.start, spec.rangeKind);
  const end = parseBoundary(input.end, spec.rangeKind);
  if (start > end) throw new Error("start must not be after end.");
  if (end.getTime() - start.getTime() > 90 * 86400000) throw new Error("The requested range exceeds 90 days.");
}

function parseBoundary(value: string, kind: "date" | "datetime") {
  if (kind === "date" && !/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error("Date bounds must use YYYY-MM-DD.");
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) throw new Error("Invalid date or datetime bound.");
  if (kind === "datetime" && !/(Z|[+-]\d{2}:\d{2})$/.test(value)) throw new Error("Datetime bounds require a timezone.");
  return parsed;
}

async function verifyMcpRequest(request: Request, env: Env) {
  const header = request.headers.get("authorization");
  if (!header?.startsWith("Bearer ")) return false;
  const issuer = env.AUTH0_ISSUER.replace(/\/$/, "");
  let keySet = jwks.get(issuer);
  if (!keySet) {
    keySet = createRemoteJWKSet(new URL(`${issuer}/.well-known/jwks.json`));
    jwks.set(issuer, keySet);
  }
  try {
    const { payload } = await jwtVerify(header.slice(7), keySet, {
      issuer: `${issuer}/`,
      audience: env.AUTH0_AUDIENCE
    });
    const scopes = typeof payload.scope === "string" ? payload.scope.split(" ") : [];
    return scopes.includes("oura:read");
  } catch {
    return false;
  }
}

function unauthorized(request: Request) {
  const metadata = new URL("/.well-known/oauth-protected-resource", request.url);
  return new Response("Unauthorized", {
    status: 401,
    headers: { "www-authenticate": `Bearer resource_metadata="${metadata}", scope="oura:read"` }
  });
}

async function setupKeyMatches(request: Request, env: Env) {
  const supplied = request.headers.get("x-setup-key") ?? "";
  const encode = (value: string) => crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  const [left, right] = await Promise.all([encode(supplied), encode(env.SETUP_KEY)]);
  const leftBytes = new Uint8Array(left);
  const rightBytes = new Uint8Array(right);
  let difference = 0;
  for (let index = 0; index < leftBytes.length; index += 1) {
    difference |= leftBytes[index] ^ rightBytes[index];
  }
  return difference === 0 && supplied.length > 0;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/.well-known/oauth-protected-resource") {
      return Response.json({
        resource: url.origin,
        authorization_servers: [env.AUTH0_ISSUER.replace(/\/$/, "")],
        scopes_supported: ["oura:read"],
        bearer_methods_supported: ["header"]
      });
    }

    const credential = env.OURA_CREDENTIAL.getByName("owner");
    if (url.pathname === "/admin/oura/authorize" && request.method === "POST") {
      if (!(await setupKeyMatches(request, env))) return new Response("Forbidden", { status: 403 });
      return Response.json({ authorization_url: await credential.authorizationUrl() });
    }

    if (url.pathname === "/oauth/oura/callback" && request.method === "GET") {
      const code = url.searchParams.get("code");
      const state = url.searchParams.get("state");
      if (!code || !state) return new Response("Oura authorization was not completed.", { status: 400 });
      await credential.completeAuthorization(code, state, url.searchParams.get("scope") ?? undefined);
      return new Response("Oura authorization complete. You may close this tab.");
    }

    if (url.pathname === "/mcp") {
      if (request.method !== "POST") return new Response("Method Not Allowed", { status: 405, headers: { allow: "POST" } });
      if (request.headers.get("host") !== url.host) return new Response("Invalid Host", { status: 400 });
      const origin = request.headers.get("origin");
      if (origin && !["https://chatgpt.com", "https://chat.openai.com"].includes(origin)) {
        return new Response("Invalid Origin", { status: 403 });
      }
      if (!(await verifyMcpRequest(request, env))) return unauthorized(request);
      return createMcpHandler(() => createServer(env), {
        legacy: "reject",
        responseMode: "json"
      }).fetch(request);
    }

    return new Response("Not Found", { status: 404 });
  }
} satisfies ExportedHandler<Env>;
