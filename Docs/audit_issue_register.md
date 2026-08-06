# Repository Audit Issue Register

**Audit date:** 2026-08-06  
**Original audit baseline:** `e5706779e0d9fed7f93d930301c5e8162ea09f05` plus ten Bechuanaland files, committed as `45d804a069721db82bfa38d36f6e076ecee9a076`
**Critical remediation commit:** `48d8794776532ae0739cabe54c07cb4a97c24272`
**Very High remediation baseline:** `48d8794776532ae0739cabe54c07cb4a97c24272`
**Target:** Victoria 3 `1.13.9`; Community Mod Framework `1.58.2`

This maintained register records open, resolved, runtime-check, performance, and code-quality findings from a repository-wide static audit, with additional scrutiny on the Bechuanaland Corridor/Crisis rewrite. It is a best-effort inventory, not a guarantee that every runtime defect has been found. The original audit was read-only; later remediation status is recorded explicitly below.

## Labels

- **Resolved**: corrected in code and statically validated; any outstanding engine playtest is stated.
- **Confirmed**: directly demonstrated by control flow, data comparison, validator output, or current 1.13.9 logs.
- **Runtime check**: static evidence is strong, but the exact engine response still needs an isolated playtest.
- **Very High**: confirmed release blocker below Critical because its reach is narrower.
- **Medium-High**: confirmed material defect whose reach or impact falls between High and Medium.
- **Design/UX**: script behavior and player-facing text or apparent intent disagree; the engine may still execute the script as written.
- **Tooling/noise**: affects validation or maintenance rather than live gameplay.

Severity order: **Critical → Very High → High → Medium-High → Medium → Low**.

**No open Critical or Very High findings remain after this pass.**

## Highest-priority open items

1. Remaining Bechuanaland settlement/lifecycle defects can still strand routes, enforce incomplete packages, or seize third-party land (`BC-07`, `BC-09`, `BC-11`, `BC-12`).
2. Broad Vanilla overrides and treaty load-order behavior remain globally risky (`CP-01`, `CP-02`, `QUAL-03`).
3. Diplomatic-play join handling can schedule duplicate frontier deployment retry trains (`PERF-03`).
4. Medium-High support, map, and release-process defects remain open, including missing STA/Griqualand presentation and invalid map connections (`SUP-01`, `SUP-02`, `SUP-05`, `QUAL-04`).

---

## A. Bechuanaland Corridor/Crisis

### ~~BC-01 — Resolved (formerly Critical) — escalation windows can no longer overwrite or revive a resolved crisis~~

**Fixed in this pass; targeted engine playtest remains.** Each Warren or Caprivi escalation is now reserved atomically at button-effect time with an exclusive, route-specific 30-day decision lease. Delayed-event triggers, cancellation guards, option effects, and queue transitions revalidate the matching lease and the live corridor state before changing land, influence, war, or route state. Queueing consumes the lease before establishing the sole pending route; terminal choices and crisis cleanup clear it. Natural JE resolution is deferred during the lease, and queued launch validation now rejects a resolved or victory-marked corridor.

Static control-flow validation confirms that a stale/cancelled window cannot clear or replace another queued route or relaunch a terminal corridor. Runtime tests should still cover simultaneous button attempts, held-open popups, lease expiry, participant death/overlord change, and save/load at each transition.

### BC-02 — Medium-High — Boer choice event can be dispatched repeatedly

**Confirmed.** The `.032` dispatch flag lasts 15 days (`effects:1180-1187`), but `.032` is a duration-three event (`events:337-377`) and the monthly retry calls the launch effect again. An unanswered player popup can therefore be redispatched, leaving competing support/neutrality choices.

### ~~BC-03 — Resolved (formerly Very High) — white peace and mixed treaty outcomes now close as unresolved~~

**Fixed in this pass; targeted engine playtest remains.** Direct, proxy, reciprocal CAP-SGO, and Cape dual-return plays now share one exact play predicate and one XOR resolver. Enforcement by exactly one marked side still selects that side's settlement; white peace or enforcement by both sides queues `.042`, whose immediate effect removes every country's claim on `STATE_BOTSWANA`, marks the corridor resolved, and runs terminal cleanup. It deliberately preserves all ownership and claims in the distinct `STATE_BECHUANALAND` region.

**Depro's comments:** So I think the flow should be like (for both proxy or direct):
White peace (caprivi ± boers, warren + SWA/O involvement) -> fire event "unresolved settlement" -> all claims on botswana are dropped and JE is closed

### BC-04 — Medium-High — international-JE AI weights run in `none` scope

**Confirmed by current logs.** The JE is global/international (`common/journal_entries/1-11_sb_bechuanaland_corridor.txt:3-4,26-30`), but button AI weights call country triggers without an explicit country scope (`common/scripted_buttons/sb_bechuanaland_corridor_buttons.txt:64-66,117-119`). Current `error.1.log` reports `has_strategy`, `gold_reserves`, and `net_fixed_income` in `none` scope. The intended subsidy/trade-mission AI weighting is not functioning.

### ~~BC-05 — Resolved (formerly Very High) — legacy no-intervention routes no longer freeze the JE~~

