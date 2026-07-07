---
name: apple-foundation-models
description: Design and implement Apple Foundation Models features with availability checks, guided generation, tool calling, prompt/transcript hygiene, privacy boundaries, and Instruments proof. Use when adding on-device Apple intelligence, local model summarization, extraction, classification, or tool-backed reasoning to an Apple app.
---

# Apple Foundation Models

## Purpose

Use this skill when the app should use Apple's on-device Foundation Models instead of a third-party LLM API. Keep the feature local, bounded, testable, and explicit about availability and fallback behavior.

Consult current Apple Developer documentation before relying on exact API syntax. Foundation Models is an Apple 27 stack surface and may drift across betas.

## Workflow

1. Define the product job.
   - Name the user-visible task: summarize, classify, extract, rank, rewrite, explain, or suggest.
   - Decide whether the model result is advisory, draft content, or an action trigger.
   - Avoid using a model where deterministic code or a simple rule is more trustworthy.

2. Check availability and privacy.
   - Gate model use behind the platform's availability APIs.
   - Keep sensitive data local and minimize transcript content.
   - Define fallback behavior for unsupported devices, disabled Apple Intelligence, missing language support, or failed generation.

3. Choose output shape.
   - Prefer guided generation or typed structured output when the app needs durable state.
   - Use constrained schemas for extraction, classification, and command planning.
   - Keep free-form text for clearly user-facing prose drafts or explanations.

4. Use tool calling deliberately.
   - Tools should expose narrow app capabilities, not raw persistence or broad side effects.
   - Validate tool inputs before mutating app state.
   - Keep a human confirmation step for destructive, expensive, privacy-sensitive, or externally visible actions.

5. Test and instrument.
   - Add deterministic tests around prompt construction, schema handling, tool routing, fallback, and error handling.
   - Use the Foundation Models Instrument when prompt/response/token/tool-call behavior matters.
   - Record the scenario, device/runtime, model availability, prompt shape, output shape, and observed failure mode.

## Strong Defaults

- Keep prompts and schemas close to the feature module.
- Keep model sessions behind an interface owned by the intelligence module.
- Do not introduce third-party LLM APIs unless an accepted design says why local Apple models cannot meet the requirement.
- Treat model output as uncertain until app code validates structure and meaning.

## Output

Provide:

- feature job and user-facing value
- availability and fallback policy
- prompt/schema/tool surface
- privacy boundary
- proof command or Instruments evidence
- remaining risk
