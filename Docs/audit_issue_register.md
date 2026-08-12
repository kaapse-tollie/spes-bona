# Repository Audit Issue Register

**Audit date:** 2026-08-06  
**Latest status refresh:** 2026-08-12 (Medium-Low remediation and archive split)
**Original audit baseline:** `e5706779e0d9fed7f93d930301c5e8162ea09f05` plus ten Bechuanaland files, committed as `45d804a069721db82bfa38d36f6e076ecee9a076`
**Critical remediation commit:** `48d8794776532ae0739cabe54c07cb4a97c24272`
**Very High remediation baseline:** `48d8794776532ae0739cabe54c07cb4a97c24272`
**High remediation baseline:** `1e733567f50ceca1aae4d0901840d15874d7b375`
**Medium-High remediation baseline:** `07410424010fe3f2e51353ef4efb29d47b5dda9b`
**Target:** Victoria 3 `1.13.9`; Community Mod Framework `1.58.2`

This maintained register records open, resolved, runtime-check, performance, and code-quality findings from a repository-wide static audit, with additional scrutiny on the Bechuanaland Corridor/Crisis rewrite. It is a best-effort inventory, not a guarantee that every runtime defect has been found. The original audit was read-only; later remediation status is recorded explicitly below.

## Labels

- **Resolved**: corrected in code and statically validated; any outstanding engine playtest is stated.
- **Confirmed**: directly demonstrated by control flow, data comparison, validator output, or current 1.13.9 logs.
- **Runtime check**: static evidence is strong, but the exact engine response still needs an isolated playtest.
- **Very High**: confirmed release blocker below Critical because its reach is narrower.
- **Medium-High**: material live-game or release-integrity defect with broad, destructive, or settlement-critical impact.
- **Medium**: contained live gameplay, compatibility, map, or recurring-work defect that should be fixed after Medium-High work.
- **Medium-Low**: narrow edge case, mitigated defect, design mismatch, or tooling/maintenance problem with indirect gameplay risk.
- **Low**: cosmetic, stale, dead, or minor hygiene issue with little direct gameplay impact.
- **Design/UX**: script behavior and player-facing text or apparent intent disagree; the engine may still execute the script as written.
- **Tooling/noise**: affects validation or maintenance rather than live gameplay.

Severity order: **Critical → Very High → High → Medium-High → Medium → Medium-Low → Low**.

**No open Critical, Very High, High, Medium-High, Medium, or Medium-Low findings remain after this pass.**

Open inventory after the Medium-Low remediation: **16 Low/blocked**. Nineteen Medium-Low findings were resolved, four received their safe immediate fixes and moved to Low/blocked, and the archived resource-path cleanup also resolved `TOOL-03`. `SUP-05` remains explicitly deferred because spline edits are not cross-mod compatible.

## Highest-priority open items

1. Human localisation review and compatibility-patch work (`BC-22`, `CP-07`, `QUAL-09`).
2. Southern African war-policy and restraint duration (`BC-20`).
3. Minor gameplay, fallback-art, UI, localisation, dead-code, and bounded-performance cleanup recorded in the Low sections below.

---

## A. Bechuanaland Corridor/Crisis

### ~~BC-01 — Resolved (formerly Critical) — escalation windows can no longer overwrite or revive a resolved crisis~~

**Fixed in this pass; targeted engine playtest remains.** Each Warren or Caprivi escalation is now reserved atomically at button-effect time with an exclusive, route-specific 30-day decision lease. Delayed-event triggers, cancellation guards, option effects, and queue transitions revalidate the matching lease and the live corridor state before changing land, influence, war, or route state. Queueing consumes the lease before establishing the sole pending route; terminal choices and crisis cleanup clear it. Natural JE resolution is deferred during the lease, and queued launch validation now rejects a resolved or victory-marked corridor.

Static control-flow validation confirms that a stale/cancelled window cannot clear or replace another queued route or relaunch a terminal corridor. Runtime tests should still cover simultaneous button attempts, held-open popups, lease expiry, participant death/overlord change, and save/load at each transition.

### ~~BC-02 — Resolved (formerly Medium) — Boer choice dispatch is globally leased~~

**Fixed in the live August 11 scripts; held-event regression remains.** Direct and proxy Boer responses share one global dispatch marker lasting four months (`common/scripted_effects/sb_bechuanaland_corridor_effects.txt:2383`), while `.032` and `.033` each have a three-month duration. The monthly launch retry cannot redispatch either event while the original popup remains answerable. Terminal choice and crisis cleanup consume the pending-choice state, so the later expiry of the dispatch lease cannot reopen the same decision.

### ~~BC-03 — Resolved (formerly Very High) — white peace and mixed treaty outcomes now close as unresolved~~

**Fixed in this pass; targeted engine playtest remains.** Direct, proxy, reciprocal CAP-SGO, and Cape dual-return plays now share one exact play predicate and one XOR resolver. Enforcement by exactly one marked side still selects that side's settlement; white peace or enforcement by both sides queues `.042`, whose immediate effect removes every country's claim on `STATE_BOTSWANA`, marks the corridor resolved, and runs terminal cleanup. It deliberately preserves all ownership and claims in the distinct `STATE_BECHUANALAND` region.

**Depro's comments:** So I think the flow should be like (for both proxy or direct):
White peace (caprivi ± boers, warren + SWA/O involvement) -> fire event "unresolved settlement" -> all claims on botswana are dropped and JE is closed

### ~~BC-04 — Resolved (formerly Medium) — international-JE AI weights are actor-scoped~~

**Fixed in this pass.** Every contextless button AI block now proves the relevant saved global country exists, enters the primary Boer actor or SWA-overlord scope, and only then evaluates finances and strategy. No Bechuanaland button calls `gold_reserves`, `net_fixed_income`, or actor strategy from `none`; the portable validator and Tiger pass the revised blocks.

### ~~BC-05 — Resolved (formerly Very High) — legacy no-intervention routes no longer freeze the JE~~

**Fixed in this pass; targeted engine playtest remains.** The CAP-SGO path now uses a dedicated closed Return State play with reciprocal demands over the two Bechuanaland partitions. The Cape dual-return path and CAP-SGO path rediscover their exact play before setting route, side, or active-war markers; missing scopes or rejected creation immediately enter the unresolved settlement. Only actual target countries are marked.

Backdown, enforced-goal tracking, and war-end resolution now use exact corridor-play identity. White peace and mixed enforcement enter `.042`, while a monthly repair closes legacy saves that retain an active marker without a live corridor play. The previous generic marker-only hooks were removed.

**Depro's comments:** "CAP begins as a colony whose subject type normally cannot start its own play, so `.020.c` is a required playtest case." -> I have tested this previously it works if via scripts / events, e.g. in the diamond arc. Also the dp's in this case for both CAP-versus-SGO should be 'return state' (reciprocally). White peace should fire event "unresolved settlement" -> all claims on botswana (not Benechualand) are dropped and JE is closed. 

### ~~BC-06 — Resolved (formerly High) — unrelated wars can no longer settle the corridor~~

**Fixed with BC-03/BC-05.** The two broad on-action blocks that inferred a corridor result from country marker pairs were removed. Backdown, wargoal enforcement, and war end now accept only the four custom corridor play types, plus a narrowly identified CAP-SGO annex play retained solely for in-flight legacy-save compatibility. An unrelated war between formerly marked countries cannot select a corridor winner.

### ~~BC-07 — Resolved (formerly High) — pending crisis cancellation is lossless, visible, and retryable~~

**Fixed in the High remediation pass; targeted engine regression remains.** Direct/proxy influence changes are now deferred until an exact diplomatic play is successfully created, so organic influence can continue while readiness waits and cancellation commits no score. Successful launch applies the route debit once; legacy pending routes without the new marker are not charged again.