**Fixed in this pass; targeted engine playtest remains.** The CAP-SGO path now uses a dedicated closed Return State play with reciprocal demands over the two Bechuanaland partitions. The Cape dual-return path and CAP-SGO path rediscover their exact play before setting route, side, or active-war markers; missing scopes or rejected creation immediately enter the unresolved settlement. Only actual target countries are marked.

Backdown, enforced-goal tracking, and war-end resolution now use exact corridor-play identity. White peace and mixed enforcement enter `.042`, while a monthly repair closes legacy saves that retain an active marker without a live corridor play. The previous generic marker-only hooks were removed.

**Depro's comments:** "CAP begins as a colony whose subject type normally cannot start its own play, so `.020.c` is a required playtest case." -> I have tested this previously it works if via scripts / events, e.g. in the diamond arc. Also the dp's in this case for both CAP-versus-SGO should be 'return state' (reciprocally). White peace should fire event "unresolved settlement" -> all claims on botswana (not Benechualand) are dropped and JE is closed. 

### ~~BC-06 — Resolved (formerly High) — unrelated wars can no longer settle the corridor~~

**Fixed with BC-03/BC-05.** The two broad on-action blocks that inferred a corridor result from country marker pairs were removed. Backdown, wargoal enforcement, and war end now accept only the four custom corridor play types, plus a narrowly identified CAP-SGO annex play retained solely for in-flight legacy-save compatibility. An unrelated war between formerly marked countries cannot select a corridor winner.

### BC-07 — High — pending cancellation is lossy, silent, and usually non-retryable

**Confirmed.** Queueing immediately changes influence, then can wait indefinitely for all core participants—and on the direct route every marked regional British subject—to be free of wars/plays (`effects:938-981`; `triggers:138-179`). If the core becomes invalid, the route cancels silently without restoring influence (`effects:1171-1175`). One-shot Warren/Caprivi country flags are not comprehensively cleared (`effects:686-815,1687-1752`), preventing retry. Warren also unconditionally requires Boer support even though its button does not require a currently valid Boer actor; this cancels instead of using Caprivi's neutrality fallback.

### BC-08 — Medium-High — SWA-overlord scopes become stale or refusal becomes a no-op

**Confirmed.** Refresh removes the stored sponsor only if the old country dies, not if it loses SWA, GP rank, or becomes aligned with Britain (`effects:44-61`). Warren refusal dispatch loops only current candidates and has no fallback (`effects:803-817`). Once queued, core validation checks life/direct subjecthood but not the original GP and British-security restrictions (`triggers:110-136`).

### BC-09 — High — no post-opening invalidation for lost prerequisites

**Confirmed.** SAF formation and CAP leaving British subjecthood skip only before `corridor_open` (`common/on_actions/sb_mineral_discoveries_on_actions.txt:181-196`). The JE invalid block checks only open/resolved state (`journal:105-110`). After opening, SAF formation, CAP death/independence, or sponsor loss can make every crisis core invalid without closing the international situation.

### BC-10 — Medium-High — each JE copy may queue a British settlement popup

Opening gives a separate contextless JE to every involved country (`effects:220-226`). Every copy's `on_complete` asks GBR to fire `.040`, with no British-pending guard (`journal:70-76`), although the failure route has such a guard (`effects:1491-1526`). If completion callbacks remain per-country, multiple `.040` popups will be created; later copies can rerun unguarded subject/claim/technology effects. Verify whether the engine coalesces international-JE completion callbacks.

### BC-11 — High — required direct/proxy return goals are not all primary demands

**Confirmed.** Reciprocal CAP/SGO return goals in the direct/proxy packages still omit `primary_demand` (`common/scripted_effects/sb_bechuanaland_corridor_effects.txt`). Backdown therefore need not impose the whole package, while settlement code can still award a full corridor victory. The play definition and localization promise both states.

The dual-return route touched in the Very High pass now makes its added Bechuanaland goal primary; the untouched direct/proxy package remains open.

### BC-12 — High — Britain's Caprivi concession can seize third-party land

**Confirmed.** Availability checks only that SWA does not own all five provinces (`buttons:213-216`). The concession unconditionally changes those provinces to SWA (`events:260-270`; `effects:574-581`) without checking current owner or control. They begin under decentralized LZO and can later belong to any country.

### BC-13 — Medium-High — SGO alignment is ignored

**Confirmed.** Natural failure treats any living SGO owning all Bechuanaland as Boer/SWA success, including a British/Cape subject SGO (`triggers:212-217,234-237`). Crisis network marking adds every living SGO and tries to put it on the SWA side (`effects:898-903,1084-1117,1150-1160`), while the British package excludes it. A later British- or third-party-aligned SGO can therefore be treated as an enemy, or fail to join while settlement logic assumes it did.

### BC-14 — Medium-High — Sponsor Settlers can be enabled but do nothing

**Confirmed for non-hard-coded fragments.** The button accepts any TSW-owned Bechuanaland fragment (`triggers:189-200,365-370`), but country creation supports only four hard-coded provinces (`effects:503-563`). If TSW retains another corridor province, the button and its AI weight remain active but create no SGO and give no influence. Also test whether `exists = c:SGO` is true for a dead static tag while dispatch requires `is_country_alive`.

### BC-15 — Medium-High — subject settlement does not reliably establish the intended direct overlord

