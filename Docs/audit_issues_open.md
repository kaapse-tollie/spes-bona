# Spes Bona Audit Issues — Open

Last refreshed: 2026-08-21

Repository baseline: `de97d34cb1776bfbe804bf524d8d9815ef55b2d7`

Target: Victoria 3 `1.13.11`, Steam build `24799966`, Vanilla checksum `a47f`

Dependency baseline: Community Mod Framework `1.63.0`, commit `bd92022`

## Status

This register tracks **open work only**: the six deferred gates below, the remaining FA-round
items, and content-design decisions awaiting DP. Closed tickets from every audit round live in
[audit_issues_completed.md](audit_issues_completed.md).

Strict release certification remains contingent on the engine-only cases in
`Docs/compatibility/1_13_11_runtime_matrix.md`; those cases cannot be certified by static
analysis and are not marked as passed here.

## Deferred Gates

The machine-readable authority is `tools/deferred_release_gates.json`. Each entry records owner, unblock condition, artifact, and acceptance test.

| ID | Status | Owner | Gate |
|---|---|---|---|
| `BC-20` | Blocked | Spes Bona content design | Broader CAP/GBR restraint duration and war behavior waits for the Southern African wars redesign. |
| `BC-22` | Deferred human | Depro | Remaining Bechuanaland prose is reviewed during in-game testing. |
| `CP-07` | Blocked | Spes Bona compatibility | A dedicated Hail Columbia Legacy Slavery compatibility patch is still required; SB must currently load after Hail Columbia. |
| `SUP-05` | Blocked | Depro | Spline regeneration waits until the release map stack is frozen. |
| `QUAL-09` | Deferred human | Depro | Remaining event prose requires a rolling historical-tone and presentation review. |
| `CONTENT-01` | Deferred content | Spes Bona content design | Transvaal and Orangia gold balancing belongs to the next resource-content pass. |

Preserved user notes:

- `BC-20`: "Move to blocked, further content (esp SAn wars) are needed. Also add CAP to this befriend strategy towards the boers, otherwise a responsible one can override."
- `BC-22`: "### TO REVIEW ### only applies to localisation blocs, remove those outside this. Then move this to deferred. This must be done by a human (me), I do it on a rolling basis when I come across the events in-game while testing."
- `SUP-05`: "This you cannot fix, I've been delaying fixing this bug bc spline changes are not compatible across mods. I will fix it near release. You can mark this as low / blocked."

`BC-20` immediate mitigation remains active through source-tracked `befriend` goals for GBR and CAP. The separate **Respect the Boer Conventions** diplomatic AI strategy was removed so this mask no longer consumes either country's diplomatic-strategy slot; the deferred gate now covers only the eventual duration and war-specific behavior redesign.

## Open FA Items

Closed FA findings are recorded in the completed register. What remains:

| ID | State | What closes it |
|---|---|---|
| `FA-14` | Backlog | Teach `check_override_inventory.py` to classify additive `zz_` files and localization `replace/` files; register both surfaces. |
| `FA-17` | Backlog | Smoke-contract tests for the 8 uncovered event namespaces (`sb_boer_compacts`, `sb_frontier_ai_wars`, `sb_gaza`, `sb_griqualand_east`, `sb_griqualand_west`, `sb_swazi_border`, `sb_swazi_frontier`, `sb_zulu_court`) and untested `common/` data domains. |
| `FA-19` / `FA-20` | Deferred maintenance | Whitespace/indent normalisation inside hash-pinned overrides; must run together with an inventory-hash regeneration pass. |
| `FA-23` | Awaiting DP decision | QWA reframing. Research delivered: `../References/natal_1836_polities_research_brief.md` (recommendation: one tag renamed away from "Qwabe"; ZUL raid-sphere framing). |
| `FA-24` | Awaiting DP decision | MTB territory trim. Research delivered: `../References/mtb_territory_proposal.md` (tiered proposal; preserves every Vegkop event input province). |


> **FA-09 update (DP, 2026-08-21):** the dead `c:SAF ?= { ... }` relations block (which contained the stray `c:TRN` rows and the duplicated SWZ pair) has been commented out in `common/history/diplomacy/00_relations.txt`; inventory hash regenerated. The manifest wording still says "removes only ORA→TRN" and should be reworded at the next touch of that file.

### Content backlogs spun out of the FA round
- **Formed-TRN opening relations (from DP note in `00_relations.txt`):** nothing sets
  TRN↔SWZ/GZA relations when Transvaal forms, so it starts at 0. Decide whether the trek
  finalization should inject mild hostility toward SWZ (border friction) and GZA, or leave
  neutral and let plays drive relations.


- **Characters for a later pass:** Faku, Maharero kaTjamuaha, Tjamuaha, Nicolaas Waterboer,
  Cape governor succession 1838–61 — evidence and suggestions per figure in
  `../References/character_todo_register.md`.
- **On-start events for content tags** (from FA-11): candidates BST, NGN, SWZ, GZA, ORL,
  ABY-on-emergence.
- **KLR display name:** "Klip River County" vs historiographic "Klip River Republic" was
  reviewed and left unchanged unless DP asks (broad surface: loc, flags, file names, tests).

## Validation Contract

Current static evidence (2026-08-21; corrected during the FA round — the previous entry still said 126 tests, 14/14 categories, 102 keyed overrides, and 17 state-region blocks):

- `139` unit tests pass.
- The integrated validator passes `13/13` categories with `0` failures.
- The override comparison reports `36` exact-path files, `103` keyed overrides, `18` changed state-region blocks, and `0` `replace_path` directives.
- Tiger passes against the installed `1.13.11` game data.
- Localisation structure passes with `91` reviewed and `143` still assigned to human review.
- The delayed-event lifecycle inventory and all `84` scripted war-goal blocks pass their structural checks.
- `git diff --check` passes.

Run:

```sh
python3 -B tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --cmf-root '/path/to/Community Mod Framework' \
  --tiger
git diff --check
```

The suite checks unit tests, exact-path and keyed overrides, game/build/dependency metadata, CMF and Vanilla API surfaces, map connectivity and generated assets, localisation structure, on-action routing, stale and unused symbols, delayed-event lifecycle, deferred gates, and 1.13.11 release invariants.

Release support becomes strict only after every engine case in the runtime matrix is recorded as passing and fresh launch logs contain no new SB-authored errors. Fresh starts are authoritative; active 1.13.9 corridor crises are not migrated.
