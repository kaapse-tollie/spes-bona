# Spes Bona Audit Issues — Open

Last refreshed: 2026-10-29

Approved implementation baseline: `51c98bf32fc9f9049c99f858f5a558bdfde0dffe`

Target: Victoria 3 `1.14.5` Open Beta Update 4, Steam build `25629520`, branch `1.14-openbeta`, core depot manifest `5521822647051867164`

Dependency baseline: Community Mod Framework `1.66.0`, commit `807c32ff42b75714a3a0e090c0db3357b5e46ed7`, plus `sb-1.14.3-r1`

## Status

This register tracks **open work only**: the five machine-readable deferred gates and the separate content item below, the remaining FA-round items, the OB1 follow-up findings, playtest follow-ups, and content-design decisions awaiting DP. Closed tickets from every audit round live in [audit_issues_completed.md](audit_issues_completed.md).

The [2026-10-13 checkpoint review](compatibility/checkpoint_review_2026_10_13.md) records four unit-test failures, one error, and five historical skips, plus compatibility drift against the installed 1.14.5 game. The 0.20.2 rebase resolves those baseline/bookkeeping issues; rebase results and explicitly conditional historical checks are recorded in the [1.14.5 rebase report](compatibility/1_14_5_rebase.md). That validation recorded 15 PASS, two WARN and zero failed gates. The [17 October spawn audit](compatibility/boer_spawn_setup_2026_10_17.md) now records one unrelated unit-test failure, also reported by the localisation gate: the existing `.050` Pretorius spelling correction differs from its reviewed-text baseline. Engine certification remains pending.

Static success is not runtime certification. Strict release certification remains contingent on every engine-only case in `Docs/compatibility/1_14_5_runtime_matrix.md`; every unrun row remains `Engine pending`. Earlier runtime matrices remain historical evidence.

## Major pre-release performance TODO — simulation tick times

**`PERF-20261028-01` — Major priority; open; reported by DP on 28 October 2026.** Tick times have become markedly slower during the Zulu court/civil-war testing. Measure the regression before selecting a fix; neither the court nor the latest force changes are yet established as its cause.

DP should collect comparable timings/profiler output at a fixed game speed and machine/settings: fresh campaign, developed peaceful court, claimant preparations, active civil war, and post-war reunification. Compare retained source checkpoints using compatible disposable campaigns. Inspect weekly polling/event queues, monthly/annual court and roster work, movement/IG recalculation, modifier churn and split/reunion work; distinguish a one-off transition stall from sustained daily slowdown. Keep game version, CMF, DLC/load order, date and population/army size in the evidence. Codex can analyse saved logs/source; DP launches and profiles.

**Completion:** a reproducible baseline, identified hot path(s), measured before/after tick costs and regression checks showing political/war behaviour is preserved. Do not optimise by removing agreed mechanics or by speculative global cadence changes. No performance fix is included in the current claimant follow-up.

## Major pre-release balance TODO — Bantu starting positions

**`BAL-20261025-01` — Major priority; open; scheduled for the pre-release balance pass by DP on 25 October 2026.** Review the technological and economic starts of BST, SWZ, ZUL and GZA. The research briefs are saved; their recommendations are not implemented balance changes.

Start with the [comparative brief](sb_bantu_starting_position_comparison_2026_10_25.md), then the country evidence:

| Country | Saved brief | Principal review targets |
|---|---|---|
| Basotho / BST | [1836 audit](bst_1836_technology_economy_audit_2026_10_25.md) | Rationalism and education assumptions; early British support treaty; ranch and trade-centre employment. |
| Swazi / SWZ | [1836 audit](swz_1836_technology_economy_audit_2026_10_25.md) | Agricultural employment and ownership; literacy; slave-pop allocation; overlapping military penalties. |
| Zulu / ZUL | [1836 audit](zul_1836_technology_economy_audit_2026_10_25.md) | Logging and ranch scale/ownership; literacy; technology unlocks versus their historical labels. |
| Gaza / GZA | [1836 audit](gza_1836_technology_economy_audit_2026_10_25.md) | Farm and subsistence representation; literacy; external exchange; direct control versus tributary reach. |

The shared pass covers starting technologies and their dependencies, literacy by profession and subsequent growth, commercial employment/ownership versus subsistence, and the combined effects of army laws, units and firearms penalties. Carry forward the observations under `PT-20261017-05` and `ZUL-EDU-01`; keep initial literacy distinct from later growth and technology spread.