**Runtime check.** The TSW helpers use transitive `is_subject_of` and then unqualified `change_subject_type` (`effects:634-684`). For example, an indirect British subject under CAP can enter the GBR branch but merely have its direct CAP pact changed; a subject in another hierarchy can reach `create_diplomatic_pact` without an explicit transfer/break. Directness should be tested against the intended GBR/CAP outcome.

### BC-16 — Medium-High — scripted transfer goals include non-transferable subject types

**Runtime check.** Direct crisis construction adds `transfer_subject` for every marked subject without checking `can_target_with_transfer_wargoal` (`effects:906-927,1070-1114`). ORA can normally be TRN's presidential-union/confederal subject, both explicitly non-transferable (`common/subject_types/sb_subject_types.txt:182-201,248-261`). The goal may be rejected while the country remains marked/joined and localization still claims it is at stake.

### BC-17 — Medium — new pacing bypasses the influence game

**Design/UX.** The current diff removes the 12-month Caprivi AI delay and Namaqualand/Namibian-core gate. SWA AI can demand immediately on opening with weight 1000; CAP/GBR Warren buttons are likewise weight 1000 and do not consult the frontier-AI rule (`buttons:135-239`). This can preempt the 12/24-month subsidy and influence loop.

### BC-18 — Medium — incomplete cleanup and contradictory claims

**Confirmed.** Six demand/refusal/concession country flags survive final cleanup (`effects:686-815,1687-1752`). Direct Warren adds CAP claims on Griqualand West and Bechuanaland (`effects:737-739`), but Boer/SWA interior settlement removes only CAP's Bechuanaland and GBR's Botswana claim (`effects:1621-1622`), leaving a Cape Griqualand claim after the proclaimed final settlement.

### BC-19 — Medium-High — “remaining Tswana-held land” transfers only the initial 20 provinces

**Confirmed.** `sb_bechuanaland_transfer_tsw_corridor_to_root` hard-codes 20 provinces (`effects:599-623`), while STATE_BECHUANALAND contains 30 (`map_data/state_regions/04_subsaharan_africa.txt:1340-1355`). Any additional corridor province later acquired by TSW stays behind despite the settlement text.

### BC-20 — Medium — the SGO British-restraint fix is permanent rather than crisis-scoped

**Fixed behavior awaiting design/playtest decision.** The new exception in `common/scripted_triggers/sb_british_boer_restraint_triggers.txt:14-32` has no open/unresolved condition. Monthly refresh continues GBR's befriend strategy and `-500` conquest offset after final settlement, although its comment describes preventing pre-emption of the crisis. The original subject-transfer hole is fixed, but duration is broader than the stated purpose.

### BC-21 — Medium-High — delayed `.010` can award victory after CAP disappears

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

### ~~GP-01 — Resolved (formerly Critical) — the Zoutpansberg crackdown JE no longer preempts its choice event~~

**Fixed in this pass.** The JE now requires `sb_zpb_crackdown_active_var`, mirroring the adjacent unity branch. Only the crackdown choice sets that flag before its guarded explicit JE addition, so the monthly scheduler can present the intended lawlessness choice and establish the claim/branch state first. Static validation confirms that the frontier-unity choice does not satisfy the gate and valid active-without-JE states still self-repair through automatic activation.

Already-poisoned legacy saves containing the crackdown JE without its active flag are not silently migrated into either branch; that separate save-migration decision remains outside this forward fix.

### ~~GP-02 — Resolved (formerly Very High) — East Transvaal pacification is event-unlocked~~

**Fixed in this pass.** `je_sb_pacifying_eastern_transvaal` no longer has a `possible` block, so it cannot auto-activate. Event `.130.b` is now the sole JE creator and independently repairs the East Transvaal claim before adding the JE. Its frontier-government marker is required for the active JE; legacy preempted copies without that marker invalidate instead of suppressing the choice.

**Depro's comments:** yes `.130.b` should be the main / only driver of creating je_sb_pacifying_eastern_transvaal

### ~~GP-03 — Resolved (formerly Very High) — Gaza consolidation now begins with its introduction~~

**Fixed in this pass.** The Gaza JE no longer exposes inactive/automatic activation. Starting Gaza schedules `.001` for the next day and sets the scheduling lock first; NGN inheritance and the monthly fallback use the same one-day dispatch. The event option sets a durable sequence marker, applies startup effects idempotently, establishes the one-month grace period, and only then adds the JE.

Legacy active JEs without the sequence marker invalidate and re-enter the guarded introduction path; an existing seed prevents duplicate startup effects.

**Depro's comments:** Yes this is wrong, the event should fire on day 1 or 2 (however the engine handles it) and then creates the JE via its button, after which the events occur. 

### ~~GP-04 — Resolved (formerly Very High) — Xhosa frontier pressure has one country-scope owner~~

**Fixed in this pass.** Only XHO's own country-monthly pulse now evaluates whether XHO owns an Eastern Cape partition carrying the resistance trait, then adds or removes `sb_xhosa_frontier_pressure` on ROOT. Unrelated country pulses can no longer remove the modifier, eliminating iteration-order dependence. The separate owner-agnostic cleanup of the state trait remains unchanged.

### ~~GP-05 — Resolved (formerly Very High) — Namibia punishment no longer affects every regional owner~~

