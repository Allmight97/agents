---
name: write-bootable-media
description: Safely prepare, write, compare, verify, and eject vendor-declared bootable USB images on macOS, including compressed ISO/IMG sources. Use when asked to inspect USB media or flash, validate, compare, verify, or eject Linux and recovery media.
disable-model-invocation: true
---

# Write bootable media

Use `scripts/bootable-media-writer`, resolved relative to this skill directory. A completed write is intermediate; the deliverable is a plan-bound exact readback (or an exact `compare` of an existing image) followed by successful eject.

Requires macOS 13 or later with Python 3, `diskutil`, `ioreg`, and administrator authorization for exact raw-device access.

Scope: this skill writes exactly one publisher-declared byte-for-byte ISO or IMG to one USB. **Do not use it for Ventoy or any multiboot USB.** For those requests, stop before `inspect` or `prepare` and route to a separate multiboot workflow.

## Required workflow

1. Establish that the publisher intends the source to be written byte-for-byte and obtain its primary-source HTTPS URL. Prefer the publisher's SHA-256. A URL-only plan is permitted only with explicit `--allow-primary-url-only`; its plan trust tier is `primary-url-only` rather than `publisher-sha256`.
2. Run `inspect` and identify the intended whole physical USB by model, exact byte size, USB serial, and physical port. Restate that target and drives that must not be touched.
3. Run `prepare` with the absolute source, publisher hash when available, provenance URL, whole-disk node, and durable plan path. The CLI detects compression by magic, creates one private read-only artifact snapshot beside the plan, validates the bounded expanded stream, binds both hashes and sizes, selects one ZIP ISO/IMG member, and checks target capacity before authorization. Review the plan ID and identity tuple before any destructive step.
4. Run `run --plan ... --confirm-plan PLAN_ID` for one write, one expected macOS authorization, same-descriptor readback, and eject. Or use staged `write`, `verify`, and `eject`; staged write and verify can each require authorization.
5. For a target written by another tool, use `compare --plan ...`; it unmounts, performs one read-only authorized exact-length hash, records `verified_external`, and permits eject only after a match.
6. Use `status --plan ...` at any time for the durable plan, source hashes/sizes, target identity, authorization count, write/verify completion metrics, receipt, and eject state. It performs no authorization. Use `discard --plan ...` to retire an unused or failed plan and remove its private snapshots without touching the USB.

Expected macOS behavior: raw-device access normally presents one authorization request for `run`. During repartitioning, macOS may report that the disk is unreadable; choose **Ignore**, not Initialize or Eject, and let the operation continue.

## Safety invariants

- Accept only a whole, external, physical, removable, writable USB disk. Refuse internal, virtual, network, RAID, partition, and APFS physical-store targets.
- Require an unambiguous USB serial and port location. Bind the plan to BSD node, raw node, model, exact bytes, serial, transport, device-tree path, port location, IORegistry entry ID, and USB attachment-session ID.
- Detect `.bz2`, `.xz`, `.gz`, and `.zip` by magic. ZIP requires exactly one `.iso`/`.img` member unless `--archive-member` selects one explicitly. Never extract into a user-controlled directory.
- Require the image to fit the target after expansion. Write only from the same private read-only verified snapshot; never reopen the source pathname after prepare.
- Verify a supplied publisher SHA-256 against the artifact. URL-only provenance requires explicit opt-in and is visibly lower trust in the plan.
- Never repartition or format before a raw write; the image owns the resulting partition map.
- Scope elevation to `/usr/libexec/authopen` on the exact raw device. Do not add root-shell or passwordless-sudo policy. `run` retains one authorized read/write descriptor through write and readback.
- Bind every destructive confirmation to the canonical plan ID. A written, verified, or ejected plan cannot be replayed.
- Hold one stable per-plan sidecar lock across each complete mutating command. If another process owns it, fail with `PLAN_BUSY` before unmount, authorization, or device I/O.
- Re-check identity before I/O and before eject. Abort on disconnect, re-enumeration, identity drift, failed unmount, short write, readback mismatch, or failed eject; never describe those states as bootable.
- Require the verifier's receipt to match the canonical plan. On macOS, eject is path-based; perform the final identity check immediately before it and disclose the residual hot-unplug/path-reuse race when relevant.
- For physical acceptance and failure triage, use the [hardware acceptance reference](references/hardware-acceptance.md). VM or filesystem proof does not substitute for a real boot test in the publisher-required firmware mode.

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

If the publisher does not publish a checksum, stop unless the user explicitly authorizes the URL-only trust tier. If the USB lacks a stable serial, use a different device rather than weakening identity checks.
