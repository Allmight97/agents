---
name: "security-best-practices"
description: "Apply security best-practice guidance for Python, JavaScript/TypeScript, or Go when the user requests a security review, secure implementation, or remediation. Skip ordinary reviews and unrelated development."
---

# Security Best Practices

## Workflow

Identify the language, framework, runtime, and app boundary in scope. Use repo files as evidence: package manifests, lockfiles, framework config, server entrypoints, routes, auth/session code, deployment config, or the user-named files.

Then check this skill's `references/` directory. Load only files that match the active language/framework/stack. The filename format is `<language>-<framework>-<stack>-security.md`; also load the matching `<language>-general-<stack>-security.md` when it applies.

For web apps with frontend and backend surfaces, load guidance for both sides when both are in scope.

If the user asks to build or improve a web app with an unspecified frontend, load `javascript-general-web-frontend-security.md` for frontend defaults.

If no matching reference exists, say that this skill has no concrete local guidance for the stack. Use current official docs or clearly label general security knowledge before relying on it.

Modes:

1. **Secure implementation:** apply the relevant guidance while writing or changing code.
2. **Security review/report:** inspect the requested scope and produce prioritized findings.
3. **Security fix:** fix one finding or one tightly related cluster at a time, preserving behavior unless the user approves a breaking security change.

Do not run this skill as passive background scanning during unrelated work. If you notice an obvious critical vulnerability outside an active security task, flag the risk briefly and ask before expanding scope.

# Overrides

Project docs, threat models, compliance constraints, or explicit user requirements can override generic best practices. When a bypass is justified, name the tradeoff and suggest documenting the reason if it will matter later.

# Report Format

Default to a chat report unless the user asks for a file or names an output path. If a file is useful and no destination was specified, use OS temp; follow a
repository-owned reporting convention when one applies.

The report should have a short executive summary at the top.

Group findings by severity. Each finding needs an ID, affected file/line references, evidence, impact, and recommended fix. Prioritize exploitable or user-impacting risks over checklist completeness.

For critical findings include a one sentence impact statement.

Important: When referencing code in the report, make sure to find and include line numbers for the code you are referencing.

If you write a report file, summarize the findings to the user and include the path.

# Fixes

If you produced a report, let the user choose which finding to fix unless they already approved remediation.

Prioritize a critical finding and its correction during an active security task.
Continue already-authorized remediation; pause only for a consequential unresolved
choice or an action outside that authority.

When producing fixes, focus on one finding or one tightly related cluster. Add comments only when the security reasoning would not be obvious from the code.

Before editing, identify likely behavior changes and regression risk. For compatibility-sensitive fixes, propose the change and ask when the secure option would break current behavior.

Follow the repo's normal change, test, and commit flow. Do not bundle unrelated findings into one commit unless the user asks.

Run verification matched to the touched surface and security boundary. Report residual risk when a fix cannot be fully proved locally.