**Fixed according to the clarified design.** Both region-wide state loops and their blanket mortality modifiers were removed. Forced Camps now applies a ROOT-country acceptance-tier Standard of Living penalty of `-7/-5/-2` for Violent Hostility/Cultural Erasure/Open Prejudice for ten years. Extermination Orders uses `-10/-7/-5` for the same tiers for its existing four-year duration. Movement suppression, refusal branches, and one-shot flags remain ROOT-local.

This removes cross-owner partition contamination and all mortality effects; the exact values are now stated in modifier and option localization.

**Depro's comments:** Okay additionally this is also not working as intended bc the mortality modifier affects all pops and not just discriminated pops of SWA. There seems to be a mismatch between standard of living effects and the mortality ones. Forced Camps -> -7 SoL for levels 1 (Violent Hostility), -5.0 for level 2 (Cultural Erasure) and -2.0 for level 3 (Open Prejudice). Extermination orders -10 SoL for levels 1, -7 SoL for level 2 and -5 SoL for level 3. The mortality effects should hence be removed, this will also fix the region ownership issues. 

### ~~GP-06 — Resolved (formerly Very High) — requester-side responsible government uses the actual overlord~~

**Fixed in this pass.** The requester action now changes relations from `scope:target_country` (the responding overlord) toward ROOT (the subject), matching Vanilla's requester pattern. Both subject-type and governance helpers read the subject's actual `overlord` link rather than phase-dependent `scope:actor`, so British and non-British grants derive government form from the correct country. The inverse overlord-grant action and AI evaluation scopes remain intact.

### GP-07 — Medium-High — Albany frontier wars check the wrong truces and still consume progression

**Confirmed.** The scheduler includes ABY but checks XHO truces only with CAP/GBR for wars 7-9 (`on_actions:871-886,915-918,965-968,1015-1018`). Events target ABY and immediately mark the step resolved after `create_diplomatic_play` (`events/sb_frontier_ai_wars_events.txt:535-565,621-635,707-737`). An ABY-XHO truce can reject play creation while permanently consuming the step.

### GP-08 — Medium-High — Gaza Portuguese raid damages the wrong land

**Confirmed.** The gate accepts Portuguese ownership in either Lourenço Marques or Zambezia (`effects/sb_eastern_sphere_effects.txt:163-170`), but event `.040` devastates every Lourenço Marques partition with no owner filter (`events/sb_gaza_events.txt:188-211`). If Portugal owns only Zambezia, Portuguese land is untouched and third-party/Gaza land can be damaged.

### GP-09 — Medium — BST retreat selects two independent frontier actors

**Confirmed.** `.020` moves a Sotho pop from one random qualifying country, then independently chooses another random country for the claim/relations result (`events/sb_bst_frontier_events.txt:126-168`). Split Vrystaat ownership can evacuate one actor's population while rewarding or penalizing another.

### GP-10 — Medium-High — Martinus delayed coercion can strand its active flag

**Confirmed.** `.010` sets `sb_martinus_coercive_chain_active_var`, while delayed child events require ORA still be an independent candidate (`events/sb_martinus_confederation_events.txt:157-164,785-1122`). If ORA is annexed or subjected before delivery, the event cancels and no failure path clears the flag. Cleanup exists only on successful resolution (`common/scripted_effects/sb_martinus_confederation_effects.txt:36-46,224-229,281-286`).

### GP-11 — Medium-High — Cape CQF delayed event can leave a permanent pending lock

**Confirmed.** Enactment start sets an untimed pending variable and schedules `.130` for 21 days (`common/on_actions/sb_cape_law_on_actions.txt:13-24`). `.130` requires Cultural Exclusion still being enacted and removes the variable only after its trigger succeeds (`events/sb_cape_events.txt:304-323`). Cancellation/change during the delay blocks all later checkpoints.

### GP-12 — Medium-High — Cape responsible-government petition button is orphaned

**Confirmed.** The player-facing button exists at `common/scripted_buttons/sb_cape_buttons.txt:39-76`, but `je_sb_cape_politics` attaches only the two favour buttons (`common/journal_entries/1-01_sb_cape_politics.txt:69-71`). Nothing attaches the petition button.

### GP-13 — Medium-High — BST frontier completion and invalidation can both be true

**Confirmed.** Completion is a qualifying Oranjeland actor owning all Vrystaat and Drakensberg; invalidation is also true when surviving BST owns none of either region (`common/journal_entries/1-07_sb_bst_frontier.txt:56-95,151-160`; `common/scripted_triggers/sb_bst_triggers.txt:15-20`). The reward is conditioned on BST being dead, so displaced-but-living BST yields invalidation or a rewardless completion depending evaluation order.

### GP-14 — Medium — Imperial Confederation has no terminal cleanup

**Confirmed.** The JE has failure cleanup only (`1-09_sb_eastern_sphere.txt:292-297`); SAF formation clears none of its globals/flags (`effects:819-865`). GBR's monthly housekeeping continues full validation/count/progress/sea-access scans and permanent subject marking after SAF formation or failure (`effects:1139-1166,1249-1259`).

### GP-15 — Medium-High — Natalia appeal can be resolved while the player popup remains open

**Confirmed timing mismatch.** The player appeal arrives day 8, Britain resolves day 9, and the appeal lasts three days (`events/sb_natal_crisis_events.txt:1003-1012,1713-1727`; `common/script_values/sb_event_travel_values.txt:105-116`). Britain's resolution respects only an already-recorded pledge, so a response after the first open day can be preempted.

