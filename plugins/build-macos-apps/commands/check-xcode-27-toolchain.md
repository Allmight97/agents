# /check-xcode-27-toolchain

Verify the active Apple 27 toolchain before diagnosing app code.

## Arguments

- `developer_dir`: explicit Xcode developer directory (optional)
- `scheme`: Xcode scheme for destination checks (optional)
- `platform`: `macos`, `ios`, `watchos`, or `all` (optional, default: `all`)

## Workflow

1. Use `xcode-27-toolchain`.
2. Discover the selected developer directory and candidate full Xcode installs.
3. Prefer the provided `developer_dir`; otherwise choose the newest full Xcode
   path that proves `xcodebuild -version`.
4. Verify Xcode version, Swift version, SDK versions, simulator runtimes,
   available devices, and scheme destinations when a scheme is provided.
5. Report exact versions and the smallest missing piece.

## Guardrails

- Do not change global `xcode-select`.
- Do not install runtimes, trust devices, or mutate Apple account state without
  explicit approval.
