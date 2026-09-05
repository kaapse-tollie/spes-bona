# Spes Bona Audit Issues — Open

Last refreshed: 2026-09-04

Approved implementation baseline: `51c98bf32fc9f9049c99f858f5a558bdfde0dffe`

Target: Victoria 3 `1.14.0` Open Beta 1, Steam build `25081502`, branch `1.14-openbeta`, core depot manifest `3868129321396195520`

Dependency baseline: Community Mod Framework `1.66.0`, commit `807c32ff42b75714a3a0e090c0db3357b5e46ed7`

## Status

This register tracks **open work only**: the six deferred gates below, the remaining FA-round items, the OB1 follow-up findings, and content-design decisions awaiting DP. Closed tickets from every audit round live in [audit_issues_completed.md](audit_issues_completed.md).

Static success is not runtime certification. Strict release certification remains contingent on every engine-only case in `Docs/compatibility/1_14_0_open_beta_1_runtime_matrix.md`; every unrun row remains `Engine pending`. The unchanged `Docs/compatibility/1_13_11_runtime_matrix.md` is historical evidence only.

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
| `FA-24` | Awaiting DP decision | MTB territory trim. Research delivered: `../References/mtb_territory_proposal.md` (tiered proposal; preserves every Vegkop event input province). |
| `FA-26R` | Reopened by playtest | Kimberley discovery can remain blocked long after the historical discovery window when WBL is annexed before discovery. In the 1879-01-01 ORA playtest save, Griqualand West had no diamond mine, potential, or discovery marker because ORA lacked both `mechanical_tools` and `dynamite`, while CAP lacked the currently required `dynamite`. Decide and implement a historical-date fallback (recommended within 1867-68) while retaining the event-led 1 + 19 package; cover the late, post-WBL-annexation case with a static test and fresh-start runtime check. |

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
- **Cape colonization of Namaqualand:** playtesting has occasionally shown Cape Colony
  colonizing Namaqualand without the expected story flag. Reproduce the route and audit
  every colonization-rights grant before changing the gate.

## 1.14 Open Beta 1 Findings Registered for Follow-up

These findings were exposed or rechecked during the exact OB1 rebase. They are outside the approved war, subject, AI-incorporation, map, asset-path, and two isolated script-fix scope. This patch records them without silently changing their mechanics or presentation.

