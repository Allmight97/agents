# Project Context Setup

Use when the user asks to initialize or refresh reusable design context.
Ordinary design tasks can work from the brief and existing code without adding
these files.

## Inspect Existing Context

Look for PRODUCT.md and DESIGN.md at the project root, `.agents/context/`, or
`docs/`, and respect an explicit `IMPECCABLE_CONTEXT_DIR`. Reuse the existing
location. Read relevant product docs, tokens, components, and brand assets once.
Preserve unrelated content when updating an existing file.

Resolve only the missing choices that will guide future design: audience,
product purpose, brand or product register, desired character, constraints, and
accessibility needs. Treat user-provided answers as evidence; do not require an
interview round when the request already settles them. Keep uncertain inferences
visible and ask when they would materially misdirect future work.

## Write The Requested Context

PRODUCT.md owns strategic context. Use the sections that have useful content:
users, purpose, personality, design principles, relevant anti-references, and
accessibility needs. Include `## Register` followed by the bare value `brand`
or `product` so the bundled scripts can read it. Choose the default by the
primary surface; individual tasks may use a different register.

DESIGN.md owns the visual system: color, typography, layout, components, and
interaction patterns. Use [document.md](document.md) when it is requested or
part of the accepted setup scope. Reference existing canonical docs rather than
copying their full rules.

Configure live mode only when that workflow is requested. Read
[live.md](live.md) for its configuration, injection, CSP, and cleanup contract.
Do not add live-server configuration or alter CSP merely because a project has
a dev server.

## Finish

Inspect the resulting files and report their paths, settled context, and any
material open choice. Suggest a relevant next command if useful. Resume an
already-authorized design task after the requested setup. Update AGENTS.md only
when requested or required by the project's guidance; use a pointer instead of
duplicating the context.
