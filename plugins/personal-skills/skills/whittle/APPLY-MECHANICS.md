# Apply Mechanics

Read this branch when the user authorized implementation changes. The shared
judgment and guardrails remain in [SKILL.md](SKILL.md).

## Apply The Cut

1. Inspect the target, its owner guidance, the real flow, and existing proof;
   done when you can name the code to cut and every caller and test that
   reaches it.
2. Name the requirement and the complexity that does not help satisfy it.
3. Choose the first option in [SKILL.md](SKILL.md)'s Find The Smallest Owner
   list that fully preserves the outcome.
4. Make the smallest coherent change, including cleanup made obsolete by it:
   tests that exercised only the removed code, and every reference that
   `python3 <this skill's directory>/scripts/leftover_refs.py [names a diff
   cannot show, such as config keys]` lists, run with the target repository as
   the working directory; done when it exits 0. Exit 2 means no removed
   definition was found: pass the removed names. After cutting tests, recheck
   the production code they called: a seam left with no other caller goes
   too, on the terms in [SKILL.md](SKILL.md). Moved or merged code keeps its
   validation and error handling.
5. Run the repository's checks for the changed owner and inspect the final
   diff; done when those checks pass and every hunk serves the named
   requirement.

Do not preserve the wrong owner merely to touch fewer files.

## Output

Lead with the implemented result and proof. Add a rejected alternative or
fuller explanation only when the user asked or its tradeoff changes their next
decision.
