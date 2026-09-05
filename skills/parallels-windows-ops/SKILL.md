---
name: parallels-windows-ops
description: "Audit or operate a local Parallels Windows VM. Use for guest access, CLI versus GUI control, measured resource tuning, and Mac/Windows integration settings."
---

# Parallels Windows Ops

Use this skill to make Parallels Windows work repeatable without blurring Mac and Windows boundaries.

## Baseline First

For an audit or tuning task, use the bundled read-only baseline with the actual
VM name from the request or `prlctl list -a`:

```bash
bash "<skill-dir>/scripts/audit_parallels_windows.sh" "<vm-name>"
```

Resolve `<skill-dir>` from this loaded skill's path. For a narrow operational
task, inspect only the state and access needed by that operation. Record the
baseline fields relevant to any proposed change.

If the VM is paused or stopped, report that state. Do not start, resume, suspend, shut down, or reconfigure the VM unless the user asked for an access test or approved that action.

If idle auto-pause interrupts the authorized test, record its current setting
and temporarily disable it with:

```bash
prlctl set "<vm>" --pause-idle off
```

Restore the prior setting when the test ends unless a persistent change was
requested or approved.

## Access Ladder

Prefer the lowest-friction truthful control surface:

1. Use `prlctl` for VM state, configuration, snapshots, and Parallels Tools.
2. Use `prlctl exec <vm> --current-user powershell ...` for logged-in Windows user tasks.
3. Use `prlctl exec <vm> ...` without `--current-user` only when `SYSTEM` context is intentional.
4. Use Computer Use through Parallels Desktop for visual confirmation or unscriptable GUI flows.

Treat Computer Use as pixel/keyboard control inside the Parallels window. It does not expose a native Windows accessibility tree, so first-run dialogs, focus shifts, and overlays can break unattended GUI work.

If a guest command hangs, narrow it to a short probe before escalating to GUI
control. Read [dated local findings](references/2026-07-06-findings.md) only when
investigating the same command or boot-readiness symptoms; verify them on the
current VM.

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
