---
name: control-native-browser
description: Control Microsoft Edge or Brave through the native ChatGPT browser-extension bridge. Use when the user invokes Native Browser Bridge or explicitly requests native extension control in Edge or Brave. Ordinary app-UI requests that only name either browser route to Computer Use instead.
---

# Control Edge or Brave Natively

This skill is a browser-family selector. The installed
`chrome@openai-bundled` plugin owns the extension bridge, Browser Use runtime,
safety rules, confirmations, diagnostics, and tab cleanup.

Use this selector for browser content such as tabs, pages, sessions, navigation,
and page inspection. Browser chrome and application settings use Computer Use
unless the user explicitly requires this bridge; if the bridge cannot perform
that operation, report the limitation instead of changing control surfaces.

1. Read the installed Chrome plugin's complete `control-chrome` skill before
   taking browser action. If it is unavailable, tell the user to enable
   `chrome@openai-bundled`; do not change control surfaces.
2. Resolve the browser family from the user's request:
   - Microsoft Edge: `edge`
   - Brave: `brave`

   If the user invoked this bridge without naming one of those browsers, ask
   which browser to use before opening or controlling anything.
3. Follow the Chrome skill's bootstrap, then acquire only the requested family
   and retain its binding for the task:

   ```js
   globalThis.edge ??= await agent.browsers.get("edge");
   globalThis.brave ??= await agent.browsers.get("brave");
   ```

   Run only the line matching the requested browser. Load that binding's
   documentation before using its APIs.
4. Prove the selected provider with the binding's read-only
   `user.openTabs()` call. A running browser, installed extension, or valid
   native-host manifest alone does not prove live control.
5. Use that binding for the entire task. Do not substitute another browser
   family, `getDefault()`, `getForUrl()`, Computer Use, or macOS Accessibility.
6. If selection or the first lightweight call fails, use the installed Chrome
   plugin's current troubleshooting guidance and diagnostics for the exact
   `edge` or `brave` family. The bundled Chrome plugin owns native-host repair;
   this selector does not.
7. Change browser family or control surface only when the user explicitly asks.
