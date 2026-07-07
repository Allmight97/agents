# Profile Apple App

Use `apple-performance-memory`.

Start with code and build-setting triage, then pick the smallest proof:

- XcodeBuildMCP coverage or logs for build/test-linked evidence
- Instruments or `xctrace` for launch/runtime CPU and hangs
- Top Functions for hot-stack narrowing
- ETTrace for Simulator latency and stack comparison
- memgraph/leaks helpers for retained-object and growth evidence
- Foundation Models Instrument for prompt, response, token, and tool-call behavior

Keep before/after evidence comparable: same scheme, destination, scenario, and build configuration.
