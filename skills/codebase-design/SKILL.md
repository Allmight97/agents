---
name: codebase-design
description: Design module interfaces that hide complexity and concentrate ownership. Use for interface design, deepening a module, dependency seams, and testability tradeoffs; related skills may use its design vocabulary.
---

# Codebase Design

Reduce what callers must know while keeping behavior and its governing rules
in an accountable owner. A smaller method count or a larger implementation is
not evidence of a better design by itself.

## Vocabulary

Use these terms when they clarify the discussion. Keep the project's domain
names and ordinary words such as service, API, component, and boundary when
those are more precise.

- **Module:** an owned unit with an interface and implementation, at the scale
  relevant to the decision: function, class, package, or feature.
- **Interface:** everything a caller must know, including types, invariants,
  ordering, errors, configuration, resource ownership, and performance limits.
- **Depth:** useful behavior behind that interface relative to the knowledge a
  caller needs. A shallow module makes callers learn nearly as much as it hides.
- **Seam:** a point where behavior can be substituted or isolated. An adapter
  supplies a concrete dependency there.
- **Locality:** how much a change, rule, or bug can be understood and corrected
  in one place. Depth earns its keep when it improves this or reduces caller
  burden.

## Design Judgment

Name the invariant and its current owner before moving code. Trace real callers
and ask which ordering rules, repeated decisions, or implementation facts they
should no longer need to know.

Apply the deletion test: if removing a layer eliminates complexity while
preserving its obligations, consider collapsing it. If that knowledge spreads
to callers, the layer was carrying useful responsibility. Thin wrappers can
still own authorization, lifecycle, interoperability, or platform contracts.

Judge reader effort along two axes: indirections to trace and mutable state to
hold in mind. Flattening calls while scattering state can make the system harder
to understand. Prefer a design that reduces their combined burden.

Introduce a seam for a present need: real variation, deterministic proof,
lifecycle ownership, isolation, or an external contract. Two useful adapters
are evidence, not a minimum count; do not invent a test adapter to justify an
otherwise unnecessary interface.

Keep pure decisions separate from effects when that makes behavior easier to
prove. Let an effectful owner manage its dependencies and resources explicitly;
inject only dependencies whose substitution or ownership matters. Keep private
test seams private and retain public handoff tests where composition can fail.

## Focused References

- When consolidating existing modules, read [DEEPENING.md](DEEPENING.md) for
  dependency and test migration decisions.
- When comparing consequential interface alternatives, read
  [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md). Use materially different designs to
  test the decision; this does not require parallel agents.