**Completion:** record fresh 1836 baselines and early development for all four tags; agree and document country-specific balance decisions against the saved evidence; implement the agreed changes with dependency/regression checks and DP gameplay verification. Measure actual technology ownership, employment, literacy, qualifications, prices and market connections rather than treating authored capacities as observed results. Exact replacement values and technology removals remain undecided.

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

## Playtest follow-ups — 16 October 2026, 21:35

DP reached Natalia's formation and stopped for the night. These are follow-up
notes, mostly outside the Anglo-Zulu arc. The 17 October army follow-up is
recorded below. The limited runtime result is recorded in the
[1.14.5 matrix](compatibility/1_14_5_runtime_matrix.md).

| ID | State | Observation / requested change | Follow-up |
|---|---|---|---|
| `PT-20261016-01` | Review requested | The grain/Corn Laws chain fires for most SB tags because of their starting setup and small size. | Review the effective Vanilla/CMF eligibility and event effects against SB starting economies. Determine appropriate eligibility/balance; no blanket exclusion has been agreed. |
| `PT-20261016-02` | Change requested; not implemented | Prevent the liberal movement from forming while Boer tags remain frontier republics. DP observed inappropriate liberal-story approval penalties for the Kommandante. | Review `REPLACE:movement_liberal` in `common/political_movements/zzz_sb_cape_political_movement_overrides.txt`, which currently has a CAP-specific exclusion but no Boer frontier-republic exclusion. Scope the restriction to the frontier phase, retain ordinary post-frontier eligibility, and trace the approval event's eligibility too. |
| `PT-20261016-03` | Source correction applied; engine replay pending | The 1839-11-01 autosave confirms one empty NAL army plus the two-unit Natalia Commando, both created on 1839-10-27. | Muster NAL/TRN/ZPB/LYD commandos before commissioning or transferring generals; assign the intended commander afterwards. KLR's founder is civilian; NRP/SGO do not create a second authored army. Replay from before formation. Existing saved armies are not removed. See the [spawn audit](compatibility/boer_spawn_setup_2026_10_17.md). |
| `PT-20261016-05` | Polish TODO only | Rebalance the first Great Trek GDP milestone by tag: keep ORA at **25,000**, consider **30,000 for NAL** because of Natal's larger population. | The current shared stage-one gate is `root.gdp >= 25000` in `common/journal_entries/1-02_sb_great_trek.txt`. Review tag-specific GDP targets and their displayed text together in a later polish pass. Do not change the values now. |

## Playtest follow-ups — 17 October 2026

