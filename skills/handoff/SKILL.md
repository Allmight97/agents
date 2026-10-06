---
name: handoff
description: "Compact the current conversation into a handoff document for another agent. Use only when the user asks for a handoff."
---

# Handoff

Write a handoff document that lets a fresh agent continue the work. Save it to
the operating system's temporary directory, not the current workspace.

- Include a "Suggested skills" section that names the skills the next agent
  should load.
- Reference specs, plans, issues, commits, and diffs by path or URL. Do not
  copy their content.
- Redact secrets and personal data, such as API keys, passwords, and personal
  identifiers.
- If the user says what the next session will do, tailor the document to that
  focus.

Give the user the file path when done.
