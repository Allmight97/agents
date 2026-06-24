# Source Principles

Reference links:

- Claude Code best practices, "Write an effective CLAUDE.md":
  https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md
- AGENTS.md project:
  https://agents.md
- OpenAI Codex AGENTS.md guide:
  https://developers.openai.com/codex/guides/agents-md

Shared principles to apply:

- Keep always-loaded instruction files concise and human-readable.
- Include project-specific commands, conventions, and gotchas that agents cannot
  reliably infer from code.
- Exclude generic language, tutorials, long API docs, frequently changing state,
  file-by-file codebase descriptions, and self-evident advice.
- Use nested instruction files for path-specific rules.
- Use skills for conditional workflows and reusable procedures that do not need
  to load every session.
- Treat instruction files like code: review, prune, and test whether changes
  alter agent behavior.
