# Current Known Issues

**Audit date:** 2026-08-06  
**Baseline:** `main` at `e5706779e0d9fed7f93d930301c5e8162ea09f05`, plus the ten then-uncommitted Bechuanaland files  
**Target:** Victoria 3 `1.13.9`; Community Mod Framework `1.58.2`

This is a fresh, repository-wide static audit with additional scrutiny on the Bechuanaland Corridor/Crisis rewrite. It is a best-effort issue inventory, not a guarantee that every runtime defect has been found. The audit was read-only; this document is the only file created by it.

## Labels

- **Confirmed**: directly demonstrated by control flow, data comparison, validator output, or current 1.13.9 logs.
- **Runtime check**: static evidence is strong, but the exact engine response still needs an isolated playtest.
- **Design/UX**: script behavior and player-facing text or apparent intent disagree; the engine may still execute the script as written.
- **Tooling/noise**: affects validation or maintenance rather than live gameplay.

## Highest-priority items

1. Bechuanaland escalation event windows can overwrite one another or launch a war after the situation has resolved (`BC-01`).
2. The Zoutpansberg crackdown JE auto-activates before the event that is meant to choose it (`GP-01`).
3. Bechuanaland white peace and mixed treaties are converted into arbitrary full settlements (`BC-03`).
4. Legacy Bechuanaland war routes can permanently lock the JE (`BC-05`).
5. Several other JEs auto-activate before their intended introductory choice/events (`GP-02`, `GP-03`).
6. Responsible-government requests use the requesting subject where the overlord is required (`GP-06`).
7. Xhosa frontier pressure and Namibia punishment effects are applied with incorrect country/owner scoping (`GP-04`, `GP-05`).
8. Several hard global overrides have drifted from Vanilla 1.13.9 outside Southern Africa (`CP-01` through `CP-06`).
9. STA has no defined CoA, one reachable event description is missing, and the requester-side responsible-government lens icon is absent (`SUP-01`, `SUP-02`, `SUP-04`).
10. The current map/spline package produces adjacency and route-strip errors on an otherwise isolated 1.13.9 load (`SUP-05`).

---

## A. Bechuanaland Corridor/Crisis

### BC-01 — Critical — stale escalation windows can overwrite or revive a resolved crisis

**Confirmed.** The escalation lock in `common/scripted_triggers/sb_bechuanaland_corridor_triggers.txt:101-108` is set only after an event option queues a route. Warren and Caprivi events are three-day popups, and their triggers/options do not recheck that the corridor is open, unresolved, and escalation-free (`events/sb_bechuanaland_corridor_events.txt:31-335`).

Consequences:

- Warren and Caprivi chains can be open together.
- A later choice starts by clearing and replacing the earlier pending route (`common/scripted_effects/sb_bechuanaland_corridor_effects.txt:938-982`).
- A popup left open until after natural settlement can queue a new crisis; neither queue/core validation requires the corridor to remain open and unresolved (`effects:938-982,1165-1214`; `triggers:110-136`).

### BC-02 — High — Boer choice event can be dispatched repeatedly

**Confirmed.** The `.032` dispatch flag lasts 15 days (`effects:1180-1187`), but `.032` is a duration-three event (`events:337-377`) and the monthly retry calls the launch effect again. An unanswered player popup can therefore be redispatched, leaving competing support/neutrality choices.

### BC-03 — High — white peace and mixed treaty outcomes become arbitrary full settlements

**Confirmed.** Both new diplomatic plays allow negotiated peace (`common/diplomatic_plays/sb_diplomatic_plays.txt:351-406`). Enforcement records only whether any holder on either marked side enforced any goal (`effects:1263-1282`). At war end, neither side flagged or both sides flagged falls through by route: direct becomes a British victory and proxy becomes a Boer/SWA victory (`effects:1285-1317`). The chosen full subject/claim settlement then runs even if no relevant goal, or mutually contradictory goals, were enforced. Comparable Vanilla locked packages disable negotiated peace.

### BC-04 — High — international-JE AI weights run in `none` scope

**Confirmed by current logs.** The JE is global/international (`common/journal_entries/1-11_sb_bechuanaland_corridor.txt:3-4,26-30`), but button AI weights call country triggers without an explicit country scope (`common/scripted_buttons/sb_bechuanaland_corridor_buttons.txt:64-66,117-119`). Current `error.1.log` reports `has_strategy`, `gold_reserves`, and `net_fixed_income` in `none` scope. The intended subsidy/trade-mission AI weighting is not functioning.

### BC-05 — High — legacy no-intervention war routes can permanently freeze the JE

**Confirmed control-flow defect; one launch subcase needs runtime confirmation.** `.020.c` starts CAP-versus-SGO annexation and `.021.c` starts the CAP dual-return route (`events:149-166,220-234`). Their helpers can set the global active flag before or without verifying that a play was created (`effects:819-827,1320-1329,1383-1428`).

- Failed play creation leaves the active flag indefinitely.
- White peace also leaves it indefinitely because the new war-end resolver handles only direct/proxy routes, while the legacy hooks handle only backdown or enforced goals.
- The JE now blocks both territorial resolutions while that flag exists (`journal:55-65,85-94`).
- CAP begins as a colony whose subject type normally cannot start its own play, so `.020.c` is a required playtest case.

### BC-06 — High — generic legacy hooks can resolve the corridor from an unrelated war

**Confirmed.** The legacy hooks test only that the route is not direct/proxy and that countries have opposing marker variables; they do not identify the CAP-SGO annex or dual-return play (`common/on_actions/sb_on_actions.txt:2518-2546,2963-2991`). Dual return marks GBR and every living ORA/TRN/WBL/SGO, including nonparticipants (`effects:1420-1426`). If markers survive a failed or white-peace route, another war between a marked pair can select a corridor winner.

### BC-07 — High — pending cancellation is lossy, silent, and usually non-retryable

**Confirmed.** Queueing immediately changes influence, then can wait indefinitely for all core participants—and on the direct route every marked regional British subject—to be free of wars/plays (`effects:938-981`; `triggers:138-179`). If the core becomes invalid, the route cancels silently without restoring influence (`effects:1171-1175`). One-shot Warren/Caprivi country flags are not comprehensively cleared (`effects:686-815,1687-1752`), preventing retry. Warren also unconditionally requires Boer support even though its button does not require a currently valid Boer actor; this cancels instead of using Caprivi's neutrality fallback.

### BC-08 — High — SWA-overlord scopes become stale or refusal becomes a no-op

**Confirmed.** Refresh removes the stored sponsor only if the old country dies, not if it loses SWA, GP rank, or becomes aligned with Britain (`effects:44-61`). Warren refusal dispatch loops only current candidates and has no fallback (`effects:803-817`). Once queued, core validation checks life/direct subjecthood but not the original GP and British-security restrictions (`triggers:110-136`).

### BC-09 — High — no post-opening invalidation for lost prerequisites

**Confirmed.** SAF formation and CAP leaving British subjecthood skip only before `corridor_open` (`common/on_actions/sb_mineral_discoveries_on_actions.txt:181-196`). The JE invalid block checks only open/resolved state (`journal:105-110`). After opening, SAF formation, CAP death/independence, or sponsor loss can make every crisis core invalid without closing the international situation.

### BC-10 — High / runtime check — each JE copy may queue a British settlement popup

Opening gives a separate contextless JE to every involved country (`effects:220-226`). Every copy's `on_complete` asks GBR to fire `.040`, with no British-pending guard (`journal:70-76`), although the failure route has such a guard (`effects:1491-1526`). If completion callbacks remain per-country, multiple `.040` popups will be created; later copies can rerun unguarded subject/claim/technology effects. Verify whether the engine coalesces international-JE completion callbacks.

### BC-11 — High — required return goals are not all primary demands