| ID | State | Finding | What closes it |
|---|---|---|---|
| `OB1-01` | Runtime/design follow-up | Several treaty matchers can select or withdraw more than their authored bundle: compact renewal, Martinus/ZPB compact cleanup, Natalia annulment, frontier-goods cleanup, TRN–ZUL expiry, and partial Delagoa/imperial duplicate checks. OB1 AI ship selling increases the chance that an unrelated ship-transfer article shares such a treaty. | Add scenario tests for mixed treaties and narrow each matcher only where the authored article identity can be proven. Do not infer safety from the isolated ORA–ZUL small-arms fix. |
| `OB1-02` | Design/reachability follow-up | `STATE_LOURENCO_MARQUES_state_name_assign` is never dispatched, leaving its authored Portuguese/Southern-Bantu state and hub names unreachable. The German Hereroland/Namaqualand keys for Windhuk, Tsumeb, Swakopmund, and Walvis Bay have no assign effect or `set_hub_names = german` route. | Decide the intended routing policy, make the smallest explicit routing change, and cover both positive and negative name transitions. |
| `OB1-03` | Design follow-up | SB's TRN replacement omits Vanilla `dyn_c_transvaal_colony`, so a mature British-controlled TRN can retain republic naming. This is a missing design branch, not a safe mechanical rebase. | DP selects the intended name/tier and approves its localisation before implementation. |
| `OB1-04` | Runtime gameplay follow-up | `law_sb_amabutho_system` may omit `country_can_only_conscript_peasants_bool = yes`. All referenced unit IDs still resolve, so the audit does not prove a parser defect. | Run the formation/conscription gameplay case, then make a balance decision from observed unit eligibility. |
| `OB1-05` | Runtime entitlement follow-up | Seven event-image calls resolve on the all-DLC installation but have no matching entitlement gates: `sb_klip_river_county.010` at `events/sb_klip_river_county_events.txt:43` (`ep1_redcoats`); `sb_nam.140` at `events/sb_namibia_events.txt:1253` (`votp_french_algeria`); `sb_natal_crisis.110` at `events/sb_natal_crisis_events.txt:1535` (`votp_gunboat_diplomacy`); `sb_natal_crisis.115` at `events/sb_natal_crisis_events.txt:2104` (`ep1_transfer_of_authority`); `sb_natal_interwar.005` at `events/sb_natal_interwar_events.txt:63` (`ip4_colonial_exploitation_going_well`); `sb_natal_interwar.030` at `events/sb_natal_interwar_events.txt:153` (`ep1_transfer_of_authority`); and `sb_pink_map.040` at `events/sb_pink_map_events.txt:305` (`ep1_printing_press`). | Run each exact event with its relevant DLC disabled and record image/error-log evidence before changing DP-selected art or adding gates. |
| `OB1-06` | Runtime/design follow-up | ORA/TRN have no explicit `stance_colonize_region`, while OB1's default excludes unrecognized countries. It is unknown whether adjacency or another engine path still produces the intended behavior. | Observe fresh ORA/TRN cases under OB1, then decide whether an explicit stance is needed. |
| `OB1-07` | Static war-launch architecture follow-up | Four launch/support paths outside the approved Step 8 file set still select a play through `random_diplomatic_play`: `sb_boer_conventions.142`, `sb_natal_crisis.114`, `sb_imperial_confederation.031`, and `sb_join_natalia_against_britain`. The first three perform post-create mutation; the support helper can still select ambiguously if matching plays coexist. | Give each route a pre-create lease and actual-root on-start configuration, or bind the support helper to one saved exact play identity. Add failed-create, duplicate-play, back-down, and cleanup tests before removing this follow-up. |

Existing `FA-26R` remains open. The Kimberley historical-date fallback must stay in scope when the Griqualand pipeline receives later content work.

## Recorded OB1 Rebase Decisions Awaiting Runtime Evidence

- `sb_griqualand_west.254` no longer starts three simultaneous plays. Phase A settles claim priority between CAP and the live Boer claimant. Phase B challenges independent WBL only when exactly one legal claim survives. A zero-demand Phase-A white peace preserves both claims and WBL ownership, starts no later play, and finalizes once. All sequence, save/reload, invalidation, retry, proxy, and last-state settlement rows `OB1-GQ-01` through `OB1-GQ-08` remain `Engine pending`.
- The open-beta target is new-game compatibility. No migration of a live pre-OB1 campaign is promised. Save/reload inside a fresh OB1 campaign remains mandatory.

## Validation Contract

The `0.20.0` static release candidate must pass all of these gates on the same integrated tree before a new completed-audit section is added:

```sh
python3 -B -m unittest discover -s tests -q
python3 -B tools/validate.py --skip-cmf-sync
python3 -B tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --cmf-root '/path/to/Community Mod Framework' \
  --tiger
python3 -B tools/check_override_inventory.py \
  --game-root '/path/to/Victoria 3/game' \
  --cmf-root '/path/to/Community Mod Framework'
git diff --check
```

The direct checker must report zero drift against build `25081502`, branch `1.14-openbeta`, core depot manifest `3868129321396195520`, and CMF `1.66.0`. The suite must also verify the depot delta, structured spline merge, localisation review boundaries and queue, subject/war contracts, AI-incorporation overrides, naval-port connectivity, delayed-event lifecycle, changed-file BOM state, and absence of stale live-baseline labels.

Tiger currently advertises older schema support, so any Victoria 3 `1.14` Tiger diagnostic is advisory unless its schema has been updated. Repository semantic gates remain mandatory. A test that actually fails is a blocker; it cannot be relabelled `Engine pending`.

Release support becomes strict only after every runtime-matrix row is recorded with a fresh OB1 run, exact command/save/load order, UTC timestamp, and rotated-log hashes, and fresh logs contain no new SB-authored errors.