Cancellation now clears only the originating Warren or Caprivi attempt's country locks before route identity is removed, releases participant/phase state, and informs a live player sponsor through `.033`. Timed attempt watchdogs repair lost/expired popup chains. Warren support falls back to neutrality if its primary Boer actor disappears instead of invalidating the core.

### ~~BC-08 — Resolved (formerly Medium-High) — SWA sponsorship now survives demotion and follows a valid replacement overlord~~

**Fixed in this pass; targeted engine playtest remains.** Initial sponsorship still requires a non-British-aligned Great Power, but an incumbent now remains the active sponsor after rank loss while it directly controls SWA. Death, detachment, transfer, or an alliance/defensive pact with Britain invalidates that incumbent. Subject-change and monthly refresh paths select the new qualifying GP, give it the corridor JE, and route buttons, response events, and queued-crisis validation through the active-sponsor contract.

British security alignment now blocks premature natural settlement and queues `.034`, a Warren ultimatum with the same local land-holder routing and claims package but no appeal to SWA's sponsor. Acceptance records the British result; refusal proceeds directly to the reciprocal Cape return-state route. An in-flight Warren refusal also takes that direct route if no valid sponsor remains, rather than becoming a no-op. Timed leases and the existing cancellation/watchdog paths keep the transition retryable.

**Depro's comments:** Losing GP rank isn't an issue as SWA-O may still be powerful. However if SWA is transfered to another GP not aligned with GBR then yes that GP should become the owner of the JE. If SWA-O becomes aligned with GBR, the JE should resolve as a victory (claims wise) for GBR, I would immediately fire a custom warren expedition that is identical except that there's no appeal to SWA-O. Alignment means a defensive pact or alliance between SWA-O and GBR. 

### ~~BC-09 — Resolved (formerly High) — post-opening prerequisite loss has deterministic terminal handling~~

**Fixed in the High remediation pass; active-play engine behavior still needs regression testing.** A shared idempotent lifecycle handler now applies the binding precedence SAF formation → invalid Cape → independent SWA. SAF formation transfers an existing British Botswana claim to SAF and closes the crisis; Cape death or departure from the British subject hierarchy removes Britain's Botswana claim and closes it; SWA independence records British victory and enters the normal British settlement.

The handler runs from the monthly owner, SAF formation, country formation/independence hooks, and JE invalidation. Pending/held `.032`, `.040`, and `.041` events now cancel or guard their effects after terminal cleanup. An independent SGO is the primary Boer actor ahead of TRN/ORA, is no longer re-subjected by repair, and is excluded from self-subsidy, self-treaty, and self-relations calculations.

**Depro's comments:** As far as I'm aware currently the only method for SAF formation is via the Imp. Conf JE, which requires boer subjects; so yes this should invalidate the BC JE and transfer the botswana claim to SAF. Cape independence yeah should also invalidate and remove GBR's Botswana claim. By sponsor loss I assume you mean SWA becomes independent, yes, in this case this should count as a victory for GBR. If you mean SGO becomes independent then SGO just becomes the primary boer actor in the JE. 

### ~~BC-10 — Resolved (formerly Medium-High) — British settlement dispatch is globally idempotent~~

**Fixed in this pass; targeted engine playtest remains.** Every JE copy now calls one guarded queue effect. The first valid callback sets a global 30-day settlement lease and dispatches `.040`; later callbacks see the lease and do nothing. Event trigger, cancellation, and option guards require the same lease, terminal cleanup removes it, and the settlement effect now encloses its complete subject/claim/technology package behind the unresolved-corridor guard. Static inspection confirms there is only one `.040` dispatch site.

### ~~BC-11 — Resolved (formerly High) — all reciprocal corridor returns are primary demands~~

**Fixed in the High remediation pass; treaty UI/backdown playtest remains.** Both CAP→SGO and SGO→CAP Return State goals added to the shared direct/proxy package now use `primary_demand = yes`. The direct, proxy, CAP-SGO, and Cape dual-return routes therefore mark every required corridor return as primary while leaving optional subject/protectorate goals unchanged.

### ~~BC-12 — Resolved (formerly High) — the Caprivi concession cannot seize third-party land~~

**Fixed according to the clarified ownership rule.** The button and its delayed decision lease now require every fixed Caprivi parcel to be owned by LZO or already by SWA, while still requiring that SWA does not own the whole strip. A centralized, third-party, or debug-created alternate owner invalidates/cancels the demand before `set_owner_of_provinces`; partial prior SWA acquisition remains valid.

**Depro's comments:** The check is just for LZO control. Other decentralised control of the strip is impossible unless the console / debugger was used.

### ~~BC-13 — Resolved (formerly Medium-High) — SGO alignment has explicit British and third-party outcomes~~

**Fixed in this pass; targeted engine playtest remains.** SGO can count as the primary Boer actor only while independent. If it enters the British hierarchy directly or through Cape, natural settlement pauses and SGO alone receives `.035`: both choices record a British victory, while acceptance transfers SGO if necessary and annexes it to Cape. The annexation AI starts at the requested 70:30 split and implements the exact relation, GDP, and army-power tiers in the comment below.

If SGO instead becomes a third-party subject, the corridor is invalidated, Britain's Botswana claim is removed, and terminal cleanup runs without forcing SGO onto the SWA side. The existing independent-SGO-first actor selection remains unchanged.

**Depro's comments:** Okay if SGO becomes a British/Cape subject, this counts as a GBR victory. A custom warren like event (that only SGO gets) should fire to get SGO annexed to CAP. For this event the AI SGO should favour annexation 70 : 30 as base, modified as: 
+10 Cordial relations
+20 Amicable relations 
+30 friendly relations 
-10 poor relations 
-20 cold relations 
-30 hostile relations 
-10 0.9x SGO GDP ≤ CAP GDP ≤ 1.5x SGO GDP 
-20 CAP GDP < 0.9 SGO GDP 
+10 CAP GDP ≥ 2x SGO GDP
-10 1.5x CAP army power projection ≥ SGO army power projection > 0.8x CAP army power projection 
-20 SGO army power projection > 1.5x CAP army power projection 
+10 2x SGO army power projection ≥ CAP army power projection > 1.5x SGO army power projection 
+20 CAP army power projection > 2x SGO army power projection 
In the case SGO becomes third party (ex SWA-O or another Boer tag) aligned invalidate the JE and drop the GBR botswana claim, this is outside of scope. For another boer tag it replaces the old one as leader, for SWA-O pretty much the same. I guess we could check if TRN/ORA exist own their states and are also the third-party aligned but this complicates things for an extreme edge case so I would rather just invalidate the whole thing.
^Above is depreciated

### ~~BC-14 — Resolved (formerly Medium-Low) — Sponsor Settlers uses one raster-border contract~~

**Fixed in this pass.** Button eligibility and SGO creation now share the same actual-raster border contract. The eligible TSW provinces are `xD76CB9`, `x20CAA7`, `x4AFDFD`, and `xA494F8`, and creation uses that exact priority. Each candidate must border land owned by the primary Boer actor, and only a live SGO blocks the action. A regression test locks both the province set and ordering.

**Depro's Comment:** The valid provinces for creation should be those in Bechuanaland bordering the primary boer actor; those listed provinces are the ones bordering w. transvaal.

### ~~BC-15 — Resolved (formerly Medium) — landed TSW establishes the intended direct overlord~~

**Fixed in this pass; subject-tree engine regression remains.** The landed-TSW helper now transfers an existing member of the intended subject tree directly, releases it from a foreign hierarchy before pact creation, and sets its completion marker only after verifying that TSW is the intended country's direct puppet. Repeated calls are idempotent and cannot certify an indirect or foreign relationship.