**Confirmed.** The dual-return package makes Griqualand West primary but not the added Bechuanaland goal (`effects:1413-1418`). Reciprocal CAP/SGO return goals in the direct/proxy packages also omit `primary_demand` (`effects:1024-1035`). Backdown therefore need not impose the whole package, while generic code still awards a full corridor victory. The play definition and localization promise both states.

### BC-12 — High — Britain's Caprivi concession can seize third-party land

**Confirmed.** Availability checks only that SWA does not own all five provinces (`buttons:213-216`). The concession unconditionally changes those provinces to SWA (`events:260-270`; `effects:574-581`) without checking current owner or control. They begin under decentralized LZO and can later belong to any country.

### BC-13 — High/medium — SGO alignment is ignored

**Confirmed.** Natural failure treats any living SGO owning all Bechuanaland as Boer/SWA success, including a British/Cape subject SGO (`triggers:212-217,234-237`). Crisis network marking adds every living SGO and tries to put it on the SWA side (`effects:898-903,1084-1117,1150-1160`), while the British package excludes it. A later British- or third-party-aligned SGO can therefore be treated as an enemy, or fail to join while settlement logic assumes it did.

### BC-14 — Medium/high — Sponsor Settlers can be enabled but do nothing

**Confirmed for non-hard-coded fragments.** The button accepts any TSW-owned Bechuanaland fragment (`triggers:189-200,365-370`), but country creation supports only four hard-coded provinces (`effects:503-563`). If TSW retains another corridor province, the button and its AI weight remain active but create no SGO and give no influence. Also test whether `exists = c:SGO` is true for a dead static tag while dispatch requires `is_country_alive`.

### BC-15 — Medium/high — subject settlement does not reliably establish the intended direct overlord

**Runtime check.** The TSW helpers use transitive `is_subject_of` and then unqualified `change_subject_type` (`effects:634-684`). For example, an indirect British subject under CAP can enter the GBR branch but merely have its direct CAP pact changed; a subject in another hierarchy can reach `create_diplomatic_pact` without an explicit transfer/break. Directness should be tested against the intended GBR/CAP outcome.

### BC-16 — Medium/high — scripted transfer goals include non-transferable subject types

**Runtime check.** Direct crisis construction adds `transfer_subject` for every marked subject without checking `can_target_with_transfer_wargoal` (`effects:906-927,1070-1114`). ORA can normally be TRN's presidential-union/confederal subject, both explicitly non-transferable (`common/subject_types/sb_subject_types.txt:182-201,248-261`). The goal may be rejected while the country remains marked/joined and localization still claims it is at stake.

### BC-17 — Medium — new pacing bypasses the influence game

**Design/UX.** The current diff removes the 12-month Caprivi AI delay and Namaqualand/Namibian-core gate. SWA AI can demand immediately on opening with weight 1000; CAP/GBR Warren buttons are likewise weight 1000 and do not consult the frontier-AI rule (`buttons:135-239`). This can preempt the 12/24-month subsidy and influence loop.

### BC-18 — Medium — incomplete cleanup and contradictory claims

**Confirmed.** Six demand/refusal/concession country flags survive final cleanup (`effects:686-815,1687-1752`). Direct Warren adds CAP claims on Griqualand West and Bechuanaland (`effects:737-739`), but Boer/SWA interior settlement removes only CAP's Bechuanaland and GBR's Botswana claim (`effects:1621-1622`), leaving a Cape Griqualand claim after the proclaimed final settlement.

### BC-19 — Medium — “remaining Tswana-held land” transfers only the initial 20 provinces

**Confirmed.** `sb_bechuanaland_transfer_tsw_corridor_to_root` hard-codes 20 provinces (`effects:599-623`), while STATE_BECHUANALAND contains 30 (`map_data/state_regions/04_subsaharan_africa.txt:1340-1355`). Any additional corridor province later acquired by TSW stays behind despite the settlement text.

### BC-20 — Medium — the SGO British-restraint fix is permanent rather than crisis-scoped

**Fixed behavior awaiting design/playtest decision.** The new exception in `common/scripted_triggers/sb_british_boer_restraint_triggers.txt:14-32` has no open/unresolved condition. Monthly refresh continues GBR's befriend strategy and `-500` conquest offset after final settlement, although its comment describes preventing pre-emption of the crisis. The original subject-transfer hole is fixed, but duration is broader than the stated purpose.

### BC-21 — Medium/high — delayed `.010` can award victory after CAP disappears

**Confirmed.** `.010` rechecks only the demand variable (`events:49-54`). If CAP dies during the delay, its annex/transfer effects safely no-op, but `.010.a` still sets British victory (`events:76`).

### BC-22 — Medium — result and tooltip text often describes a different system

**Confirmed UX drift.** Notable examples:

- Proxy play says “humiliation-only” although reciprocal Return State goals can be added.
- `.032` uses implementation jargon and one tooltip for direct and proxy paths although British subject goals exist only on direct.
- `.040` implies a London-versus-Cape choice, but has one option and silently selects the outcome from Cape laws/government while also normalizing subjects and adding British claims.
- Victory prose can be false after arbitrary draw fallback because settlement does not universally transfer corridor land.
- “Will begin” ignores indefinite pending and silent cancellation.
- Fixed influence numbers ignore score clamping.
- `.041` can dereference missing claimant scopes if countries die between save and display.

Evidence: `localization/english/sb_bechuanaland_corridor_l_english.yml:45-48,67-90,114-118,137-166`; `events:379-451`; `effects:1003-1037,1149-1160,1285-1317,1465-1658`.

### BC-23 — Low/medium — crisis support is asymmetric and disconnected from `.032`

**Design/UX.** Support is free and grants +5% offense/defense. Britain buffs CAP only; the SWA sponsor buffs SWA and SGO even when `.032` chose neutrality (`buttons:242-279`; `effects:1660-1685`; `common/static_modifiers/sb_bechuanaland_corridor_modifiers.txt:3-6`). Localization describes one aligned government rather than this behavior.

---

## B. Other gameplay systems

### GP-01 — Critical — Zoutpansberg crackdown JE preempts its own choice event

**Confirmed.** `je_sb_zpb_crackdown` becomes possible from independent TRN plus living ZPB without requiring `sb_zpb_crackdown_active_var` (`common/journal_entries/1-05_sb_transvaal_unity.txt:203-209`). The event is supposed to set that flag and add the JE (`events/sb_boer_conventions_events.txt:604-617`), while its scheduler explicitly requires that the JE not already exist (`common/on_actions/sb_on_actions.txt:2084-2104`). Automatic activation therefore blocks the lawlessness choice and can later time out without its branch setup.

### GP-02 — High — East Transvaal pacification JE preempts the frontier-republic choice

**Confirmed.** Its `possible` block omits `has_modifier = sb_trek_frontier_republic` (`1-05_sb_transvaal_unity.txt:438-444`). Event `.130.b` is meant to grant that modifier, claim the state, and add the JE (`events/sb_boer_republics_events.txt:278-302`). Because the JE can already exist, that guarded setup is skipped; the catch-up path correctly requires the modifier (`on_actions:1782-1792`).

### GP-03 — High — Gaza consolidation JE preempts its introduction and grace period

**Confirmed.** The JE can activate directly and seed itself (`common/journal_entries/1-09_sb_eastern_sphere.txt:19-54`). Both the intro scheduler and event require no existing JE; the event is meant to set `sb_gaza_consolidation_grace_var` and add it (`common/scripted_effects/sb_eastern_sphere_effects.txt:1260-1277`; `events/sb_gaza_events.txt:16-38`). The complete check depends on that missing grace. An early save already shows the JE active on 1836-01-02 without the intro-scheduled marker.

### GP-04 — High — Xhosa frontier pressure is removed by almost every country pulse

**Confirmed.** Country monthly pulse adds the modifier when current ROOT owns the qualifying Eastern Cape state, but its paired `else` removes it from XHO (`common/on_actions/sb_on_actions.txt:803-848`). Since ROOT is each country in turn, nearly every country removes it; final state is iteration-order dependent.

