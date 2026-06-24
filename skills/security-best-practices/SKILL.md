---
name: "security-best-practices"
description: "Perform language and framework specific security best-practice reviews, reports, and secure-by-default implementation guidance. Use only when the user explicitly asks for security best practices, a security review/report, or secure coding help for supported languages: python, javascript/typescript, or go. Do not trigger for ordinary code review, debugging, or non-security work."
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

## Workflow Decision Tree

- If the language/framework is unclear, inspect the repo to determine it and list your evidence.
- If matching guidance exists in `references/`, load only the relevant files and follow their instructions.
- If no matching guidance exists, state that concrete local guidance is unavailable for that stack. You may still report clear vulnerabilities, but separate sourced findings from general judgment.

# Overrides

Project docs, threat models, compliance constraints, or explicit user requirements can override generic best practices. When a bypass is justified, name the tradeoff and suggest documenting the reason if it will matter later.

# Report Format

Default to a chat report unless the user asks for a file or names an output path. If a file is needed and no path is provided, ask for the destination before writing.

The report should have a short executive summary at the top.

Group findings by severity. Each finding needs an ID, affected file/line references, evidence, impact, and recommended fix. Prioritize exploitable or user-impacting risks over checklist completeness.

For critical findings include a one sentence impact statement.

Important: When referencing code in the report, make sure to find and include line numbers for the code you are referencing.

If you write a report file, summarize the findings to the user and include the path.

# Fixes

If you produced a report, let the user choose which finding to fix unless they already approved remediation.

If you found a critical issue during an active security task, stop and recommend the highest-impact fix first.

When producing fixes, focus on one finding or one tightly related cluster. Add comments only when the security reasoning would not be obvious from the code.

Before editing, identify likely behavior changes and regression risk. For compatibility-sensitive fixes, propose the change and ask when the secure option would break current behavior.

Follow the repo's normal change, test, and commit flow. Do not bundle unrelated findings into one commit unless the user asks.

Run verification matched to the touched surface and security boundary. Report residual risk when a fix cannot be fully proved locally.

# General Security Advice

Below is a few bits of secure coding advice that applies to almost any language or framework.

### Avoid Using Incrementing IDs for Public IDs of Resources

When assigning an ID for some resource, which will then be used by exposed to the internet, avoid using small auto-incrementing IDs. Use longer, random UUID4 or random hex string instead. This will prevent users from learning the quantity of a resource and being able to guess resource IDs.

### A note on TLS

While TLS is important for production deployments, most development work will be with TLS disabled or provided by some out-of-scope TLS proxy. Due to this, be very careful about not reporting lack of TLS as a security issue. Also be very careful around use of "secure" cookies. They should only be set if the application will actually be over TLS. If they are set on non-TLS applications (such as when deployed for local dev or testing), it will break the application. You can provide a env or other flag to override setting secure as a way to keep it off until on a TLS production deployment. Additionally avoid recommending HSTS. It is dangerous to use without full understanding of the lasting impacts (can cause major outages and user lockout) and it is not generally recommended for the scope of projects being reviewed by codex.
