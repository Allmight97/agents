---
name: write-bootable-media
description: Write one publisher-declared ISO or IMG (compressed or not) to a USB disk on macOS, verify it byte for byte, and eject it.
disable-model-invocation: true
---

# Write bootable media

Use `scripts/bootable-media-writer`, resolved relative to this skill directory. A completed write is intermediate. Done when `status` shows the plan verified (by `run`, `verify` or `compare`) and ejected.

Requires macOS 13 or later with Python 3, `diskutil`, `ioreg`, and administrator authorization for exact raw-device access.

Scope: this skill writes exactly one publisher-declared byte-for-byte ISO or IMG to one USB. For a Ventoy or multiboot USB, stop before `inspect` and tell the user this skill does not build one.

## Required workflow

1. Establish that the publisher intends the source to be written byte-for-byte and obtain its primary-source HTTPS URL and the publisher's SHA-256. Without a publisher SHA-256, stop and ask the user; pass `--allow-primary-url-only` only on their yes. That plan's trust tier is `primary-url-only` rather than `publisher-sha256`.
2. Run `inspect` and identify the intended whole physical USB by model, exact byte size, USB serial, and physical port. Restate that target and drives that must not be touched.
3. Run `prepare` with the absolute source, publisher hash when available, provenance URL, whole-disk node, and a plan path outside OS temp on a volume with room for a copy of the source file. Show the user the plan ID and target identity. Done when the user confirms that plan ID; pass `--confirm-plan` only a plan ID the user confirmed, never one you chose yourself.
4. Then take one branch:
   - **4a. Writing with this tool.** Before `run`, tell the user macOS may show one authorization prompt and, when the image's partition map lands, a dialog saying the disk is unreadable; they choose **Ignore**, not Initialize or Eject. Run `run --plan ... --confirm-plan PLAN_ID` for one write, same-descriptor readback, and eject. Or use staged `write`, `verify`, and `eject`; staged write and verify can each require authorization.
   - **4b. Checking media another tool wrote.** Run `compare --plan ...`; it unmounts, performs one read-only authorized exact-length hash, records `verified_external`, and permits eject only after a match.
5. After eject, tell the user the write is verified but booting is not; for boot testing or a failed boot, read the [hardware acceptance reference](references/hardware-acceptance.md).

`status --plan ...` shows the durable plan, source hashes/sizes, target identity, authorization count, write/verify completion metrics, receipt, and eject state at any time, without authorization. `discard --plan ...` retires an unused or failed plan and removes its private snapshots without touching the USB.

## Safety invariants

- Accept only a whole, external, physical, removable, writable USB disk. Refuse internal, virtual, network, RAID, partition, and APFS physical-store targets.
- Require an unambiguous USB serial and port location. Bind the plan to BSD node, raw node, model, exact bytes, serial, transport, device-tree path, port location, IORegistry entry ID, and USB attachment-session ID.
- Detect `.bz2`, `.xz`, `.gz`, and `.zip` by magic. ZIP requires exactly one `.iso`/`.img` member unless `--archive-member` selects one explicitly. Never extract into a user-controlled directory.
- Require the image to fit the target after expansion. Write only from the same private read-only verified snapshot; never reopen the source pathname after prepare.
- Verify a supplied publisher SHA-256 against the artifact.
- Never repartition or format before a raw write; the image owns the resulting partition map.
- Scope elevation to `/usr/libexec/authopen` on the exact raw device. Do not add root-shell or passwordless-sudo policy. `run` retains one authorized read/write descriptor through write and readback.
- Bind every destructive confirmation to the canonical plan ID. A written, verified, or ejected plan cannot be replayed.
- Hold one stable per-plan sidecar lock across each complete mutating command. If another process owns it, fail with `PLAN_BUSY` before unmount, authorization, or device I/O.
- Re-check identity before I/O and before eject. Abort on disconnect, re-enumeration, identity drift, failed unmount, short write, readback mismatch, or failed eject; never describe those states as bootable.
- Require the verifier's receipt to match the canonical plan. On macOS, eject is path-based; perform the final identity check immediately before it and disclose the residual hot-unplug/path-reuse race when relevant.
- VM or filesystem proof does not substitute for a real boot test in the publisher-required firmware mode.

## Commands

```text
scripts/bootable-media-writer inspect [--json]
scripts/bootable-media-writer prepare --image /abs/source.iso[.bz2] --sha256 HEX --provenance-url HTTPS --device /dev/diskN --plan /abs/plan.json
scripts/bootable-media-writer prepare --image /abs/source.img.zip --archive-member release.img --allow-primary-url-only --provenance-url HTTPS --device /dev/diskN --plan /abs/plan.json
scripts/bootable-media-writer run --plan /abs/plan.json --confirm-plan PLAN_ID
scripts/bootable-media-writer write --plan /abs/plan.json --confirm-plan PLAN_ID
scripts/bootable-media-writer verify --plan /abs/plan.json
scripts/bootable-media-writer compare --plan /abs/plan.json
scripts/bootable-media-writer status --plan /abs/plan.json
scripts/bootable-media-writer eject --plan /abs/plan.json
scripts/bootable-media-writer discard --plan /abs/plan.json
```

If the USB lacks a stable serial, use a different device rather than weakening identity checks.