### ~~BC-16 — Resolved (formerly Medium-High) — non-transferable subjects remain backers without invalid goals~~

**Fixed in this pass; targeted engine playtest remains.** Direct-crisis construction now checks transfer eligibility before adding a scripted `transfer_subject` goal against either side's auxiliary subject. Presidential-union and Boer-confederal subjects are still added as play backers, but receive neither an invalid transfer goal nor the British settlement marker that claims such a goal exists. Independent non-SGO Boer participants retain the engine-valid `make_protectorate` alternative; no substitute goal is fabricated for an already-subject country when the engine exposes no valid vassalization/protectorate target.

**Depro's comments:** Yes for presidential-union/confederal just have the dp be puppet/vassilise/etc (which ever is the correct one) if possible

### ~~BC-17 — Accepted design (formerly Medium-Low) — escalation may pre-empt the influence phase~~

**Closed as intentional pacing.** The one-year Caprivi delay was explicitly removed and the principal Warren, Caprivi, and corridor-question buttons intentionally use weight `1000`. Competition actions now use 12-month durations and cooldowns. Early escalation can still shorten the organic influence phase, but this is the selected design rather than an implementation defect.

### ~~BC-18 — Resolved (formerly Medium) — terminal claim cleanup is centralized~~

**Fixed in this pass.** Boer/SWA terminal settlement now removes CAP's Bechuanaland and Griqualand West claims plus GBR's Botswana claim before awarding the result claims. White peace and CAP subject-breakage invalidation remove GBR's Botswana claim, while third-party SGO subject invalidation deliberately preserves it. Terminal cleanup clears the obsolete Caprivi marker, and the dead dual-corridor transfer helper and its residual call sites were removed.

### ~~BC-19 — Resolved (formerly Medium) — all Tswana-held Bechuanaland fragments transfer~~

**Fixed in this pass.** The settlement helper now iterates TSW's live state fragments in `STATE_BECHUANALAND` and transfers every owned province in those fragments. The result no longer depends on a copied 20-province list and automatically covers later Bechuanaland ownership changes.

### BC-20 — Low / blocked (formerly Medium-Low) — restraint duration awaits the Southern African wars rework

**Safe immediate fix completed.** CAP now receives the same anti-conquest/befriend restraint as GBR. Source-specific markers ensure CAP and GBR can refresh or clear only their own AI goals, so a responsible Cape government cannot overwrite Britain's restraint and neither source accidentally removes the other's policy.

The broader duration and war-specific behavior remain deliberately blocked until the Southern African wars rework establishes the intended post-crisis policy. The current restraint therefore remains persistent rather than being given a speculative crisis-only lifetime.

**Depro's comments:** Move to blocked, further content (esp SAn wars) are needed. Also add CAP to this befriend strategy towards the boers, otherwise a responsible one can override.

### ~~BC-21 — Resolved (formerly Medium) — delayed Warren demand revalidates its destination~~

**Fixed in this pass; held-popup engine regression remains.** Before `.010` can resolve, it now revalidates live CAP, CAP's British relationship, the frontier foothold, and the current demand owner. Losing any prerequisite cancels through normal corridor invalidation and cannot award a British victory from a stale popup.

### BC-22 — Low / deferred (formerly Medium-Low) — Bechuanaland prose awaits rolling human review

**Safe immediate fix completed.** All `### TO REVIEW ###` and `### REVIEWED ###` markers were removed from event scripts without changing event prose. Review state now exists only beside the corresponding localisation blocks, and the validator enforces one localisation-side classification per scripted event.

Substantive proofreading remains intentionally deferred to Depro's rolling in-game review. No event prose was rewritten in this pass.

**Depro's comments:** `### TO REVIEW ###` only applies to localisation blocs, remove those outside this. Then move this to deferred. This must be done by a human (me), I do it on a rolling basis when I come across the events in-game while testing.

### ~~BC-23 — Resolved (formerly Medium-Low) — crisis support follows active participants and the influence model~~

**Fixed in the live August 11 scripts; war-participant regression remains.** SWA-overlord support now costs `£1,000` monthly, remains active only while SWA or the participating primary Boer network fights Britain/Cape, buffs only those active participants, and contributes `-0.125` monthly influence. Neutral or uninvolved actors no longer receive the modifier (`common/scripted_buttons/sb_bechuanaland_corridor_buttons.txt:296-328`; `common/scripted_effects/sb_bechuanaland_corridor_effects.txt:3369-3448`).

### ~~BC-24 — Resolved (formerly Medium) — missing crisis sponsor scopes are safe~~

**Fixed in this pass.** Crisis-sponsor and CAP-subject checks now enter a nested branch only after the saved SWA-overlord scope is proven to exist. A missing global scope returns cleanly without dereferencing it; Tiger reports no revised-script scope error.

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

### ~~GP-07 — Resolved (formerly Medium) — Albany frontier wars use the actual target and retry failed launches~~

**Fixed in this pass; diplomatic-play launch regression remains.** Each war now requires XHO to lack a truce with CAP, GBR, and the actual CAP-or-ABY target. The delayed event no longer marks progression resolved when it merely attempts play creation; the matching diplomatic-play start hook records success and clears the scheduled marker. A rejected launch therefore remains retryable.

### ~~GP-08 — Resolved (formerly Medium-High) — the Gaza raid damages only Portuguese partitions in both eligible regions~~

**Fixed in this pass.** Event `.040` now iterates both `STATE_LOURENCO_MARQUES` and `STATE_ZAMBEZIA`, applying ten devastation only to state partitions owned by Portugal. Gaza and third-party partitions are excluded, and the outcome now matches either branch of the existing eligibility gate.

### ~~GP-09 — Resolved (formerly Medium-Low) — BST retreat uses one frontier actor~~

**Fixed in this pass.** `.020` selects one Boer frontier actor and reuses it for migration, relations, the Drakensberg claim, and its completion marker. Selection prefers an eligible actor with at least 5,000 Sotho in its Vrystaat fragment, then falls back to any eligible actor. A regression assertion prevents a second actor scope from being introduced.

### ~~GP-10 — Resolved (formerly Medium-Low) — Martinus coercion has one leased lifecycle~~

**Fixed in this pass.** Active and backer state now use 90-day leases. A single idempotent cleanup effect clears TRN, ORA, LYD, ZPB, and NAL chain state, and every completion or cancellation route uses it. Monthly repair cancels the chain when ORA dies or ceases to be an independent candidate, so a delayed event cannot strand the active marker.

### ~~GP-11 — Resolved (formerly Medium) — Cape CQF pending state is a timed lease~~

**Fixed in this pass.** The pending marker now expires as a timed lease and is explicitly cleared by `on_law_enactment_ended` and event cancellation. Ending or changing a Cultural Exclusion attempt during the delay no longer blocks a later qualifying attempt.

### ~~GP-12 — Resolved (formerly Medium) — obsolete responsible-government JE button removed~~

**Fixed in this pass.** The unattached JE button and its orphaned localisation were deleted. The current subject interaction and its existing flavour follow-up event remain the sole responsible-government implementation.

### ~~GP-13 — Resolved (formerly Medium) — displaced BST yields one Oranje frontier victory~~

**Fixed in this pass.** Complete Oranje control of Vrystaat and Drakensberg is now a victory even when BST survives elsewhere. The reward is guarded to fire once, and its event text describes Basotho expulsion from the frontier rather than requiring destruction of the country.

### ~~GP-14 — Resolved (formerly Medium-Low) — Imperial Confederation terminal state is explicit~~

