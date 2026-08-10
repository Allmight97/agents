---
name: control-edge
description: Control Microsoft Edge through the first-party ChatGPT browser extension and the official Chrome plugin's Browser Use runtime. Use when the user invokes Edge Browser, requests extension-based Edge automation, or explicitly wants Edge without Computer Use or macOS Accessibility.
---

# Control Microsoft Edge

Use the official `chrome@openai-bundled` plugin as the owner of browser setup,
safety, API use, confirmations, troubleshooting, and tab cleanup. This skill
fixes the external browser family to Microsoft Edge and adds Edge-specific
failure classification.

1. Read the installed Chrome plugin's complete `control-chrome` skill before
   taking browser action. If that skill or plugin is unavailable, tell the user
   to enable `chrome@openai-bundled`; do not substitute desktop automation.
2. Treat Microsoft Edge as an explicit hard constraint. Reuse an existing
   `globalThis.edge` binding when present. Otherwise follow the Chrome skill's
   bootstrap and select Edge exactly:

   ```js
   if (globalThis.edge == null) {
     globalThis.edge = await agent.browsers.get("edge");
     nodeRepl.write(await edge.documentation());
   }
   ```

3. Use the Edge binding for the entire task. Do not call `getDefault()`,
   `getForUrl()`, `get("extension")`, or `get("chrome")` as a substitute.
4. If Edge selection or its first lightweight browser call fails, read
   [Edge recovery](references/edge-recovery.md). Collect its read-only evidence
   before recommending installation, reinstallation, or cache repair. The
   official Chrome plugin owns the extension host; `browser@openai-bundled`
   does not.
5. After recovery, prove the browser provider works by selecting Edge and
   successfully calling `edge.user.openTabs()`. A valid manifest or running
   process alone is not completion proof.
6. If file upload alone fails, direct the user to `edge://extensions`, open the
   ChatGPT extension's details, and enable **Allow access to file URLs**.
7. Use Computer Use or macOS Accessibility only after the user explicitly
   changes the requested control surface.

OpenAI documents the extension for Google Chrome, not other Chromium browsers.
Treat Edge as a compatibility route whose live provider handshake must be
proved after ChatGPT, Chrome-plugin, extension, or Edge updates.
