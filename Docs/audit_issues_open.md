# Spes Bona Audit Issues — Open

Last refreshed: 2026-11-22

Approved implementation baseline: `51c98bf32fc9f9049c99f858f5a558bdfde0dffe`

Current implementation target: Victoria 3 `1.15.2`, Steam build `26763837`, branch `public`, core depot manifest `5942745929618312121`

Installed dependency: Community Mod Framework `1.67.9`, commit `9103c9cb4130d46cb18204d588def1266e5c1555`, plus `sb-1.15.2-r1`

The [CMF 1.67.9 update](compatibility/cmf_1_67_9_update_2026_11_19.md) moves the four-point bar gap to the shared outliner row. DP’s fresh-campaign visual checks are pending.

The [combined CMF 1.67.3 / game 1.15.1 patch](compatibility/cmf_1_67_3_and_1_15_1_patch_2026_11_11.md)
imports the reviewed hotfix deltas while retaining SB's Griqua setup and
performance changes. **DP's [fresh-start hotfix checks](compatibility/1_15_1_runtime_matrix.md)
remain pending.** Full static validation passes: **15 PASS, two existing WARN, zero FAIL**.
The [11 November launch review](compatibility/1_15_1_launch_review_2026_11_11.md)
finds no new compatibility-patch parser/scope errors in the supplied capture.
Panama's mismatch is present in native map data. The pre-existing unused
Chiefdoms scope record was subsequently removed with DP's approval after a
reader audit; all 43 focused tests pass. Visual and gameplay acceptance remains pending.
The [7 November smoke pass](compatibility/1_15_0_fresh_smoke_bolivia_2026_11_07.md)
applies to the preceding 1.15.0 target. No save migration is included.

The working-tree port follows the [approved design](compatibility/1_15_0_rebase_design_2026_11_05.md) and [implementation plan](compatibility/1_15_0_implementation_plan.md). Release version is `0.21.3`; source implementation does not certify runtime compatibility. The preceding 1.14.5/CMF 1.66.0 baseline remains recorded in its historical reports.

## Cape Colonial Affairs playtest — 19 November 2026

`PLAY115-08` · **Source and autosaves reviewed. Player replay pending.** DP reports
difficulty with CAP's usual Frontier Colonisation enactment in 1.15.x.

