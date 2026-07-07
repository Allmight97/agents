# Check Apple 27 Toolchain

Use `apple-27-toolchain`.

Run the narrowest checks that prove the active Apple toolchain:

```bash
xcode-select -p
DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer xcodebuild -version
DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer xcrun swift --version
DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer xcrun xcodebuild -showsdks
DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer xcrun simctl list devices available
```

Report exact versions, selected paths, missing SDKs/runtimes, and the smallest next action.