### GP-05 — High — Namibia punishment applies one country's atrocities to every owner's partition

**Confirmed.** Events `.200` and `.201` are triggered by ROOT-specific law/movement conditions, then loop every state in Namaqualand/Hereroland without `owner = ROOT` (`events/sb_namibia_events.txt:1442-1481,1529-1570`). Rival colonial partitions and independent Nama/Herero land receive ROOT's forced-camp/extermination effects. The monthly caller does not require full-region ownership.

### GP-06 — High — subject-requested responsible government uses the wrong country scope

**Confirmed by control flow and runtime log.** In `sb_ask_responsible_government`, ROOT/actor is the requesting subject. The accept effect changes relations with `scope:actor` (self) and calls helpers that inspect `scope:actor` as though it were the overlord (`common/diplomatic_actions/sb_subject_autonomy_actions.txt:157-166`; `common/scripted_effects/sb_subject_autonomy_effects.txt:13-20,38-85`). Non-British government/subject type can be selected from the subject's laws; the relation change is a self-target/no-op. Vanilla's analogous requester action enters the target/overlord scope.

### GP-07 — Medium — Albany frontier wars check the wrong truces and still consume progression

**Confirmed.** The scheduler includes ABY but checks XHO truces only with CAP/GBR for wars 7-9 (`on_actions:871-886,915-918,965-968,1015-1018`). Events target ABY and immediately mark the step resolved after `create_diplomatic_play` (`events/sb_frontier_ai_wars_events.txt:535-565,621-635,707-737`). An ABY-XHO truce can reject play creation while permanently consuming the step.

### GP-08 — Medium — Gaza Portuguese raid damages the wrong land

**Confirmed.** The gate accepts Portuguese ownership in either Lourenço Marques or Zambezia (`effects/sb_eastern_sphere_effects.txt:163-170`), but event `.040` devastates every Lourenço Marques partition with no owner filter (`events/sb_gaza_events.txt:188-211`). If Portugal owns only Zambezia, Portuguese land is untouched and third-party/Gaza land can be damaged.

### GP-09 — Medium — BST retreat selects two independent frontier actors

**Confirmed.** `.020` moves a Sotho pop from one random qualifying country, then independently chooses another random country for the claim/relations result (`events/sb_bst_frontier_events.txt:126-168`). Split Vrystaat ownership can evacuate one actor's population while rewarding or penalizing another.

### GP-10 — Medium — Martinus delayed coercion can strand its active flag

**Confirmed.** `.010` sets `sb_martinus_coercive_chain_active_var`, while delayed child events require ORA still be an independent candidate (`events/sb_martinus_confederation_events.txt:157-164,785-1122`). If ORA is annexed or subjected before delivery, the event cancels and no failure path clears the flag. Cleanup exists only on successful resolution (`common/scripted_effects/sb_martinus_confederation_effects.txt:36-46,224-229,281-286`).

### GP-11 — Medium — Cape CQF delayed event can leave a permanent pending lock

**Confirmed.** Enactment start sets an untimed pending variable and schedules `.130` for 21 days (`common/on_actions/sb_cape_law_on_actions.txt:13-24`). `.130` requires Cultural Exclusion still being enacted and removes the variable only after its trigger succeeds (`events/sb_cape_events.txt:304-323`). Cancellation/change during the delay blocks all later checkpoints.

### GP-12 — Medium — Cape responsible-government petition button is orphaned

**Confirmed.** The player-facing button exists at `common/scripted_buttons/sb_cape_buttons.txt:39-76`, but `je_sb_cape_politics` attaches only the two favour buttons (`common/journal_entries/1-01_sb_cape_politics.txt:69-71`). Nothing attaches the petition button.

### GP-13 — Medium — BST frontier completion and invalidation can both be true

**Confirmed.** Completion is a qualifying Oranjeland actor owning all Vrystaat and Drakensberg; invalidation is also true when surviving BST owns none of either region (`common/journal_entries/1-07_sb_bst_frontier.txt:56-95,151-160`; `common/scripted_triggers/sb_bst_triggers.txt:15-20`). The reward is conditioned on BST being dead, so displaced-but-living BST yields invalidation or a rewardless completion depending evaluation order.

### GP-14 — Medium — Imperial Confederation has no terminal cleanup

**Confirmed.** The JE has failure cleanup only (`1-09_sb_eastern_sphere.txt:292-297`); SAF formation clears none of its globals/flags (`effects:819-865`). GBR's monthly housekeeping continues full validation/count/progress/sea-access scans and permanent subject marking after SAF formation or failure (`effects:1139-1166,1249-1259`).

### GP-15 — Medium — Natalia appeal can be resolved while the player popup remains open

**Confirmed timing mismatch.** The player appeal arrives day 8, Britain resolves day 9, and the appeal lasts three days (`events/sb_natal_crisis_events.txt:1003-1012,1713-1727`; `common/script_values/sb_event_travel_values.txt:105-116`). Britain's resolution respects only an already-recorded pledge, so a response after the first open day can be preempted.

### GP-16 — Medium — Delagoa acceptance/rejection fans out beyond the actor that qualified

**Confirmed.** Event `.010` needs only one ready AI actor, but acceptance creates treaties and sends completion events to every route actor with the JE; rejection flags every such actor (`events/sb_delagoa_events.txt:16-70`; `common/scripted_effects/sb_eastern_sphere_effects.txt:548-580`). Actors without completed railways, actors that already refused, or otherwise unready actors are swept into the result.

### GP-17 — Medium — Delagoa gateway logic admits British-network and self-treaty cases

**Confirmed control-flow risk.** `sb_delagoa_has_valid_gateway` excludes only a market leader whose country definition is GBR, rather than the broader British network (`common/scripted_triggers/sb_eastern_sphere_triggers.txt:474-492`). If the route actor is itself the market leader, `actor_has_trade_through` still requires a transit treaty and the accept effect can attempt a treaty from the actor to itself (`triggers:524-545`; `effects:548-580`).

### GP-18 — Medium — Mozambique Company creation omits Vanilla charter setup

**Confirmed parity gap / design decision needed.** The custom effect activates the base charter laws but omits the racialized subjecthood amendment and `resource_extraction_charter_modifier` applied by Vanilla colonial-administration chartering (`common/scripted_effects/sb_eastern_sphere_effects.txt:382-418`; Vanilla `events/colonial_administration_events.txt:47-92`). This makes MZQ mechanically weaker/different from the charter path it mirrors.

### GP-19 — Medium — GUI overrides do not register after required CMF

**Confirmed current diagnostic; impact partly mitigated.** Spes defines `journal_panel`, `journal_entry`, and `journal_entry_panel`, but CMF has already registered them. Current `gui.log` reports all three as already registered, so the Spes copies are ineffective. CMF provides its own dynamic double-sided bar, but Spes-specific GUI changes cannot be assumed live (`gui/journal.gui:18,342`; `gui/journal_entry.gui:19`).

### GP-20 — Low — stake-colonial-claim action can expose an empty picker

**Confirmed UX regression.** The override removes Vanilla's top-level “any target state has sufficient interest tier” availability gate (`common/diplomatic_actions/zz_sb_stake_colonial_claim_override.txt:29-79`). Per-state checks remain, so the action can appear available with no selectable state.

### GP-21 — Low — unreachable histories and duplicate John Philip

**Confirmed data drift.** XHG/XHR/XHT country and character histories describe live splits, but all Xhosa land starts under XHO and no creation/ownership path for those tags was found. CAP and PHL histories also create matching John Philip templates, producing duplicate contemporary characters (`common/history/countries/{xhg,xhr,xht}*`; `common/history/characters/{xhg,xhr,xht,cap,phl}*`; `common/history/states/00_states.txt:3503-3512`).

---

## C. Vanilla and third-party compatibility

### CP-01 — High — political-movement replacements are stale global copies

