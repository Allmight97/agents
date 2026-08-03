---
name: control-edge
description: Control Microsoft Edge through the first-party ChatGPT browser extension and the official Chrome plugin's Browser Use runtime. Use when the user invokes Edge Browser, requests extension-based Edge automation, or explicitly wants Edge without Computer Use or macOS Accessibility.
---

# Control Microsoft Edge

Use the official `chrome@openai-bundled` plugin as the owner of browser setup,
safety, API use, confirmations, troubleshooting, and tab cleanup. This skill
only fixes the external browser family to Microsoft Edge.

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
4. If Edge is unavailable, direct the user to install and enable the first-party
   ChatGPT browser extension in Edge through **Settings -> Computer use**. If
   file upload alone fails, direct them to `edge://extensions`, open the
   extension's details, and enable **Allow access to file URLs**.
5. Use Computer Use or macOS Accessibility only after the user explicitly
   changes the requested control surface.