### GP-16 — Medium-High — Delagoa acceptance/rejection fans out beyond the actor that qualified

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

### CP-02 — High — treaty `replace_path` removes reference-mod files when SB loads after them

**Confirmed VFS behavior.** `descriptor.mod` replaces the whole `common/history/treaties` directory even though the exact-path Vanilla file is already shadowed. With SB at higher priority, this drops Hail Columbia's `usfp_starting_treaties.txt` and Gates of the Bosphorus's `gbbf_treaties_history.txt`. The load-order constraint is undocumented.

### CP-03 — Medium-High — frontier-colonization law override omits unrelated 1.13.9 behavior

**Confirmed.** The comment says the change only adds trekker eligibility, but the full replacement omits Vanilla's `disallowing_laws = { law_sakoku }` and replaces JE AI bonuses for `ai_has_enact_weight_modifier_journal_entries`/`je_taming_the_north` with zero (`common/laws/00_sb_governance_principles.txt:27-100`; Vanilla `common/laws/00_colonial_affairs.txt:89-136`).

### CP-04 — Medium-High — ideology replacements contain out-of-scope drift

**Confirmed.** `REPLACE:ideology_reformer` omits Vanilla's Edo social-system stance, and the Junker-colonialism replacement omits Vanilla `law_social_monarchy = approve` (`common/ideologies/zz_sb_reformer_ideology_override.txt`; `zz_sb_junker_colonialism.txt`; corresponding Vanilla ideology files).

### CP-05 — Medium — Highveld exact-path override removed selector safeguards

**Confirmed.** Fallback `ordered_scope_character` selectors for Piet Retief and Mpande omit `character_is_valid_for_events = yes` and `position = 0`, changing a highest-clout single selection into iteration/last-save behavior and admitting invalid characters (`events/iberia_events/struggle_for_the_highveld_events.txt:374-380,593-599`). Two optional `interest_group ?=` dereferences were also hardened to `=`, increasing missing-scope risk. These differences are unrelated to the map-province edits that justify the override.

### CP-06 — Medium-High — commander-retirement override changes the entire world

**Confirmed.** All AI commanders receive +50 retirement chance at age 60 (`common/character_interactions/zz_sb_commander_retirement_override.txt:111-116`), while Vanilla uses 75. The header describes SB ruler/general handling, but the change is not region/tag scoped.

### CP-07 — Medium — Hail Columbia can conditionally undo the Inboekstelsel visibility guard

Both mods hard-replace `law_legacy_slavery`. If Hail Columbia's copy wins load order, it lacks SB's Boer visibility guard (`common/laws/02_sb_inboekstelsel_slavery.txt:3-12`; HC `common/laws/usfp_law_slavery_overrides.txt:517`), allowing the legacy law where SB expects the variant.

### CP-08 — Medium-High — override manifests are materially incomplete

**Confirmed.** `Docs/compatibility/override_manifest.md` and `third_party_compatibility.md` omit:

- New changed blocks `STATE_GRIQUALAND_WEST` and `STATE_BECHUANALAND` from the claimed state-region list.
- 29 of 37 same-path Vanilla files, including character/country history, the Highveld event file, all five generated locator files, spline network, both journal GUI files, `province_terrains.txt`, and `provinces.png`.
- Global hard replacements for dominion actions/subject type, stake-colonial-claim, abolish-monarchy, and ideology/movement content.

Full map rasters/locators also conflict with other map mods outside the named state blocks, contrary to the narrow compatibility claim.

---

## D. Localization, graphics, map, and presentation

### SUP-01 — Medium-High — STA flag references a nonexistent CoA

**Confirmed by static scan and Tiger.** `common/flag_definitions/sb_flag_definitions.txt:373-378` uses `coa = STA` and `subject_canton = STA`, but neither SB nor Vanilla defines `STA`. STA is a live country definition. Expect missing or fallback flag art.

### SUP-02 — Medium-High — reachable Griqualand West event description is missing

**Confirmed by current 1.13.9 log.** `events/sb_griqualand_west_events.txt:1884` references `sb_griqualand_west.025.oranje_annexation_d`, but only `.cap_d`, `.ora_d`, and generic descriptions exist. `error.log` reports the key as unrecognized; the branch can show a raw/blank key.

### SUP-03 — Medium — SGO uses an undefined named color

**Confirmed by Tiger.** `common/coat_of_arms/coat_of_arms/sb_countries.txt:484` uses `"dark green"`; the live named-color database has `green_dark`. The opaque textured emblem may mask normal display, but fallback rendering is invalid.

### SUP-04 — Medium — diplomatic lens icons are missing

**One path runtime-confirmed.** Visible responsible-government actions have action-panel textures but no same-ID lens icons. Current logs report missing `gfx/interface/icons/lens_toolbar_icons/sb_ask_responsible_government.dds`; the grant-side file is also absent. Because the ask action permits obligations, an `_obligation.dds` variant is an additional runtime check.

### SUP-05 — Medium-High — current map and spline overrides produce invalid graph connections

**Confirmed on an isolated 1.13.9 + CMF + SB load.** `error.log:18-33` reports eight state-adjacency connections with no node and four route-strip errors for locator pairs `25503-26101` and `26204-26300`. CMF contains no map files. Travel/route rendering and adjacency behavior are therefore suspect.

