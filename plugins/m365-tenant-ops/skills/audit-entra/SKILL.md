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
   - On macOS, remember the caller is normally `zsh`: either start an interactive PowerShell session with `pwsh -NoLogo -NoProfile`, or wrap each unattended command with `pwsh -NoLogo -NoProfile -Command '<PowerShell>'`. Never send a bare PowerShell cmdlet to the macOS shell.
   - If Graph authentication is missing, propose the local mutation before running it. Prefer the smallest current-user install:

     ```zsh
     pwsh -NoLogo -NoProfile -Command 'Install-PSResource -Name Microsoft.Graph.Authentication -Repository PSGallery -Scope CurrentUser -TrustRepository -Quiet -ErrorAction Stop'
     ```

   - Verify the installed module and required commands from a fresh `pwsh -NoProfile` process. Do not persistently mark PSGallery trusted merely to suppress the installation prompt.

3. Plan the smallest read-only access set.
   - Name the exact questions and Graph commands before requesting scopes.
   - Resolve their least-privileged delegated permissions from current Microsoft Graph metadata or documentation.
   - Require an MSP-owned, reviewed application client ID for Graph access to a client tenant. If none exists, remain portal-only and report Graph as blocked by missing approved infrastructure.
   - Do not omit `-ClientId` or use the shared Microsoft Graph Command Line Tools application for client-tenant operations. Its tenant-local delegated grant can accumulate unrelated authority across prior sessions.
   - Treat first-time consent, admin consent, app registration, credential creation, diagnostic export, and permission escalation as mutations requiring review.

4. Connect interactively to the explicit tenant.
   - For an agent-operated macOS terminal, prefer one non-PTY `pwsh -NoLogo -NoProfile -Command '<complete PowerShell batch>'` process containing connect, context verification, planned reads, and disconnect. Interactive PowerShell PTYs can emit terminal-control replies that corrupt injected commands; use one only after proving clean command entry in the live host.
   - Use delegated device authentication and `-ContextScope Process` for human-led audits. Capture the short-lived device code from the managed PowerShell process. When browser control is available, open `https://login.microsoft.com/device` in the user's designated private browser window and enter the code there; hand off only for account selection, password, MFA, or an unapproved consent decision. When browser control is unavailable, display the code prominently in the conversation instead of directing the user to a hidden terminal.
   - Supply both the approved application client ID and target tenant ID explicitly.
   - Pass only the previously reviewed read scopes. Pause at any unexpected consent or admin-consent screen because accepting it can mutate tenant authorization.
   - Before the first query, inspect `Get-MgContext` and programmatically verify the expected account, tenant ID, delegated authentication, process context, and complete effective scope set. Requested scopes are not an authority boundary: an existing delegated grant can cause Microsoft to issue previously consented scopes as well.
   - Stop and disconnect on an unexpected identity, tenant, application-only context, persistent context, unexpected substantive scope, or any write-capable scope. Report requested scopes separately from effective scopes.

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