**Fixed in this pass.** Success and failure set a permanent terminal marker and immediately clear runtime globals, participant state, warnings, and JE copies through one helper. Failure-reason variables survive only until `.051` renders and are then cleared. Monthly Imperial Confederation maintenance exits once the terminal marker exists.

### ~~GP-15 — Resolved (formerly Medium) — every Natalia appeal receives its full response window~~

**Fixed in this pass; held-popup and disappearing-recipient regressions remain.** Every eligible Boer player now receives a three-month reply marker. The chain resolves immediately after the final outstanding response, while the Natal monthly pulse acts only as timeout and cancellation safety. Britain can no longer resolve the ultimatum while a valid appeal is still within its answer window.

### ~~GP-16 — Resolved (formerly Medium-High) — Delagoa results remain bound to the actor that qualified~~

**Fixed in this pass; delayed-scope engine regression remains.** Monthly dispatch saves the qualifying route actor before queueing `.010`. The event revalidates that actor's independence, JE, railway, refusal, and trade-through state; acceptance creates one treaty and sends `.020` only to that actor, while refusal changes relations and sets the refusal lock only there. The previous `every_country` result fan-out has been removed. Static scope checks pass; a save/load test across the one-day delayed event should still confirm named-scope retention in engine.

### ~~GP-17 — Resolved (formerly Medium-Low) — Delagoa uses the actual market gateway~~

**Fixed in this pass.** Gateway validity now uses the existing “outside the British imperial network” predicate on Lourenço Marques's market leader. Completion accepts either the Boer actor itself as market leader or transit rights from that leader. Treaty creation and AI treaty helpers skip the self-owner case, so no self-treaty is attempted.

### ~~GP-18 — Resolved (formerly Medium-Low) — MZQ mirrors Vanilla charter setup~~

**Fixed in this pass.** MZQ now receives Vanilla's racialized-subjecthood amendment, extraction charter, Industrialist ideology adjustment, qualifying-overlord IG package, charter laws, extraction strategy, and modifiers. SB's existing territory transfer, company-country link, capital selection, presentation, and additional company slot remain intact.

**Depro's comments:** It should mirror vanilla.

### ~~GP-19 — Resolved (formerly Medium-Low) — progress bars rely on CMF widgets~~

**Fixed in this pass.** The ineffective `gui/journal.gui` and `gui/journal_entry.gui` copies were deleted, and their exact-path inventory entries were removed. Standard and double-sided progress bars now rely exclusively on the required CMF widget injection, eliminating the duplicate-registration path.

### GP-20 — Low — stake-colonial-claim action can expose an empty picker

**Confirmed UX regression.** The override removes Vanilla's top-level “any target state has sufficient interest tier” availability gate (`common/diplomatic_actions/zz_sb_stake_colonial_claim_override.txt:29-79`). Per-state checks remain, so the action can appear available with no selectable state.

### GP-21 — Low — unreachable histories and duplicate John Philip

**Confirmed data drift.** XHG/XHR/XHT country and character histories describe live splits, but all Xhosa land starts under XHO and no creation/ownership path for those tags was found. CAP and PHL histories also create matching John Philip templates, producing duplicate contemporary characters (`common/history/countries/{xhg,xhr,xht}*`; `common/history/characters/{xhg,xhr,xht,cap,phl}*`; `common/history/states/00_states.txt:3503-3512`).

---

## C. Vanilla and third-party compatibility

### ~~CP-01 — Resolved (formerly High; user-assessed release blocker) — political-movement replacements are rebased and dependency-safe~~

**Fixed in the High remediation pass.** The five movement objects with real SB deltas were rebuilt from Community Mod Framework `1.58.2`, itself based on Vanilla `1.13.9`, then limited to the documented CAP creation/disband exclusions and Anglo-African utilitarian eligibility. This restores the Vanilla post-defeat, Meiji, Hungarian, homeland-radicalism, targeting, law-multiplier, and value changes, plus CMF's compatibility ideologies/triggers/multipliers.

The religious-majority replacement was deleted because it had no authored SB delta. The retained object and dependency-baseline hashes are locked in the override inventory, so future Vanilla, CMF, or local drift fails validation instead of silently replacing global mechanics.

**Depro's comments:** This is actually a very high even critical issue... 

### ~~CP-02 — Resolved (formerly High) — treaty history no longer deletes additive third-party files~~

**Fixed in the High remediation pass; cold-start load-order tests remain.** The directory-level `replace_path="common/history/treaties"` was removed. SB still exact-shadows Vanilla's `00_historical_treaties.txt` and loads `sb_treaties.txt`, while uniquely named files from Gates of the Bosphorus, Hail Columbia, and other mods can load additively in either priority order.

Another mod owning the exact `00_historical_treaties.txt` remains a last-writer conflict requiring a compatibility patch; the updated compatibility docs and machine inventory now state that residual boundary explicitly.

### ~~CP-03 — Resolved (formerly Medium) — frontier-colonization override is rebased to 1.13.9~~

**Fixed in this pass.** The replacement now restores Vanilla's Sakoku exclusion, petition/JE enactment weights, and complete 1.13.9 law body. Exact-object review confirms that the only remaining functional delta is SB's Boer eligibility clause; the reviewed object hash is locked in the override inventory.

### ~~CP-04 — Resolved (formerly Medium-Low) — ideology overrides retain only SB deltas~~

**Fixed in this pass.** The redundant Reformer replacement was deleted. Junker is rebased to Vanilla 1.13.9, including Social Monarchy, and retains only SB's Colonial Exploitation and Colonial Resettlement stances. The reviewed object hash is pinned in the override inventory.

### ~~CP-05 — Resolved (formerly Medium) — Highveld selector safeguards restored~~

**Fixed in this pass.** The exact-path file again matches Vanilla's event-validity filters, selector ordering, `position = 0`, and optional interest-group links. The remaining diff is limited to SB's intentional Transvaal state split, Southern Africa geographic selection, and Cape Creole reset behavior; its reviewed hash is locked against Vanilla 1.13.9.

### ~~CP-06 — Resolved (formerly Medium-High) — commander retirement is rebased to Vanilla 1.13.9~~

**Fixed in this pass.** The override now matches the complete Vanilla `1.13.9` `retire_commander` object, including the age-75 AI threshold and current coup path. The sole functional SB delta is a `-1000` AI retirement modifier for commanders owned by BST, preserving the intended historical protection without changing retirement behavior worldwide. An exact object-parity assertion passes after removing that one modifier. Tiger's inherited `golpista_ig` strict-scope warning remains validator/schema noise shared with the Vanilla effect contract.

**Depro's comments:** Okay so there must have been vanilla drift on this since 1.12.x. Originally iirc the issue was vanilla retired historically old commanders like Moshoeshoe so we increased the retirement age to 60. If vanilla is at 75 now, remove this feature. 

### CP-07 — Low / blocked (formerly Medium-Low) — Hail Columbia requires an explicit load order

**Documented compatibility boundary.** Both mods hard-replace `law_legacy_slavery`. The compatibility guide now requires SB to load after Hail Columbia so SB's Boer visibility guard wins. A dedicated compatibility patch remains a Low/blocked TODO; this pass deliberately does not weaken Inboekstelsel behavior.

### ~~CP-08 — Resolved (formerly Medium-High) — override manifests cover the complete live surface~~

**Fixed with QUAL-03.** The canonical inventory includes the previously omitted exact-path files, `STATE_GRIQUALAND_WEST`, `STATE_BECHUANALAND`, and every global keyed replacement. Human compatibility notes disclose full raster, terrain, locator, spline, history, treaty, and keyed-object load-order risks, while the checker prevents either the prose-backed inventory or the live surface from drifting silently. The retired GUI copies and Reformer replacement have since been removed from that surface.

## D. Localization, graphics, map, and presentation

