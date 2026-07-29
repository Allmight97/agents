#!/usr/bin/env swift

import AppKit
import Foundation
import Security

guard CommandLine.arguments.count == 3 else {
    fputs("Usage: pass-agent-store-token.swift <keychain-service> <keychain-account>\n", stderr)
    exit(2)
}

let service = CommandLine.arguments[1]
let account = CommandLine.arguments[2]

guard
    let clipboard = NSPasteboard.general.string(forType: .string)?
        .trimmingCharacters(in: .whitespacesAndNewlines),
    clipboard.hasPrefix("pst_"),
    clipboard.contains("::"),
    clipboard.rangeOfCharacter(from: .whitespacesAndNewlines) == nil,
    let tokenData = clipboard.data(using: .utf8)
else {
    fputs("The clipboard does not contain a raw Proton Pass access token.\n", stderr)
    exit(3)
}

let lookup: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrService as String: service,
    kSecAttrAccount as String: account,
]

let attributes: [String: Any] = [
    kSecValueData as String: tokenData,
    kSecAttrLabel as String: "Codex Proton Pass agent token",
    kSecAttrDescription as String: "Viewer-scoped PAT used to recover the dedicated pass-cli session",
    kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock,
]

let status: OSStatus
if SecItemCopyMatching(lookup as CFDictionary, nil) == errSecSuccess {
    status = SecItemUpdate(lookup as CFDictionary, attributes as CFDictionary)
} else {
    var item = lookup
    attributes.forEach { item[$0.key] = $0.value }
    status = SecItemAdd(item as CFDictionary, nil)
}

guard status == errSecSuccess else {
    fputs("macOS Keychain rejected the Proton Pass token (status \(status)).\n", stderr)
    exit(4)
}

NSPasteboard.general.clearContents()
print("The Proton Pass agent token was stored in macOS Keychain and the clipboard was cleared.")