### SUP-06 — Medium-High — several hub locator coordinates remained on old split-state land

**Confirmed by coordinate sampling against `provinces.png`.** Examples:

- Cape farm locator 261 samples Northern Cape rather than declared Cape hub x407453.
- Northern Cape farm locator 262 samples Griqualand West rather than x70C050.
- Cape mine locator 261 samples Northern Cape rather than x60DD97.
- Northern Cape wood locator 262 samples Bechuanaland rather than x7040D0.

Relevant definitions are `map_data/state_regions/04_subsaharan_africa.txt:1293-1314` and locator entries around lines 1509-1516 of the generated farm/mine/wood files.

### SUP-07 — Medium — provisional Bechuanaland map mask may contain isolated provinces at runtime

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
8. Highest-value Bechuanaland runtime scenarios are the resolved-BC-01/03/05 matrices plus BC-02/07/09/10/11/12/13/15/16 and SGO/SWA alignment changes during pending routes.

---

## Validation results and noise separation

### Passed

- `git diff --check -- :!Docs/audit_issue_register.md`; the register exception is one trailing space in Depro's preserved GP-05 comment.
- Independent repository-wide Clausewitz brace/quote scan.
- Targeted control-flow assertions for the four exact corridor plays, XOR settlement, unresolved claim cleanup, explicit-only East Transvaal/Gaza JE creation, XHO-only pressure routing, Namibia modifier removal/values, and requester/overlord scopes.
- `python3 tools/check_state_region_hub_impassables.py`.
- Changed-file BOM/UTF-8 and changed-localization header/key checks.
- Tiger reported no errors or scope warnings in the changed gameplay files; its one changed-file warning is the known CMF GUI dependency false positive.
- Explicit asset reference scan: no missing literal gfx paths.
- State/province membership, state-ID collision, terrain/image-palette, and locator ID count/uniqueness checks.
- The pre-remediation 1.13.9 startup parsed the Bechuanaland diplomatic-play/effect/on-action rewrite without an unknown-effect/trigger/parser error. BC-01/03/05 and the other resolved Very High paths still require the targeted engine regressions recorded above.

### Failed or diagnostic

- Resource pipeline: 82 pass, one aggregate failure covering 12 mismatches.
- Tiger after the Very High pass: `0 fatal, 16 errors, 53 warnings, 0 untidy`; the 16 errors remain the known 1.13.5-schema noise below.
- Current logs: missing Griqualand description, duplicate `Spies`, missing requester lens icon, four never-set variables, map adjacency/spline errors, and Bechuanaland button AI wrong-scope errors.

### Known validator/external noise

- All 16 Tiger `seal_and_signature_texture` errors are 1.13.5 schema lag; the field is widespread in Vanilla 1.13.9.
- Tiger's military-formation warnings occur on Vanilla-identical lines outside the POR diff.
- `IsDoubleSidedRyukyu`, movement-owner, slavery-ideology, and several lobby-scope warnings reproduce Vanilla syntax.
- CMF supplies `gui/com_journal_injects/injects.gui`; Tiger's missing-CMF GUI warning is false in the declared dependency setup.
- CMF duplicate-effect on-action warnings, save-deserialization invalid-date errors, and old treaty-article log lines were not attributed to current SB scripting.

## Suggested triage order

1. Harden the remaining Bechuanaland pending-route cleanup, post-opening invalidation, primary-demand package, and third-party Caprivi transfer (`BC-07`, `BC-09`, `BC-11`, `BC-12`).
2. Rebase global Vanilla replacements and document third-party load-order constraints (`CP-01`, `CP-02`, `QUAL-03`).
3. Guard diplomatic-play deployment retry scheduling (`PERF-03`).
4. Repair the remaining country-scope AI and stale-sponsor cases (`BC-04`, `BC-08`).
5. Fix runtime-visible support defects and invalid map connections (`SUP-01`, `SUP-02`, `SUP-04`, `SUP-05`).
6. Reconcile resource audit/live data and make validation fail reliably.
7. Run the BC-01/03/05, GP-02/03/04/05/06, and other delayed-event regression queues before release.


---

## G. Runtime performance audit

This pass is structural: recurring work and asymptotic shape are confirmed from script, but no engine wall-time profiler was available. One-shot startup effects, event option effects, and static map loading were not treated as performance defects merely because they are large.

### ~~PERF-01 — Resolved (formerly Critical) — Delagoa maintenance has one global monthly owner~~

**Fixed structurally in this pass; no wall-time profiler was available.** Root-independent Delagoa stale-state repair and actor enrollment remain on `sb_on_monthly_pulse` through `sb_delagoa_route_monthly_open_check`. The duplicate repair, root enrollment, and global `any_country`/`every_country` enrollment block was removed from per-country eastern-sphere housekeeping. The O(N²)-shaped country fan-out is no longer present; genuinely actor-relative AI railway and treaty work remains on the country pulse.

### ~~PERF-02 — Resolved (formerly Critical) — Imperial Confederation monthly maintenance is consolidated and active-gated~~

**Fixed structurally in this pass; no wall-time profiler was available.** GBR country-monthly housekeeping is now the sole recurring owner. After the unlock watchdog, a named phase gate suppresses all recurring work while dormant or terminal; failure is checked first and the active state is revalidated before synchronization. Owner-JE repair now direct-scopes GBR and no longer validates or recounts internally. Involvement validation and subject counting each run once, bar setters consume cached values, and sea-access maintenance runs once.