### ~~SUP-01 — Resolved (formerly Medium) — unused STA flag placeholder removed~~

**Fixed in this pass.** The unused STA placeholder block was deleted, removing both references to the nonexistent CoA without changing any live Stellaland flag definition.

**Depros comments:** You can remove this, this was placeholder for stellaland only.

### ~~SUP-02 — Resolved (formerly Medium-Low) — Griqualand annexation description is defined~~

**Verified in this pass.** `sb_griqualand_west.025.oranje_annexation_d` exists exactly once and the event references that exact key. The localisation validator now locks both definition and use. The historical error-log entries predate the key; a fresh launch remains authoritative for presentation.

### SUP-03 — Low — SGO uses an undefined named color

**Confirmed by Tiger.** `common/coat_of_arms/coat_of_arms/sb_countries.txt:484` uses `"dark green"`; the live named-color database has `green_dark`. The opaque textured emblem may mask normal display, but fallback rendering is invalid.

### ~~SUP-04 — Resolved (formerly Medium-Low) — responsible-government lens icons supplied~~

**Fixed in this pass.** Grant, ask, and ask-with-obligation lens icons now reuse `responsible_government.dds` byte-for-byte under their required action IDs. Regression tests lock all three assets to the source icon.

**Depros comments:** reuse diplomatic_action_icons/responsible_government.dds

### SUP-05 — Low / blocked — spline graph repair is release-only compatibility work

**Deferred by explicit user direction.** No spline, route-strip, or graph-connection file was changed in this pass. The isolated errors remain real, but generated spline edits are not composable across map mods; attempting a static repair now would trade a known local defect for cross-mod incompatibility. Recheck and repair this item only against the final release map stack.

**Depro's comments:** This you cannot fix, I've been delaying fixing this bug bc spline changes are not compatible across mods. I will fix it near release. You can mark this as low / blocked. 

### ~~SUP-06 — Resolved (formerly Medium-High) — confirmed split-state hub locators are back on their declared land~~

**Fixed in this pass.** Four confirmed cross-state locators were moved to the corresponding declared hub province: Cape farm 261 to `{ 4535 0 710 }`, Northern Cape farm 262 to `{ 4575 0 751 }`, Cape mine 261 to `{ 4583 0 740 }`, and Northern Cape wood 262 to `{ 4624 0 768 }`. The other generated coordinates were left unchanged rather than guessing at same-state placement. Pixel sampling now places all four corrected coordinates in the exact declared farm/mine/wood hub provinces, and the hub-impassable checker still passes.

### ~~SUP-07 — Resolved (formerly Medium) — intentional Bechuanaland isolation is machine-checked~~

**Resolved as intentional design with a regression guard.** The temporary/WIP comment was replaced with the intended Kalahari-barrier rationale. `tools/map_connectivity_manifest.json` allowlists exactly the three isolated passable Orange River provinces (`x03B0A7`, `x2CC006`, and `x798773`), pins the province raster, and records the full Bechuanaland adjacency graph. The portable validator fails if state membership, passability, hubs, raster, or any additional isolated component changes.

**Depro's comment:** This is by design, such that you have to go through griqualand to get to the other passable states;

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

### ~~TOOL-01 — Resolved (formerly Medium-Low) — resource/live differences are archived and documented~~

**Resolved as an archival/research boundary.** The complete resource workbook, scripts, data, and audit package moved to outer-repository `References/Resource rework/resources/`. The inner `Docs/resource_balance_summary.md` records the methodology and the accepted state-split/balance differences. The live state file is explicitly authoritative; only Transvaal/Orangia gold remains deferred to the next relevant content block.

The archived pipeline currently reports 82 passes and one expected aggregate failure covering accepted live-cap differences:

- Cape Colony: Arable 44→42; Fishing 15→12.
- Northern Cape: Arable 12→6; Fishing 0→3; Iron 21→0; undiscovered Gold 20→0.
- West Transvaal: Wood 0→1; undiscovered Gold 94→0.
- Eastern Transvaal: undiscovered Gold 4→0.
- Transorangia: Wood 0→1; undiscovered Gold 4→0.
- Namaqualand: Arable 2→4.

This non-green result is retained honestly rather than baselined as a release success.

**Depro's comments:* With the exception of the gold in transvaal & orangia these come from balance passes or introduction of new states (griqualand, bechuanaland). Mark the gold issue todo for the next content bloc. Otherwise the resource audit and related docs / tools can be moved into the super folder and removed from the inner repo, just write an executive summary somewhere on how we came to these numbers.

### ~~TOOL-02 — Resolved (formerly Medium-Low) — archived resource validation fails honestly~~

**Fixed in the archived package.** Paths are derived from the archive location, stale command examples were corrected, and the public test command exits nonzero whenever any check fails. Running the current accepted-live mismatch case returns status 1 after reporting 82 passes and one failure; no unconditional success path remains.

### ~~TOOL-03 — Resolved (formerly Low) — archived resource commands use live paths~~

**Fixed while archiving TOOL-01/02.** Both resource READMEs invoke the CLI at its actual `References/Resource rework/resources/scripts/resources.py` location relative to the outer repository.

### ~~TOOL-04 — Resolved (formerly Medium-Low) — release metadata and commands are current~~

**Fixed in this pass.** README and compatibility commands are repository-relative, target strict `1.13.9`, and use the unified validator. Documentation links resolve with the repository's actual capitalization. Metadata now advertises 21 custom journal entries, and stale claims about inner resource validation and SB journal-GUI ownership were removed.

### ~~TOOL-05 — Resolved (formerly Medium-Low) — map validation is consolidated and hash-pinned~~

**Fixed in this pass.** `tools/validate.py` now checks raster membership, unique terrain records, state membership, passable hubs, the exact Bechuanaland isolation allowlist, locator uniqueness, audited coordinate samples, and pinned terrain/locator/spline hashes. The obsolete standalone hub checker was deleted. Semantic `.splnet` inspection remains outside this ticket and `SUP-05` remains the release-map blocker.

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

## F. Runtime performance audit

This pass is structural: recurring work and asymptotic shape are confirmed from script, but no engine wall-time profiler was available. One-shot startup effects, event option effects, and static map loading were not treated as performance defects merely because they are large.

### ~~PERF-01 — Resolved (formerly Critical) — Delagoa maintenance has one global monthly owner~~

**Fixed structurally in this pass; no wall-time profiler was available.** Root-independent Delagoa stale-state repair and actor enrollment remain on `sb_on_monthly_pulse` through `sb_delagoa_route_monthly_open_check`. The duplicate repair, root enrollment, and global `any_country`/`every_country` enrollment block was removed from per-country eastern-sphere housekeeping. The O(N²)-shaped country fan-out is no longer present; genuinely actor-relative AI railway and treaty work remains on the country pulse.

### ~~PERF-02 — Resolved (formerly Critical) — Imperial Confederation monthly maintenance is consolidated and active-gated~~

**Fixed structurally in this pass; no wall-time profiler was available.** GBR country-monthly housekeeping is now the sole recurring owner. After the unlock watchdog, a named phase gate suppresses all recurring work while dormant or terminal; failure is checked first and the active state is revalidated before synchronization. Owner-JE repair now direct-scopes GBR and no longer validates or recounts internally. Involvement validation and subject counting each run once, bar setters consume cached values, and sea-access maintenance runs once.

The duplicate JE monthly pulse was removed; its `immediate` block remains as event-driven initialization with an explicit validate/count/apply order. Distinct failure and sea-access watchdog scans remain because they enforce separate semantics, but the repeated eight-to-nine-pass maintenance path and pre-unlock validation/count scans are gone. `GP-14` remains an independent terminal-cleanup issue rather than a recurring-work owner.

