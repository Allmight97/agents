# Edge recovery

Use this branch only when the explicit Edge provider is unavailable or its
first lightweight call fails. Preserve the Chrome skill's browser-safety and
confirmation rules.

## Establish the failed layer

Read the installed Chrome skill's `chrome-troubleshooting` documentation, then
run its current diagnostic scripts from the installed `chrome@openai-bundled`
plugin root:

```text
node scripts/chrome-is-running.js --browser edge --json
node scripts/installed-browsers.js --json
node scripts/check-extension-installed.js --browser edge --json
node scripts/check-native-host-manifest.js --browser edge --json
```

Use the inspected plugin root rather than caching a versioned path. On macOS,
also check whether the signed helper exists at the plugin's current `latest`
path:

```text
extension-host/macos/arm64/ChatGPT for Chrome
```

Classify the evidence before changing state:

- **Edge is not running:** ask before launching it unless the task already
  authorized opening Edge. Use the Chrome plugin's Edge launch helper, wait two
  seconds, and retry once.
- **Extension is absent or disabled:** direct the user to the ChatGPT extension
  in the active Edge profile. Do not treat a different profile's installation
  as proof.
- **Manifest is absent but the cached helper exists:** remove and re-add
  `chrome@openai-bundled` through ChatGPT's plugin setup, restart ChatGPT, and
  recheck. Do not reinstall `browser@openai-bundled` for this failure.
- **Cached helper is absent:** inspect the signed helper in the installed
  ChatGPT application bundle. If that canonical helper is also absent, update
  or reinstall ChatGPT. If it is present, classify the failure as corrupted
  derived Chrome-plugin state and use the local Codex operations procedure
  below.
- **All checks pass but Edge remains unavailable:** follow the Chrome skill's
  connection troubleshooting and collect current ChatGPT logs. Do not switch
  browser families behind the user's request.

## Repair corrupted derived plugin state

Use `codex-local-ops-doctor` when available. Before mutation, name the exact
Chrome-plugin marketplace and cache directories, preserve them in a dated
backup, and verify the canonical helper is signed by OpenAI.

Rebuild only the derived `chrome@openai-bundled` source from the installed,
signed ChatGPT application bundle; then reinstall that Chrome plugin and
restart ChatGPT so its native-host lifecycle creates the registration. Verify
that the restored helper matches the canonical helper by hash and still passes
code-signature validation.

Do not synthesize a native-host manifest, download a helper binary, execute the
plugin's internal manifest installer directly, or modify the Edge profile.
Those actions bypass ownership and create update-fragile state.

## Completion proof

Recovery is complete only when all of these hold:

1. The Chrome plugin's native-host check reports `correct: true` for Edge.
2. `agent.browsers.get("edge")` succeeds.
3. `edge.user.openTabs()` returns without a provider error; an empty list is a
   valid result.

Retain the backup through one normal ChatGPT restart or update cycle, then
remove it only with user approval.
