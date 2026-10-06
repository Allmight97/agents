---
name: handoff
description: "Write a handoff file so a fresh agent can continue this work; saved to the OS temp directory."
disable-model-invocation: true
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