The duplicate JE monthly pulse was removed; its `immediate` block remains as event-driven initialization with an explicit validate/count/apply order. Distinct failure and sea-access watchdog scans remain because they enforce separate semantics, but the repeated eight-to-nine-pass maintenance path and pre-unlock validation/count scans are gone. `GP-14` remains an independent terminal-cleanup issue rather than a recurring-work owner.

### PERF-03 — High — play-start handler is rerun on every side join and queues duplicate deployment trains

**Confirmed.** The same handler is registered for `on_diplomatic_play_started` and `on_diplo_play_join_side` (`common/on_actions/sb_on_actions.txt:32-38`). Every invocation reaches the frontier deployment scheduler (`:2169-2249`), which queues six `.900` events at days 1/7/21/45/90/180 without a pending marker (`common/scripted_effects/sb_frontier_ai_deployment_effects.txt:70-94`). War start adds another retry series; each join adds six more. Successful retries run four war checks and can iterate every military formation.

The dual registration also redispatches the hidden Natal balance event on every join, although an internal flag makes later bodies no-op.

**Direction:** separate play-start, join-side, and war-start responsibilities. Schedule one guarded retry train per play/country; leave only join-specific support logic on the join hook.

### PERF-04 — Medium-High — Firearms JE rebuilds a 60-tier modifier every unchanged month

**Confirmed.** The monthly pulse always updates and syncs (`common/journal_entries/1-04_sb_firearms_acquisition.txt:111-137`). The sync path checks/removes 60 modifiers and walks a 60-deep ladder before re-adding the same tier (`common/scripted_effects/sb_firearms_effects.txt:12-73,336-763`), after treaty/article/state and building eligibility scans (`common/scripted_triggers/sb_firearms_triggers.txt:22-42`). Up to five countries can carry the JE indefinitely.

**Direction:** store the applied tier and change old→new only when progress crosses a boundary. Keep monthly eligibility detection if its latency is gameplay-relevant; use a much cheaper idempotent/annual repair.

### PERF-05 — Medium-High — broad country-monthly routing sends fixed-tag work through every country

**Confirmed structure; wall-time unprofiled.** Eleven actions are dispatched from four `on_monthly_pulse_country` registrations. The central router alone sends eight handlers to every country (`common/on_actions/sb_on_actions.txt:56-58`); Cape and Trek handlers are approximately 585 and 564 lines, with dozens of internally gated branches. BST and CAP cleanup add separate 226/109-line handlers.

The clearest concrete case is Namibia: its country handler first calls coastal-access and coast-race helpers for every country (`common/on_actions/sb_namibia_on_actions.txt:1-4`). Coast-race closure is root-independent fixed-province/global state (`common/scripted_effects/sb_namibia_effects.txt:120-128`) yet is repeated N times monthly until closure. Countries with both technologies but no relevant access also repeat state scans indefinitely (`common/scripted_triggers/sb_namibia_triggers.txt:16-34`).

**Direction:** retain monthly latency only where required. Put cheap tag/active/terminal gates at handler entry, direct-scope fixed tags from a singleton pulse, move root-independent work to `on_monthly_pulse`, and use technology/colony/subject events plus yearly catch-up for slow repair.

### PERF-06 — Medium-High — Bechuanaland progress is computed per JE copy and then broadcast again

**Confirmed duplication; exact engine cost needs profiling.** Opening creates a contextless JE for every involved actor (`common/scripted_effects/sb_bechuanaland_corridor_effects.txt:220-226`). Each copy's 253-line `monthly_progress` traverses four treaty/article paths and repeatedly queries relations (`common/scripted_progress_bars/sb_progress_bars.txt:949-1201`). A separate global monthly effect refreshes the same scopes/score and broadcasts the canonical value with an `every_country` scan (`effects:33-145`; `common/on_actions/sb_mineral_discoveries_on_actions.txt:198-207`).

Monthly scope refresh also runs `any_country` and `random_country` with the same SWA-sponsor predicate, including treaty checks, although the sponsor is cached. Opening separately scans all countries for actors that can only be TRN or ORA.

**Direction:** one canonical score/delta calculation per month; JE copies render the stored result. Validate the cached direct SWA overlord rather than rediscovering it twice, and test fixed actor tags directly.

### PERF-07 — Medium-High — other JEs churn stable modifier ladders

**Confirmed.** Zulu succession removes/checks and re-adds one of 20 modifier tiers each month (`common/journal_entries/1-03_sb_zulu_kingdom.txt:100-114`; `common/scripted_effects/sb_zulu_dynasty_effects.txt:320-625`). Namibia consolidation clears country and split-state modifiers and then re-iterates the regions to restore the current tier every month (`common/journal_entries/1-08_sb_namibia.txt:90-94`; `common/scripted_effects/sb_namibia_effects.txt:737-897`). Cape balance bands use the same remove-all/re-add pattern (`common/on_actions/sb_on_actions.txt:1137-1179`).

**Direction:** cache current tier and resync only on bar/state change; keep a low-frequency repair path for save robustness.

### PERF-08 — Medium — Boer restraint scans the world for eight fixed tags