**Confirmed against Vanilla 1.13.9.** Headers describe Cape-only coordination, but the full replacements omit newer global mechanics: post-defeat suppression on six movements, Japan/Meiji creation/disband checks, cultural-majority unowned-homeland radicalism, and a utilitarian active-law multiplier. Evidence is in `common/political_movements/zzz_sb_cape_political_movement_overrides.txt` and the three `zz_sb_*majority*_override.txt` files versus Vanilla `common/political_movements/{00_ideological_movements,02_cultural_movement,04_country_specific_ideological_movements}.txt`. These changes affect Japan and unrelated countries contrary to the compatibility documentation.

### CP-02 — High when co-loaded after reference mods — treaty `replace_path` removes their files

**Confirmed VFS behavior.** `descriptor.mod` replaces the whole `common/history/treaties` directory even though the exact-path Vanilla file is already shadowed. With SB at higher priority, this drops Hail Columbia's `usfp_starting_treaties.txt` and Gates of the Bosphorus's `gbbf_treaties_history.txt`. The load-order constraint is undocumented.

### CP-03 — Medium — frontier-colonization law override omits unrelated 1.13.9 behavior

**Confirmed.** The comment says the change only adds trekker eligibility, but the full replacement omits Vanilla's `disallowing_laws = { law_sakoku }` and replaces JE AI bonuses for `ai_has_enact_weight_modifier_journal_entries`/`je_taming_the_north` with zero (`common/laws/00_sb_governance_principles.txt:27-100`; Vanilla `common/laws/00_colonial_affairs.txt:89-136`).

### CP-04 — Medium — ideology replacements contain out-of-scope drift

**Confirmed.** `REPLACE:ideology_reformer` omits Vanilla's Edo social-system stance, and the Junker-colonialism replacement omits Vanilla `law_social_monarchy = approve` (`common/ideologies/zz_sb_reformer_ideology_override.txt`; `zz_sb_junker_colonialism.txt`; corresponding Vanilla ideology files).

### CP-05 — Medium — Highveld exact-path override removed selector safeguards

**Confirmed.** Fallback `ordered_scope_character` selectors for Piet Retief and Mpande omit `character_is_valid_for_events = yes` and `position = 0`, changing a highest-clout single selection into iteration/last-save behavior and admitting invalid characters (`events/iberia_events/struggle_for_the_highveld_events.txt:374-380,593-599`). Two optional `interest_group ?=` dereferences were also hardened to `=`, increasing missing-scope risk. These differences are unrelated to the map-province edits that justify the override.

### CP-06 — Medium — commander-retirement override changes the entire world

**Confirmed.** All AI commanders receive +50 retirement chance at age 60 (`common/character_interactions/zz_sb_commander_retirement_override.txt:111-116`), while Vanilla uses 75. The header describes SB ruler/general handling, but the change is not region/tag scoped.

### CP-07 — Conditional — Hail Columbia can undo the Inboekstelsel visibility guard

Both mods hard-replace `law_legacy_slavery`. If Hail Columbia's copy wins load order, it lacks SB's Boer visibility guard (`common/laws/02_sb_inboekstelsel_slavery.txt:3-12`; HC `common/laws/usfp_law_slavery_overrides.txt:517`), allowing the legacy law where SB expects the variant.

### CP-08 — High documentation/compatibility risk — override manifests are materially incomplete

**Confirmed.** `Docs/compatibility/override_manifest.md` and `third_party_compatibility.md` omit:

- New changed blocks `STATE_GRIQUALAND_WEST` and `STATE_BECHUANALAND` from the claimed state-region list.
- 29 of 37 same-path Vanilla files, including character/country history, the Highveld event file, all five generated locator files, spline network, both journal GUI files, `province_terrains.txt`, and `provinces.png`.
- Global hard replacements for dominion actions/subject type, stake-colonial-claim, abolish-monarchy, and ideology/movement content.

Full map rasters/locators also conflict with other map mods outside the named state blocks, contrary to the narrow compatibility claim.

---

## D. Localization, graphics, map, and presentation

### SUP-01 — High — STA flag references a nonexistent CoA

**Confirmed by static scan and Tiger.** `common/flag_definitions/sb_flag_definitions.txt:373-378` uses `coa = STA` and `subject_canton = STA`, but neither SB nor Vanilla defines `STA`. STA is a live country definition. Expect missing or fallback flag art.

### SUP-02 — High — reachable Griqualand West event description is missing

**Confirmed by current 1.13.9 log.** `events/sb_griqualand_west_events.txt:1884` references `sb_griqualand_west.025.oranje_annexation_d`, but only `.cap_d`, `.ora_d`, and generic descriptions exist. `error.log` reports the key as unrecognized; the branch can show a raw/blank key.

### SUP-03 — Medium — SGO uses an undefined named color

**Confirmed by Tiger.** `common/coat_of_arms/coat_of_arms/sb_countries.txt:484` uses `"dark green"`; the live named-color database has `green_dark`. The opaque textured emblem may mask normal display, but fallback rendering is invalid.

### SUP-04 — Medium — diplomatic lens icons are missing

**One path runtime-confirmed.** Visible responsible-government actions have action-panel textures but no same-ID lens icons. Current logs report missing `gfx/interface/icons/lens_toolbar_icons/sb_ask_responsible_government.dds`; the grant-side file is also absent. Because the ask action permits obligations, an `_obligation.dds` variant is an additional runtime check.

### SUP-05 — Medium/high — current map and spline overrides produce invalid graph connections

**Confirmed on an isolated 1.13.9 + CMF + SB load.** `error.log:18-33` reports eight state-adjacency connections with no node and four route-strip errors for locator pairs `25503-26101` and `26204-26300`. CMF contains no map files. Travel/route rendering and adjacency behavior are therefore suspect.

### SUP-06 — Medium — several hub locator coordinates remained on old split-state land

**Confirmed by coordinate sampling against `provinces.png`.** Examples:

- Cape farm locator 261 samples Northern Cape rather than declared Cape hub x407453.
- Northern Cape farm locator 262 samples Griqualand West rather than x70C050.
- Cape mine locator 261 samples Northern Cape rather than x60DD97.
- Northern Cape wood locator 262 samples Bechuanaland rather than x7040D0.

Relevant definitions are `map_data/state_regions/04_subsaharan_africa.txt:1293-1314` and locator entries around lines 1509-1516 of the generated farm/mine/wood files.

### SUP-07 — Runtime check — provisional Bechuanaland map mask may contain isolated provinces

The hub/impassable checker passes, but the state file labels the mask temporary/WIP (`04_subsaharan_africa.txt:1344-1347`). Independent connectivity sampling found three passable provinces isolated from the main passable component. Cold-start pathing/front testing is required before release.

### SUP-08 — Low — unused presentation content and stale localization

Confirmed candidates:

- `gfx/interface/icons/je_icons/sb_je_cape_politics.dds` is unused; the JE uses a Vanilla icon.
- `gfx/event_pictures/convict_crisis_1849.png` is unused; the event uses a Vanilla `.bk2`.
- `sb_boer_conventions.150.b` localization has no event option.
- Twelve Martinus `.042/.044-.048.a/.b` keys are bypassed because those events reuse `.041.a/.b`.
- `sb_bst_l_english.yml:39-40` is stale after removal of the STA decision.
- `je_sb_bechuanaland_corridor_status` is stale; the JE always uses triggered alternatives.
- `sb_boer_ai_economy_create_wheat_farm` is definition-only.
- `sb_force_ora_potgieter_commandant_general` has only a commented-out caller.
- `sb_should_be_involved_in_delagoa_route` is definition-only.

`te_sgo_united_flag.tga` is intentionally staged by a TODO and should not be treated as accidental orphan content.

### SUP-09 — Low — localization formatting and collision hygiene

All 34 active English files have a BOM, valid header, UTF-8 decoding, and no internal exact/case-insensitive duplicate keys. Remaining hygiene:

- `Spies` in `sb_natal_crisis_l_english.yml:153` duplicates an identical Vanilla key and is logged as a duplicate.
- Two files lack a final newline.
- Several files contain leading tabs; `sb_l_english.yml` also has trailing whitespace.

These formatting items are tolerated by the current Paradox loader; only the duplicate produces a current diagnostic.

---

## E. Tooling, resources, and documentation

### TOOL-01 — Medium — accepted resource audit data does not match live state caps

**Confirmed by running the pipeline with its report redirected outside the repository:** 82 checks pass and one aggregate check fails, covering 12 live mismatches on rows marked accepted and `live_synced=yes`:

- Cape Colony: Arable 44→42; Fishing 15→12.
- Northern Cape: Arable 12→6; Fishing 0→3; Iron 21→0; undiscovered Gold 20→0.
- West Transvaal: Wood 0→1; undiscovered Gold 94→0.
- Eastern Transvaal: undiscovered Gold 4→0.
- Transorangia: Wood 0→1; undiscovered Gold 4→0.
- Namaqualand: Arable 2→4.

The checked-in `resource-rework/resources/audit/test_report.md` is also stale and reports a different mismatch count.

### TOOL-02 — Medium — resource validation can print failure and still exit successfully

`resource-rework/resources/scripts/resources.py:62-69` reports failed checks without a nonzero process exit. The internal tester also contains a hard-coded checkout path (`scripts/_internal/test_resources_pipeline.py:12-18`) and an unconditional pass path around `:968-979`, making CI/portable use unreliable.

### TOOL-03 — Low — resource documentation points to retired paths

Commands in `resource-rework/resources/README.md:660-681` and `audit/README.md:32-35` refer to nonexistent `Docs/resources/scripts/resources.py`. The live CLI is under `resource-rework/resources/scripts/`.

### TOOL-04 — Medium — root README and metadata are stale/nonportable

- README says Victoria 3 `1.12.5`, while descriptors target `1.13.9`.
- Three links use absolute machine-local lowercase `docs/...` paths that do not exist.
- The documented Tiger command fails from repo root because it assumes execution from the mod parent.
- Metadata says 19 JEs; the current static count is 21 custom JEs (24 including three Vanilla overrides).

### TOOL-05 — Low/medium — map checker is narrow and format-fragile

`tools/check_state_region_hub_impassables.py:37-38` recognizes province IDs only on the physical line containing `impassable`; a valid multiline block would be missed. It does not verify locator coordinates, province duplication/membership, image/terrain palette, state connectivity, or spline consistency—the areas where this audit found current risk/errors.

### TOOL-06 — Low — active dead-variable cleanup produces engine diagnostics

Current 1.13.9 logs report these as read but never set:

- `sb_bechuanaland_caprivi_escalated_var`
- `sb_bechuanaland_boer_influence_positive_var`
- `sb_bechuanaland_swa_influence_positive_var`
- `sb_imperial_confederation_scheme_scope`

The first three appear to be legacy score-migration inputs; the last is cleanup-only. Removing them may affect intended save migration and should therefore be decided explicitly rather than done as incidental cleanup.

### TOOL-07 — Low — additional documentation drift

- `gfx/coat_of_arms/textured_emblems/README_sb_flag_assets.txt` references missing CAP/ABY source DDS files and no longer describes the live MZQ textured flags.
- `Docs/cross_tag_event_travel_times.md` retains a `sb_mozambique_company` event-namespace row although that event namespace/file was removed.
- `common/history/countries/mzq - mozambique company.txt` still says MZQ is created by the removed Portuguese administration event chain.
- `zz_sb_mozambique_company_override.txt` says only AI selection weight changes, but it also removes Vanilla incorporated-state checks.

---

## F. Suspicions and explicit runtime test queue

These were not promoted to confirmed defects:

1. Cape `.200` can carve Albany from any current Eastern Cape owner after the delayed London response; this may be intentional robustness.
2. Delayed Natalia backer events retain `scope:natalia` with minimal life checks; test NAL death during the 5-8 day delay.
3. Vanilla history still attempts the dormant SAF subject and GBR protect-TRN secret goal; test whether dead scopes create ghost diplomacy.
4. Firearms localization says access/industry must be continuous for 24 months, while JE progress only increments and never resets; clarify cumulative versus continuous intent.
5. `sb_revoke_oranje_griqualand_claim` can remain valid if ORA disappears midwar but may enforce nothing without the TRN federation marker.
6. MZQ territory transfer is direct-owner-only and does not collect land held by subordinate administrations; confirm this is intended.
7. The SGO restraint patch cannot cancel a transfer-subject play already started before the next monthly refresh.
8. Highest-value Bechuanaland runtime scenarios are BC-01/02/03/05/10/13/15/16 plus SGO/SWA alignment changes during pending routes.

---

## Validation results and noise separation

### Passed

- `git diff --check`.
- Independent Clausewitz brace/quote scan.
- `python3 tools/check_state_region_hub_impassables.py`.
- Localization BOM/header/UTF-8 checks.
- Explicit asset reference scan: no missing literal gfx paths.
- State/province membership, state-ID collision, terrain/image-palette, and locator ID count/uniqueness checks.
- Current 1.13.9 startup parses the new Bechuanaland diplomatic-play/effect/on-action syntax; no unknown-effect/trigger/parser error was found for the rewrite.

### Failed or diagnostic

- Resource pipeline: 82 pass, one aggregate failure covering 12 mismatches.
- Tiger: `0 fatal, 16 errors, 53 warnings, 2 untidy`.
- Current logs: missing Griqualand description, duplicate `Spies`, missing requester lens icon, four never-set variables, map adjacency/spline errors, and Bechuanaland button AI wrong-scope errors.

### Known validator/external noise

- All 16 Tiger `seal_and_signature_texture` errors are 1.13.5 schema lag; the field is widespread in Vanilla 1.13.9.
- Tiger's military-formation warnings occur on Vanilla-identical lines outside the POR diff.
- `IsDoubleSidedRyukyu`, movement-owner, slavery-ideology, and several lobby-scope warnings reproduce Vanilla syntax.
- CMF supplies `gui/com_journal_injects/injects.gui`; Tiger's missing-CMF GUI warning is false in the declared dependency setup.
- CMF duplicate-effect on-action warnings, save-deserialization invalid-date errors, and old treaty-article log lines were not attributed to current SB scripting.

## Suggested triage order

1. Lock/revalidate Bechuanaland event windows and make war-end settlement goal-specific.
2. Fix JE auto-activation gates (`GP-01` to `GP-03`).
3. Repair country/owner scoping (`BC-04`, `GP-04` to `GP-06`).
4. Harden legacy Bechuanaland route identity and cleanup.
5. Rebase global Vanilla replacements and document third-party load-order constraints.
6. Fix the small runtime-visible support defects (STA CoA, missing loc, lens icon, named color).
7. Regenerate/reconcile map locator/spline output and resource audit/live data.
8. Run the explicit Bechuanaland and delayed-event playtest queue before release.


---

## G. Runtime performance audit

This pass is structural: recurring work and asymptotic shape are confirmed from script, but no engine wall-time profiler was available. One-shot startup effects, event option effects, and static map loading were not treated as performance defects merely because they are large.

### PERF-01 — Critical — Delagoa maintenance becomes quadratic in live-country count

**Confirmed.** A correct once-per-world monthly path already exists (`common/on_actions/sb_mineral_discoveries_on_actions.txt:9-10,211-214` -> `common/scripted_effects/sb_eastern_sphere_effects.txt:713-743`). Substantially identical repair/enrollment logic is repeated at `sb_eastern_sphere_effects.txt:1300-1340` inside `sb_eastern_sphere_monthly_housekeeping`, which is called once for every country (`common/on_actions/sb_on_actions.txt:56-58,454-457`). Its `any_country` and `every_country` scans therefore run N times per month, in addition to the singleton global copy. While a gateway remains open with incomplete actors, this is O(N²)-shaped work.

