---
name: externalize-structure
description: Externalize operational structure by turning dependency-heavy or stateful material into the smallest useful spatial model inside the answer. Use for procedures, setups, troubleshooting, plans, workflows, systems, or decisions whose inputs, scopes, branches, merges, intermediate states, or completion checks are hard to track in prose.
---

# Externalize Structure

Expose the model the reader would otherwise have to reconstruct and hold in
working memory.

## Core Rule

Never make the reader remember structure that the answer can keep visible.

Use a visual when it materially reduces reconstruction work. Strong signals are:

- several inputs or actors;
- operations with different scopes;
- branches, merges, parallel work, or loops;
- intermediate states that later steps depend on;
- ordering or dependency constraints;
- a meaningful completion check.

A visual usually earns keep when two or more signals are present, or when one
relationship is unusually dense. Keep a short sentence or numbered list when
the material is simply linear. Do not add a diagram as decoration.

## Build the Operational Model

1. **Lead with the answer.** State the outcome, recommendation, or reason the
   model matters. Finish when the reader knows how to use the visual.
2. **Extract the structure.** Identify:
   - sources: inputs, actors, prerequisites, files, facts, or resources;
   - operations: actions and the exact sources or states they affect;
   - states: meaningful intermediate and final conditions;
   - edges: order, dependency, flow, or containment;
   - control: choices, conditions, loops, and stopping rules;
   - proof: the observable result or verification.

   Finish when every operation has an unambiguous scope, incoming state, and
   resulting state, and every choice has a condition and outcome. Keep this
   model internal unless the user asks for it.
3. **Select the form.** Match the hardest relationship rather than forcing all
   material into a recipe-style merge table:

   | Relationship to expose | Smallest fitting form |
   |---|---|
   | Exact mappings or repeated-field comparison | Table |
   | Inputs transformed in groups and later combined | Merge table or left-to-right flow |
   | Conditions leading to different outcomes | Decision tree |
   | State changing across events or steps | State table or timeline |
   | Ownership, nesting, or containment | Tree |
   | Components with several dependencies | Dependency graph |
   | Physical or interface placement | Wireframe |
   | One path with no meaningful convergence | Numbered list or sentence |

   Finish when one primary form exposes the difficult relationship without
   needing a second visual. Combine forms only when each answers a distinct
   question.
4. **Render beside the answer.** In ordinary chat, prefer a compact Markdown
   table, text diagram, or Mermaid diagram supported by the surface. Create a
   dedicated visual artifact only when the user asks for one or the inline form
   would be unreadable. Finish when the visual stands on its own at a glance.
5. **Compress and verify.** Delete prose that merely narrates the geometry,
   decorative nodes, obvious legends, and connectors that carry no information.
   Finish when removing anything else would hide a relationship or necessary
   meaning.

## Spatial Grammar

- Place a source where it enters the process; do not separate inputs from the
  operations that consume them.
- Use alignment, enclosure, span, or connecting lines to show the exact scope of
  an operation.
- Make branches, convergence, parallel work, loops, and exit conditions visible.
- Name an intermediate state when a later action depends on what it contains or
  what has already happened.
- Scan operation labels from the reader's likely knowledge level. Replace or
  define specialized and ambiguous verbs at their point of use, such as
  `reseat — remove, then install firmly`; do not send the reader to a detached
  glossary.
- Keep enough context visible that the reader can look away and resume by
  recognition rather than recall.
- Use geometry for structure and prose for meaning, caveats, uncertainty, and
  exceptions.

## Show What Done Looks Like

End with a concrete final state:

- show the expected output or selected result;
- name observable verification checks;
- include an actual photo, screenshot, or preview when the result is inherently
  visual and that evidence is available.

Do not fabricate evidence of an actual result. Label a schematic or illustrative
preview as such.

## Completion Check

Before finishing, verify:

- the start, transformations, and final state are traceable;
- operation scope and ordering are unambiguous;
- branches and merges reflect the source rather than invented certainty;
- specialized or ambiguous action labels are plain or defined where encountered;
- facts, inference, and recommendations remain distinct;
- completion is observable;
- the visual is materially easier to use than the prose it replaces.