### ~~PERF-03 — Resolved (formerly High) — frontier deployment schedules one origin-bound train per play~~

**Fixed in the High remediation pass; diplomatic-play scope retention needs engine regression testing.** Play start and side join now have distinct handlers, with the join hook limited to membership-sensitive force-floor, frontier-trade/restraint, Natalia-support, and Swazi-muster work. War start is the sole scheduler for one guarded six-event TRN retry train.

The diplomatic-play root owns the TRN-specific marker and is saved into every delayed `.900` event. Events require that exact originating play to retain the marker and be at war; backdown and war end remove it. Direct TRN frontier wars and ORA-led frontier wars are both covered, while side joins, unrelated wars, and stale day-180 events cannot multiply or revive trains.

### ~~PERF-04 — Resolved (formerly Medium) — Firearms modifiers update only across tier boundaries~~

**Fixed structurally in this pass; wall-time profiling remains optional.** Each country caches its applied Firearms tier. Monthly processing changes only the old and new modifiers when progress crosses a boundary; unchanged months return cheaply. JE opening and an annual repair retain the complete rebuild path for desynchronized or migrated state.

### ~~PERF-05 — Resolved (formerly Medium) — monthly handlers have narrow entry gates~~

**Confirmed structure; wall-time unprofiled.** Eleven actions are dispatched from four `on_monthly_pulse_country` registrations. The central router alone sends eight handlers to every country (`common/on_actions/sb_on_actions.txt:56-58`); Cape and Trek handlers are approximately 585 and 564 lines, with dozens of internally gated branches. BST and CAP cleanup add separate 226/109-line handlers.

The clearest concrete case is Namibia: its country handler first calls coastal-access and coast-race helpers for every country (`common/on_actions/sb_namibia_on_actions.txt:1-4`). Coast-race closure is root-independent fixed-province/global state (`common/scripted_effects/sb_namibia_effects.txt:120-128`) yet is repeated N times monthly until closure. Countries with both technologies but no relevant access also repeat state scans indefinitely (`common/scripted_triggers/sb_namibia_triggers.txt:16-34`).

**Fixed structurally in this pass; wall-time profiling remains optional.** Fixed-tag and inactive country handlers now have cheap top-level triggers. Root-independent Namibia coast-race work moved to the singleton monthly pulse, its empty yearly handler was removed, and only actor-relative coastal-access work remains country-scoped. Existing monthly gameplay latency is preserved.

### ~~PERF-06 — Resolved (formerly Medium) — Bechuanaland drift is calculated once per month~~

**Confirmed duplication; exact engine cost needs profiling.** Opening creates a contextless JE for every involved actor (`common/scripted_effects/sb_bechuanaland_corridor_effects.txt:220-226`). Each copy's 253-line `monthly_progress` traverses four treaty/article paths and repeatedly queries relations (`common/scripted_progress_bars/sb_progress_bars.txt:949-1201`). A separate global monthly effect refreshes the same scopes/score and broadcasts the canonical value with an `every_country` scan (`effects:33-145`; `common/on_actions/sb_mineral_discoveries_on_actions.txt:198-207`).

Monthly scope refresh also runs `any_country` and `random_country` with the same SWA-sponsor predicate, including treaty checks, although the sponsor is cached. Opening separately scans all countries for actors that can only be TRN or ORA.

**Fixed structurally in this pass; UI-source regression remains.** The global monthly owner refreshes actor scopes once, evaluates each drift source once, caches source flags, updates GBR's canonical score, and broadcasts one synchronized value. Every contextless JE copy reads the same cached source flags for its localized progress breakdown instead of repeating treaty, relations, territory, and sponsor scans.

### ~~PERF-07 — Resolved (formerly Medium-Low) — stable JE modifier bands are cached~~

**Fixed structurally in this pass.** Zulu dynastic stability, Namibia consolidation, and Cape political balance cache their currently applied tier or band. Unchanged pulses return without rewriting modifiers; boundary crossings remove only the old tier and apply the new one. JE-open/annual repair remains, and Namibia resynchronizes immediately after relevant buttons or ownership changes.

### PERF-08 — Low — Boer restraint scans the world for eight fixed tags

**Confirmed.** Monthly GBR refresh uses `every_country` (`common/scripted_effects/sb_british_boer_restraint_effects.txt:4-75`) although the candidate trigger is exactly ORA/TRN/ZPB/LYD/NAL/SGO/ABY/KLR. It is also called on every play start/join through the shared handler.

**Direction:** direct-scope the eight optional tags. Refresh on relevant war/play/subject transitions and retain only a quarterly or annual GBR watchdog if other systems can overwrite secret goals.

### ~~PERF-09 — Resolved (formerly Medium-Low) — CAP/ABY cleanup is transition-owned~~

**Fixed structurally in this pass.** One idempotent helper owns CAP/ABY autonomy and presentation cleanup. Subject and independence hooks call it immediately; an annual fallback repairs missed transitions. The all-country monthly registration and duplicate Cape-pulse cleanup are gone.

### ~~PERF-10 — Resolved (formerly Medium) — Imperial form validity uses one counted scan~~

**Confirmed structure; GUI evaluation cadence is engine-dependent.** Button validity calls `sb_imperial_confederation_has_two_complete_state_owners` (`common/scripted_buttons/sb_eastern_sphere_buttons.txt:46-56`). The trigger nests `any_country` inside `any_country`, and each candidate evaluates 16 region-ownership predicates (`common/scripted_triggers/sb_eastern_sphere_triggers.txt:298-328`). The GUI binds button validity live.

Related duplication: the bind button evaluates the same “unbound independent participant” trigger twice (`scripted_buttons:12-18`), and JE failure re-runs deep global sea-access/state/treaty checks already maintained monthly.

**Fixed structurally in this pass.** The nested country-within-country query was replaced by one `any_country` scope with `count >= 2`, retaining the existing complete-state-owner predicate without the quadratic scan.

### ~~PERF-11 — Resolved (formerly Medium-Low) — Bechuanaland mutates and broadcasts once~~

**Fixed structurally in this pass.** Canonical score preparation is separate from participant broadcast. Each discrete shift performs one read, one clamped mutation, and one post-mutation broadcast. Crisis participant snapshots are built once at queue initialization and rebuilt only when missing or invalid; stalled retries no longer reconstruct a valid snapshot every pulse.

### PERF-12 — Low — smaller recurring redundancies

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

## G. Comparative hygiene, readability, and auditability

### Method and overall verdict

The comparison sampled equivalent event, JE, effect, trigger, on-action, diplomatic-play, override, documentation, and validation surfaces in Hail Columbia, Gates of the Bosphorus, Morgenröte, and Vanilla 1.13.9. These projects are comparators, not correctness gold standards.

**Current verdict:** Spes Bona retains its strong feature-oriented foundation and is now mechanically auditable across the highest-risk surfaces. The central router is bounded, recurring systems have early gates and cached transitions, the complete override surface is pinned, and validation/documentation are self-enforcing. Remaining gaps are engine regression coverage, broader legacy scope contracts, release-only spline work, and human localisation review rather than an architectural release blocker.

The right conclusion is not a broad rewrite. Preserve the strong naming and feature slices; surgically improve state contracts, router ownership, override containment, and executable validation.

### Quantitative context, not a quality score