**Direction:** retain one global monthly owner. Remove the root-independent Delagoa block from country housekeeping; keep only actor-relative work behind an early actor gate.

### PERF-02 — Critical — Imperial Confederation performs about eight to nine full-country passes in an active month

**Confirmed.** GBR housekeeping calls ensure/validate/sync/update (`sb_eastern_sphere_effects.txt:1252-1258`). The ensure helper already counts participants, scans for an owner, validates involvement, and syncs/counts again (`:1079-1097`). Housekeeping repeats validate and sync; the JE repeats both on its own monthly pulse (`common/journal_entries/1-09_sb_eastern_sphere.txt:216-220`). Validation and counting each use `every_country` (`effects:1100-1167`), while failure and sea-access maintenance add `any_country` scans.

Two full scans also run from 1836 because outer validate/sync calls are not gated by unlocked/active/unresolved state. Existing terminal-cleanup defect `GP-14` makes this permanent after success/failure.

**Direction:** one active-gated composite monthly pass owned by either GBR or the JE, not both. Count and validate participants once; setters should consume cached values rather than recount. Event-drive involvement changes and use quarterly/yearly repair where possible.

### PERF-03 — High — play-start handler is rerun on every side join and queues duplicate deployment trains

**Confirmed.** The same handler is registered for `on_diplomatic_play_started` and `on_diplo_play_join_side` (`common/on_actions/sb_on_actions.txt:32-38`). Every invocation reaches the frontier deployment scheduler (`:2169-2249`), which queues six `.900` events at days 1/7/21/45/90/180 without a pending marker (`common/scripted_effects/sb_frontier_ai_deployment_effects.txt:70-94`). War start adds another retry series; each join adds six more. Successful retries run four war checks and can iterate every military formation.

The dual registration also redispatches the hidden Natal balance event on every join, although an internal flag makes later bodies no-op.

**Direction:** separate play-start, join-side, and war-start responsibilities. Schedule one guarded retry train per play/country; leave only join-specific support logic on the join hook.

### PERF-04 — High — Firearms JE rebuilds a 60-tier modifier every unchanged month

**Confirmed.** The monthly pulse always updates and syncs (`common/journal_entries/1-04_sb_firearms_acquisition.txt:111-137`). The sync path checks/removes 60 modifiers and walks a 60-deep ladder before re-adding the same tier (`common/scripted_effects/sb_firearms_effects.txt:12-73,336-763`), after treaty/article/state and building eligibility scans (`common/scripted_triggers/sb_firearms_triggers.txt:22-42`). Up to five countries can carry the JE indefinitely.

**Direction:** store the applied tier and change old→new only when progress crosses a boundary. Keep monthly eligibility detection if its latency is gameplay-relevant; use a much cheaper idempotent/annual repair.

### PERF-05 — High/medium — broad country-monthly routing sends fixed-tag work through every country

**Confirmed structure; wall-time unprofiled.** Eleven actions are dispatched from four `on_monthly_pulse_country` registrations. The central router alone sends eight handlers to every country (`common/on_actions/sb_on_actions.txt:56-58`); Cape and Trek handlers are approximately 585 and 564 lines, with dozens of internally gated branches. BST and CAP cleanup add separate 226/109-line handlers.

The clearest concrete case is Namibia: its country handler first calls coastal-access and coast-race helpers for every country (`common/on_actions/sb_namibia_on_actions.txt:1-4`). Coast-race closure is root-independent fixed-province/global state (`common/scripted_effects/sb_namibia_effects.txt:120-128`) yet is repeated N times monthly until closure. Countries with both technologies but no relevant access also repeat state scans indefinitely (`common/scripted_triggers/sb_namibia_triggers.txt:16-34`).

**Direction:** retain monthly latency only where required. Put cheap tag/active/terminal gates at handler entry, direct-scope fixed tags from a singleton pulse, move root-independent work to `on_monthly_pulse`, and use technology/colony/subject events plus yearly catch-up for slow repair.

### PERF-06 — Medium/high — Bechuanaland progress is computed per JE copy and then broadcast again

**Confirmed duplication; exact engine cost needs profiling.** Opening creates a contextless JE for every involved actor (`common/scripted_effects/sb_bechuanaland_corridor_effects.txt:220-226`). Each copy's 253-line `monthly_progress` traverses four treaty/article paths and repeatedly queries relations (`common/scripted_progress_bars/sb_progress_bars.txt:949-1201`). A separate global monthly effect refreshes the same scopes/score and broadcasts the canonical value with an `every_country` scan (`effects:33-145`; `common/on_actions/sb_mineral_discoveries_on_actions.txt:198-207`).

Monthly scope refresh also runs `any_country` and `random_country` with the same SWA-sponsor predicate, including treaty checks, although the sponsor is cached. Opening separately scans all countries for actors that can only be TRN or ORA.

**Direction:** one canonical score/delta calculation per month; JE copies render the stored result. Validate the cached direct SWA overlord rather than rediscovering it twice, and test fixed actor tags directly.

### PERF-07 — Medium/high — other JEs churn stable modifier ladders

**Confirmed.** Zulu succession removes/checks and re-adds one of 20 modifier tiers each month (`common/journal_entries/1-03_sb_zulu_kingdom.txt:100-114`; `common/scripted_effects/sb_zulu_dynasty_effects.txt:320-625`). Namibia consolidation clears country and split-state modifiers and then re-iterates the regions to restore the current tier every month (`common/journal_entries/1-08_sb_namibia.txt:90-94`; `common/scripted_effects/sb_namibia_effects.txt:737-897`). Cape balance bands use the same remove-all/re-add pattern (`common/on_actions/sb_on_actions.txt:1137-1179`).

**Direction:** cache current tier and resync only on bar/state change; keep a low-frequency repair path for save robustness.

### PERF-08 — Medium — Boer restraint scans the world for eight fixed tags

**Confirmed.** Monthly GBR refresh uses `every_country` (`common/scripted_effects/sb_british_boer_restraint_effects.txt:4-75`) although the candidate trigger is exactly ORA/TRN/ZPB/LYD/NAL/SGO/ABY/KLR. It is also called on every play start/join through the shared handler.

**Direction:** direct-scope the eight optional tags. Refresh on relevant war/play/subject transitions and retain only a quarterly or annual GBR watchdog if other systems can overwrite secret goals.

### PERF-09 — Medium — CAP/ABY subject cleanup is both event-driven and perpetual

**Confirmed.** Subject/independence hooks already call the cleanup (`common/on_actions/sb_cap_subject_cleanup_on_actions.txt:9-15`), but a separate all-country monthly registration remains (`:5-7`). Dominion color variables are written every month without “not already set” guards, and part of CAP autonomy cleanup duplicates work in the main Cape pulse.

**Direction:** consolidate the owner, make writes idempotent, use transition hooks, and keep annual rather than monthly repair if subject-type transitions cannot all be observed.

### PERF-10 — Medium/high when UI is open — Imperial form validity is O(N²)

**Confirmed structure; GUI evaluation cadence is engine-dependent.** Button validity calls `sb_imperial_confederation_has_two_complete_state_owners` (`common/scripted_buttons/sb_eastern_sphere_buttons.txt:46-56`). The trigger nests `any_country` inside `any_country`, and each candidate evaluates 16 region-ownership predicates (`common/scripted_triggers/sb_eastern_sphere_triggers.txt:298-328`). The GUI binds button validity live.

Related duplication: the bind button evaluates the same “unbound independent participant” trigger twice (`scripted_buttons:12-18`), and JE failure re-runs deep global sea-access/state/treaty checks already maintained monthly.

**Direction:** cache the qualifying-owner count and terminal/failure causes in the existing single participant pass; button and JE read cached scalars/flags.

### PERF-11 — Medium — Bechuanaland broadcasts twice and rebuilds marker sets while stalled