1.15 added Internal Colonisation (`law_internal_colonization`) to Colonial Affairs.
It requires Colonisation technology, and CAP meets its colonial country-type
condition. Vanilla Colonialist **approves** Internal Colonisation and Colonial
Exploitation and is **neutral** on Frontier Colonisation and No Colonial Affairs.
The installed 1.15.2 ideology file matches the 1.15.0 depot hash. SB's pre-1.15
Colonialist mirror at `1a3d7c3` already lists Frontier as neutral. The exact
1.14.5 Vanilla stance remains unverified. [Paradox 1.15 release notes](https://steamcommunity.com/games/529340/announcements/detail/680766201707627232) · [1.15.0 depot record](compatibility/evidence/1_15_0_implementation/current_target.json)

CAP's Imperial Establishment and colonial Industrialists use Vanilla Colonialist.
Internal gives them a preferred alternative and would make a subsequent switch
to Frontier less attractive. The Frontier Settlers and Eastern Cape Separatist
League still strongly favour Frontier. Three 1.15.2 observer saves from May to
October 1842 show No Colonial Affairs active and Per-Capita Taxation in progress.
The Imperial Establishment was in government and the Frontier Settlers were
outside it in the May save. The cause of the player enactment issue remains open.
[Cape interest groups](../common/scripted_effects/sb_interest_group_identity_effects.txt) · [SB ideology stances](../common/ideologies/sb_ideologies.txt)

Replay a fresh player CAP start and compare Frontier's eligibility and support
from the opening No Colonial Affairs and after Internal. Record the cabinet,
interest-group and movement support, and whether enactment can start and pass.
Review where Internal should count in Cape settler pressure and the balance bar,
whose direct law checks still list Frontier, Resettlement and Exploitation.
[Frontier eligibility](../common/laws/00_sb_governance_principles.txt) · [Settler pressure](../common/on_actions/sb_cape_on_action_handlers.txt) · [Cape balance bar](../common/scripted_progress_bars/sb_progress_bars.txt)

## Griqualand East playtest — 14 November 2026

`GLE-20261114-01`: **source correction applied; DP replay pending**. GLE's existing
founding candidates and five-province transfer footprint now accept Cape-owned
as well as Xhosa-owned land. Other owners remain excluded. Replay acceptance
from before the petition is resolved; this does not repair an already completed
settlement. See the [fix and verification record](compatibility/gle_natal_playtest_2026_11_14.md).
DP clarified that Natal's reported extra +20% bonuses came from Farmers and
Extraction Economy; its sugar-only trait remains unchanged and needs no fix.

## Thirteen Chiefdoms playtest — 14 November 2026

`ZUL-CHIEFS-20261114`: **source corrections applied; DP replay pending**.
Five January–May 1886 autosaves confirm frozen container timers and establish
ZUL's weekly tribute/budget figures. The [investigation and checks](compatibility/chiefdoms_playtest_2026_11_14.md)
record the JE-age clock, movement Prominence totals, 15% temporary tribute and
withdrawal from the current Boer/NRP undertaking on joining Natal's overlord.
DP approved halving Chiefdoms bribes after the scaling comparison; the reduction
is applied to new quotes only. Domestic court patronage prices are unchanged.
The later [May–September 1889 follow-up](compatibility/chiefdoms_followup_2026_11_14.md)
finds Dinuzulu alive in exile and diagnoses the obsolete flag blocking claimant
selection. It adds successor returns without repeat rewards, explicit agitator
careers, Natal AI weights, a whole-day review countdown and stronger uSuthu
opposition to Chiefly Council. The earlier disappearance observation and
reported 81% discrepancy remain unproven causes; no character is recreated or
save rewritten. The 100% endpoint remains unchanged.
15 November: DP approved [full political backing and capped target pressure](zulu_chiefdoms_prominence_design_2026_11_15.md).
Source now applies 0.1 percentage point per royal prominence advantage, bounded
at ±30 points. Dynamic AI requires ≥20% Natal Zulu radicals for claimant return,
and that unrest plus the current claimant actually returned/present for refugee
offloading. Strict Historical retains its three-year delay. Source checks and
remaining engine gates are in the [implementation report](compatibility/chiefdoms_prominence_2026_11_15.md).

## Thirteen Chiefdoms refinement — 10 November 2026

`ZUL-CHIEFS-20261110`: **source implemented; DP engine acceptance pending**.
The [current record](zulu_thirteen_chiefs_implementation_2026_11_10.md) separates
partition from Prerogative, adds the one ten-year review/event-restoration model,
scoped competing-uprising restriction, payer-G bribery and persistent shared house
views. [Every runtime row remains pending](zulu_thirteen_chiefs_runtime_matrix_2026_11_10.md).
The native-war alternative is explicitly test-only until exclusion of all foreign
regular participants is demonstrated. No broader IR or country-profile rollout is
included; prior closed playtests do not certify the new path.

## Status

This register tracks **open work only**: the 1.15 follow-ups and selected extensions, the five machine-readable deferred gates and the separate content item below, the remaining FA-round items, the OB1 follow-up findings, playtest follow-ups, and content-design decisions awaiting DP. The 1.15.0 core rebase is closed; the 1.15.1 hotfix awaits DP runtime acceptance; accepted core tickets and other closed audit items live in [audit_issues_completed.md](audit_issues_completed.md).

The [2026-10-13 checkpoint review](compatibility/checkpoint_review_2026_10_13.md) records four unit-test failures, one error, and five historical skips, plus compatibility drift against the installed 1.14.5 game. The 0.20.2 rebase resolves those baseline/bookkeeping issues; rebase results and explicitly conditional historical checks are recorded in the [1.14.5 rebase report](compatibility/1_14_5_rebase.md). That validation recorded 15 PASS, two WARN and zero failed gates. The [17 October spawn audit](compatibility/boer_spawn_setup_2026_10_17.md) recorded one unrelated unit-test failure, also reported by the localisation gate: the existing `.050` Pretorius spelling correction differed from its reviewed-text baseline. That historical review mismatch is resolved by the 7 November approval below.

Static success is not runtime certification. Core acceptance does not certify every engine-only case in the [1.15 runtime matrix](compatibility/1_15_0_runtime_matrix.md); unrun and unitemised checks remain recorded for release verification. Earlier runtime matrices remain historical evidence.

DP's [1870 follow-up](compatibility/1_15_0_playtest_1870_2026_11_07.md) records
observational passes for the resumed campaign's crash, journal/war, once-only
and map/resource checklist, with no SB errors seen. The subsequent fresh-start
smoke test also passes; Bolivia's HQ warning coincides with complete Chilean
occupation of its coast, with native port routes preserved. Two SB encoding
warnings received BOM-only corrections. These observations do not claim
individual coverage of every stress case; unattributed diagnostics are not
established SB regression failures.

**Core rebase closed by DP, 7 November 2026.** DP approved the
[localisation review packet](compatibility/1_15_0_localisation_gate_review_2026_11_07.md):
three baseline entries were reconciled and one stale queue row removed, with no
prose or marker changes. The full validator reports **15 PASS, two WARN, zero
FAIL**. See the [closure record](compatibility/1_15_0_closure_2026_11_07.md).
Deferred release gates, targeted engine coverage and diagnostic follow-ups below
remain separate; no release, commit or version bump is included.

## Victoria 3 1.15 — remaining verification and secondary extensions

**Core implementation accepted and closed by DP, 7 November 2026.** See the [closure record](compatibility/1_15_0_closure_2026_11_07.md); the six native once-only migrations are included in the accepted port. The rows below retain separate verification, diagnostic and extension work.
The [extension priority discussion](compatibility/1_15_0_extension_priorities_2026_11_07.md)
records DP's selection of the Zulu court/institutions glossary pilot first.
The four-term pilot is now implemented; the remaining sequence and later designs are provisional;
the agreed later destinations remain unchanged.
The [D1–D8 register](compatibility/1_15_0_modding_digest_review_2026_11_05.md#decisions-to-settle-when-building-the-plan)
records authority and status; the [design](compatibility/1_15_0_rebase_design_2026_11_05.md)
holds evidence and boundaries. `EXT115` is the first extension tranche after
the core rebase. Deferred tickets select timing and investigation scope, not
unreviewed mechanics or immediate implementation.

| ID | Status / timing | Work and acceptance boundary |
| --- | --- | --- |
| `PLAY115-01` | Source correction applied; engine replay pending | Native `paralegal_discrimination.1` calls country-only AI predicates from state scope. The exact-path event shadow adds only two owner wrappers; native byte parity and AI-path regressions pass. Restart and replay before the event's once-only state has been consumed. See the [six-month investigation](compatibility/1_15_0_first_six_months_2026_11_05.md#paralegal-discrimination-ai-scope). |
| `PLAY115-02` | HQ warning investigated; runtime cause open | Riograndense naval HQ 634 logs no port travel position between the May and June saves; country 296 is eliminated on 10 May and its HQ is absent by June. Relevant port/history/spline/graph sources match Vanilla. Wartime control or HQ retirement is a hypothesis; retain an immediate replay save if the warning recurs with a controlled port. No speculative map change. See the [HQ evidence and limits](compatibility/1_15_0_first_six_months_2026_11_05.md#riograndense-naval-hq). |
| `CRASH115-03` | DP observed pass (resumed); original cause unresolved | The 14:01 crash after an observer toggle fails in the native investment-pool modifier-name tooltip, separate from law/JE creation. No direct SB/CMF override or bad BST investment-pool source was found. Preserve the April–August 1855 saves; distinguish ordinary hover from both observer transitions and existing-save state. No speculative gameplay/UI patch. See [evidence and focused replay](compatibility/1_15_0_observer_crash_2026_11_07.md). |
| `PLAY115-07` | No established SB attribution; separate diagnostic follow-up | DP confirms a resumed campaign, reports chat checks 3–6 as fine and saw no SB-related log errors. The January 1875 intake retains treaty, character-root AI and naval diagnostics, with no established SB cause. Preserve them for source/caller attribution rather than counting them as SB rebase failures. See [accepted observations and subsequent smoke pass](compatibility/1_15_0_playtest_1870_2026_11_07.md). |
| `RES115-01` | Deferred; resource audit after native-copper port | Revisit copper geology/extraction, technology/discovery timing, state allocation and economic balance; audit all lead proxies. Northern Cape's eight confirmed proxy lead levels were removed in phase one. Hereroland has a real lead rationale; Namaqualand's two lead levels remain an explicit uncertainty. Reconcile research and gameplay totals without duplicating native parent capacity. Keep the separate `RES-DISC-01` gold/oil semantics issue visible. |
| `CMF115-01` | Upstream debug-only defect; no live SB patch | CMF’s orphan `com_debug.2` example leads to an undefined combined timeout conclusion key in `com_international_situation.txt`. No SB caller exists; preserve the minimal patch and revisit only if that example becomes live. See the [bounded CMF JE audit](compatibility/evidence/1_15_0_journal_implementation/cmf_source_audit.json). |
| `EXT115-02` | Four-term pilot implemented and statically verified; DP rendering/prose review and wider rollout pending | Amabutho, amaKhosi, uSuthu and Umkhosi now have native glossary definitions and one body-text link each, following the [brief](research/zulu_glossary_pilot_2026_11_07.md), [main review / Vanilla comparison](research/zulu_glossary_review_2026_11_07.md) and DP's implementation instruction. See the [implementation and verification record](compatibility/1_15_0_zulu_glossary_pilot_2026_11_07.md). Preserve existing labels and review markers; generic uSuthu/“Great Chiefs” naming questions remain separate. Select later historical scopes through the [scope-owner workflow](compatibility/1_15_0_rebase_design_2026_11_05.md#glossary-workflow). |
| `EXT115-03` | Deferred; priority JE extension | Evaluate JE scaling modifiers against manual modifier maintenance. Preserve numerical effects, scope, stacking and cleanup; no automatic performance claim. |
| `EXT115-04` | Deferred; JE extension | Add useful JE map modes after selecting information/legend design. Verify foreign ownership, split states and actual rendering. |
| `EXT115-05` | Deferred; priority JE extension | Use scripted progress-bar conditions to explain real progress contributors. Verify arithmetic parity, conditional visibility and tooltips. |
| `EXT115-06` | Deferred; JE extension | Scripted button costs/icons/tags and selected uses such as proclaiming an heir. Displayed `cost` neither checks nor charges resources; automation is a separate behaviour decision. Verify availability, payment, repeated clicks and resulting state. |
| `EXT115-07` | Deferred investigation; JE extension | Objective-associated JEs: establish where previews help and whether an objective is appropriate. Association alone does not activate content. |
| `EXT115-08` | Deferred; secondary extension | Regnal numbers, especially ZUL. Reconcile historical numbering and existing naming/succession before adoption; verify repeated names and display. |
| `EXT115-09` | Deferred investigation; secondary extension | Hidden modifiers for AI-versus-AI historical/dynamic bookkeeping. Identify appropriate hidden effects without obscuring consequential player information. |
| `EXT115-10` | Deferred investigation; secondary extension | Regional exile pools, potentially for “ZUZ” as DP wrote. Confirm intended actor/tag before design; review access, return, country loss and character-role interactions. |
| `EXT115-11` | Deferred; JE extension grouping | SB currently uses native Historical Content, Global International Situations and Expeditions groups. Design useful SB thematic groups while preserving country/shared contexts, activation and participation; verify ordering, visibility and illustrations. See [1850 grouping note](compatibility/1_15_0_playtest_1850_2026_11_07.md#journal-groups--ext115-11). |
| `EXT115-12` | Deferred investigation; Prerogative JE extension | Review Russia's Emperor and Autocrat group, widgets and linked entries for lessons applicable to SB's court design. This records an example to investigate, not adoption of its mechanics. See [reference and scope](compatibility/1_15_0_playtest_1850_2026_11_07.md#russia--prerogative-extension--ext115-12). |
| `CHAR115-01` | Deferred; Characters, Companies, IDEOLOGY rework | Dynamic institution names and character-role backgrounds. Tentatively `v0.23.*`; follow the thematic patch if its version changes. This does not defer schema fixes required for 1.15 compatibility. |
| `RC115-01` | Deferred; `v1.0.0.rc` | Weighted music if suitable Creative Commons material is found. Record exact licences/attribution and mod redistribution rights, then verify weights and playback. |
| `RC115-02` | Deferred; `v1.0.0.rc` | Weighted loading screens after SB artwork exists; verify selection and presentation. |

Power bloc effects and the strait grievance multiplier are explicitly skipped /
N/A in the design inventory; they are not open work tickets. None of these
entries closes the existing performance, map/spline or historical content gates.

## Major content refactor TODO — unified South African Republic (ZAR)

**`ARCH-20261030-01` — Major refactor; open; requested by DP on 30 October 2026.** A player unifying the Transvaal as LYD or ZPB can remain excluded from content written exclusively for TRN. Design a common **ZAR** successor tag and audit the affected content rather than adding the name to isolated event gates. ZAR is not currently defined; this entry implements no new country or migration.

Scope: formation and player continuity from TRN/LYD/ZPB; historical setup versus ongoing regional eligibility; events, journal entries, decisions, Boer compacts, diplomatic AI, border settlements, government/character setup, names/localisation, and territorial rewards. Preserve the actual country identities held by pending plays, succession wars, contracts and event callbacks. A qualifying retag/unification must retain its own undertakings; an unrelated conqueror must not inherit them merely by using a similar name. Do not mechanically replace every `c:TRN` reference: origin-country setup and an active sponsor/beneficiary have different meanings.

The immediate design dependency is [Hamu's Boer bargain](zulu_later_court_story_design_2026_10_30.md#2-hamu-the-zulu-kingdom): TRN or future ZAR owns part of East Transvaal after the Boer–Swazi border settlement, pays 1G for a lasting promise, optionally funds Hamu further, and can receive **Greater NRP as a subject** if he accedes. Reserve the actual sponsor/overlord identity and share the once-only NRP entitlement with the later Thirteen Chiefs route. The broader refactor must audit the existing NRP formation, boundary and union paths, which contain TRN/NAL-specific assumptions. This Hamu route excludes automatic annexation; a British ultimatum becomes eligible only under actual British control of residual ZUL, including later, and must involve the actual NRP overlord.

**Completion:** agree formation/retag rules and enumerate affected authored routes; test equivalent access for TRN, LYD and ZPB unifiers, player continuity, pending-contract retention and unrelated-country negative controls. Preserve country-specific historical entry content where appropriate. This is future architecture work, separate from the current design-only Hamu exploration; no save migration or blanket eligibility expansion is authorised by this note.

## Major pre-release performance TODO — simulation tick times

**`PERF-20261028-01` — Major priority; open; reported by DP on 28 October 2026.** Tick times have become markedly slower during the Zulu court/civil-war testing. Measure the regression before selecting a fix; neither the court nor the latest force changes are yet established as its cause.

DP should collect comparable timings/profiler output at a fixed game speed and machine/settings: fresh campaign, developed peaceful court, claimant preparations, active civil war, and post-war reunification. Compare retained source checkpoints using compatible disposable campaigns. Inspect weekly polling/event queues, monthly/annual court and roster work, movement/IG recalculation, modifier churn and split/reunion work; distinguish a one-off transition stall from sustained daily slowdown. Keep game version, CMF, DLC/load order, date and population/army size in the evidence. Codex can analyse saved logs/source; DP launches and profiles.

**29 October follow-up:** DP supplied three-month 1843 timings for movement/IG calculations and the monthly router. A [small performance pass](performance_pass_2026_10_29.md) now reduces repeated predicate work and adds equivalent handler guards. Calculations and cadence are preserved; the largest inherited neighbour scans remain. DP then confirmed noticeably faster ticks and waived further first-pass measurement. A [deeper pass](performance_deeper_pass_2026_10_29.md) reduces repeated house ranking and global country scans without changing cadence or outcomes. Numerical before/after engine timings and child-handler profiling remain pending for the broader pre-release audit.

**Completion:** a reproducible baseline, identified hot path(s), measured before/after tick costs and regression checks showing political/war behaviour is preserved. Do not optimise by removing agreed mechanics or by speculative global cadence changes. The limited source pass does not close this audit.

## 30 October playtest follow-up — reform and Lesotho food balance

**Open investigation/design, not a new gameplay baseline.** [Targeted fixes and evidence](zulu_playtest_followup_2026_10_30.md) record Dunn's missing-window crash, two-state barracks restoration, Mbuyazi's event trait, loyal-claimant protection and JE presentation. Their DP rendering/engine checks remain pending.

**Succession follow-up:** the [August 1856 save investigation](compatibility/zulu_retirement_succession_2026_10_30.md) explains why Cetshwayo's displayed 31.04% did not meet the former all-court threshold. DP approved using 25% of succession-pledged Prominence instead. The threshold, retirement presentation and delayed first Dunn delivery are corrected in source; pre-retirement engine replay remains pending.

**`IR-20261030-01` — Deferred design TODO by DP on 30 October 2026: Institutional Reach expansion.** [Regional reform research](institutional_reach_regional_reform_research_2026_10_30.md) evaluates Swazi, Gaza and potentially Basotho, research penalties and the proposed IR100/technology arithmetic. Revisit the proposed IR-scaled Society/Production research penalties (up to −25%), technology contributions and country-specific reform objectives together. Exact values, technology-count convention, penalty stacking and regional rollout remain undecided; retain the current IR model for now and do not enable Zulu claimant helpers for other tags. The broader balance pass below remains open.

**`BST-20261030-01` — Deferred investigation TODO by DP on 30 October 2026: Lesotho starvation after the mountain retreat.** Retain a **pre-annexation** retreat/famine checkpoint. The latest five autosaves are already post-annexation. Inspect the 5,000-person single-Pop retreat transfer and conditional 14-level conscription assistance against remaining agricultural employment, subsistence capacity and food supply. Neither missing refugees nor insufficient base population is established by the retained saves. Diagnose the cause before choosing population, arable-land or military-support changes; no balance change is authorised by this entry.

**1 November follow-up — investigation reopened by DP; next trial selected, not implemented.** The [new five-save investigation](compatibility/bst_lesotho_famine_2026_11_01.md) covers July–November 1841 **before annexation**, with The Mountain Refuge active. Lesotho loses 874 people net; maize employment stays at 20. Native inspection confirms that Serfdom's 50% protected-subsistence-employment floor blocks recruitment from subsistence at only 10.85% staffing. Vacant arable capacity and existing farmer qualifications do not bypass that restriction. Conscription is inactive in these saves. The selected proposal is a BST-owned Drakensberg hiring exemption for the existing 60-month refuge period, plus a 24-month +0.50 Food Security bridge; retain the current population transfer for the first comparison. A 10–20% mixed-household transfer remains a separate option. Original saves/logs are archived under git-ignored `generated/diagnostics/bst_lesotho_famine_2026_11_01`; source hashes, extracted observations and native evidence are retained with the report. DP still needs a pre-retreat checkpoint and, after implementation, hiring/output, relief-expiry and ownership-loss tests. This does not reopen the deferred IR expansion or change the baseline population setup.

**1 November clarification — second proposal, superseded by DP's decision below:** DP highlighted that subsistence farms themselves supply grain. The [second proposal](compatibility/bst_lesotho_famine_2026_11_01.md#revised-first-trial--actual-food-production) replaced the proposed direct Food Security bridge with **+0.50 subsistence-farm throughput**, alongside the local −0.50 protected-employment offset, both for 60 months. At unchanged saved staffing, this increases subsistence grain from 1.17212 to about 1.66050. It would have kept the 5,000-person transfer unchanged and evaluated food supply, hiring and expiry before adding further relief. This package was not implemented; retain it as design history alongside the diagnostic evidence.

**1 November decision — implemented, engine replay pending:** DP rejected the extra hiring exemption and selected **only +50% subsistence-farm throughput for ten years**. The Mountain Refuge now has that sole effect; its former −15% goods-input and +10% in-kind subsistence bonuses are removed. The existing country-scope grant uses `years = 10`. No population, Serfdom, Food Security or Mountain King changes. This is the authoritative implementation choice; the earlier packages above are historical proposals. Verify actual grain output, starvation and expiry from before the retreat grant. See the [implemented decision](compatibility/bst_lesotho_famine_2026_11_01.md#implemented-decision--throughput-only-for-ten-years).

**1 November playtest follow-up — Shepstone-equivalent bonus implemented:** DP reports the throughput-only trial is insufficient and requests Shepstone's subsistence bonus. The Mountain Refuge now additionally has **+30% Subsistence Output**, exactly matching `amendment_sb_shepstone_system`, alongside +50% subsistence-farm throughput for the same ten years. This supersedes the earlier sole-effect restriction; the additive interpretation was stated before implementation. Shepstone's tax, employment-protection, arable-reservation and migration effects are not copied. Check in-kind income, food affordability and starvation in the next replay; recovery remains unverified. See the [current follow-up](compatibility/bst_lesotho_famine_2026_11_01.md#current-follow-up--match-shepstones-subsistence-bonus).

**1 November current trial — balanced refugee workforce implemented; DP replay pending:** DP subsequently disabled the throughput line and reports famine with only +30% in-kind Subsistence Output. After the [income replay](compatibility/bst_subsistence_income_replay_2026_11_01.md), DP approved making the existing 5,000-person refugee cohort **2,500 workers and 2,500 dependants**. The [replacement transfer](compatibility/bst_refuge_workforce_ratio_2026_11_01.md) conserves total people, retains religion, native destination-profession rules and selected-donor wealth/literacy, and prevents duplicate delivery. Native removal/creation still resets some Pop metadata; this is an explicit trial, not a migration clone. The +30% income bonus and ten-year duration remain, and the throughput line stays commented out. No extra hiring, law, military or food changes. Replay from before the retreat to verify the arrival increment and subsequent employment/starvation; this does not close the famine investigation.

**3 November DP replay — balanced-workforce trial accepted:** DP reports that the trial works. The immediate Lesotho famine blocker is resolved in the reported playtest; retain the 5,000-person 50:50 arrival cohort and current ten-year +30% Subsistence Output bonus. No further relief increase is requested. Detailed population accounting, metadata preservation and expiry checks were not individually reported; keep those under the broader pre-release balance verification, without treating them as new failures or requiring another immediate replay. See the [playtest follow-up](compatibility/bst_refuge_workforce_ratio_2026_11_01.md#playtest-follow-up--3-november-2026).

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

The direct checker must report zero drift against build `26591675`, branch `public`, core depot manifest `5537848810174326853`, and CMF `1.67.9` plus `sb-1.15.1-r2`. The suite must also verify the depot delta, structured spline merge, localisation review boundaries and queue, subject/war contracts, AI-incorporation overrides, naval-port connectivity, delayed-event lifecycle, changed-file BOM state, and absence of stale live-baseline labels.

Installed Tiger 1.19.0 lacks 1.15 JE outcomes and native once-only fields; it is not run as a target validator. See the [schema evidence](compatibility/evidence/1_15_0_implementation/tiger_schema.json). Repository semantic gates remain mandatory. A test that actually fails is a blocker; it cannot be relabelled `Engine pending`.

Release support becomes strict only after every runtime-matrix row is recorded with a fresh campaign on the target build, exact command/save/load order, UTC timestamp, and rotated-log hashes, and fresh logs contain no new SB-authored errors.

Current dependency: CMF `1.67.9` plus `sb-1.15.1-r2`. The patch manifest and expected installed-tree digest are pinned by the compatibility inventory. See the [dependency report](compatibility/cmf_1_67_9_update_2026_11_19.md) and the [game hotfix matrix](compatibility/1_15_1_runtime_matrix.md).


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
