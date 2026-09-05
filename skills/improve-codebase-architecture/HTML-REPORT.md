# Architecture Report

Use for multiple candidates or comparisons that benefit from diagrams. Write
one HTML file in OS temp, open it, and give the absolute path. Use inline CSS;
prefer static HTML/SVG diagrams for a standalone artifact. If a renderer needs
network resources, disclose that dependency and verify it loads.

Lead with the recommended candidate and the evidence behind it. For each
candidate, include location, friction, proposed owner, benefits, preserved
obligations, proof, and migration risk. Use before/after diagrams when they make
ownership or call flow clearer; prose is appropriate for details a diagram
cannot carry.

Use project terms and plain language. The shared `codebase-design` vocabulary
is a reasoning aid, not a required list of words. Distinguish observed facts,
proposed designs, and unresolved assumptions visually or in their labels.

Inspect the rendered report for readability, clipping, and accurate diagram
labels. Keep the source evidence sufficient for another agent to check the
recommendation without reconstructing the conversation.