**Confirmed.** Influence shifts call a full sync/broadcast before mutation and broadcast again afterward (`common/scripted_effects/sb_bechuanaland_corridor_effects.txt:107-195`). Pending monthly retry can clear/rebuild Boer and British participant sets with up to four `every_country` scans (`effects:875-935`) plus readiness scans until actors are free.

**Direction:** initialize/read once and broadcast once after mutation. Build marker sets when queued; revalidate marked scopes and rebuild only on invalidation or a throttled repair cadence.

### PERF-12 — Low/medium — smaller recurring redundancies

- The frontier-force monthly wrapper checks eligibility and the callee repeats the identical trigger; only four tags can qualify (`common/on_actions/sb_on_actions.txt:2763-2778`; `common/scripted_effects/sb_frontier_force_effects.txt:53-56`).
- An empty Namibia yearly country action is still registered (`sb_on_actions.txt:60-62`; `sb_namibia_on_actions.txt:123-126`).
- Mineral technology hooks place several `any_scope_state` searches before their one-shot global completion flags (`sb_mineral_discoveries_on_actions.txt:39-101`).
- CAP yearly pop conversions use an `any_scope_pop` prepass followed by a matching `every_scope_pop` pass (`sb_on_actions.txt:484-594`).
- ORA reissues two strategies monthly despite history/setup already assigning them (`sb_on_actions.txt:1428-1436`).
- The Imperial bind button and Boer Compact decision duplicate live conditions in shown/possible blocks.

### Performance items deliberately not raised

- Startup-only `every_country`/`every_state` work.
- Empty diplomatic-play `on_weekly_pulse` fields; they mirror Vanilla schema and do no work.
- Great Trek monthly stages, Transvaal/ZPB 36-month counters, BST yearly raids, and the abolish-monarchy monthly counter; cadence matches explicit mechanics and scopes are narrow.
- Static map raster/locator/spline size; current map defects are correctness/load/render concerns, not recurring simulation scans.
- Scramble-for-Africa weekly progress, which preserves Vanilla cadence; change only after profiling and a deliberate parity decision.


---

## H. Comparative hygiene, readability, and auditability

### Method and overall verdict

The comparison sampled equivalent event, JE, effect, trigger, on-action, diplomatic-play, override, documentation, and validation surfaces in Hail Columbia, Gates of the Bosphorus, Morgenröte, and Vanilla 1.13.9. These projects are comparators, not correctness gold standards.

**Verdict:** Spes Bona has a good feature-oriented foundation and is locally readable. It is markedly more maintainable than Morgenröte, generally more granular and better documented than Gates of the Bosphorus, and competitive with Hail Columbia. Its event/JE file sizes are close to Vanilla norms. It is **not yet consistently best-practice/audit-ready**, because global lifecycle and scope contracts are implicit, a 3,285-line router centralizes unrelated systems, recurring work is poorly gated, the Vanilla override surface is broad and incompletely tracked, and validation/documentation is not self-enforcing.

The right conclusion is not a broad rewrite. Preserve the strong naming and feature slices; surgically improve state contracts, router ownership, override containment, and executable validation.

### Quantitative context, not a quality score

For a common sample surface (`events`, on-actions, scripted effects/triggers, JEs, and scripted buttons):

| Project | Files | Lines | Median file | Files over 3,000 lines |
|---|---:|---:|---:|---:|
| Spes Bona | 99 | 45,789 | 236 | 1 |
| Hail Columbia | 82 | 53,156 | 333 | 2 |
| Gates of the Bosphorus | 161 | 95,612 | 253 | 8 |
| Morgenröte | 237 | 509,000 | 489 | 46 |
| Vanilla 1.13.9 | 624 | 387,729 | 365 | 11 |

Event files specifically are also healthy in size: SB median 413/max 2,363; Morgenröte median 2,659/max 31,537; Vanilla median 558/max 7,083. File size alone does not establish quality, but SB is not suffering from the pervasive event monoliths seen in Morgenröte or parts of GotB.

### Strengths to preserve

1. **Stable ownership/naming.** Most authored top-level effects and triggers use `sb_`; feature families such as Bechuanaland, Firearms, Namibia, BST, and Great Trek are easy to grep across JE/event/effect/trigger/localization files. A static sample found 501/512 top-level effects and 175/177 triggers using the SB prefix or an engine-required override name.
2. **Feature-oriented layering.** Event options often call named transition effects; compound conditions have named triggers. This is much easier to audit than large inline event bodies.
3. **Descriptive intent comments where they exist.** Good examples include the startup rationale in `common/on_actions/sb_on_actions.txt:1-22`, the Cape JE design/cross-reference header, Cape button cross-references, and the country-scope explanation in `common/scripted_effects/sb_firearms_effects.txt:240-257`.
4. **Optional-scope safety is common.** `c:TAG ?=` and descriptive saved scopes are used more consistently than in many example-mod scripts.
5. **Unusually good audit/research artifacts.** The compatibility manifest, travel-time audit, resource provenance package, map checker, and this evidence-classified issue ledger are stronger governance than the sampled example mods provide.
6. **Localization structure is healthy.** Active English files have correct BOM/header/UTF-8 structure and no internal duplicate keys.
7. **Explicit override naming is directionally good.** `zz_sb_*_override` plus `REPLACE:` is more discoverable than silent generic-name collisions.

### QUAL-01 — Critical maintainability risk — scope and state-machine contracts are implicit

The Bechuanaland state machine spans a 1,752-line near-commentless effect file, triggers, buttons, a global JE, events, progress bar, and on-actions. At least 46 Bechuanaland variables/saved scopes participate, but there is no transition table, authoritative phase value, invariants, or terminal-path matrix. Four near-duplicate queue transitions live at `common/scripted_effects/sb_bechuanaland_corridor_effects.txt:938-982`; validation and popup state live elsewhere. The functional failures in `BC-01` through `BC-21` are the practical consequence.

More broadly, nontrivial helpers rarely declare expected ROOT, required named scopes, outputs, idempotence, or cleanup owner. This makes implicit `root`, `PREV`, `scope:actor`, and contextless-JE behavior difficult to review and has already produced `BC-04`, `GP-04`, `GP-05`, and `GP-06`.

**Best practice:** add a short contract above every public nontrivial effect/trigger/on-action: caller/root type, required/optional scopes, variables set/cleared, idempotence, and allowed transitions. For long chains, use one authoritative phase/route value, guarded transition helpers, and one idempotent finalizer covering complete/fail/cancel/backdown/white peace.

### QUAL-02 — High — router ownership is hard to audit

`common/on_actions/sb_on_actions.txt` is 3,285 lines, while its header still says “Game Start Effects” and “Runs once.” It now registers monthly/yearly, diplomacy, war, law, election, company, colony, revolution, and technology hooks; it contains approximately 585-line Cape and 564-line Trek monthly blocks plus large war-goal handlers. Monthly registration is spread across four files.

Complex blocks also show indentation drift (`sb_on_actions.txt:2213-2249,2783-2846`; the Great Trek monthly block), so valid braces do not guarantee visually obvious control flow.

**Best practice:** keep a small central registration/dispatch inventory, then move startup, pulse, diplomacy/war, and feature resolution into feature-owned on-action files. Put cheap top-level triggers on handlers. Generate or test the hook inventory so execution order is searchable.

### QUAL-03 — High — override policy is better than peers, but implementation is not mechanically contained

SB has 37 exact-path Vanilla collisions; only one is byte-identical. It also has roughly 104 explicit replacement objects and whole GUI/map/history baselines. The manifest is a strong idea, but currently omits 29 same-path files, new state-region blocks, and several global hard replacements (`CP-08`). Current drift in political movements, frontier colonization, ideologies, commander retirement, and Highveld selectors demonstrates the risk.

`replace_path = "common/history/treaties"` is broader than needed for a single same-path Vanilla shadow and deletes additive files from co-loaded mods. Full GUI copies are ineffective after required CMF. Broad raster/locator/spline copies create map-mod conflicts outside the named regional block.

