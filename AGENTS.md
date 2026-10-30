# Repository instructions

## Working boundaries

- Change only what the task requires; preserve unrelated work already present.
- SB requires all Victoria 3 DLC, including DLC whose content SB does not directly use. Design against that baseline; do not add no-DLC alternatives unless DP changes this policy.
- Use British English in player-facing text and documentation. Preserve script identifiers and quoted upstream names.
- Existing `# ### REVIEWED ###` markers record DP's approval. Preserve them; changes within reviewed localisation namespaces are limited to spelling or grammar. If mechanics require a substantive rewrite, ask DP to supply or approve the replacement before editing it.
- Leave launching Victoria 3 to check launch errors to DP. Do not launch the game for this purpose. Run relevant static validation and inspect existing logs as needed; record launch checks awaiting DP as pending.

## Read for the task

| Task | Required reading |
| --- | --- |
| Change or review Victoria 3 scripts; debug a regression | [Pitfall index](common_pitfalls.md), then the applicable topic and rule sections. Search selected files first; follow the index's guidance for expanding the search. |
| Change a cross-country chain or a helper called from another country's event or a diplomatic-play callback | Relevant [scope rules](Docs/pitfalls/scope.md) and [event lifecycle rules](Docs/pitfalls/events.md). Trace every handoff and verify helper routing with a foreign root. |
| Edit or review localisation, classify review markers, or write event/journal flavour prose | Read the complete [localisation review policy](Docs/policies/localisation-review.md) before acting. |
| Draft or substantially rewrite event prose or choices; review event presentation | Use the `victoria-3-events` skill from the active skill catalogue. Apply it within the localisation policy's approval boundaries. |
| Design regression checks, inspect saves or diagnose a crash | Relevant [verification and diagnosis rules](Docs/pitfalls/verification.md). |

Read supporting investigations when their evidence is needed. Historical reports
explain observations and limits; current feature specifications determine intent.

## Verification

Use the [README validation guidance](README.md) for checks appropriate to the
change. Keep static and engine verification distinct: successful static checks
do not prove in-game event delivery. Report what was checked, its limits, and any
pending engine scenarios.

## Versioning before committing or pushing

- Keep `descriptor.mod` and `.metadata/metadata.json` on the same version.
- Major: only when DP explicitly says so.
- Minor: significant thematic content or engineering work.
- Patch: tweaks and elaboration within an existing thematic content bloc, plus fixes, balance adjustments, localisation changes and maintenance.
- A batch of related commits may share one bump. For a mixed batch, use the highest applicable increment and reset lower components when incrementing a higher component.
- Complete the version update before committing or pushing, and verify the two version fields still match.

## Maintaining this hierarchy

Keep this file to repository boundaries and routing. When an investigation
establishes a lesson, update its canonical topic through the
[pitfall index](common_pitfalls.md). Preserve the cause, prevention and verification
limits; label unresolved hypotheses explicitly. Put incident-specific evidence
and reproduction steps in the supporting investigation.
