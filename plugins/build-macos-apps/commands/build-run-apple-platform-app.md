# /build-run-apple-platform-app

Build and, when requested, run a macOS, iOS, or watchOS Apple platform app.

## Arguments

- `scheme`: Xcode scheme name (required unless unambiguous)
- `platform`: `macos`, `ios-simulator`, `watchos-simulator`, `ios-device`, or `watchos-device`
- `developer_dir`: explicit Xcode developer directory (optional)
- `destination`: exact Xcode destination string or simulator UDID (optional)
- `mode`: `build`, `install`, `launch`, `screenshot`, `logs`, or `runtime-proof` (optional, default: `build`)

## Workflow

1. Use `xcode-27-toolchain` if the toolchain or destination is uncertain.
2. Use `build-run-debug` for macOS app run-script work.
3. Use `ios-watch-substrate` for iOS and watchOS simulator/device proofs.
4. Run the smallest proof that matches `mode`.
5. Classify the result as compile, signing, destination, simulator runtime,
   install, launch, Info.plist/scene lifecycle, capability, or runtime failure.

## Guardrails

- Do not treat a generic device build as physical-device runtime proof.
- Do not disable code signing for physical-device install or launch.
- Do not hardcode simulator model names when `-showdestinations` can discover
  valid destinations.