For the original audit's common sample surface (`events`, on-actions, scripted effects/triggers, JEs, and scripted buttons):

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
3. **Descriptive intent comments where they exist.** Good examples include the startup handler rationale, the Cape JE design/cross-reference header, Cape button cross-references, and the country-scope explanation in `common/scripted_effects/sb_firearms_effects.txt`.
4. **Optional-scope safety is common.** `c:TAG ?=` and descriptive saved scopes are used more consistently than in many example-mod scripts.
5. **Unusually good audit/research artifacts.** The compatibility manifest, travel-time audit, resource provenance package, map checker, and this evidence-classified issue ledger are stronger governance than the sampled example mods provide.
6. **Localization structure is healthy.** Active English files have correct BOM/header/UTF-8 structure and no internal duplicate keys.
7. **Explicit override naming is directionally good.** `zz_sb_*_override` plus `REPLACE:` is more discoverable than silent generic-name collisions.

### ~~QUAL-01 — Resolved for the agreed scope (formerly Critical maintainability risk) — Bechuanaland lifecycle and scope contracts are explicit~~

**Scope-limited resolution.** The Bechuanaland state machine touched by this pass now documents its authoritative decision, queued-crisis, active-war, and terminal phases; route/lease ownership; required ROOT and saved-scope expectations; transition guards; and cleanup owner. The BC-01 implementation enforces those contracts through live-state predicates, atomic route-specific decision leases, event cancellation/effect guards, queue validation, and terminal cleanup.

This does not claim that every legacy helper in the repository now has a formal contract. Broader ROOT/`PREV`/named-scope documentation, a full transition table, selective queue deduplication, and one idempotent finalizer remain non-blocking maintenance guidance; the independent functional findings below remain open at their recorded severities.

### ~~QUAL-02 — Resolved (formerly Medium-Low) — central on-actions are a bounded router~~

**Fixed in this pass.** `common/on_actions/sb_on_actions.txt` is now a 92-line registrations-only router. Startup, Cape, Boer-story, regional, and diplomatic-play bodies live in feature-owned handler files with their original ordering and cheap entry triggers. The validator requires every registered handler to be defined exactly once and keeps the router below its bounded size.

### ~~QUAL-03 — Resolved for the agreed scope (formerly High) — override policy is mechanically enforced~~

**Fixed in the High remediation pass.** `Docs/compatibility/override_inventory.json` is the canonical review lock for all 35 current exact-path Vanilla collisions, 100 keyed replacement objects, all 17 changed/added state-region blocks, and the empty approved `replace_path` set. Entries record upstream and mod/object hashes, intended delta, global/regional scope, owner, rebase date, and load-order semantics; the five retained movement objects also pin CMF `1.58.2` baselines.

`tools/check_override_inventory.py` fails nonzero on unmanifested/stale surfaces, upstream/mod/dependency hash drift, object-set drift, state-block drift, or descriptor drift. Five mutation tests cover clean, collision, hash, keyed-object, parser, version, and replace-path cases. The human compatibility documents disclose global map and keyed surfaces rather than implying purely regional compatibility.

This resolves mechanical containment, not every broad override's design quality; narrower open CP/QUAL findings remain independently tracked.

### ~~QUAL-04 — Resolved (formerly Medium) — one portable validation and CI gate~~

**Fixed in this pass.** `tools/validate.py` is a repository-relative, non-writing Python-standard-library gate for unit tests, overrides, map connectivity, localisation, on-action routing, stale symbols, and delayed-event lifecycle. Vanilla/CMF comparison and Tiger are optional and report `SKIP` when proprietary dependencies are absent; `.github/workflows/validate.yml` runs the portable subset in CI. The archived resource-research package has its own honest nonzero test command rather than being baselined into the release gate. README and compatibility instructions target strict 1.13.9 and the unified command.

### ~~QUAL-05 — Resolved for the agreed scope (formerly Medium-Low) — three duplicated transitions are centralized~~

**Fixed within the explicitly selected scope.** The four Bechuanaland crisis queues share one initializer, Transvaal Unity progress and completion use one readiness predicate, and the three stable modifier ladders use the cached transitions recorded under `PERF-07`. Treaty normalization and diplomatic-play boilerplate were deliberately left untouched; this ticket does not claim repository-wide deduplication.

### QUAL-06 — Low — dead/retired scaffolding and manual archaeology remain in the active tree

Strong candidates include the 677-line uncalled treaty normalizer, deprecated definition-only migration effect, definition-only economy/commandant/Delagoa helpers, disabled country blocks in `sb_on_actions.txt:201-252`, and `always = no` references used to suppress orphan diagnostics. Current issue sections list additional unused assets/localization.

Do not delete every definition-only symbol blindly: save compatibility, scripted API use, and intended migration helpers must be reviewed first.

**Best practice:** commit an allowlisted unused-symbol report that distinguishes public/save/migration API from accidental dead code. Remove decided code rather than commenting it out; let Git carry history.

### QUAL-07 — Low — comment quality and terminology are uneven

The strongest comments explain why; several complex feature files still have sparse scope/invariant commentary, especially Bechuanaland, Eastern Sphere, Namibia, and Griqualand West. Other comments are stale or understate their override delta. The central on-action header itself was corrected during `QUAL-02`.

Persistent/saved-scope names are mostly descriptive in new code, but generic legacy names (`ig`, `britain`, `migration_target`) and stable typos reduce searchability. Do not rename stable keys casually; register/deprecate aliases when cleanup is justified.

**Best practice:** add concise scope/invariant/ownership comments, not syntax narration. Require every hard override comment to state the exact Vanilla delta.

### ~~QUAL-08 — Resolved (formerly Medium) — every delayed dispatch is classified and lifecycle-checked~~

**Fixed for the audited surface in this pass.** `tools/delayed_event_lifecycle_manifest.json` classifies all 365 current delayed dispatches and 205 unique destinations as interactive, pending-state, mechanical-finalizer, or narrative. Interactive/pending routes document their lease marker, destination revalidation, cancellation, idempotence, and centralized cleanup; explicit exceptions carry rationale. The validator pins the duplicate-preserving dispatch fingerprint and fails on any unclassified, duplicated, stale, or changed route. The touched Xhosa, CQF, Natalia, Warren, and Martinus chains received the concrete lifecycle repairs recorded above.

### QUAL-09 — Low / deferred (formerly Medium-Low) — substantive localisation review remains human-owned

**Structural fix completed.** The validator checks UTF-8/BOM state, headers, final newlines, trailing and leading whitespace, duplicate and missing keys, review-marker placement, and exactly one review classification per scripted event. Current coverage is printed as `89 reviewed / 131 to review`, and event scripts may no longer contain review markers.

Substantive proofreading remains intentionally deferred to Depro's rolling in-game pass and is therefore tracked as Low rather than represented as machine-complete.

### Comparator-specific lessons

#### Hail Columbia

- **SB advantage:** stronger feature naming, smaller median core files, explicit compatibility/issue documentation, and more feature-aligned effect/trigger slices.
- **HC advantage:** selective parameter helpers (`$AMOUNT$`, `$MULT$`, `$RADICALS$`), three scripted gameplay tests, and a mature changelog. SB's central router is now smaller and registrations-only, so router size is no longer an HC advantage.
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

SB is **readable at the feature/file level and mechanically auditable across its highest-risk lifecycle, override, map, localisation, and routing surfaces**. Engine-only outcomes still require the recorded gameplay matrix. Relative position:

- **Better than Morgenröte** on granularity, naming, and documentation.
- **Usually better than GotB** on local feature readability and governance, while GotB has some stronger scope-contract/router patterns.
- **Comparable to HC**, with SB ahead on explicit governance, naming, feature topology, and the bounded central router; HC still has more committed gameplay tests and selective parameter reuse.
- **Near Vanilla norms for event/JE size**, with delayed-event classification and rebase discipline now mechanically enforced for the audited surface.

### Maintainability priority order