| ID | State | Observation / requested change | Follow-up |
|---|---|---|---|
| `PT-20261017-01` | Reproduced by DP; design hold retained | ORA–BST occupation issue persists on 1.14.5. | Record the failed retest in `B145-05`. Keep the two-stage workaround on hold; no occupation-rule redesign is authorized by this note. |
| `PT-20261017-02` | Reproduced by DP; unresolved | CAP still fails to deploy troops to its immediate front after Natalia refuses Britain. | Record the failed retest in `B145-21`; existing deployment work is not engine-verified. Continue tracing orders, fronts and transport from an active-war checkpoint before choosing another fix. |
| `PT-20261017-03` | Source correction applied; engine replay pending | Martin West briefly becomes British Natal's ruler and AF leader, then a generated Landowner replaces him. The 1848-06-01 save confirms Marinus Vermaak rules while West remains AF leader. | Colonial Administration already precedes installation. Protect the appointment through Vanilla's subsequent government-change ruler selection using its seven-day `keep_current_ruler_var`. No recurring governor reinstall. Replay from before the 1848-05-15 conversion; see the [governor investigation](compatibility/natal_governor_2026_10_17.md). |
| `PT-20261017-04` | Polish TODO only | Boer AIs should ask their compact allies to join defensive diplomatic plays. | Review compact obligations and AI call-in/backing behavior in a later polish pass. No treaty or AI changes in this investigation. |
| `PT-20261017-05` | Wider reform deferred by DP; institutional decree gate implemented, engine verification pending | DP reports literacy around ZUL **30%**, GZA **28%**, SWZ **25%** by January 1847, compared with Ottoman **27%** in 1837. DP suspects base literacy growth plus Promote Social Mobility; the decree supplies **+25 percentage points Education Access** and **+25% Qualifications gain**, not a direct growth-speed multiplier. | Keep the broader literacy/society/production reform as a TODO, with no numerical nerf approved. The implemented **Prerogative/institutional JE** blocks Promote Social Mobility while active and restores normal eligibility on exit; firearms acquisition is separate. Native restrictions are preserved. DP must verify weekly invalidation of existing decrees and ownership changes in the [implementation matrix](zulu_institutions_implementation_2026_10_18.md). Later audit the reported trajectory before designing wider penalties. |
| `PT-20261017-06` | Source correction applied; engine replay pending | Other named appointments share the unguarded native government-refresh path: Boer founders/refresh, Albany's Godlonton, German SWA governors and, with lower observed risk, Klip River's Spies. | DP authorized native seven-day guards in these paths; implementation and scope regressions are in the [appointment report](compatibility/natal_governor_2026_10_17.md#authorized-follow-up-implementation--17-october-2026). Zulu and ordinary succession logic remain unchanged. Replay each founding/appointment and later succession under `B145-25`; no additional replacement or corrected retention has been engine-confirmed. |
| `PT-20261017-07` | Unreviewed text corrected; DP revised `.060`/`.080`; `.081` remains open | Klip refusal-path text mixed the abandoned annexation demand with the current Return State plus Make Protectorate settlement. | Corrected the unreviewed ZUL refusal tooltip and punitive-play description/tooltip. DP subsequently edited reviewed `.060.d`, `.060.a` and `.080.d`; preserve that wording. `.081.d` still claims no frontier change even after partial enforcement, but its false delivery after full victory must first be resolved under `PT-20261017-08`. The separate secession route still uses annexation. |
| `PT-20261017-08` | Source correction applied; engine replay pending | NAL's complete Klip victory followed by Thirteen Chiefdoms opens `.081`, the incomplete/white-peace notice. | Recognise the earned GBR protectorate and finalize Klip in NAL scope during handoff before its government choice can change ZUL's type. Both update orders and all three choices pass source regressions. DP confirms both allied demands remain primary and ZUL's Return State remains secondary; the earlier priority proposal is withdrawn. Replay from before victory/handoff, checking `.080` and the government event once and no later `.081`. The occupation-rule workaround remains on hold. See the [save investigation and correction](compatibility/klip_punitive_handoff_2026_10_17.md). |
| `PT-20261017-09` | B works in DP’s early replay; modifier-preservation testing TODO — deferred by DP, 2026-10-17 | Zulu national movement disappeared after the attraction-only annexation package. | Retain the working marked-disband/hidden-receipt replacement. DP authorized preserving tracked Initial Enthusiasm and both Shepstone bonuses at remaining strength/expiry, plus a separate fresh annexation bonus. Source regressions cover timing, reload, expiry, flags and foreign roots. No polling, player-facing bookkeeping or CMF edit. Old untracked grants cannot be recovered; test grants made under the updated scripts in `B145-26`. See the [preservation contract](compatibility/zulu_national_movement_2026_10_17.md#authorized-modifier-preservation). |
| `PT-20261017-10` | Source change applied; engine replay pending | DP requests concept links in `.030` tooltips and relations instead of ZUL loyalists in Control the Crown. | ZUL now gains +15 relations with NAL and GBR; NAL retains +10% Zulu loyalists. Once-only and foreign-root source tests pass. Tooltips use verified concepts, plus the native modifier-description hover for Pop Attraction, which has no dedicated concept. All 88 focused tests pass. DP checks actual tooltip presentation and Crown rewards under `B145-09`. |

## Playtest follow-ups — 29 October 2026

| ID | State | Observation | What closes it |
|---|---|---|---|
| `PT-20261029-01` | Observed; design review open | CAP's successful revolution is recorded on 21 March 1854. All January–May 1857 autosaves show independent CAP with Cape Malay, Cape Creole and Nama primary cultures and `colonial_collapse_var`. Vanilla's The Severed Limb majority-rule option explains the culture replacement through CAP's starting `southern_africa_subject_var`. See the [save investigation and evidence](compatibility/cape_colonial_collapse_2026_10_29.md). | Decide the intended revolutionary/independent Cape settlement; trace marker inheritance, successor identity, cleanup and pending-event delivery. Implement only the agreed change, with source checks and DP verification of colony continuity, revolution victory/defeat, peaceful independence and an already-open collapse event across cleanup/save/reload. The initiating movement and exact choice date remain unproved. |

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
| `OB1-08` | Failed launch — fixes awaiting engine verification | The 2026-09-05 OB1 launch exposed malformed preset entries, script/building/law/name errors, and stale spline identities. Targeted source and local-preset repairs are applied; see `Docs/compatibility/1_14_0_launch_debug_2026_09_05.md`. | Cold-launch a new 1836 campaign and verify `OB1-CF-01`, `OB1-CF-10`, and `OB1-MAP-01`. If harbor-node errors persist, compare a Vanilla-only launch before changing the generated naval network. |

Existing `FA-26R` remains open. The Kimberley historical-date fallback must stay in scope when the Griqualand pipeline receives later content work.

## Recorded OB1 Rebase Decisions Awaiting Runtime Evidence

- `sb_griqualand_west.254` no longer starts three simultaneous plays. Phase A settles claim priority between CAP and the live Boer claimant. Phase B challenges independent WBL only when exactly one legal claim survives. A zero-demand Phase-A white peace preserves both claims and WBL ownership, starts no later play, and finalizes once. All sequence, save/reload, invalidation, retry, proxy, and last-state settlement rows `OB1-GQ-01` through `OB1-GQ-08` remain `Engine pending`.
- The open-beta target is new-game compatibility. No migration of a live pre-OB1 campaign is promised. Save/reload inside a fresh OB1 campaign remains mandatory.

## Validation Contract

The `0.20.2` static release candidate must pass all of these gates on the same integrated tree before a new completed-audit section is added:

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

The direct checker must report zero drift against build `25629520`, branch `1.14-openbeta`, core depot manifest `5521822647051867164`, and CMF `1.66.0` plus `sb-1.14.3-r1`. The suite must also verify the depot delta, structured spline merge, localisation review boundaries and queue, subject/war contracts, AI-incorporation overrides, naval-port connectivity, delayed-event lifecycle, changed-file BOM state, and absence of stale live-baseline labels.

Tiger currently advertises older schema support, so any Victoria 3 `1.14` Tiger diagnostic is advisory unless its schema has been updated. Repository semantic gates remain mandatory. A test that actually fails is a blocker; it cannot be relabelled `Engine pending`.

Release support becomes strict only after every runtime-matrix row is recorded with a fresh campaign on the target build, exact command/save/load order, UTC timestamp, and rotated-log hashes, and fresh logs contain no new SB-authored errors.

Current dependency: CMF `1.66.0` plus `sb-1.14.3-r1`. The patch manifest and expected installed-tree digest are pinned by the compatibility inventory. See `Docs/compatibility/1_14_5_rebase.md` and `Docs/compatibility/1_14_5_runtime_matrix.md`; earlier matrices remain historical evidence.


## Resource discovery follow-up — 18 October 2026

| ID | State | Finding | What closes it |
|---|---|---|---|
| `RES-DISC-01` | Native-source confirmed; separate implementation pending | Seven gold and one oil technology stages use `change_resource_potential`, which changes capped capacity rather than native undiscovered reserves. Earlier documentation incorrectly described them as hidden additions. The diamond-only revision leaves these scripts unchanged. See [native evidence and verification limits](compatibility/diamond_discovery_2026_10_18.md). | A separately scoped correction preserves all budgets/thresholds while populating real undiscovered reserves, with fresh-game discovery and ownership checks. |


## Zulu institutions and court politics — 18 October 2026

| ID | State | Finding | What closes it |
|---|---|---|---|
| `ZUL-INST-01` | Implementation complete; engine verification pending DP | Ongoing Prerogative, law-scaled Institutional Reach, named-following politics, constitutional movements/coups, and outcome-driven Thirteen Chiefdoms replace terminal dynasty/deadline mechanics. | Run the [fresh-game and pre-partition matrix](zulu_institutions_implementation_2026_10_18.md#dp-engine-matrix--every-row-pending), including one-state ideological civil war, active-decree invalidation and repeated callback/open-popup checks. |
| `ZUL-INST-02` | Deferred country rollout | The institutional core is separated from Zulu-specific cast/content. | DP verifies Zulu before adding other landed Bantu country profiles. NGN's existing Zulu inheritance remains included. |
| `ZUL-EDU-01` | Deferred to major pre-release balance pass | Broader literacy and social/production-technology penalties are not part of this implementation. Social Mobility is gated while the institutional JE is active. | Include in `BAL-20261025-01` above; retain DP's literacy-growth observations. Exact penalties remain undecided. |
| `LOC-20261018-01` | Existing static regression failure; prose preserved | Reviewed namespace baselines differ from current working-tree wording in `sb_natal_crisis.050`, `sb_klip_river_county.060`, `.080`. | Resolve approval bookkeeping explicitly; this implementation neither edits their reviewed narrative nor silently repins its baseline. |
