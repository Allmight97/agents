---
name: library-research
description: "Answer a version-sensitive question about a third-party library from the exact version the project locks. Use when a dependency's behavior, API, or bug depends on which release is installed."
---

# Library Research

Answer the library question for the version this project actually runs, and
return the answer to the code that owns the decision.

## Evidence

Start from the owning code, its tests, and the contract the question serves.
Then resolve the exact version and source from the lockfile or vendor pin: the
manifest states the intended range, the lockfile selects the release.

Read the installed declarations and source for version-sensitive behavior.
When they are absent or incomplete, fetch the exact registry package and
verify its version and checksum. Exact-version documentation is enough only
for a documented API; inspect the implementation when the answer depends on
it.

When the package leaves a material gap, look for primary docs, source,
issues, or history, and reconcile each to the resolved version before treating
it as proof. Current docs describe the current release.

## Upstream Source

Go upstream only when the question needs tests, examples, internals, or
history the package omits. Map the package to its upstream commit from
registry metadata or `.cargo_vcs_info.json`; a tag with a matching name is not
proof that it built the published package. Prefer a single-file or API fetch.
For a tree, tests, or history, check the verified commit out into an ephemeral
OS-temp directory, shallow or sparse when that is enough, cite its SHA, and
remove it after use.

## Finish

Report the behavior, the owning code it constrains, any constraint that
changes the implementation, and the version and source evidence, with the
commit SHA when upstream source was used. When the evidence falls short or
conflicts, label the answer: current-only (evidence from a newer release only),
version-mismatched (evidence contradicts the locked version), or unproven; and
state the decision left to the project's owner.

Stop when the question is answered with evidence for the locked version, or
when the missing evidence and its consequence for the implementation are
explicit.
