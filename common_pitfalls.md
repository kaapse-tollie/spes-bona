# Common Victoria 3 modding pitfalls

Use this index before changing or reviewing scripts or investigating a regression.
Select the relevant topics below. Search those files first using headings and
rule IDs, then read the matched rule sections in full, including their exceptions
and verification limits. Read a whole topic when most of its rules apply.

Follow affected callers and consumers. Expand to another topic when the selected
rules and available task/code evidence leave a concrete question unresolved.
A shared keyword alone does not justify another topic. Search the whole reference
when the index cannot locate the issue; there is no fixed topic limit.

[Repository instructions](AGENTS.md) contain working boundaries and task-specific
skill routes.
The [localisation review policy](Docs/policies/localisation-review.md) is required
reading before editing or reviewing localisation, classifying markers, or writing
event/journal flavour prose.

## Topic index

| Read when working on | Topic | Rule prefix |
| --- | --- | --- |
| Scope changes, shared helpers, saved actors or foreign event roots. | [Scope and reference identity](Docs/pitfalls/scope.md) | `SCP` |
| Delayed events, open choices, retries, receipts or cancellation. | [Event scheduling, choices and cleanup](Docs/pitfalls/events.md) | `EVT` |
| Country creation, annexation, restoration, inheritance or creation callbacks. | [Country creation, inheritance and object lifetimes](Docs/pitfalls/country-lifecycle.md) | `LIFE` |
| Counters, projections, snapshots, rankings, arithmetic or random selection. | [State modelling, arithmetic and selection](Docs/pitfalls/state.md) | `STATE` |
| Durations, decay, repeated grants or modifier cleanup. | [Time, modifiers and reversible effects](Docs/pitfalls/modifiers.md) | `MOD` |
| Tooltip evaluation, localisation context, journal widgets, portraits or GUI layout. | [Tooltips, localisation and GUI](Docs/pitfalls/presentation.md) | `UI` |
| Templates, identity, careers, traits, succession records or character roles. | [Characters, templates and political roles](Docs/pitfalls/characters.md) | `CHAR` |
| Laws, movement eligibility, recruitment or political calculations. | [Native laws, movements and political calculations](Docs/pitfalls/politics.md) | `POL` |
| Diplomatic plays, demands, civil-war callbacks or military allocation. | [Civil wars, diplomatic plays and military allocation](Docs/pitfalls/conflicts.md) | `WAR` |
| Construction queues, resource discovery, markets or payments. | [Economy, resources and effect semantics](Docs/pitfalls/economy.md) | `ECON` |
| Overrides, dependency updates, copied definitions or performance. | [Overrides, rebases and performance](Docs/pitfalls/compatibility.md) | `UPSTREAM` |
| Image reconstruction, compositing, export checks or visual presentation. | [Visual assets and presentation checks](Docs/pitfalls/assets.md) | `ASSET` |
| Regression design, save inspection, crash attribution or engine replay. | [Verification and diagnosis](Docs/pitfalls/verification.md) | `VERIFY` |

## Common combinations

- Cross-country event chains: `SCP` for actor and state ownership; `EVT` for delivery,
  choices and cleanup.
- Country creation callbacks: `LIFE` for readiness, `SCP` for scope boundaries, and
  the affected subsystem, such as `POL` for inherited-law or movement effects.
- Tooltip changes: `UI` plus the topic governing the effect being previewed.
- War settlement and restoration: `WAR` and `LIFE`; add `STATE` when restoring
  snapshots or committing outcomes.
- Upstream changes: `UPSTREAM` plus each affected subsystem.
- Regression tests, crash diagnosis and replay plans: `VERIFY` plus the rule
  describing the failure mechanism.

## Evidence and version limits

These lessons come from investigations of Victoria 3 1.14.x, including native
inspection of 1.14.5. Treat implementation details as version-bound: recheck them
against the target build's script documentation, Vanilla and DLC examples, and
the effective Community Mod Framework (CMF) definitions. Hail Columbia and Gates
of the Bosphorus provide useful implementation examples, but an example from
another version is not an API contract. Supporting investigations live in
[Docs/compatibility/](Docs/compatibility/).

Each rule retains its own evidence limits. Static validation, source-executed
tests, save observations and engine replay establish different things; do not
promote a proposed mitigation or pending replay into a confirmed fix.

## Maintaining the reference

Keep one canonical rule for each reusable lesson. Merge duplicates without losing
exceptions or verification limits. Keep rule IDs and their explicit anchors
stable; add new IDs without renumbering existing ones. The rule format is a
failure mechanism, prevention, and the limit of the available evidence.

When adding a lesson, merge it into the relevant topic. Keep the reusable cause,
prevention and evidence limit there; put exact dates, saves, actors, tuning trials
and feature-specific reproduction steps in the supporting investigation. Feature
specifications, balance values, incident chronologies and pending playtest lists
belong in their own documents.
