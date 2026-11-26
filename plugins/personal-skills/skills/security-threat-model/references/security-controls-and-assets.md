# Security Controls and Asset Categories

A category checklist for coverage. Prefer concrete, system-specific items over
generic text.

## Asset categories (pick only what applies)

- User data (PII, content, uploads)
- Authentication artifacts (passwords, tokens, sessions, cookies)
- Authorization state (roles, policies, ACLs)
- Secrets and keys (API keys, signing keys, encryption keys)
- Configuration and feature flags
- Models and weights (if ML systems)
- Source code and build artifacts
- Audit logs and telemetry
- Availability-critical resources (queues, caches, rate limits, compute budgets)
- Tenant isolation boundaries and metadata

## Security control categories

- Identity and access: authN, authZ, session handling, mTLS, key rotation
- Input protection: schema validation, parsing hardening, upload scanning, sandboxing
- Network safeguards: TLS, network policies, WAF, rate limiting, DoS controls
- Data protection: encryption at rest/in transit, tokenization, redaction
- Isolation: process sandboxing, container boundaries, tenant isolation, seccomp
- Observability: audit logs, alerting, anomaly detection, tamper resistance
- Supply chain: dependency pinning, SBOMs, provenance, signing
- Change control: CI checks, deployment approvals, config guardrails
