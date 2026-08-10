---
name: audit-entra
description: Audit Microsoft Entra and Microsoft 365 tenants through delegated Microsoft Graph PowerShell and current admin surfaces. Use for guest access, sign-in failures, directory history, external collaboration, Conditional Access, application permissions, or other tenant troubleshooting that must remain read-only until mutations are reviewed.
---

# Audit Entra

## Outcome

Produce an evidence-backed tenant diagnosis without changing tenant state. Keep confirmed facts, inferences, missing access, expired evidence, and proposed mutations distinct.

## Workflow

1. Establish the practical outcome, affected identity or resource, resource tenant, time window, and client authorization. Stop if the tenant or authority is ambiguous.

2. Inspect the live environment before prescribing setup.
   - Verify `pwsh` and its version.
   - Discover installed Microsoft Graph modules rather than assuming them.
   - Prefer the current portal or Microsoft documentation for drift-prone commands, permissions, licensing, and retention.

3. Plan the smallest read-only access set.
   - Name the exact questions and Graph commands before requesting scopes.
   - Resolve their least-privileged delegated permissions from current Microsoft Graph metadata or documentation.
   - Treat first-time consent, admin consent, app registration, credential creation, diagnostic export, and permission escalation as mutations requiring review.

4. Connect interactively to the explicit tenant.
   - Use delegated authentication and `-ContextScope Process` for human-led audits.
   - Supply the tenant ID explicitly.
   - Before querying, inspect `Get-MgContext` and verify the expected account, tenant ID, delegated authentication, and granted scopes.
   - Stop on an unexpected identity, tenant, application-only context, or write-capable scope.

5. Trace the problem through separate control layers.
   - Identity: object, user type, account state, invitation or redemption state.
   - Authentication: sign-in result, application, resource tenant, correlation ID, authentication details.
   - Policy: Conditional Access, external collaboration, cross-tenant access, sharing limits, governance.
   - Authorization: groups, applications, site or resource permissions, inheritance, item-specific grants.
   - Automation: service principals, provisioning, access reviews, entitlement management, lifecycle workflows.

6. Correlate sources instead of treating one surface as complete.
   - Use Graph for structured tenant evidence and the relevant admin portal for current configuration and permission-bound surfaces.
   - Use the ticket, affected user, target resource, and event time to constrain the search.
   - Record a 401 or 403 as a blocked check, not proof that the feature is absent.
   - State when log retention prevents attribution; another tool cannot recover evidence Microsoft no longer retains.

7. Preserve the read-only boundary.
   - Use retrieval and reporting operations only.
   - Keep customer content in memory or concise console output by default; create no exports, tenant profiles, or credential files without authorization.
   - If a write appears necessary, stop and provide the exact target, old state, proposed new state, expected effect, rollback, and validation for review.

8. Close the session and report.
   - Disconnect the Graph session.
   - Lead with the diagnosis or smallest next check.
   - Include verified evidence, unresolved cause, blocked surfaces, retention limits, and the mutation ledger.

## Scope boundary

Keep Windows Server, Active Directory Domain Services, endpoint, and LiveConnect operations outside this skill. Route those through their own transport- and authority-specific workflow.