**Best practice:** generate the override inventory and fail validation for an unmanifested collision. Record upstream path/version/hash, exact intended delta, global/regional scope, owner, rebase date, and load-order semantics. Where a full copy is unavoidable, maintain a machine-checkable patch/parity test for unrelated Vanilla behavior.

### QUAL-04 — High — validation and release documentation are rich but not trustworthy as an automated release gate

There is no single repo-relative non-writing `validate` command or CI workflow. The resource tester can report failure and return success; it contains a hard-coded checkout path and stale checked output. The map checker covers one narrow format and cannot catch current connectivity/locator/spline defects. Localization and override audits used here are not committed reusable tools.

README/version/link/command drift and incomplete compatibility manifests mean prose does not reliably describe the live build. The report itself should become a tracked closure ledger, not only a snapshot.

**Best practice:** aggregate repository-only checks under one portable entry point with nonzero failure; optionally run Tiger/game-dependent checks when configured. Add generated-output no-diff, override-manifest/upstream-hash, localization/reference, delayed-event lifecycle, and map connectivity/locator checks.

### QUAL-05 — Medium/high — useful abstractions exist, but duplication remains the dominant source of drift

Examples:

- `sb_normalize_boer_trade_treaties` is a 677-line definition-only block (`common/scripted_effects/sb_treaty_effects.txt:5-681`). Later treaty creators/fallbacks repeat parallel bodies across targets.
- Transvaal unity repeats its completion requirements in monthly progress.
- Bechuanaland has four near-identical queue transitions and multiple repeated participant scans.
- Modifier ladders manually encode 20-60 parallel branches.
- Province/country lists are copied into triggers/effects/history; the 20-versus-30 Bechuanaland transfer drift is the functional example.

SB currently uses no scripted `$PARAM$` placeholders, compared with selective use in HC and GotB. Parameterization is not automatically better—Morgenröte's thousands of dynamic substitutions harm static tracing—but small documented helpers can remove genuine repeated transitions.

**Best practice:** extract one named invariant/transition when behavior is truly identical; use a parameterized or saved-target helper only when its scope contract remains obvious. Do not abstract mandatory diplomatic-play boilerplate merely to reduce line count.

### QUAL-06 — Medium — dead/retired scaffolding and manual archaeology remain in the active tree

Strong candidates include the 677-line uncalled treaty normalizer, deprecated definition-only migration effect, definition-only economy/commandant/Delagoa helpers, disabled country blocks in `sb_on_actions.txt:201-252`, and `always = no` references used to suppress orphan diagnostics. Current issue sections list additional unused assets/localization.

Do not delete every definition-only symbol blindly: save compatibility, scripted API use, and intended migration helpers must be reviewed first.

**Best practice:** commit an allowlisted unused-symbol report that distinguishes public/save/migration API from accidental dead code. Remove decided code rather than commenting it out; let Git carry history.

### QUAL-07 — Medium — comment quality and terminology are uneven

The strongest comments explain why; several most complex files have almost none: Bechuanaland effects (1,752 lines), Eastern Sphere effects (1,430), Namibia effects (1,020), and Griqualand West events (2,363). Other comments are stale or understate their override delta. The central on-action header is materially false.

Persistent/saved-scope names are mostly descriptive in new code, but generic legacy names (`ig`, `britain`, `migration_target`) and stable typos reduce searchability. Do not rename stable keys casually; register/deprecate aliases when cleanup is justified.

**Best practice:** add concise scope/invariant/ownership comments, not syntax narration. Require every hard override comment to state the exact Vanilla delta.

### QUAL-08 — Medium — delayed event lifecycle is below Vanilla's defensive standard

A static comparison found cancellation triggers on roughly 11/242 SB events versus 1,076/2,252 Vanilla events. This is not a quota—many events do not need cancellation—but Vanilla's default is safer for delayed interactive chains. SB frequently sets a pending lock late, rechecks only part of the original invariant, or has cleanup only on success.

**Best practice:** for delayed chains, set the pending lock before scheduling; recheck all country/scope/phase invariants in trigger or `cancellation_trigger`; make choices idempotent; and route cancellation, target death, backdown, white peace, and success through explicit cleanup.

### QUAL-09 — Medium/low — localization review status is not reliable QA state

There are 128 `TO REVIEW` markers across 17 localization files. Some blocks labelled reviewed still contain visible proofreading errors. A 668-line residual `sb_l_english.yml` contains empty sections and inconsistent indentation. Formatting drift is small but machine-checkable.

**Best practice:** move review state to a checklist/generated coverage report, proofread remaining blocks, and lint BOM/header/newline/whitespace, mod/Vanilla collisions, referenced event keys, and review-marker counts.

### Comparator-specific lessons

#### Hail Columbia

- **SB advantage:** stronger feature naming, smaller median core files, explicit compatibility/issue documentation, and more feature-aligned effect/trigger slices.
- **HC advantage:** a much smaller single on-action router (~1,197 lines versus SB's 3,285-line central file), selective parameter helpers (`$AMOUNT$`, `$MULT$`, `$RADICALS$`), three scripted gameplay tests, and a mature changelog.
- **Do not treat HC as a gold standard:** its country-monthly router drives a very large event/random-event list for every country, it has no comparable override manifest/known-issue ledger, helper scope contracts are not systematic, and its Tiger dependency path is machine-specific.

#### Gates of the Bosphorus

- **Adopt:** aligned module/file maps, early on-action triggers, explicit ROOT/target contracts in complex helpers, selective parameterized triggers/effects, and its more portable Tiger configuration.
- **Preserve SB advantages:** stable single prefix, smaller feature event files, better JE design headers, optional-scope use, CMF detection, and much stronger compatibility/issue documentation.
- **Do not copy:** GotB also has 5,000-8,000-line event monoliths, stale hand-maintained TOCs, empty placeholder files, broad undocumented overrides, and at least one N×N monthly pattern.

#### Morgenröte

- **Adopt selectively:** feature-sliced on-action files, small documented parameter contracts, and randomized delays to spread already-gated yearly work.
- **Preserve SB advantages:** SB is dramatically closer to Vanilla file granularity, uses a stable prefix, has far less commented-out script, and provides real compatibility/research/validation documentation.
- **Do not copy:** giant per-person event/effect files, mixed/unprefixed namespaces, thousands of dynamically composed parameters, blanket error-suppression effects, silent “vanilla overwrite” files, and many independent country pulses.

#### Vanilla 1.13.9

- **Adopt:** delayed-event cancellation, idempotent terminal cleanup, explicit on-action `trigger`/`effect` separation, cheap gates before broad scopes, and upstream parity discipline.
- **Use judgment:** Vanilla itself contains large framework files and mandatory boilerplate; matching its architecture everywhere would not automatically improve a focused regional mod.

### Comparative bottom line

SB is **readable at the feature/file level but not yet reliably auditable across feature lifecycles**. Relative position:

- **Better than Morgenröte** on granularity, naming, and documentation.
- **Usually better than GotB** on local feature readability and governance, while GotB has some stronger scope-contract/router patterns.
- **Comparable to HC**, with SB ahead on explicit governance, naming, and feature topology but behind on compact routing, selective reuse, and committed gameplay tests.
- **Near Vanilla norms for event/JE size**, but behind Vanilla's defensive delayed-event and rebase discipline.

### Maintainability priority order

1. Fix `PERF-01`/`PERF-02` and the scope/state defects while introducing explicit contracts.
2. Split the on-action router at existing feature boundaries and add early gates.
3. Generate and enforce the override/upstream-delta manifest.
4. Build one portable nonzero-on-failure validation entry point and CI.
5. Centralize repeated invariants/transitions; selectively parameterize only clear repetitions.
6. Triage dead code with a save/API allowlist, then remove decided scaffolding.
7. Reconcile README/compatibility/metadata and complete localization proofreading.
