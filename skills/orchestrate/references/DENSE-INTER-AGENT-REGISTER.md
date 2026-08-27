# Dense Inter-Agent Register

Use these patterns when an orchestration assignment, handoff, steering message,
or result report needs a concrete compact form. They demonstrate a register,
not a required schema: retain only fields that change the recipient's action or
the root's final decision. Do not add fields whose values are unknown. Use
numeric confidence only when a source supplies it or the assessment method
defines it; otherwise state the evidence status directly.

## Assignment

```text
ROOT→SCOUT auth401: OUTCOME=locate cause after cfg rollout; AUTH=read-only;
CHECK=diff pre/post cfg + auth logs, repro once; EXCLUDE=code/config/provider
mutation; STOP=causal delta reproduced or secret/mutation required; RETURN=
finding|evidence|conf|changes|residual|next.
```

## Confirmed Result

```text
SCOUT→ROOT auth401: FINDING=OAuth redirect mismatch; introduced=14:32Z;
EVIDENCE=post-rollout URI repros 401, prior URI succeeds; conf=high;
CHANGES=none; RESIDUAL=other env/provider registrations unverified;
NEXT=align cfg, then login+refresh+logout smoke.
```

## Uncertain Result

```text
SCOUT→ROOT pkg-install: HYP=Arch packaging incompat; conf=low; STATE=testing;
EVIDENCE=Debian path assumed by installer, causal repro pending; PUBLIC_WRITE=
hold; NEXT=compare clean Arch/Debian installs.
```

The uncertainty markers are load-bearing. This lossy relay is invalid:

```text
pkg bug is Arch incompat; file issue.
```

## Steering

```text
ROOT→SCOUT pkg-install: continue repro only; do not publish or patch; report when
HYP confirmed/disconfirmed or blocked on unavailable fixture.
```

## Delegate Handoff

```text
SCOUT→REVIEW auth401: inspect evidence bundle @/tmp/auth401; QUESTION=does cfg
delta fully explain 401 onset? AUTH=read-only; RETURN=confirm|counterevidence|
conf. Scope/authority changes→ROOT.
```

Peer `NEXT` and `RECOMMEND` fields communicate advice, not permission. The
recipient acts only within its own root-granted assignment and returns requests
for new authority or cross-lane action to root.

## Root Translation For The User

Inter-agent traffic:

```text
SCOUT→ROOT auth401: FINDING=redirect mismatch; introduced=14:32Z; repro=401;
CHANGES=none; conf=high.
```

Human-facing answer:

```text
The 401s are caused by an OAuth redirect-URI mismatch introduced in the 14:32
UTC configuration rollout. Read-only checks reproduced the failure; no code or
configuration was changed. Align the deployed URI with the provider registration,
then verify login, token refresh, and logout in each environment.
```

The root preserves evidence and uncertainty while expanding shorthand, resolving
references, and stating the practical decision in ordinary prose.
