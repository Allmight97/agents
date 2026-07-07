# Fix Apple Signing

Use `apple-signing-distribution`.

Classify the failure before changing anything:

- missing or wrong entitlement
- capability not enabled for the target
- provisioning profile mismatch
- team/signing identity mismatch
- hardened runtime, sandbox, Gatekeeper, notarization, or TestFlight validation failure
- physical device trust or account state

Do not mutate Apple account, team, certificate, profile, device trust, or global Xcode settings without explicit user approval.