**Confirmed.** Monthly GBR refresh uses `every_country` (`common/scripted_effects/sb_british_boer_restraint_effects.txt:4-75`) although the candidate trigger is exactly ORA/TRN/ZPB/LYD/NAL/SGO/ABY/KLR. It is also called on every play start/join through the shared handler.

**Direction:** direct-scope the eight optional tags. Refresh on relevant war/play/subject transitions and retain only a quarterly or annual GBR watchdog if other systems can overwrite secret goals.

### PERF-09 — Medium — CAP/ABY subject cleanup is both event-driven and perpetual

**Confirmed.** Subject/independence hooks already call the cleanup (`common/on_actions/sb_cap_subject_cleanup_on_actions.txt:9-15`), but a separate all-country monthly registration remains (`:5-7`). Dominion color variables are written every month without “not already set” guards, and part of CAP autonomy cleanup duplicates work in the main Cape pulse.

**Direction:** consolidate the owner, make writes idempotent, use transition hooks, and keep annual rather than monthly repair if subject-type transitions cannot all be observed.

### PERF-10 — Medium-High — Imperial form validity is O(N²) when its UI is open

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

### ~~QUAL-01 — Resolved for the agreed scope (formerly Critical maintainability risk) — Bechuanaland lifecycle and scope contracts are explicit~~

**Scope-limited resolution.** The Bechuanaland state machine touched by this pass now documents its authoritative decision, queued-crisis, active-war, and terminal phases; route/lease ownership; required ROOT and saved-scope expectations; transition guards; and cleanup owner. The BC-01 implementation enforces those contracts through live-state predicates, atomic route-specific decision leases, event cancellation/effect guards, queue validation, and terminal cleanup.

This does not claim that every legacy helper in the repository now has a formal contract. Broader ROOT/`PREV`/named-scope documentation, a full transition table, selective queue deduplication, and one idempotent finalizer remain non-blocking maintenance guidance; the independent functional findings below remain open at their recorded severities.

### QUAL-02 — Medium-High — router ownership is hard to audit

`common/on_actions/sb_on_actions.txt` is 3,285 lines, while its header still says “Game Start Effects” and “Runs once.” It now registers monthly/yearly, diplomacy, war, law, election, company, colony, revolution, and technology hooks; it contains approximately 585-line Cape and 564-line Trek monthly blocks plus large war-goal handlers. Monthly registration is spread across four files.

Complex blocks also show indentation drift (`sb_on_actions.txt:2213-2249,2783-2846`; the Great Trek monthly block), so valid braces do not guarantee visually obvious control flow.

**Best practice:** keep a small central registration/dispatch inventory, then move startup, pulse, diplomacy/war, and feature resolution into feature-owned on-action files. Put cheap top-level triggers on handlers. Generate or test the hook inventory so execution order is searchable.

### QUAL-03 — High — override policy is better than peers, but implementation is not mechanically contained

SB has 37 exact-path Vanilla collisions; only one is byte-identical. It also has roughly 104 explicit replacement objects and whole GUI/map/history baselines. The manifest is a strong idea, but currently omits 29 same-path files, new state-region blocks, and several global hard replacements (`CP-08`). Current drift in political movements, frontier colonization, ideologies, commander retirement, and Highveld selectors demonstrates the risk.

`replace_path = "common/history/treaties"` is broader than needed for a single same-path Vanilla shadow and deletes additive files from co-loaded mods. Full GUI copies are ineffective after required CMF. Broad raster/locator/spline copies create map-mod conflicts outside the named regional block.

**Best practice:** generate the override inventory and fail validation for an unmanifested collision. Record upstream path/version/hash, exact intended delta, global/regional scope, owner, rebase date, and load-order semantics. Where a full copy is unavoidable, maintain a machine-checkable patch/parity test for unrelated Vanilla behavior.

### QUAL-04 — Medium-High — validation and release documentation are rich but not trustworthy as an automated release gate

There is no single repo-relative non-writing `validate` command or CI workflow. The resource tester can report failure and return success; it contains a hard-coded checkout path and stale checked output. The map checker covers one narrow format and cannot catch current connectivity/locator/spline defects. Localization and override audits used here are not committed reusable tools.

README/version/link/command drift and incomplete compatibility manifests mean prose does not reliably describe the live build. The report itself should become a tracked closure ledger, not only a snapshot.

**Best practice:** aggregate repository-only checks under one portable entry point with nonzero failure; optionally run Tiger/game-dependent checks when configured. Add generated-output no-diff, override-manifest/upstream-hash, localization/reference, delayed-event lifecycle, and map connectivity/locator checks.

### QUAL-05 — Medium-High — useful abstractions exist, but duplication remains the dominant source of drift

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

### QUAL-08 — Medium-High — delayed event lifecycle is below Vanilla's defensive standard

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

1. Split the on-action router at existing feature boundaries and add early gates.
2. Generate and enforce the override/upstream-delta manifest.
3. Build one portable nonzero-on-failure validation entry point and CI.
4. Centralize repeated invariants/transitions; selectively parameterize only clear repetitions.
5. Extend explicit scope/lifecycle contracts beyond the Bechuanaland paths touched here.
6. Triage dead code with a save/API allowlist, then remove decided scaffolding.
7. Reconcile README/compatibility/metadata and complete localization proofreading.