1. Run the recorded fresh-start and engine-only regression matrices.
2. Finish the release-only spline repair after the final map/mod stack is frozen.
3. Complete rolling human localisation review and the Hail Columbia compatibility patch.
4. Use the enforced inventory to rebase or upstream any remaining broad global overrides.
5. Extend explicit scope/lifecycle contracts beyond the currently classified delayed-event and Bechuanaland surfaces.
6. Triage dead code with a save/API allowlist, then remove decided scaffolding.

---

## H. Suspicions and explicit runtime test queue

These were not promoted to confirmed defects:

1. Cape `.200` can carve Albany from any current Eastern Cape owner after the delayed London response; this may be intentional robustness.
2. Delayed Natalia backer events retain `scope:natalia` with minimal life checks; test NAL death during the 5-8 day delay.
3. Vanilla history still attempts the dormant SAF subject and GBR protect-TRN secret goal; test whether dead scopes create ghost diplomacy.
4. Firearms localization says access/industry must be continuous for 24 months, while JE progress only increments and never resets; clarify cumulative versus continuous intent.
5. `sb_revoke_oranje_griqualand_claim` can remain valid if ORA disappears midwar but may enforce nothing without the TRN federation marker.
6. MZQ territory transfer is direct-owner-only and does not collect land held by subordinate administrations; confirm this is intended.
7. The SGO restraint patch cannot cancel a transfer-subject play already started before the next monthly refresh.
8. Highest-value Bechuanaland runtime scenarios are the resolved BC-01/02/03/04/05/07/08/09/10/11/12/13/14/15/16/18/19/21/23/24 matrices: test all four direct/proxy Warren and Caprivi routes, support versus neutrality, backdown, white peace, mixed goal enforcement, held response popups, sponsor demotion, SWA transfer/security alignment, British/third-party SGO subject changes, landed TSW hierarchy, SGO creation through TRN and ORA, and presidential/confederal backers.
9. Hold and save/reload the one-day Delagoa `.010` delay while multiple actors qualify to confirm the saved `sb_delagoa_actor_scope` remains bound to the dispatching actor.

---

## Validation results and noise separation

### Passed

- `python3 -B tools/validate.py`: all eight portable categories pass, including unit tests, local override inventory, map data, localisation, on-action routing, stale symbols, delayed-event lifecycle, and the dependency-optional override comparison.
- `python3 -B -m unittest discover -s tests -v`: all 18 override, validator, and Medium-Low contract regressions pass.
- The override inventory validates 35 exact-path files, 100 keyed overrides, 17 changed state-region blocks, and zero `replace_path` directives.
- The delayed-event lifecycle manifest classifies all 365 dispatches and 205 destinations with zero unclassified or stale entries.
- Map validation covers state/raster/terrain membership, passable hubs, the exact Bechuanaland isolation allowlist, locator uniqueness and audited coordinates, plus pinned terrain, locator, and spline hashes.
- Localisation validation reports 89 reviewed and 131 to-review event blocks, with one classification per event and no review markers in event scripts.
- The central on-action router is 92 lines and every registered handler is defined exactly once.
- The three responsible-government lens icons are byte-identical to their source asset; the Griqualand annexation key is uniquely defined and referenced.
- The archived resource test is repository-relative and honest: it reports 82 passes and one accepted live-cap mismatch failure, then exits nonzero.
- Tiger reports `fatal: 0`, `error: 65`, and `warning: 59`; review found no new Medium-Low authored parser error. The remaining diagnostics are the known 1.13.9-schema and dependency limitations summarized below.
- No spline semantic data was edited; `SUP-05` remains intentionally deferred to the final release map stack.

### Outstanding or diagnostic

- A fresh 1.13.9 launch was not performed in this remediation run. Cold-start logs and the targeted gameplay matrices remain authoritative for engine-only behavior.
- The locally installed CMF is `1.55.1`, while the dependency inventory is pinned to required `1.58.2`; dependency-baseline comparison is therefore skipped rather than accepting stale CMF hashes.
- The archived resource package intentionally remains non-green until its accepted live-cap rows are resynchronized; it is research evidence, not an inner release-gate baseline.
- The previous `--unused` Tiger report remains historical diagnostic context; unrelated unused-content cleanup is not part of this remediation.

### Known validator/dependency noise

- All 16 Tiger `seal_and_signature_texture` errors are 1.13.5 schema lag; the field is widespread in Vanilla 1.13.9.
- The commander override now matches Vanilla `1.13.9`, but Tiger follows `character_execute_immediate_coup` into a scripted effect that expects `scope:golpista_ig`; Vanilla no longer initializes that scope in this interaction. The warning is inherited contract/schema noise, not an SB delta.
- The three rebased movement files intentionally reproduce CMF `1.58.2` integration ideologies, compatibility triggers, and multipliers for optional companion mods. Tiger does not load/model every companion definition and also rejects CMF/Vanilla `days_since_movement_defeated`; the reported symbols and one-item `OR` warnings are dependency-source-equivalent content after line-end normalization, not authored SB deltas.
- Tiger's military-formation warnings occur on Vanilla-identical lines outside the POR diff.
- `IsDoubleSidedRyukyu`, movement-owner, slavery-ideology, and several lobby-scope warnings reproduce Vanilla syntax.
- CMF supplies `gui/com_journal_injects/injects.gui`; Tiger's missing-CMF GUI warning is false in the declared dependency setup.
- The two `--unused` untidy groups are pre-existing unused DDS/localization findings; the DDS group also descends into the ignored `.claude/worktrees` copy. Neither identifies an authored High-remediation script regression.
- CMF duplicate-effect on-action warnings, save-deserialization invalid-date errors, and old treaty-article log lines were not attributed to current SB scripting.

## Suggested triage order

Each numbered line is intended as a separate, reviewable remediation batch.

### Completed Medium-High pass

`BC-08`, `BC-10`, `BC-13`, `BC-16`, `GP-08`, `GP-16`, `CP-06`, and `SUP-06` are resolved. `SUP-05` is deferred to the final release map stack and tracked below as Low/blocked.

### Completed Medium pass

`BC-04`, `BC-15`, `BC-18`, `BC-19`, `BC-21`, `BC-24`, `GP-07`, `GP-11`, `GP-12`, `GP-13`, `GP-15`, `CP-03`, `CP-05`, `SUP-01`, `SUP-07`, `PERF-04`, `PERF-05`, `PERF-06`, `PERF-10`, `QUAL-04`, and `QUAL-08` are resolved. Runtime-sensitive entries retain explicit engine-regression notes in their sections.

### Completed Medium-Low pass

`BC-14`, `GP-09`, `GP-10`, `GP-14`, `GP-17`, `GP-18`, `GP-19`, `CP-04`, `SUP-02`, `SUP-04`, `TOOL-01`, `TOOL-02`, `TOOL-04`, `TOOL-05`, `PERF-07`, `PERF-09`, `PERF-11`, `QUAL-02`, and `QUAL-05` are resolved. `BC-20`, `BC-22`, `CP-07`, and `QUAL-09` received their safe immediate fixes and are now Low/blocked or Low/deferred. `TOOL-03` was resolved as part of the resource archive move.

### Low / blocked batches

1. Deferred human/compatibility/policy work (`BC-20`, `BC-22`, `CP-07`, `QUAL-09`).
2. Minor gameplay, fallback-art, UI, and localization cleanup (`GP-20`, `GP-21`, `SUP-03`, `SUP-08`, `SUP-09`).
3. Release-map-only spline and graph repair after the final mod stack is frozen (`SUP-05`).
4. Documentation, bounded performance, dead-code, and comment cleanup (`TOOL-06`, `TOOL-07`, `PERF-08`, `PERF-12`, `QUAL-06`, `QUAL-07`).

5. Run the resolved Critical/Very High/High/Medium-High/Medium/Medium-Low engine regression matrices before release; do not mix those regressions into a remediation batch.

---
