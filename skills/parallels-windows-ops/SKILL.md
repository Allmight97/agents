---
name: parallels-windows-ops
description: Audit and operate a local Parallels Desktop Windows VM from Codex. Use when testing Codex access to Windows through Parallels, choosing CLI vs GUI automation, tuning VM performance/resource settings, or scrutinizing Mac/Windows integration features for MSP-style work.
---

# Parallels Windows Ops

Use this skill to make Parallels Windows work repeatable without blurring Mac and Windows boundaries.

## Baseline First

Run the read-only audit before recommending changes:

```bash
scripts/audit_parallels_windows.sh "Windows 11"
```

Completion criterion: capture host hardware, Parallels version/license state, VM state, CPU/RAM/storage/network/sharing settings, Parallels Tools status, and whether guest command execution works.

If the VM is paused or stopped, report that state. Do not start, resume, suspend, shut down, or reconfigure the VM unless the user asked for an access test or approved that action.

## Access Ladder

Prefer the lowest-friction truthful control surface:

1. Use `prlctl` for VM state, configuration, snapshots, and Parallels Tools.
2. Use `prlctl exec <vm> --current-user powershell ...` for logged-in Windows user tasks.
3. Use `prlctl exec <vm> ...` without `--current-user` only when `SYSTEM` context is intentional.
4. Use Computer Use through Parallels Desktop for visual confirmation or unscriptable GUI flows.

Treat Computer Use as pixel/keyboard control inside the Parallels window. It does not expose a native Windows accessibility tree, so first-run dialogs, focus shifts, and overlays can break unattended GUI work.

## Cross-Talk Classification

Before changing integration settings, classify each feature:

- Essential: Parallels Tools, network access needed by the workload, `prlctl exec` access.
- Useful but risky: shared clipboard, shared apps, printer sync, drag-and-drop, shared folders, shared profile, cloud sharing.
- Usually off for MSP hygiene: broad host folder sharing, shared profile, guest-to-host app sharing, location sharing, automatic camera/microphone passthrough.
- Workload-specific: Coherence, USB auto-connect, bridged networking, snapshots, Windows-side security agents.

State the proposed change and expected impact before mutating Parallels, macOS privacy, Windows, credentials, account state, or client-sensitive tooling.

## Optimization Loop

Use a measurement loop, not folklore:

1. Record the current config and workload complaint.
2. Verify current official guidance and current user/admin trend evidence. Read `references/2026-07-06-findings.md` only as a dated starting point.
3. Classify the candidate change as essential complexity, accidental complexity, invited complexity, or redundancy.
4. Change one variable at a time after approval.
5. Re-test the actual workflow and compare host memory pressure, guest Task Manager, responsiveness, battery impact, and disk growth.

Default stance for Apple Silicon Windows 11 ARM: keep Automatic CPU/RAM or the existing measured baseline until a workload proves otherwise. More vCPUs or RAM can make both macOS and Windows worse.

## Known Local Pattern

On the July 6, 2026 test VM, `prlctl exec` initially failed until Windows finished booting and Parallels Tools were ready. Default `prlctl exec` ran as `nt authority\system`; `--current-user` mapped to the logged-in Windows user and launched visible apps. Preserve that distinction in future tests.
