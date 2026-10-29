## Cape revolutions and Vanilla colonial collapse (29 October 2026)

- `southern_africa_subject_var` also admits Vanilla's monthly `colonial_administration_events.2` (The Severed Limb) after independence. Its majority-rule option `.b` adds cultures present in the capital that have a homeland there, then removes European primary cultures. With the Cape's homelands, this produces Cape Malay, Cape Creole and Nama while removing Anglo-African; it is separate from SB's liberal victory, which only adds Cape Creole.
- Same-playthrough saves show British colony CAP 732 with only Anglo-African in December 1842, January 1849 and January 1852. All January–May 1857 autosaves instead have CAP 16777796, the three replacement cultures, `colonial_collapse_var`, no British subject pact and a successful-revolution catalyst dated 21 March 1854. Its initial law records date to 18 July 1853. The retained outcome supports the Vanilla majority-rule route, but does not preserve the initiating movement or the exact colonial-collapse choice date.
- Do not assume the independence/yearly marker cleanup protects a revolutionary successor or an already-open Vanilla event. Investigate inheritance and event delivery separately before changing those hooks; these checkpoints do not establish precisely why cleanup did not prevent this outcome. See the [save investigation and preserved evidence](Docs/compatibility/cape_colonial_collapse_2026_10_29.md), tracked as `PT-20261029-01`. This investigation changed no gameplay scripts or saves.

## Rival recruitment and recognition share the same unpledged pool (29 October 2026)

- Recognition assigns roughly half the incumbent's supporting house prominence to the chosen heir. If a story also promises an unpledged backer to the other brother, reserve that named house before applying recognition; otherwise the ordinary transfer can consume it and silently prevent the promised rival backing. Future-successor pledges are separate from present allegiance and constitutional alignment. Reuse the actual appointment/backing helper, preserve existing promises, and count outside backers rather than the prince's own prominence when testing whether he already has support.
- Coming-of-age choices need a receipt before trait/heir callbacks, with cancellation and cleanup if either son dies, renounces or the ruler/heir changes while the popup is open. The existing first-adult check prevents a later accession from replaying the birthday. Source execution covers both choices, existing heirs/backers, no available house, stale participants and foreign ROOT; monthly timing, cancellation and portraits remain pending DP.

## AI recognition needs a continuing eligibility check (29 October 2026)

- A positive JE button weight and equally weighted candidate options let the AI repeatedly redesignate an heir. Apply ruler-specific AI rules both to button willingness and the shared candidate check used during selection and final payment. Dingane must not use recognition; Mpande may use it only without a living recognised heir, selecting Cetshwayo or Mbuyazi at 66:33. Weight the character identity rather than the prominence-ranked slot, and remove the cancellation weight while an eligible son is available. Preserve human recognition and other rulers. Source execution checks cover all twelve slots, repeat payment, dead/renounced candidates and foreign preview scopes; native AI scheduling and observed choice frequency still await DP.

## AI faction choices and post-war consolidation (29 October 2026)

- Event weights alone do not make an AI side choice work: the claimant answer helper still restricted faction inversion to `is_player = yes`. Allow the same chosen-side receipt for both controllers, then test the actual installed rulers and absence of player switching. Compare the frozen coalition totals displayed in the event; equal totals favour the incumbent.
- Prerogative follows the contender, not the original/rebel country. DP clarified that the incumbent retains the pre-split value and the challenging prince starts at zero: backing Mpande therefore puts zero P in the main country and Dingane's existing P in the rebels. Transfer the original value before resetting the claimant's actual country; test both assignments under AI and human control. For the actual victor, reserve the 18-month low-Prerogative challenge cooldown before cleanup, ruler callbacks and notification; waiting for the +10 acknowledgement reward leaves an opening for immediate retriggering. Duplicate callbacks must neither reset Prerogative nor refresh the cooldown. Death/retirement succession and player-initiated coercion keep their own rules. Source checks cover both side choices and both winners; runtime timing remains pending DP.

## Lasting campaign outcomes versus temporary AI context (29 October 2026)

- The Swazi campaign clears `sb_zulu_swazi_ai_lost_blood_river_var` when its offer is answered. Later consequences must use a lasting country outcome, not that presentation/AI-context flag or the shared result marker (which also covers victory and white peace). Blood River's defeat option now records its own defeat flag and costs 25 P; a later Swazi defeat uses that flag for 50 P instead of 30. Keep the tooltip and applied branch consistent, and test context cleanup, other prior outcomes, foreign ROOT and repeated acknowledgement. Native delivery remains a DP check.

## Movement history creation can hide stale eligibility (29 October 2026)

- A movement present from country history does not prove its natural creation conditions match the starting laws. CAP's Liberal Movement was created directly at startup, but its creation trigger accepted only Racial Segregation while CAP actually began with Subjecthood. Check both paths when changing starting laws. The repair admits either law only during the active, unresolved Cape politics contest; it does not change recruitment or force-disband existing movements. Focused tests evaluate the shipped gate, including other countries, other citizenship laws and closed/resolved contests. Native recreation and absence of duplicates still require engine verification.

## AI coercion targets and preview scope collisions (28 October 2026)

- An interaction with generic eligible-prince targeting can make AI Mpande remove either son's future claim. DP's historical-mode exception now excludes Cetshwayo and Mbuyazi while AI Mpande rules, retaining Gqugqu as a target. Put the rule in the shared target check so both selection and a stale popup's resolution respect it; leave human control, Off, other rulers and war outcomes alone. This prevents future coercion without rewriting an existing renunciation. [Replay evidence](Docs/zulu_heirs_preview_followup_2026_10_28.md).
- A temporary saved scope cannot reuse an existing permanent event/JE target name. The successor preview's `save_temporary_scope_as = sb_court_country` caused 864 hover errors. For this country-owned list check, compare the candidate's home with the iterator's `prev` country instead; do not mutate the permanent target or assume it is the displayed court. Test with a deliberately foreign permanent target and both empty/eligible candidate lists. Native hover replay is still required.

## Claimant eligibility and shared terminal receipts (28 October 2026)

- A missing candidate is not necessarily a missing character. Check identity, adulthood, renunciation and retirement before repairing the roster. Cetshwayo survives in all five September 1851–January 1852 saves with a renounced claim and a renunciation cooldown; the candidate filter correctly excludes him. A cooldown's expiry does not undo a successfully renounced claim. Do not reset that outcome as a presentation fix.
- Shared terminal flags prove resolution, not which event resolved it. Klip River's departure helper clears intermediate markers and is reached by Natal ratification, invalid-setup fallback and later outcomes. Those flags cannot prove a particular AI choice or a civil-war ownership race. Record the ambiguity and seek a pre-resolution checkpoint before changing routing. [Evidence](Docs/zulu_court_save_followup_2026_10_28.md).
- AI supply assistance belongs to the actual two countries of the tracked war, not a hard-coded ZUL tag or the organising movement. Remove it on end/cancellation and recheck player control through the existing reconciliation. Static scope checks do not establish that a supply reduction cures native attack behaviour.

## Weighted episode destinations and later war goals (28 October 2026)

- Changing an opening counter-demand does not stop later additions. Restrict the requested goal in both selection and validity, scoped to the exact authored play and holder/target; keep launch admission separate from unrelated plays. Preserve recovery of the originally attacked state so native territorial mirrors remain usable. Copy the effective CMF definition and test that only the documented guard differs; do not erase all territorial demands on a recurring pulse. Native AI selection and timer reversal still require DP replay.
- A Popularity-weighted prince draw should reuse the established attraction curve, preserve integer weight precision and exclude an already selected alternative. Freeze the result at episode preparation; do not reroll existing patrons or the destination when a player clicks. If every eligible weight is zero, define the fallback explicitly rather than leaving blank participants. Source tests integrate the actual reservoir branches and exercise foreign ROOT, zero weights and stale popups.
- Repeated assistance pulses must not remobilise an already mobilised formation. Use the verified native `is_mobilized` trigger alongside `is_army`; keep actual engine eligibility distinct from the script's source tests.

## Dynastic-war inheritance and native victory penalties (28 October 2026)

- A rebel sharing ZUL's definition does not inherit the original country's active Firearms JE or its supply counter. Copy completion or progress explicitly at the actual split, before the JE's immediate can seed a fresh counter. Copy no completed reward, then allow each market to earn its own weeks. Do not initialise country JEs in the earlier inherited-law callback, before the rebel has land/AI.
- Native ideological victory applies `revolution_lost_ig` (−100% Political Strength, decaying over twenty years). A personal claimant contest can therefore crush four IGs despite both sides restoring Monarchy and correctly removing SB's temporary Approval penalty. Record pre-existing penalties before creation, copy that record by IG type, and remove only new penalties from the actual winner after native application. Preserve unrelated modifiers/earlier penalties; do not promise identical pre-war Clout after intentional character deaths. Cancellation or a missing snapshot is not permission to erase a penalty. [Evidence](Docs/compatibility/zulu_contested_crown_2026_10_27.md).
- A guaranteed barracks floor changes the final military shares. Reserve it from the existing total, round one side and give the other the remainder, then divide military workforce by those actual integer quotas. Using the old raw coalition share for staff defeats the floor's purpose. Four barracks at 177:334 now give 2:2 and 50:50 staffing; conscription limits and native recruitment remain separate runtime checks.
- Put the +10 victory reward in the acknowledgement option with a consumed receipt, not the event's launch or war callback. Test repeated callbacks, repeated acknowledgement, both actual winners, foreign ROOT and the upper clamp.

## Missing event GUI windows can crash rather than fall back (28 October 2026)

- Validate `gui_window` against actual installed `gui/eventwindow.gui` names. Invented `event_window_char` in the claimant victory notification reaches `CEventWindow::Setup` with no widget and crashes; Vanilla's single-character template is `event_window_1char_tabloid`, using `left_icon`. Successful script parsing and outcome arithmetic do not check this presentation contract. Keep a native-window regression for the succession events. Engine replay remains necessary.
- The same-country transfer guard applies at reunification as well as the initial split. Restore each survivor's political records, but only call `transfer_character` when their current owner differs from the actual winner. Preserve transfers out of the disappearing defeated country. Do not infer that other nearby assertions caused a crash when the fatal stack and final missing-widget message identify the popup. [Evidence and replay status](Docs/compatibility/zulu_contested_crown_2026_10_27.md).

## Military building levels are not staffed armies (28 October 2026)

- Successful native creation and correct rebuilding quotas do not establish usable force division. The replay gives Gqugqu three Natal barracks but zero battalion manpower, one serviceman and no officers; eleven requested conscription levels are absent. Inspect military Pop workforce/dependants, actual building levels and unit manpower separately. Native conscription limits still depend on civilian population/rate; relocating military households does not bypass them.
- For the approved claimant experiment, count each profession's workforce across both real factions before deleting workplaces; move only the surplus with `move_partial_pop`, once under the existing rebuild receipt. This preserves people and moves their dependants rather than creating soldiers or converting civilians. Native hiring, rounding and training remain engine checks. Both professions have Vanilla's `unemployment = yes`, allowing the native move to retain their profession; do not assume every Pop profession behaves alike.
- Determine the stronger homeland from frozen contender backing and the selected side, not from the original/rebel tag or live post-split prominence. Use native state weights before its territorial proposal; zero protects a loyalist state. Retain one-state behaviour and CMF hooks. An already-organising saved war will retain the old proposal; source tests do not prove engine allocation. [Observed deviation and current trial](Docs/compatibility/zulu_contested_crown_2026_10_27.md).

## Recruitment preparation and final faction quotas have different timing (28 October 2026)

- A post-split rebuild cannot rescue native creation rejected for absent rebel forces. In the approved destructive claimant experiment, relocate an existing recruitment level into empty states before creating the movement, retaining at least one level in each donor and conserving regular/conscript totals separately. Do not assume which state will rebel; keep final coalition quotas tied to the actual countries after splitting. Never manufacture levels when the available pool cannot cover all states.
- Reserve preparation once per answered episode, scope it to the actual court and read the donor's level/training before removal. Do not rebuild every weekly poll or silently undo the move on cancellation. Disclose the immediate unit reset as well as the later rebuild. Source tests establish level conservation and callback ordering; DP must still verify native unit registration, conscription caps, staffing and creation. Existing failed-start cooldowns are not removed by changing source.

## Native failed-start dates distinguish allocation failure from missing eligibility (28 October 2026)

- Inspect a movement's `last_failed_civil_war_start_date` before increasing activism or changing sponsors again. In installed 1.14.5, native creation records this after a proposal has no uprising states or, for a revolution, no army units/conscription capacity. The three-month failed-start cooldown then blocks retries even at 100% activism. A recorded failure proves an attempted creation, not a successful war or a particular sponsor. The rejected state proposal is not retained in the inspected saves; label an inferred empty-army allocation accordingly.
- A military rebuild after actual rebel creation cannot satisfy this earlier army requirement. Keep pre-creation eligibility, territorial allocation and post-split redistribution separate in diagnosis and testing. The June–August all-IG replay establishes the cooldown and concentrated military geography, but not a working cure. [Evidence](Docs/compatibility/zulu_contested_crown_2026_10_27.md).

## Broadening claimant sponsorship requires matching cleanup (28 October 2026)

- DP's all-IG trial supersedes the AF-only filter. Change both `can_pressure_interest_group` and `revolution.interest_group_can_join`, and broaden country-scoped package application, rebel penalty retention and cleanup together. Every-group iteration must use the actual crisis country, not a foreign event root. Test all groups before/after selection, repeated polls, both actual winners and cancellation. Opening `.990` only reserves the choice; the cost belongs to the `.004.a/b` choice effects. These checks establish script scope and cleanup, not native sponsorship or war creation.

## Preferred demand is not proof of complete revolution eligibility (28 October 2026)

- The February/March 1840 replay has a verified Contested Crown demand, 100% activism and over 13% AF internal backing, but still no native war. Earlier evidence that the approved current law permits a preferred replacement establishes demand calculation only; it cannot rule out the stance change elsewhere in native creation. DP requested restoring strong opposition as a controlled trial. Retain other tuning, record the old/new source and require runtime evidence rather than claiming the arithmetic tests prove a fix. The shared crisis ideology also affects the AF package; leave ordinary leader ideologies intact and disclose possible native compatibility limits. [Current trial and save evidence](Docs/compatibility/zulu_contested_crown_2026_10_27.md).

## Manual console events can collide with the simulation's random access (28 October 2026)

- The 11:51 claimant test crashed in native harvest-condition processing while the console's `event` wrapper tried to acquire global random access. The wrapper acquires it before dispatching the event; adding a guard inside the SB event cannot protect that operation. Distinguish this signature from inherited-law/rebel-creation crashes and from the scripted first-fruits event. Pause and wait for the date to stop advancing before manual test-event calls. This workaround awaits DP replay; do not report an engine fix or blame the latest movement modifier without evidence. [Crash evidence and limits](Docs/compatibility/zulu_claimant_console_crash_2026_10_28.md).

## An approved current law can still have a preferred replacement (28 October 2026)

- The movement stance display alone does not establish that it has no demand. Installed `CalcMostDesiredLawToEnact` compares the eligible candidate law with the active law and accepts a strictly higher stance. In the September 1839 claimant save, the script's actual-demand check verifies Contested Crown despite both royal laws appearing in the approving column. Do not infer the cause of a missing revolution from the thumb-up icon or undo sponsor compatibility without checking the actual desired law. Native creation still has separate eligibility gates; this investigation does not establish its remaining refusal.
- A crisis-only attraction modifier increases recruitment over time; it is not a direct support assignment, IG sponsorship bypass or coalition-strength bonus. Reuse the existing mobilisation modifier so weekly polling cannot stack the boost and existing cancellation/resolution cleanup removes it. Source scope/cleanup checks do not prove that the next native war will form. [Two-save evidence and pending trial](Docs/compatibility/zulu_claimant_demand_attraction_2026_10_28.md).

## Pressure labels, recruitment and approved military resets (28 October 2026)

- An IG absent from the pressured/influencing list is not necessarily barred from sponsoring a revolution. Installed 1.14.5 uses 10% internal backing for influence, with three slots and retention preference, but 5% for revolutionary sponsorship; the latter scans all IGs. The latest AF has 6.338% and −20 Approval. Correct the claimant movement's blanket `can_pressure_interest_group = { always = no }` to AF-only eligibility, but do not claim that this proves why its native war failed to start. Exact refusal remains unresolved; [bounded evidence](Docs/compatibility/zulu_claimant_rebuild_2026_10_28.md).
- Copying Absolutist recruitment also copied allegiance to the incumbent: a disliked king reduced his rival's recruitment. A personal claimant movement must read the named claimant's Popularity. Source tests prove independence from incumbent Popularity and preserve the inherited bounds; native support growth/war creation still needs replay.
- DP expressly approved the destructive army experiment. Count completed recruitment levels across both actual countries before deleting either side's buildings, reserve the reset once, and conserve separate regular/conscript totals after rounding. Use faction identities rather than presumed rebel geography. Native building recreation produces new units in a default formation; it does not preserve manpower, experience or composition. Conscription caps and staffing remain native and must be measured after the next updates. Source conservation is not engine military acceptance; keep automatic challenges off.

## Explicit sponsorship, approval pressure and military relocation are separate (28 October 2026)

- Applying an IG ideology/Approval modifier does not make it the exclusive sponsor. Use the movement's native `revolution.interest_group_can_join` restriction for AF-only claimant wars; this is an additional filter, not a bypass of native backing or stance checks. The new −20 package cannot be described as forcing every possible AF leader to rebel. Royalist/neutral compatibility is covered; an anti-monarchical leader or insufficient internal support can still prevent creation. Keep leader ideologies intact and test actual native sponsorship after a full restart.
- `transfer_to_formation` is a character effect, not a battalion transfer. Installed `create_building` only increases existing levels, so it cannot reduce an over-allocated military building. Removal/recreation destroys the old unit records and is not a lossless army redistribution. Obtain the design decision about that reset before using it; do not assume an observed rebel state is guaranteed in future splits. A source arithmetic test cannot prove manpower/experience retention or native conscription behaviour.
- Rehoming a frozen character cohort must skip anyone already in the intended country. The native split may already have placed some actors correctly; an unconditional transfer produces the observed same-country script error. Both side choices now exercise this check.

## Claimant territorial targets do not divide concentrated armies (28 October 2026)

- The June–August 1839 replay preserves the 177:334 house quote and correctly inverts the rebel target to 34.638% when backing Gqugqu. Nevertheless, the native uprising plan assigns the whole Zululand state, all four regular battalions and all seventeen conscription records to Dingane's rebels; Gqugqu retains Natal with no military buildings or units. The plan predates country creation and SB character transfers. Native army setup collects units from the receiving country's military buildings. Do not treat a territorial fraction, correct named commanders or source arithmetic as evidence of a proportional military split. The military release criterion has failed this observed case; automatic activation stays off. [Save investigation](Docs/compatibility/zulu_claimant_allocation_investigation_2026_10_28.md).
- Check the actual native sponsor, not just the intended package. This replay's war was sponsored by the tiny Intelligentsia, with one movement supporter; Landowners remained Happy and below 5% internal movement backing. In the stalled replay the intended sponsor still fails both gates. Approval/ideology pressure does not create the required population support, and national IG clout is not the percentage of that IG supporting the movement.
- A live script reload can leave new database objects absent. The log names the missing Landowner modifier; the saved IG has an unnamed modifier and +9 Approval despite the intended −30 package. Current valid files on disk do not prove the running process loaded them. Validate changed database definitions after a full process restart from a pre-crisis checkpoint, and distinguish that loading fault from the independent backing/allocation problems. Saved ideology names alone cannot reconstruct every in-memory stance during a partial reload.

## Native civil-war lists belong to the origin country (27 October 2026)

- The completed April 1840 claimant split left a generated rebel king and no SB crisis record. The handoff tested `any_civil_war` inside the rebel country; the installed `CScopeCivilWarListBuilder` calls `CollectCivilWarsForOriginCountry`, so that test could never match. The subsequent cancellation erased the pending record. Match the callback's actual rebel country through `civil_war_origin_country` and Vanilla's `civil_war_type_var`, then select the exact recorded movement's war from the original country. Persist that original country on both sides: monthly validation in the rebels must query the origin's list too. Test fixtures must supply the rebel's empty war list, not an invented copy of the origin's list.
- Making an agitator the movement leader does not install the country's ruler. On the ready-country callback, route the frozen factions, install each named contender and remove generated ruler/heir placeholders absent from the pre-split cast. Install before killing placeholders to avoid another vacant-throne succession. Preserve authored princes and children, guard recursive ruler-selection callbacks, and retain the owned `no_heirs` policy throughout the war even when a faction contains only one dynast.
- A player-side inversion also inverts the opposition's territorial fraction. Keep frozen contender identities separate from original/rebel country identities, and resolve coalition casualties by the actual winning contender. Source checks cover both choices, both winners, generated and authored heirs, monthly validation and late native ruler replacement. Native replay remains pending; the completed pre-fix split proves creation, not correct assignment or military scaling. [Evidence and current handoff](Docs/compatibility/zulu_contested_crown_2026_10_27.md).

## Annual allegiance must not make claimants withdraw from themselves (27 October 2026)

- The 1 June 1838 observation save retained Gqugqu's candidacy and supporters but replaced his Claimant card with Uncommitted. The February checkpoint records his annual transition away from self-endorsement; this also removed the card's +25 Prominence. Exclude dynastic candidates from both the annual allegiance roll and its commit loop. Skipping only the roll leaves an absent new patron which the commit step can misread as withdrawal. Keep candidates in the patron pools so ordinary houses can still join them, and preserve a prince's authored support for his father.
- Source-executed regressions force withdrawal and verify candidate cards, Prominence and commitments survive while ordinary houses still withdraw or join. No save repair is applied; replay before the annual transition to verify the prevention in-engine.

## Claimant characters must survive the actual country lifecycle (27 October 2026)

- A character scope/list preserves an identity reference, not its life. Native country removal kills characters still belonging to the abolished country. Keep a distinct pre-split cast list, copy it to both actual sides, and rehome living survivors in the verified victory callback before country cleanup. Include minors and unrepresented advisers; the live adult coalition projection is not a complete cast archive. Do not reconstruct characters who genuinely died.
- Freeze which characters belong to each side separately from aggregate Prominence. House members count through their representative numerically, but all recorded members face the agreed faction outcome. Third-party princes and uncommitted characters must not be swept into the losing faction by native geography or IG membership.
- An endorsement of `1` means that character's current incumbent. Save the incumbent's identity before the split and rebase against the real winner after restoring political records; otherwise restoring a raw number can silently turn an old allegiance into loyalty to the victor. Preserve future-successor pledges separately.
- An agitator role alone does not name a movement. The installed manager selects the best valid character-support weight; restrict the claimant movement to the recorded prince and wait for his actual movement link before scripted advancement. Preserve existing ideology and undo only roles added by this crisis. Static tests supply native assignment/split/end callbacks; engine attachment, survivor-transfer timing and all allocation trials still require DP.

## Law activation during country creation is not a ready-country callback (27 October 2026)

- The two claimant-war crash stacks reach `add_journal_entry` from inherited-law activation, before `CreateCountry` transfers land and creates the country's AI. `CJournalEntry::OnActivated` accesses that AI, so a post-lobby global guard alone cannot protect later rebel creation. Gate SB's institutional law callback on its actual owner's `is_country_alive = yes`; the installed trigger requires a non-zero state count. Preserve the existing post-creation revolution handoff and ordinary live-country law updates.
- Exercise incomplete-country callbacks before the normal split fixture. The earlier tests supplied already-created rebel countries and therefore missed this lifecycle boundary. The new regression fails at premature JE activation before the guard and passes after it; a fresh DP replay is still needed to verify the native split. [Crash and native-order evidence](Docs/compatibility/zulu_contested_crown_2026_10_27.md).

## Temporary claimant sponsorship must clear the native IG gates (27 October 2026)

The sponsor changed from Armed Forces to **Landowners** at DP's request on 28 October. The same native gates and cleanup rules apply; preserve the earlier trial evidence rather than relabelling its saved IG data. The historical Landowner backing was below 5%, so approval/ideology pressure alone is not proof of eligible population support in a new replay.

- Giving an IG the new-law stance alone does not override a leader's stance on the old law. The Armed Forces sponsorship trial pairs explicit neutrality on the old royal law with strong support for Contested Crown and a temporary −30 Approval modifier. That supplies the matching second comparison and Angry tolerance while preserving the leader's own ideology. The 5% internal movement-support requirement still applies; a sponsor label is not a native bypass. Native negative IG traits may activate during sponsorship.
- Restrict application to the answered reserved crisis, never event `root` or a global tag. Remove the temporary package from both actual countries on cancellation/resolution/abandoned-war cleanup. Prevent crisis pressure from assigning its core ideology to new IG leaders, or restoring only the IG package would leave permanent character changes. Source checks cover these paths; native split, inheritance and military influence remain pending DP. The earlier blocker evidence below is preserved as the pre-change result.

## Native revolution eligibility precedes scripted permission (27 October 2026)

- In installed 1.14.5, `CanStartCivilWar` requires `HasInterestGroupSupportForRevolution` before evaluating a movement's scripted `revolution.possible`. An eligible IG needs at least 5% of its own clout supporting the movement, non-Happy/Loyal approval and sufficient ideological agreement. No comparable law positions also fails. `interest_group_can_join` is evaluated after these checks and cannot force an otherwise ineligible IG to join.
- A narrow movement strongly opposing Monarchy and demanding a new independent royal law can exclude every intended royalist IG: those IGs favour Monarchy and have no stance on the custom law. Court allegiance, 100% activism and a scripted territorial target do not override this native requirement. An agitator can affect attraction but does not bypass happiness or ideological compatibility. Diagnose IG eligibility before tuning activism again.
- The 17:43 save and read-only native-function inspection establish this blocker for the Dingane–Mpande replay; they do not verify a cure or army allocation. Source tests which supply a civil-war object cannot establish native creation. [Evidence and limits](Docs/compatibility/zulu_contested_crown_2026_10_27.md). Keep automatic activation disabled until the agreed engine acceptance succeeds.

## Claimant wars need a distinct demand and an exact native conflict (27 October 2026)

- Activism **target**, weekly activism **growth**, and civil-war **progress** are separate controls. The first 1 February 1840 snapshot had +2 target pressure but only 0.23 actual activism after about 23 weeks. Native `MOVEMENT_WEEKLY_RADICALISM_CHANGE = 0.01` needs a separate growth multiplier: the initial 99 trial gave 1.00/week; the current **24** gives **0.25/week**. Japan's `modifier_ended_sakoku_movement` confirms movement-scoped usage. The subsequent replay's 1 January 1840 snapshot reaches actual activism 1.00, but has no organising war or attached character. It does not establish that rapid growth caused the failure. Leave the separate exact-war `add_civil_war_progress = 1` unchanged; replay before movement creation to test slower growth, since lowering the rate does not lower saved activism. Attaching the rival as an agitator is deferred. Source tests verify arithmetic, scope and cleanup; native war creation remains unverified.
- Parented laws inherit ideology stances: a Monarchy child cannot by itself express a rival dynast's separate demand. Contested Crown is independent, copies the royal modifiers and is explicitly recognised by institutional, regency, title and heir checks. Store the exact original law type, including variants; a social-monarchical dispute must not silently restore ordinary Monarchy.
- Movement demand eligibility and ordinary enactment are separate concerns. Keep the temporary law evaluable within the reserved crisis; cancel only its ordinary enactment in `on_law_enactment_started`. The crisis movement must name the expected desired law before advancing its own organising revolution. Do not advance the first revolution merely because it exists.
- A stored movement may be organising while a different movement splits first. Match that movement on the actual rebel country as well as the original country before reserving the war. Keep both actual countries and the exact native war receipt through the callbacks; neither `c:ZUL` nor a dead contender proves who won.
- `target_fraction_of_states` controls a territorial target, not an identical army fraction. The native army calculation also uses movement military support, insurrectionary IG clout and geography. Source arithmetic and simulated callback inputs cannot establish military influence. Keep automatic entry off until repeated engine trials demonstrate a meaningful advantage; do not hide a failure behind unapproved combat buffs or troop transfers.
- Snapshot current allegiance for a challenge to a living ruler and future pledges for death/retirement. Count each aggregated house once. Do not turn a current patron's victory into universal conversion of future pledges, or add neutral/third-party influence, λ or Popularity to the two-side allocation fraction.
- An `incumbent` endorsement is relative to its home country. After the split, a claimant's recorded faction must support him as its own incumbent; a third prince must remain that house's named patron. Reconcile winning/losing endorsements before rehoming the reunited registry, or the former country context is lost and the winner's own supporters can be neutralised. Exercise both winners and native allocation of unaffiliated advisers.
- Cancellation does not retract a scheduled hidden event. Keep a single queued-poll receipt until its actual delivery consumes it; a reopened episode reuses that slot. Native movement disbanding is deferred too: wait for the retired crisis movement to disappear before reserving another, rather than accidentally reviving it. These checks are exercised from source; native timing remains pending DP.
- An invalidated but unanswered choice still exists on screen. Keep its selection receipt until dismissal before offering another pair, including the same two people after institutional re-entry. Actor identity checks alone cannot distinguish two episodes involving identical participants.
- A shared native `coup_event_active` reservation prevents concurrent native coups but does not justify retaining SB's superseded coup mechanics. Remove only a lock owned by this controller. Participant death, institutional exit and missing native war objects clean up without granting a faction victory; unrelated wars are not a blanket eligibility gate.

The old SB coup path and unchanged-law claimant prototype described in earlier dated notes are superseded. Historical notes are evidence of the earlier investigations, not current activation instructions. The [Contested Crown report](Docs/compatibility/zulu_contested_crown_2026_10_27.md) records the current scope and verification limits.

## Ranked campaign defections (27 October 2026)

- Ranking is not an identity exemption: the strongest loyalist eventually becomes the smallest when other houses defect. Explicitly exclude a protected character by template, and use a bounded ordered list for multiple distinct defections. Reuse the eligibility rule in reservation, preview and execution; do not refill a stale slot after the popup opens.

- Court events move a represented house through its leader. Rank by aggregate house Prominence, not the leader's personal score, and keep a reserved neutral recruit separate from a reserved incumbent defector: their eligibility checks differ. Both must join the same saved rival. Revalidate the original incumbent before defecting a supporter, so a pending predecessor's defeat does not take support from a new ruler. Source tests cover ranking, previews, stale targets and unchanged future pledges; native replay remains pending DP.

## Outcome options and direct report scopes (27 October 2026)

- A result popup's `immediate` block runs before its button is pressed. Reserve the responsible ruler and named houses there, but apply campaign Popularity, Prerogative and allegiance changes from the valid option. Keep the original receipt and once-only result guard through the click. A dead or newly committed preview target is skipped; do not draw an unpreviewed replacement. Source tests cover open popups, repeated callbacks, expiry and participant changes; native delivery remains pending DP.
- A custom-localisation selector can choose the right branch while its nested text loses `THIS` or a named event scope. The harvest log shows precisely this: the house name rendered in the outer row but its destination name did not. Select separate join/withdraw/switch tooltips in script, then dereference both names in that outer row. Select royal/chiefly descriptions with native `first_valid`; retain literal-only title/flavour selectors. Static scope checks do not prove rendering.
- The October 1842 saves show Mpande alive with syphilis and a politician career ending on 4 October, then absent in November. Career expiry is a strong explanation, not proof that illness played no part. Give authored long-lived claimants an explicit career after adding their politician role; preserve mortality. Zero Popularity still gives 50% annual attractiveness and is not itself a reason for no recruitment. P ≤−50 checks the legacy coup eligibility; it does not enable the unverified same-constitution claimant-war prototype.

## Constitutional eligibility is separate from personal allegiance (27 October 2026)

- An IG exclusion must cover recruitment, paid-target selection and native movement membership as well as the alignment writer. Otherwise an unavailable faction can still recruit a character or charge for an ineffective bribe. Refresh existing alignment after IG changes; retain personal backing, succession pledges and prominence.
- Dynastic eligibility previously required royal alignment. Clearing that alignment for an excluded IG must not silently revoke a prince's claim. Keep that exception confined to the excluded IGs and preserve explicit renunciation/retirement checks. Change the requested ideologies only on actual alignment transitions; monthly trait presentation must not bulk-convert Moderates. The home country's JE controls the contest exception, including exiles and foreign event roots. Source tests cover these paths; engine rendering remains pending DP.

## Annual allegiance and integer random-list weights (27 October 2026)

- Native `CJominiRandomListEffect::CEntryEffect::CalcChanceIfEnabled` converts the evaluated fixed-point factor to a whole-number weight. A reservoir draw using attraction fractions 0.05, 0.50 and 0.55 therefore supplied three zero weights; withdrawal rates below 1% also disappeared. Scale **all competing weights equally** before the native draw. The court uses 100,000 to preserve five-decimal script precision; its probabilities, annual frequency and popularity coefficients are unchanged. Tests must truncate weights as the engine does, not silently use Python floating-point selection. See the bounded [native evidence](Docs/compatibility/evidence/zulu_random_list_weight_1_14_5_arm64.txt).
- An uncommitted character has no old-patron scope. `this ?= scope:actor.var:old_patron` still evaluates the missing right side. Branch on its existence before comparing; guard both annual change detection and a withdrawn council promise. A silent harvest is correct only when no current/future allegiance changed, not when every possible patron had a zero engine weight.
- The concession receipt must supply its remaining duration through a named script value. The earlier bare-variable duration pitfall also applies to newly authored concessions; test the actual duration parser contract, expiry and recreation together.
- In installed 1.14.5, `on_wargoal_enforced_by_timer` is separate from final `on_wargoal_enforced`. The old `enforced_by_timer` marker is no longer documented as an engine-provided scope. SB now sets a temporary marker only in its timer adapter for the existing Klip/Bechuanaland tracking. Do not route timer callbacks through final accepted-demand bookkeeping. Earlier notes describing the warning as merely engine-provided were based on the older contract.
- UI-only variables can legitimately produce the engine's unused warning: it does not count localisation reads. Keep annual report weights and pledged shares; remove an actually unread derived share instead of adding dummy reads. Runtime confirmation remains DP's responsibility.

## Native adulthood and historical characters' careers (27 October 2026)

- Native political adulthood is 16 (`NCharacters.ADULT_AGE`); the portrait switch at 18 is a separate graphics setting. An age-18 court gate silently delayed the sons' declarations relative to the character screen. Use `is_adult` for matching native adulthood, including candidature and regency, rather than duplicating a number.
- A historical flag does not protect a politician from career expiry. The retained autosaves give historical Cetshwayo (ID 4481, born 1826) a career end of 30 November 1843; he is retired in December and absent by January. The generated Cetshwayo kaMpande (ID 16783864, born 1797) already existed alongside him. Compare IDs, templates, birth dates and career dates before treating a namesake as a recreated character. Native politicians have 5–10-year careers; scripted historical arcs may need `set_career_length`, as in Vanilla's Vargas events and Hail Columbia's character templates. Extending the career does not extend life or protect against scripted removal. Template creation fixes do not resurrect deleted saves. Native replay remains pending DP.
- A base IR-scaled effect must use IR/50, independently of the signed P multiplier: otherwise a negative P can reverse the intended deduction. Include the base component in zero-P UI and exit cleanup tests. Construction limits must count queued as well as completed levels across all of the owner's states; native queuing still requires DP verification.

## Character banners need one click target (27 October 2026)

- DP reported intermittent court-banner navigation again after the earlier list-collapse action was removed. The current log contains no associated court-link error, so that earlier explanation was insufficient.
- `Character.GetFullName` adds an interactive character link inside `button_standard`'s label, whose native `text_single` defaults to `alwaystransparent = no`. Keep the button's label unformatted and mouse-transparent, put the character tooltip on the button, and bind the button directly to its list item's `Scope.AccessCharacter`, as the Japanese JE portraits do. One shared court button now handles all six roster contexts without changing panel state before navigation. Competing text hit targets are a plausible source of the symptom, not an engine-confirmed diagnosis; label/edge, nested-house and repeated-click checks remain pending DP.

## Formation names, defeated tags and created-character handles (27 October 2026)

- Vanilla's `FRONT_COUNTRY_COMBATUNITS` embeds the rendered breakdown inside `GetRawTextTooltipTag('$BREAKDOWN$')`. An ASCII apostrophe in SB's “Dingane's Amabutho” terminates that argument; the reported parser errors identify the exact point. Use a typographic apostrophe in this name. The current save retains the localisation key, so no formation or save rewrite is needed. Native hover rendering still needs DP verification.
- A conquest can remove `c:SWZ` before war-end cleanup runs. Compare the recorded play's actual participants with `country_definition = cd:SWZ` and clean those participants directly, retaining the exact-play check. Merely adding a live-tag guard would silence the error but skip the winning side's cleanup. Source tests cover annexation, surviving SWZ, repeat cleanup and unrelated/missing participants.
- Export a newly created character with `create_character.save_scope_as` when later effects in the caller need it; installed `psychology_events.5` uses this field. Do not rely on a scope saved only inside `on_created` escaping that callback. Uthumbu's old path could create the baby without completing recognition, then find him on the second activation. The earlier test interpreter shared callback scopes and concealed this boundary. Isolated-callback tests now cover first-click creation/recognition, the single 50-P charge, foreign ROOT and reuse; native first-click delivery remains pending DP.

## Ended Blood River plays and stranded result records (26 October 2026)

- `has_variable` is not proof that a saved diplomatic-play object still exists. The October–February checkpoints retain `sb_natal_story_play_scope` after play 16777219 disappears between 1 November and 1 December 1839. Zulu's accepted-demand flag survives, but no terminal receipt exists. Generation recovery's presence-only guard therefore leaves the result stuck. The saves establish that missed handoff, not precisely why the native closing callback failed to resolve it.
- Recover only from the original generation's saved actors, their admitted-play records, a now-missing play object on both actors and an authenticated accepted demand. An active play, timer-only result, missing generation or disappearance without accepted demands cannot grant victory. Use the same result dispatcher and once-only popup receipt as the native callback; preserve the sovereign at demand enforcement so a later succession cannot inherit the personal reward. Monthly recovery must test dead handles, not wait for the old generation's expiry. Source tests cover both entry routes, both winners, mutual settlement, foreign ROOT, retags and unrelated ongoing wars; native delivery remains pending DP.

## Court refusals and signed eligibility thresholds (26 October 2026)

- A refusal option can also be the safe dismissal when its scene becomes invalid. Apply its penalty only while the original scene remains valid, then use the existing cleanup to prevent repeated charges. The `.212`/`.213`/`.215` refusals now lose 5 P without requiring positive P or forcing the concession; stale dismissals remain free. Source execution checks invalid participants, a changed ruler and repeated choices. Native popup behaviour remains pending DP.
- Distinguish a threshold's sign from a payment which can cross it. The 1 January 1841 autosave has +4.19663 P, the Honour settlement and a Swazi popup opened on 27 December. That satisfies the then-current P < +10 rule; the save cannot establish the exact P when Uthumbu was introduced. DP subsequently changed the low-P branch to P ≤ −10, retaining independent Blood River victory/white-peace triggers. Test the exact boundary, a recovered queued offer and Uthumbu's 50-P payment; do not assume that a nearby popup was directly called by the character action.

## Outcome events own their consequences (26 October 2026, Blood River)

- A successful terminal callback does not establish that the affected player received an event. The 1 September 1838 save showed ORA's settlement completed while ZUL silently received defeat politics and 10% firearms progress. DP confirmed that these belong in the Zulu outcome event even after backdown; do not remove the reward or invent a fought-war requirement.
- Keep the resolved result in its receipt and preserve the responsible ruler on the Zulu country. DP clarified that court consequences apply when the Zulu event opens, but the firearms reward belongs to its option: opening or hovering the popup must not grant it. After ORA settles Natalia, hand the existing receipt to ZUL's defeat event rather than destroying it early. The option reports the political effects and grants firearms before consuming the receipt; repeated or expired options cannot award them again. Finish that outcome before opening the Swazi question.
- DP's follow-up gives neutral `.081` the same firearms learning as `.080`/`.082`, without political victory/defeat consequences. A consumed Blood River result marker therefore does not by itself mean victory or defeat. Keep each campaign's defeat shock explicit at the shared helper's call: Blood River is now −25 P; Swazi remains −10 P. Retire obsolete ORA-labelled reward previews when the Zulu outcome owns the effects.
- Moving a reward into an option exposes it to tooltip preview. Guard the firearms increment and dependent recalculation after initialisation, since preview does not execute that initialisation. Source execution covers the missing-counter preview, deferred button reward, backdown, enforced-demand outcomes, neutral settlement, foreign ROOT, handoff/retry, repeated callbacks and a changed/dead ruler. This does not establish native capitulation timing, popup delivery or portrait rendering; those remain DP checks.

## Adulthood declarations and a common supply gate (26 October 2026, follow-up)

- A once-only coming-of-age branch should consume its age check even when the parent is already ruler or dead. Otherwise a later overthrow can masquerade as the son's adulthood. Record current allegiance separately from future claims, and let the notification acknowledge the recorded result without applying it again. Apply a January adulthood declaration after the annual allegiance roll, so that same pulse cannot immediately undo it. Source tests cover each son, repeated pulses, dead/ruling participants and foreign ROOT; native birthdays and portraits remain pending DP.
- A child introduced as a newborn needs age relative to creation (`age = 0`), not a fixed historical birth date that makes later introductions older. The installed Sicilian newborn template supplies the native precedent. Reusing an already-existing identity must not reset its age.
- DP now uses one firearms rule: positive market Small Arms sell orders and no native market shortage. This supersedes the treaty-specific progress rule below; it does not change treaty creation itself. Use whole weekly ticks and proportionate seed/reward values to avoid a rounded fractional monthly increment delaying the intended 104th-week completion. Preserve the existing display/penalty scale and story archives. Native supply accounting remains pending DP.

## Delivered arms and resolved frontier outcomes (26 October 2026)

- An acknowledgement-only popup need not own a mechanical handoff. DP retired `.021`; Honour in Retief’s `.020` records its context directly. Keep the actual settlement gate and monthly follow-up, so removing the notification neither blocks the chain nor starts it before ORA resolves Natal. Source execution covers the exact choice and later once-only eligibility; popup timing remains pending DP.

- A goods-transfer partner can supply imported firearms without owning an arms factory. Test receipt through the recipient's market-goods `treaty_imports` and a matching inward small-arms treaty; do not substitute the supplier's industrial buildings for deliveries. The market total is aggregate, not an article-specific quantity. Source tests cover foreign ROOT, direction, goods, interrupted shipments and retained progress; native delivery accounting remains pending DP.
- A diplomatic concession offered in a popup is not yet the recipient's resolved settlement. The low-Prerogative Swazi route waits for the completed Natal outcome; the honour/guns description flags alone cannot open it. Recheck eligibility when a delayed offer arrives, retain its outcome context if an undelivered offer is cancelled, and leave an already-open choice under its existing receipt. Source tests cover recovery through the strict P <10 boundary and once-only delivery; engine replay remains pending.
- A fictional optional child should be created by the introducing action. The original `on_created` scope capture was superseded by the creation effect's exported `save_scope_as` field after the 27 October two-click report (see above). Do not pre-populate the opening cast merely so the action can find the character. Reuse an existing identity, register once, retain the authored age and use the normal heir-blocker handoff.

## Name the parties to court bargains (26 October 2026)

- “Promise a prince a Council” reverses the succession bargain. The prince promises the institution; the household representative promises support. Name both parties in the preview and distinguish a law enacted now from a promise fulfilled after accession. Do not use “the displayed alternative” where a valid character scope is available.
- DP's Council threshold is the bargaining representative's own native Prominence ≥50, not the prince's Prominence or the household's combined score. Gate both the visible choice and execution, including the shared helper. A bargain scene should not select a low-Prominence actor when the only remaining concession requires 50.
- Council and privileges are separate concessions. The Council choice changes/promises the law and grants no amaKhosi attraction bonus. Privileges retain their separately authorised attraction effect. Verify both state changes and absence of the other concession's receipt/modifier.
- Explain dependent actions together, but split distinct actors' gains/losses into separate effect rows. A future law promise deserves its own named explanation. Native portraits should show the actual people competing: the patronage exchange and disputed award now use two-character windows. Concrete prose and source tests do not establish final text wrapping or portrait rendering; DP checks those in-game.
- When charging for a previously free refusal, review the event's timeout default too. `.210` now defaults to accepting the proposed pledge; blocking it requires and spends 10 Prerogative. Revalidate before charging and let an invalidated scene close without payment. Source tests check the declared default and costs; native timeout delivery remains pending DP.

## Frozen court payments and meaningful reports (25 October 2026, later playtest follow-up)

- DP now freezes cash prices when a pledge or paid incident opens. Debit the stored quote even if reserve capacity or prominence changes; do not open replacement confirmations as the player reads. Revalidate the same participants, ruler, eligibility and once-only reservation. This supersedes the older cash-requote guidance below; coercion odds still require their separate revalidation.
- Debt is permitted for both Secure a Pledge and paid court incidents. Display the stored price and current reserves, then debit directly. Do not add a cash-only availability check or silently recalculate the payment.
- Run the annual allegiance roll normally, but notify only when a current allegiance or future pledge actually changes. A silent unchanged year must still record its annual completion and must not roll again on repeated pulses.
- Filter new uncommitted-house recruitment by the representative's own positive native Prominence and non-agitator status. Apply the same eligibility to random incidents, frontier rewards, annual joining and purchases. This does not ban generated court characters, remove existing allegiances or change the prominence of an entire house.
- A house joining a named rival is one dependent outcome: guard both eligible actors together and show one sentence with full names and the house's Prominence. Keep independent payment and outcome rows separate. Do not explain unchanged future pledges in scenes solely about allegiance to the living ruler.
- Paired portraits use native `event_window_2char` with two actual saved characters. Retief's petition captures the Zulu ruler and living ORA Piet Retief; execution uses that same saved envoy. Installed `shogunate.2` informed the concrete scene/choice style and `commander_events.4` the portrait layout. Source tests do not verify portrait rendering, native debt accounting or popup timing; those remain DP checks.

## Court incident previews and portrait subjects (25 October 2026, 21:35 follow-up)

- An event's `after` block can be traversed during tooltip preview, including a hidden scheduler called by cleanup. “A Name on Every Tongue” exposed the deck's temporary availability counter after preview skipped its initialisation. Guard both increments and dependent comparisons behind a separate `has_variable` branch. Source-execution regressions cover all six incident previews without mutations, exhausted and empty decks, normal draws and the existing delays; native hover replay remains pending DP.
- Character action popups use Vanilla's `event_window_1char_tabloid` and a saved character `left_icon`; `event_portrait.dds` alone only supplies the small event icon. Preserve the named event scope through result notifications after country action variables are cleared. A successor-selection scene can show the sovereign without pretending the first candidate has already been chosen. Portrait rendering remains pending DP.

## Independent coercion limits and Authority commitments (25 October 2026)

- “Per rival per ruler” needs a record of every ruler who attempted the purge, not only the latest ruler. Otherwise A→B→A allows A another attempt. Renunciation’s ten-year target cooldown is separate; a shared attempt marker incorrectly blocks the other action. Static regressions exercise both directions and a returning ruler.
- A current challenge uses current pledged prominence. Including future succession promises can treat a king’s loyal follower as today’s enemy. Releasing a claim must clear those two records independently; a future-only promise must not erase unrelated personal loyalty.
- Do not assume repeated same-key timed Authority modifiers stack and expire independently. SB records the total outstanding commitment and schedules one hidden expiry per paid action. Classify those mechanical receipts in the delayed-event manifest. Their validity cannot depend on the target remaining alive, the same ruler staying in office or the institutional JE remaining active. Source-execution tests cover staggered expiry and invalidated participants; native delivery and the aggregate tooltip still require DP’s check.
- Snapshot the actual current backing and failure threshold before displaying the odds, revalidate before charging, and use the same rounded weights in the display and roll. Changed coercion odds require a new confirmation, not permission to roll an unseen probability. Cash-price freezing is a separate, later DP requirement above.

## Court preview scopes and reporting (25 October 2026, 18:30 follow-up)

- A character variable list may still expose an expired GUI handle. Do not make that handle the root of a character-scoped SGUI: its type check fails before predicates can reject it. Anchor the court filters on the JE country, pass the optional character as a saved scope, and guard it with `exists` / `?=`. Match Japan’s character-validity display check too. Static invalid-handle checks pass; engine replay remains DP’s check.
- Optional equality (`?=`) does not make an absent **right-hand** variable valid. Check for an existing future pledge in a separate branch before comparing it to a current patron; otherwise Retief’s backing recalculation repeatedly logs an invalid RHS. Preserve the rule that one house counts once when both commitments name the same prince.
- Tooltip preview does not create an execution-only container. Guard the container and every dependent saved-scope write after creation. Hiding the effect removes internal watchdog schedules from the tooltip, but does not replace scope guards. A foreign-ROOT test must still confirm ORA owns the refusal receipt and both original actors receive the same receipt.
- List reports should localise against the current `THIS` scope, as installed Spain’s vernacular-policy report does. Do not rely on `save_scope_as` inside a tooltip-only loop. The original fix reported empty lists explicitly; DP subsequently requested no popup at all on unchanged years (see the later follow-up above). The May 1838 save recorded the annual check with no changed-house lists.
- Keep initial and revised event quotes on the same price value. DP doubled all court reserve-capacity costs in this follow-up; at q=100 a pledge costs 160% of capacity. Capacity is a native soft threshold, not a hard treasury ceiling. Do not silently clamp the price back to 100%.

## Coercion outcomes and debt-funded pledges (25 October follow-up)

- In the earlier formula, a 5–45% capture chance was not a 5–45% chance of removing a minor rival from court: the exposed-failure branch exiles them. Distinguish killing, renunciation, exile and surviving claims when explaining balance. The purge’s 50-P cost limits access; it does not alter that guaranteed departure. The later rework changes odds and adds Authority commitment, not this two-outcome distinction. Charge only after participant/reign/prototype validation, and recheck P at resolution.
- Reserve capacity is the price basis; actual gold reserves are not an affordability limit for debt-funded pledges. DP explicitly permits borrowing for Secure a Pledge. Retain native treasury debits and participant checks, show reserves against cost, and do not impose a new cash-only gate. The later follow-up extends borrowing to paid incidents and freezes their displayed cash quotes too. Static negative-treasury tests do not replace DP checking the engine's debt accounting.

# Common Victoria 3 scripting pitfalls

## Character packages must be evaluated by active role (25 October 2026)

- A trait name does not establish its effect. Installed Popular Commander has no universal Popularity bonus, Ruthless has no command kill-rate bonus, and Tactful adds flat Defence rather than a percentage. Separate universal, ruler, commander and IG-leader blocks before adding package totals. Ruler-only Dingane does not supply his potential command bonuses to Zulu armies; Ndlela's actual command package matters when replacing his political traits.
- Do not flatten repeated or differently scoped blocks into asserted engine results. Installed Elder has two `country_modifier` blocks, and Pillager's −10 Popularity is in `command_modifier`, not its universal character block. Their runtime handling remains unverified. The exact source comparison and role tables are in `Docs/zulu_vanilla_character_packages_2026_10_25.md`.

## A low political target does not guarantee a coup (25 October 2026)

- Distinguish equilibrium target T, actual Prerogative P, coup entry, attempt progress and final outcome. In the current court, entry checks P ≤−50 and a candidate's strength against resistance, plus concurrency/cooldown conditions. Progress can still fail or time out. A fixed target −51 takes 27 monthly pulses to reach P ≤−50 from P=0 under the current drift; this is an algebraic check, not engine verification.
- A neutral representative joining opposition is not equivalent to an incumbent supporter defecting. Count the actual house prominence and current allegiance; aggregate rival backing does not prove that a particular claimant meets a succession threshold. If design requires a guaranteed historical confrontation, agree that explicit rule rather than claiming a few headcount effects prove it. See `Docs/zulu_umkhosi_and_dynastic_balance_2026_10_25.md`; the resisted native claimant-war route remains unverified.
- A scripted `target_fraction_of_states` is a territorial target, not a battalion-share setter. Installed 1.14.5 defines also weight the native uprising army fraction by movement military support and insurrectionary IG clout. `play_as` proves that an existing rebel country can be selected, not that a same-constitution conflict can be created or split by court prominence. Verify these separately, especially for one-state countries; see `Docs/zulu_court_rewards_and_claimant_wars_2026_10_25.md`.
- Distinguish current and future commitments when assigning a civil-war side. A chief's promise to a prince after the king dies does not itself make them a rebel against the living king. The 25 October purge rework separates current house allegiance for a living-ruler challenge from the accession prototype's future promises. Static placement logic is not proof of a native war or its force allocation.

## Empty trait lists still use native trait generation (24 October 2026)

- `traits = { }` does not mean that an adult character will enter the game without personality or skill traits. Installed 1.14.5 `common/character_templates/00_default_template.txt` runs `trait_generation`: an adult with zero trait value receives a random personality and skill, with further age-dependent generation. Setting `historical = yes` alone does not bypass that branch. The opening court investigation found this relevant to Dambuza, Mawa, Nongalaza and Sotobe.
- Distinguish “no unsupported trait authored” from “no random trait generated”. If a researched character needs a controlled package, review its own trait-generation behaviour as well as its explicit trait list; preserve intended child and experience handling. Do not change the global default to solve a local historical-cast problem. The default-script behaviour is confirmed; a future scoped replacement still needs DP's fresh-campaign verification.

## Present allegiance versus succession pledges (24 October 2026)

- A king and loyal followers may have no pledge about the next succession. That does not make them personally uncommitted. Display Current Allegiances separately from Next Succession, including the incumbent's own house in the former. The February 1836 checkpoint already included Dingane's 206 prominence in Prerogative; its succession-only display made that backing look missing.
- DP's trial λ = 0.25 discounts personally uncommitted prominence only in the court-backing denominator. Do not discount future-unpledged prominence, coalition display totals, purchase prices or the 25% major-challenger denominator. Test a chief who supports the king now and another prince later.
- Projection totals and supporter lists must reset before rebuilding, and must not overwrite the opposite court after a constitutional split. Opposition to a living patron assigned to the other court still counts at home; present it separately without modifying that patron's home projection. CAP exile alone does not change home-court membership.
- Save variable values use signed fixed-point numbers stored as unsigned 64-bit identities; omitted identities can represent zero. Decode the sign before dividing by 100,000, and extract country/character IDs within their respective managers. These static/source and save checks do not establish in-game rendering after the change.

## House prominence and court presentation (20 October 2026)

- DP replaced representative-only weighting with summed house prominence. Sum each eligible adult once, use the named head's commitments, and keep the UI's share of pledged prominence distinct from the major-challenger share of total prominence. Adult self-claimants contribute native Prominence including the Claimant trait's +25; do not add that bonus again as a separate modifier or supporter. A bonus meant to appear on a trait card belongs in its `character_modifier`, as with Vanilla Ambitious/Imposing. Removing the former separate +20 modifier also requires testing the card's accession, renunciation and exit lifecycle. Supporting a claimant is a different card without this bonus.
- Apply the approved −10 modifier to all adult non-leaders, including unaffiliated councillors. Rank shared-house heads before that penalty; otherwise a previous subordinate can never overtake a head with an only slightly higher score. Repeated recalculation must not stack modifiers or oscillate leadership. Exclude each domestic agitator's contribution from additional scripted recruitment, even when a non-agitator heads the combined house.
- New procedural adults need registry membership and neutral allegiance cards before joining the calculations. Do not infer a historical household from their randomly selected surnames. When expanding representative eligibility, preserve restrictions which previously followed implicitly from exclusion: claimant princes must not become ordinary purchasable backers or promise their automatically self-counted branch to another candidate.
- Character-link buttons should navigate with their live Character context. The old buttons also collapsed their enclosing list, a plausible cause of intermittent navigation failure. Removing that competing action is a source correction awaiting DP's engine check. The contemporaneous FindChild('interest_group_top') errors originate in native IG panel/outliner expressions; the log does not prove their relationship to the court.
- Plain localisation review markers must match exactly. Put explanatory comments above `# TO REVIEW (non-event/JE keys)`, not after it; a suffixed comment is not recognised by the queue validator.

## Court tooltip and layout replay (19 October 2026)

- Tooltip previews skip counter initialisation but still visit hidden effects and can read a `change_variable` operand. The successor picker produced 397 missing-counter reads on hover. Put both the increment and dependent comparisons behind a separate `has_variable` branch. Exercise preview traversal without mutations; an ordinary execution test cannot catch this.
- A `window` nested in a vertical flow still participates in layout even with `layer = popups`. The 780-pixel court window displaced a 504-pixel JE, and its raw scrollarea lacked scrollbars. Japan's JE `section_header_button` plus the native `scrollbox` provides a bounded inline alternative with the existing JournalEntry context. Use autoresizing, width-bounded multiline rows; reduced widths can invalidate formerly adequate fixed heights. Static geometry checks do not establish actual rendering.
- CMF's `no_heirs` flag suppresses newly generated heirs by killing them in `on_heir_born`; it is not an engine generation switch. Track ownership of the block, release it for authored appointments and reapply afterwards, including minority regency. Release on institutional exit or exhaustion of the living authored line, and preserve another route's independently owned block. This callback ordering still needs DP verification.
- A kill-attempt option is not evidence that its capture roll succeeded. The checkpoints retain both princes alive, with flight recorded for Mpande by February and Gqugqu by March. Report the actual outcome, and distinguish an unchanged coalition target from Prerogative approaching it gradually. Reapplying the same timed Popularity penalty refreshes its duration rather than stacking another deduction.
- Explicitly console-invoked test events use Vanilla's `orphan = yes`; do not add a fake production caller merely to silence orphan warnings.

## Court commitments, quotations and succession (19 October 2026)

- Current endorsement and a future-successor pledge are different records. A representative can co-operate with the incumbent while supporting another prince's eventual accession. Calculate each following once. The original candidate exclusion was superseded by DP's 20 October own-prominence rule above; a candidate must still not be counted twice. Coercion also has to account for the target's present adherents, deduplicated against future pledges.
- A popup reservation must survive unanswered monthly pulses, and its participants still require revalidation on selection. If a named nominee dies, do not silently substitute a new candidate beneath the old choice. The original cash-price revalidation rule was superseded by DP’s 25 October frozen-quote request above. Tests should execute invalidated-participant transitions with a foreign event root.
- Capture a sovereign's outgoing commitments in the death/selection callback before clearing dead references. Fulfil an accepted council promise before checking whether the new ruler has repudiated it. Otherwise the native ruler-selection interval can falsely punish an undertaking while the accession popup is still open.
- Use native `game_date` for a specific date comparison; `current_date` was rejected by Tiger in the new retirement controller. Re-establish the current country inside `create_character.on_created` before calling helpers which require a saved owner scope.
- Native revolutionary eligibility and high activism do not prove that a same-constitution claimant war can start. The current court prototype is deliberately opt-in. This remains an engine-verification question, not a demonstrated engine impossibility; do not replace it with a foreign war or lock ordinary actions behind an undeliverable event.

Read this before changing or reviewing Victoria 3 scripts and when investigating
a regression. These notes record lessons from SB's bug investigations, not a
replacement for the installed game's script documentation and working examples.
Update them when a new cause or useful prevention is established. Label hypotheses
and unverified engine behavior; do not promote them into rules merely because a
static test passes.

## Crash attribution and generated map validation

- A native exception stack identifies the failing operation, not necessarily the
  cause of its invalid state. The 19 September 2026 ZUL-war crash enters Goods
  Transfer eligibility from AI treaty selection and fails in a market-capital
  port lookup. It does not identify the evaluated country or prove a Zulu event,
  mod defect or Vanilla defect caused it. Nearby log errors are leads, not proof.
- A second matching stack and matching gameplay snapshot establish a repeatable
  failure, not its proposed association with capitulation. The 20 September
  replay still saved ZUL at 97.1 support with zero demand timer progress. Native
  inspection found an unguarded market-capital-to-port-search boundary; the
  Goods Transfer eligibility wrapper now guards scope validity explicitly before
  evaluating the original native predicate. This mitigation awaits DP's replay.
  Do not call a guard a verified crash fix solely because static parity passes.
- DP subsequently completed ZUL capitulation after defending for roughly a month
  before advancing again. An altered-order replay can demonstrate a playable
  route without isolating a patch's effect: record both the changed timing and
  whether the new script was loaded before attributing the successful outcome.
- Check save references against their exact manager/database boundaries. IDs can
  repeat across managers; a broad numeric-record search can silently overwrite a
  state with another type. Dead countries can retain stale capitals normally,
  and omitted serialized fields may represent defaults.
- A valid configured port and a connected harbor in the shipped naval graph do
  not prove that the engine accepts the deployed spline. Anchor 8414308 was
  rejected at launch even though raster sampling and sea adjacency pass. Record
  that runtime discrepancy; do not certify it from hashes or static counts.
  See `Docs/compatibility/zul_war_crash_2026_09_19.md`; the cause remains unresolved.

## Country scope is not event ROOT

- Entering `c:NAL` from a Zulu event changes the current scope, not `ROOT`.
  Klip county creation compared Natal-owned provinces with Zulu's event root and
  rejected its valid input. Capture the current actor for reusable country helpers.
- In play callbacks, `ROOT` may intentionally identify the exact diplomatic play.
  Preserve that reference when recording or comparing the play; do not replace
  every `ROOT` mechanically with a country tag.
- Trace who writes and reads each variable. The Klip punitive queue wrote its
  pending marker on Natal, while a callback originally looked for it on Zulu.
- A fixed tag can later identify a different country. Rollback must return land
  to the original captured owner, including if that owner retags. Do not adopt
  a new country simply because it now has the expected tag.

## Preconditions must admit the intended scenario

- In a split state, Return State targets the opponent's actual state, not the
  holder's existing portion. Klip's Natal demand is NAL against the ZUL-owned
  `STATE_NATAL` state. ZUL's counter-demand targets NAL's different state object.
  Use `primary_demand = yes` for the added primary goal (installed 1.14.2 effect
  documentation), not an invented `primary` field.
- A two-demand victory needs both actual outcomes. Retaining original territory
  is not proof of gaining the disputed land. Check stable province ownership
  after split-state merging and the actual protectorate relationship. Preserve
  the route's eligibility requirement after transient war markers are cleared,
  so partial peace cannot accidentally open the government choice.
- Scope and eligibility restrictions are design requirements: agree them explicitly
  with DP before adding them. Do not invent peace, diplomatic-play, ownership,
  subject-status, or other broad gates because they seem prudent. Keep technical
  scope-validity checks tied to the actual operation; they do not authorize extra
  gameplay restrictions.
- Natal's annexed-Zululand government choice was blocked by an unrelated WTI–WAS
  war. Both settlement eligibility and punitive orphan cleanup required blanket
  peace/no active play, leaving a deleted Klip play reference in place from August
  through November 1851. Remove those broad gates from both steps; test cleanup
  followed by eligibility while unrelated wars/plays remain active. The saved
  blockers are confirmed; why the original war-end callback missed cleanup is
  unresolved, and engine delivery after this correction still awaits DP.
- British Natal is a colony. Ordinary aggressive-play permission therefore cannot
  be required for a bespoke Klip play that deliberately bypasses diplomatic
  status. The contradictory condition also caused monthly cleanup to mistake
  normal colonial status for permanent failure.
- Distinguish a busy participant from an invalid route. Britain's unrelated war
  blocked the Natal refusal response when a blanket British peace check was
  added. Check the relevant confrontation and actor, not unnecessary world peace.
- Blood River `.050` repeated while ORA fought PHL/BST because the real Rally
  default, initial launcher, and retry all required blanket peace/no active play.
  A second option with the same label only requeued the popup and was not a
  default. Keep one escalation choice, record it once, and retry creation
  internally; only the actual ORA-ZUL conflict/truce delays this launch. Test
  the default's availability and both launch stages under unrelated wars/plays.
  The 1838-12-01 save also recorded ZUL as both refusal actors: its builder ran
  inside ORA but retained the ZUL event ROOT. Capture the current country for
  the receipt actor and container parent, including the reciprocal guns route.
  These causes are confirmed by source/save/log evidence; corrected engine
  delivery still requires DP's replay from before the receipt was created.
- Test player and AI ownership separately. The British Zululand handoff accepted
  AI subject owners but excluded player Natal; adding a Natal-owned settlement
  also requires excluding Natal from the competing British handoff.
- Partial ownership and an existing unrelated ZUL are not equivalent to annexed
  Zululand. A restoration option must not silently take territory or another
  country's subject to manufacture its expected starting state.

## Dispatch, open popup, and answered choice are different states

- A short dispatch timeout permits retry if an event never opens. Once the popup
  opens, retain a reservation for its entire lifetime. Clear it on answer or
  terminal cleanup, not merely on delivery. Clearing it in Klip `.060.immediate`
  caused another popup at the next monthly pulse.
- In these country events, `duration = 3` means three months. Saved `.060` events
  created on 6 January expired on 6 April. Do not compare that lifetime with a
  20-day queue timeout as though both were measured in days.
- Every settlement option must revalidate before applying irreversible effects.
  A popup may remain open while ownership, subjects, or the active play change.
  Retain the once-only outcome guard as well as exact-play checks.
- Pre-war cancellation is not white peace. Calling the Klip war-result finalizer
  from pending-delivery cleanup produced `.081` before the player answered `.060`.
- Terminal cleanup must clear the launch-pending marker too, or monthly retries
  can continue after the route is finished.
- Do not add narrative filler or redundant options to explain a missing internal
  reference. Fix the routing failure. A normal story choice should not become an
  invented “this notice is irrelevant” branch.

## Use only the state machinery the lifecycle needs

- After replacing state machinery, remove route flags and stored country scopes
  that no longer have readers. The Chiefdoms cleanup on 16 October removed three
  such writes. Check localisation, GUI and dependency consumers too: the engine
  does not count localisation reads, and SB's definition-only symbol checker
  checks top-level definitions rather than variable assignments. Do not add dummy
  reads just to silence an unused-variable warning.
- The Klip autosave contained open events and a country variable referencing a
  container that no longer existed. The exact engine cause of that disappearance
  was not established. Do not generalize this observation into “containers never
  work.” The once-only Klip follow-ups did not need containers and were simplified
  to country-bound delivery with pending/resolved markers.
- A helper named for restoring or normalizing a country may also schedule events.
  Reusing it from an option can reopen the very choice being resolved. Keep subject
  setup separate from event scheduling where both entry paths need the setup.
- A later government choice can invalidate an earlier victory predicate. In the
  17 October Klip saves, both war demands execute, ZUL first becomes GBR's
  protectorate, and the British handoff opens Natal's government event before
  Klip is finalized. Chiefdoms changes the exact protectorate type; the next Klip
  reconciliation calls this an incomplete result and opens `.081`. Finalize the
  earned result before a dependent choice changes its evidence, and test the
  foreign-overlord handoff as well as the direct-subject path. The correction
  recognises the earned GBR protectorate while NAL is British and runs the
  existing reconciler in NAL scope before scheduling its government choice.
  Source regressions cover both update orders and all three choices; corrected
  engine delivery remains pending. The native reason NAL's initial protectorate
  goal was replaced by GBR's remains unproven. Vanilla colonies can hold subjects;
  do not assume responsible government is required without checking the effective
  subject definitions and ordinary overlord-rank eligibility.
- Mark a restoration choice resolved only after the required country and subject
  relationship exist. Creating a country is not proof that the subsequent setup
  succeeded. Avoid extra speculative recovery frameworks; retain valid pending
  state and inspect the actual failure.

## Tooltip evaluation does not execute prior mutations

- Write for a Victoria 3 player who has not read the design discussion. Explain
  what a value means, what changes it and what the player can do. Separate the
  short gameplay explanation from detailed law or contribution breakdowns.
  Internal terms such as "native", excluded formula inputs and implementation
  commentary do not belong in ordinary tooltips. Compare relevant DLC examples
  for concrete flavour prose, rather than describing abstract system plumbing.
- Display constitutional preference separately from personal allegiance. The
  court's variables retain the authoritative commitments; zero-value, non-random
  traits show them without overwriting a character's wider ideology. Neither
  registration nor movement pressure should reintroduce a forced faction
  ideology. A named allegiance display must use the recorded home court and
  claimant, not an exile's current host country. Trait descriptions alone have
  no guaranteed Character context; the roster supplies that context explicitly.
- A static modifier needs a valid icon and a non-zero effect to make its entry
  useful. Following recruitment previously added an empty zero-strength row
  with no icon. Omit zero-strength entries; verify the chosen asset exists.
- Lobby JE names come from `JournalEntryType.GetName`, which supplies no script
  root. `ROOT.GetCountry.IsValid` is not a safe guard: promoting the missing ROOT
  fails before the validity check or fallback can run. DP's 19 October launch
  log also rejected ROOT inside the nested active-title localisation. The
  scope-free native `IsInGame` check fixed the lobby, as DP verified. However,
  changing the selected text to `SCOPE.GetRootScope` then failed in-game too:
  `SelectLocalization` creates a fresh localisation data container and does not
  forward the temporary ROOT/SCOPE bindings supplied by `JournalEntry.GetName`.
  Read the live GUI's `JournalEntry.GetCountry` in that selected text instead,
  following Vanilla's `JOURNAL_ENTRY_TOOLTIP` -> `JOURNAL_ENTRY_STATUS` pattern.
  Direct native JE titles using SCOPE do not establish that it survives a nested
  localisation call. Do not substitute GetPlayer, which can name another
  country's JE incorrectly. Context tests must discard temporary script bindings
  on the nested call while retaining the widget's JournalEntry; the earlier test
  incorrectly forwarded the script scope and therefore passed a broken route.
  The new GUI-context route still requires DP's in-game rendering check.
- Show scaled effects from the applied timed modifier, not the unscaled static
  definition. The installed engine exposes `Country.GetTimedModifier(string)`
  and `TimedModifier.GetDesc`. Hide remove/reapply maintenance in the shared
  recalculation helpers so actions do not preview losing and regaining identical
  effects. Preserve execution and test it separately from tooltip visibility;
  actual lobby and modifier-description rendering still needs DP verification.
- Exposed `has_variable`, variable comparisons and `any_in_list` conditions can
  render as generic variable text or missing-localisation errors. Wrap each
  player-facing requirement in a named `custom_tooltip`; preserve the predicates
  inside it. Check readable failure reasons as well as whether a button works.
- CMF's `com_journal_scripted_buttons` widget adds another renderer; placing it
  in `custom_widget_container_2` does not replace the default JE button grid.
  Use the default grid alone unless deliberately configuring a replacement.
  The Prerogative JE now removes the redundant widget; rendering awaits DP.
- A progress bar's `desc` labels the bar itself. The normal hover text comes
  from `GetPeriodicProgressBreakdown`, which lists declared weekly/monthly/yearly
  progress. A bar projected with `set_bar_progress` from a shared situation has
  no such breakdown. Use a local widget tooltip for its explanation; adding
  periodic progress solely to populate the tooltip would also change the bar.
- A hidden effect is still evaluated for tooltip construction. The refugee helper
  initialized a counter during execution, but its tooltip read that counter when
  no initialization had happened. Put reads behind an existence-guarded branch.
- Likewise, an unguarded named-container lookup after `create_container` can fail
  in preview. Initialize in the supported creation context and guard later reads.
- Delayed retries must supply every localization scope they use. Do not assume
  the original foreign event's saved country scopes accompany a monthly retry.
- Hide internal cleanup effects, such as `destroy_container`, from option text;
  use authored tooltips to communicate the actual gameplay consequence.
- Internal random scheduling can also leak into option tooltips. The Chiefdoms
  follow-up helper exposes four equal cooldown branches as “25% nothing happens.”
  That lottery schedules the next incident; it does not decide whether the current
  incident's main effect succeeds. Hide scheduling and display the real outcome.

## Check native identities and mechanics before duplicating them

- Renaming an IG or increasing its attraction does not change `pop_potential`.
  Vanilla 1.14.3 PB excludes aristocrats and most subsistence peasants. A chiefly
  constituency needs eligibility reviewed before attraction or strength tuning.
  IG strength, relative clout, supporter attraction and pop profession are distinct:
  a +25% strength modifier neither adds 25 clout points nor changes occupations.
- Treat a law variant's military package separately from its political purpose.
  SB Amabutho and Vanilla National Militia differ sharply in recruitment and
  building caps. Copying the latter for chiefly political influence would also
  change military capacity; record and agree those consequences explicitly.
- Vanilla already defines `ZUL_zibhebhu_kamaphitha` with a character usage path.
  SB separately creates `ZUL_zibhebhu_ka_mapitha`. The 1878.11.1 test save contains
  both as politicians, neither with the ruler role. Reconcile the creation paths;
  do not infer the installation failure's exact cause from duplication alone.
- Native Liberty Desire already includes economic dependence and endpoint scaling
  in `liberty_desire_weekly_change`. Replacing a scripted bar requires removing
  duplicate contributions and accounting for weekly versus monthly units. A raw
  modifier contribution is not necessarily the final displayed weekly change.
- The same native calculation checks the exact `lobby_pro_overlord` and
  `lobby_anti_overlord` types. New lobby IDs sharing their categories would not
  automatically receive those LD contributions. Prefer scoped names for native
  instances. Native maintenance also disbands lobbies whose members are all
  marginal; creating the requested membership is not proof the bloc will persist.
- A saved payment modifier proves it was applied, not that the intended bilateral
  cash transfer changed. Verify both countries' actual payments and modifier scope;
  Vanilla's Decrease Payments pact provides a targeted reference implementation.

## Preserve state across annexation deliberately

- Character-valued variables are references, not backups. The Klip archive kept
  Mpande/Cetshwayo IDs, but both character records were absent after annexation;
  the Crown option could only leave the generated ruler. The intermediate custom
  annexation/custody attempt was superseded by Return State plus Make Protectorate.
  Keep ZUL alive through this choice; do not reintroduce custody machinery.
- Capture both ruler and heir before transferring or exiling either: removing
  the ruler can change the heir accessor through succession. Restore the archived
  characters after country creation and subject setup. Do not consume the archive
  in the creation baseline before those steps have finished.
- A character hosted in CAP is no longer found by exile-pool-only searches.
  Follow the explicit host when returning the king; otherwise successor fallback
  can replace a surviving original. Static ordering/reference tests cover the
  transfer contract; engine survival and return still require DP's verification.
- Annexation can remove the country and its court before a restoration event.
  Archive the royal house and story-specific firearms state before the relevant
  annexation, then restore those records when recreating ZUL.
- Create the intended state footprint explicitly. A general Release Country UI
  action may include historical territory outside the settlement's agreed area.
  Compare Vanilla and Gates of the Bosphorus creation examples against the exact
  installed version before choosing scope and origin arguments.
- Do not release and re-annex a country merely to present a direct-rule choice.
  Owned territory and an existing protectorate need different entry handling,
  even when they share the final settlement branches.

## Founding countries: technology and commandos

- Setting a governance law before installing a historical ruler does not ensure
  the appointment survives the native post-government-change callback. In
  1.14.5, `gov_crown_colony` calls `post_change_to_presidential_elective`, which
  selects a ruler again unless `keep_current_ruler_var` exists. British Natal
  installed Martin West after its law changes, yet the June 1848 save has a
  Landowner ruler while West remains AF leader. Set Vanilla's temporary
  seven-day protection on the current country before conversion and leave it
  through the refresh; do not remove it in the same effect or keep reinstalling
  the governor monthly. The unprotected callback is confirmed in source; its
  timing in this playthrough is inferred from DP's observation and the saves.
  Corrected engine retention still requires replay from before conversion.
- `keep_current_ruler_var` is specific to native ruler-selection helpers. In
  1.14.5 the presidential, parliamentary and ordinary dictatorial post-change
  helpers read it; `post_change_to_hereditary` does not. ZUL's Chiefdoms and
  monarchy routes therefore cannot be protected by adding this variable.
  Use temporary protection only where a named appointment or explicit retention
  must survive a government refresh. Ordinary constitutional succession and
  generated-country ruler selection must remain available. The Boer refresh
  previously removed its guard in the same effect, leaving later callbacks
  unprotected. Its protection now expires after seven days, as do the guards
  placed in the named Boer, Albany, German SWA and Klip founding/appointment
  paths. Write to the receiving country, not the foreign event ROOT. Source
  scope/lifetime checks cover these changes; engine retention remains pending.
  See the broader audit and implementation in the governor report.
- Compare completed research, active research and the founding date before
  diagnosing missing inheritance. In the 17 October investigation, ORA, NAL
  and TRN had the same 16 completed technologies; Empiricism was still being
  researched by ORA. The lack of explicit technology grants in a helper is not
  evidence that `create_country` with `origin` failed. Do not replace native
  inheritance with a fixed technology floor based on that assumption.
- Create the authored commando before commissioning or transferring its
  general, then assign the final commander to the saved formation. NAL's save
  contained an empty default army created at the same time as its commando;
  the old founding order installed Pretorius first. TRN and the shared ZPB/LYD
  baseline also commissioned generals before their authored formations. Keep
  TRN's Andries/Marthinus selection before commander assignment so an early
  muster does not unnecessarily commission the fallback son. Static ordering
  tests cover these corrections; prevention of engine-created empty armies
  still requires DP's replay from before country formation. Do not sweep-delete
  existing formations. KLR's civilian founder is not this commissioning case.

## Verification must follow the whole chain

- Check each side's primary demand separately. The authored ZUL–SWZ conquest
  play never assigned SWZ's intended humiliation counter-demand; the autosave
  instead showed SWZ demanding a ZUL state. Assign the defender's primary goal
  in the exact launch callback and remove only its unwanted opening conquest.
  Keep ZUL's conquest and later territorial recapture mirrors intact. Static
  checks cover holder/target and removal scope; engine setup and settlement still
  require DP's check from before the play starts.
- Presence tests cannot prove runtime actor identity or delivery. Test foreign
  roots, normal colony status, held popups across monthly pulses, failed dispatch,
  replacement tags, and duplicate consumption using the actual script references.
- Inspect saved event creation/expiry dates, scopes, country flags, and play
  records together. Error-log timestamps alone do not identify the saved route.
  Preserve evidence before a new autosave overwrites it.
- Separate observed engine results, static verification, and pending scenarios.
  DP confirmed the simplified Klip follow-up works; that does not establish that
  every later chiefdom or settlement branch works. Game launches and engine
  testing remain with DP, as required by `AGENTS.md`.
- An already-open popup retains saved scopes. Reloading script text does not
  convert an old container receipt into a country receipt or undo a completed
  settlement. State the checkpoint required for a meaningful retest.

## Rebases and localization

- Compare upstream semantics before refreshing inventory hashes. Exact-path
  files, keyed replacements, GUI types, and dependency patches can overlap in
  different ways; a matching filename inventory alone is insufficient.
- Keep compatibility fixes reproducible and distinguish patched CMF from the
  immutable upstream release. Do not let ordinary synchronization erase the patch.
- Rebase every effective layer of a copied definition. In 1.14.3, updating CMF's
  cultural-majority movement alone leaves SB's CAP-specific replacement using the
  old API. Six comparisons now require an explicit target_country = owner; the
  value accessor takes (owner). Verify the installed Vanilla examples and preserve
  each layer's intended additions.
- A missing historical Steam manifest is not current-build corruption. Keep old
  evidence/schema checks, condition only historical reproduction on exact retained
  inputs and old installed-payload checks on their exact build. Current-target
  manifest and payload checks must remain mandatory.
- Preserve DP-reviewed prose and its exact namespace boundaries. A variant should
  use separately tracked new localization when the existing text remains valid
  for another route. `(DP) REVIEWED` and other supported markers must be classified
  explicitly rather than moved to make a bookkeeping check pass.

For detailed evidence, see the Klip, Natal refusal, Port Natal, and 1.14.2/1.14.3 reports
in `Docs/compatibility/`.


## Native movement contests and international journals

- Movement history can explicitly create a movement despite its normal
  `creation_trigger`. Excluding Zulu Absolutists only in that trigger leaves a
  launch duplicate until the disband check. Guard the specific history call
  using pre-bootstrap institutional eligibility; preserve all other countries
  and movement setup. Compare the complete history shadow against Vanilla and
  register its hash contract. Static parity does not prove engine load order.
- A movement record in a save database may already be dead. Check the manager's
  `dead.dead_objects` and `death_date` before treating record presence as survival
  or its cleared supporters as the cause of death. The July 1850 Klip checkpoint
  retains a Zulu movement that died on 16 June; August removes the record.
- Reusing an existing movement does not renew its native minimum-support grace.
  An attraction modifier's duration is separate from movement age. In 1.14.5,
  cultural movements must maintain 10% support within their culture after the
  twelve-month grace, independently of their scripted `disband_trigger`.
  Annexation enlarges the culture-specific support denominators. Dilution of the
  old movement's backing is the leading, not numerically replayed, explanation
  for the early Klip annexation disappearance; see the
  [17 October investigation](Docs/compatibility/zulu_national_movement_2026_10_17.md).
- Do not describe Initial Enthusiasm as a survival guard or assume it can renew
  movement age. No creation-age reset effect was found in the inspected 1.14.5
  effect registry; `set_movement_defeated` changes a different date. A proposed
  grace renewal must remain unverified until an exposed mechanism is established.
  Recovery after deletion and protection through an actual supporting character
  have different gameplay consequences; see the
  [annexation exploration](Docs/zulu_annexation_movement_exploration_2026_10_17.md).
- A false movement `disband_trigger` is not a veto on later native removal checks.
  The 1.14.5 category parser reads `minimum_support_to_maintain` as a fixed-point
  number, not a scripted value. A temporary variable cannot conditionally change
  that native threshold. Do not ship a flag-only guard that leaves the actual
  low-support deletion path untouched, or broaden all cultural-movement rules
  silently to work around it.
- A country-level initial-enthusiasm marker can outlive the movement it originally
  seeded. If a later authored settlement explicitly grants enthusiasm to a new
  instance, handle that in its absent-movement branch; do not clear the shared
  marker or refresh every existing movement. The annexation package uses the
  existing once-only settlement gate. Native recruitment is gradual, and no direct
  supporter-assignment effect was found in the inspected 1.14.5 interface. DP
  subsequently reports that the +100% attraction package still permits removal;
  its static tests establish branch/grant behavior, not movement survival.
- Replacing a movement requires actual deletion before creating the same identity.
  In 1.14.5, no direct scripted disband effect was found. The native
  `on_disbanded` callback runs **before** the manager removes the old instance,
  and `create_political_movement` refuses an already-existing identity. Mark only
  the intended movement for its `disband_trigger`, then schedule creation from
  its owner on the following day. Consume the delivery marker before creation;
  never mark the replacement or turn subsequent ordinary deaths into a revival
  loop. Native creation bypasses spontaneous-formation support checks, but native
  recruitment and subsequent survival still require engine verification.
  The NAL annexation replacement preserves the CMF body outside these two hooks;
  a partial `INJECT` cannot overwrite its already-read disband trigger (the native
  parser reports "Trigger section already read earlier"). Test full-body parity,
  foreign event roots, unrelated movements and duplicate delivery.
- Country-level "already applied" flags survive movement replacement while the
  old movement's modifiers do not. Shepstone's refusal/repeal helpers therefore
  skip a replacement after an earlier grant, losing any unexpired attraction.
  This interaction is confirmed in source; DP's successful early replacement
  replay does not verify those branches. Clearing the flags would renew the full
  grants, not preserve their remaining strength and expiry. The annexation
  replacement now records grant expiries for Initial Enthusiasm and the two
  Shepstone bonuses, snapshots them to the owner before deletion, then restores
  only the unexpired remainder. Country flags stay set. Time continues through
  the hidden receipt; temporary owner/scratch variables are consumed afterward.
- GUI timed-modifier accessors are not event-script APIs. In the inspected 1.14.5
  native `CModifierValueLink::GetScope`, `modifier:` does not support political
  movement scope either: do not snapshot aggregate attraction through it or
  infer individual modifier duration from that total. For these three known
  grants use the recorded game-day expiry, `remaining / original_days` multiplier,
  and remaining duration with `is_decaying = yes`. Script years are 365 days,
  months 30; the refusal's 300 months are 9,000 days, not 25 calendar years.
  Keep restoration separate from the fresh annexation bonus. This preserves
  day-level expiry/linear decay with fixed-point rounding, not sub-day timestamps.
  Untracked old-save grants cannot be recovered exactly; do not invent full
  durations. Native delivery and values still require DP verification.
- `add_modifier` duration fields do not parse a bare `var:` link. DP's 18 October
  launch rejected the three preservation calls with "Named value not found".
  Pass a named script value whose formula reads the movement variable instead.
  Installed `CJominiScriptDuration::Read` resolves a number or named value;
  `GetDaysWithScopes` evaluates that named formula at execution. This keeps the
  existing expiry arithmetic without polling or renewing grants. Tests must
  reject bare variable durations, not merely emulate their intended arithmetic.
  A fresh engine check of the corrected formula remains DP's responsibility.
- A law with `parent` inherits ideological stances; explicit stances on the child
  are rejected at load. This matters especially when the proposed child must
  oppose its parent: Elder Council itself inherits Autocracy. The two authored
  chiefly constitutional laws therefore need independent definitions to keep
  their approved royal/chiefly divisions. Do not remove a longstanding army-law
  parent casually: it also participates in native family checks and IG behavior.
  DP approved Traditionalist `++` on the shared Peasant Levies family: author it
  on `law_peasant_levies` and let Amabutho inherit it.
- `ordered_in_list` with an unavailable `position` caps at the last available
  item, logging a warning and potentially assigning the same character to several
  choices. The successor menu now iterates each candidate once, ordered by
  prominence and bounded by `max = 12`. `check_range_bounds = no` allows a shorter
  list; it is not a fix for repeated positional lookups. Clear old menu selections
  before rebuilding them. Test zero, one, two, full and oversized candidate lists.
- Removing an absent timed modifier logs a script error. Zero Prerogative has no
  institutional modifiers, so unconditional removal during recalculation and exit
  floods the log. Guard optional removals with `has_modifier`, including named
  following recruitment and coup resistance. Test repeated neutral updates and
  repeated cleanup with a fixture that rejects absent removals.
- Law-activation callbacks also run during history setup. Reconciling the Zulu
  institution then can add its JE before country history adds the authored opening
  JE. Gate this callback on the existing post-lobby bootstrap marker; history
  remains responsible for the opening entry and post-lobby reconciliation for
  dynamic setup. This is initialization ordering, not a new gameplay prerequisite.
- Use the documented JE pin field
  `should_be_pinned_by_default_uninvolved_or_context`. A custom `complete` trigger
  also makes automatic `_goal` localisation redundant, even with a numeric
  progress bar. Keep the intended text in the referenced status/progress field;
  do not alter the completion condition merely to silence the warning.
- Trace every caller before converting a shared political effect. Chiefdoms'
  `sb_zululand_shift_liberty_usuthu_5` is used by skirmishes, defections and refugee
  returns. Replacing it with one activism modifier would also change the refugee
  route, even though recruitment is the proposed consequence there. Inventory
  narrative callers as well as direct LD writes; the new mappings remain design
  proposals until implemented and verified.
- A projected modifier breakdown must reflect current modifier strength. The
  Chiefdoms attraction display currently reports a hardcoded +50% while the
  contest is active. Adding decay to its source modifier would make that display
  stale; inspect the live decayed value rather than treating an active flag as
  proof of full strength. This is a confirmed source-level dependency, not an
  observed engine defect in the still-unimplemented decaying version.
- Liberty Desire describes the subject relationship, not membership of a domestic
  faction. A high-LD chiefly government and a low-LD restored monarchy are both
  coherent. Do not label either as a faction victory from LD alone. Native
  `political_movement_support` also combines popular, military and wealth support;
  do not label it as only popular support.
- Subject-type eligibility can depend on the **overlord's** country type. In
  installed 1.14.3, Vassal requires an unrecognized overlord; Puppet accepts a
  colonial overlord such as NAL. The subject being unrecognized does not make
  Vassal the correct native relationship automatically.
- A copied movement ideology brings active-law satisfaction with it. In 1.14.3,
  positive stances on inherited laws lower calculated activism; opposition to two
  newly imposed laws does not erase approval of unrelated retained laws. Inspect
  the full native breakdown before attributing low activism to one factor.
  `character_ideologies` lists possible ideologies for pressured IG leaders;
  it is not a list of automatically stacked core movement platforms.
- Movement pressure is not a second IG or an exhaustive division of its clout.
  Installed 1.14.5 documents `can_pressure_interest_group` with an IG root and
  reads `movement_pressure(scope:ig_for_calc)` in law negotiations. Two movements
  can be designed to target LO; national movement support must not be presented
  as their respective shares of LO. New ZUL definitions still need engine checks.
- Copying the Carlist guerrilla modifier does not copy its no-occupation rule.
  In 1.14.5 that rule is a separate Spanish-JE check in `battle_victory_score`;
  battle conditions, scoring and escalation have further Spanish dependencies.
  Any future adaptation must isolate the intended conflict from unrelated wars.
  These are source findings, not a tested ZUL port; see the
  [crown-and-chiefs exploration](Docs/zulu_crown_and_chiefs_exploration_2026_10_18.md).
- Japan's daimyō cache holds one loyalty value per state. Copying its assignment
  loop for several ZUL chiefs in the same state would overwrite earlier values;
  aggregate the actors before writing a shared recruitment input. Its native
  movement factors are attraction multipliers, not direct support transfers, and
  its loyalty input reverses when the emperor is in power. These are confirmed
  1.14.5 source findings, not an engine-tested ZUL adaptation; see the
  [B development](Docs/zulu_chiefly_coalitions_design_2026_10_18.md).
- Native character loyalty is not a pure personal-allegiance measure. Installed
  1.14.5 derives it partly from IG approval and enacted/enacting-law agreement;
  ruler popularity also already affects native Authority capacity. A proposed
  personal-cooperation system must distinguish constitutional preference from
  endorsement of a particular ruler and avoid counting popularity repeatedly.
  These are source findings, not a tested custom loyalty model; see the
  [institutional exploration](Docs/southern_african_institutions_and_zulu_politics_2026_10_18.md).
- `state_literacy_growth_add` is additive. Installed 1.14.5 supplies a base
  contribution of `0.0005`; subtracting half that contribution does not establish
  a 50% reduction in the final literacy growth rate after all modifiers. Education
  access, literacy growth, research speed and technology spread are separate
  controls. Verify the final engine breakdown before describing a proposed
  adjustment as a percentage reduction; no new education penalty was tested.
- Promote Social Mobility in installed 1.14.5 adds 0.25 Education Access and
  0.25 to the qualifications multiplier; it does not directly modify literacy
  growth speed. Its eligibility block runs in state scope, so a country-JE gate
  must inspect the owner and preserve the existing Vanilla restrictions. Whether
  a newly invalid active decree is removed needs engine verification. The
  institutional-JE gate is now implemented with native-body parity tests;
  weekly invalidation and ownership changes remain pending DP.
- Do not use one owned state as a blanket bar to ideological civil war. DP
  confirms that a one-state country with multiple provinces can undergo an
  ideological revolution, distinguishing it from secession (18 October 2026).
  The planned ZUL character, province and army routing remains untested; that is
  a separate question from whether a second owned state is required.
- International journal pulses can have **no country root** (see the installed
  `journal_entries.md`). Select the owning story actor explicitly before invoking
  a country helper; testing `country_definition` at the pulse root silently misses
  the global situation. The Chiefdoms weekly pulse now enters `c:NAL` explicitly.
- Script-value order matters: `value = 200` after a claimant-specific `add` resets
  the accumulated result. Initialize first, then add or multiply. A structural
  order check prevents the uSuthu claimant preference from being erased.
- Customizable-localization functions do not support `REPLACE:` prefixes. Use an
  inventoried exact-path shadow where a native function must change, and compare
  every untouched function plus the changed function's native fallback branches.
- Native subject drift identifies pro-/anti-overlord lobby **types**. Renaming
  those native lobbies preserves their clout contribution; inventing equivalent
  custom type names does not establish equivalent Liberty Desire behaviour.
- A movement's `political_movement_radicalism_add` changes calculated activism
  pressure; it is not a direct assignment to current activism or a monthly
  increment. The takeover must check actual `political_movement_radicalism`.
  Keep pressure, support, attraction and native LD distinct in UI and tests.
- For an automatic terminal settlement, reserve and apply it in the event's
  immediate effect; its acknowledgement must not repeat gameplay effects. Guard
  still-open earlier incident options against an already-ended contest. This
  avoids invented fallback choices and permanent pending popups blocking timers.
- Native civil-war initiation can race an event-based takeover. Suppress that
  initiation only for the designated contest movement while its contest flag is
  active; restore ordinary political behaviour after resolution. Static checks
  establish scope and threshold ordering, not same-tick engine execution.

- Check the **effective dependency definition**, not only Vanilla, before adding a
  replacement. CMF also replaces the absolutist movement and supplies Bavarocrat
  eligibility plus Grey PLP support/state-weight hooks. The ZUL exclusion must
  retain those hooks; the uSuthu derivative preserves them too. Pin the dependency
  object and compare the whole replacement after undoing only the intended gates.
- A count of 120 month-boundary pulses can expire before ten full years have
  elapsed. Use a ten-year timed marker for the actual deadline; a monthly counter
  may remain as approximate presentation. Test both dates disagreeing and victory
  taking precedence when the expiry and 99% threshold coincide.

## Rebase evidence and nested native triggers (16 October 2026)

- A retained depot delta covers only its two exact manifests. Steam may evict the
  earlier baseline. A 1.14.4→1.14.5 delta alone missed the fleet transports absent
  from SB's older 1.14.3 shadow. Compare every pinned override/source contract as
  well; preserve the historical report rather than relabeling its endpoints.
- Historical reproduction may skip when its exact input is absent. Current
  target build, manifest integrity and installed payload checks must fail instead.
  Keep active compatibility checks separate from historical test skip conditions.
- Trace nested trigger calls when porting native AI logic. In 1.14.5 the ordinary
  and colonial incorporation gates also call ai_can_incorporate_state; its old
  description as a scoring-only helper is no longer complete. Test native culture,
  population and same-owner adjacency boundaries alongside SB's regional exceptions.
- A changed generated naval-network hash is evidence to review, not evidence of
  a broken SB port. Verify graph structure and every authored port before repinning;
  keep malformed/disconnected rejection checks. Connectivity does not prove that
  AI armies will deploy or naval missions will complete in the engine.


## Resource capacity is not undiscovered reserves (18 October 2026)

- In installed 1.14.5, `add_resource_potential` and `change_resource_potential`
  initialize/change capped capacity, including for a discoverable building group.
  They do not fill `undiscovered_amount`. Native discovery reads a separate reserve
  count; merely changing the building group cannot hide those capacity grants.
- Use native state-region resource entries with `undiscovered_amount` and the
  resource building's technology requirement when discovery itself must be gated.
  The diamond revision uses three otherwise equivalent mine definitions for its
  three technologies; Kimberley keeps its original event-driven mine. Preserve
  shared mining bonuses and company coverage when introducing these definitions.
- Native inspection confirms the distinct fields and technology checks; static
  script tests do not demonstrate discovery timing, split-state allocation or
  foreign-investor behavior in a campaign. See the dated diamond discovery report.
  The same pre-existing gold/oil capacity issue remains outside this revision.


## Ongoing institutions and constitutional wars (18 October 2026)

- `on_law_activated` has a **Law** root. Enter its `owner` before country predicates, variables or institutional recalculation; test a foreign root rather than merely checking for an effect name.
- A projected JE bar must not also own native monthly drift. Keep signed political state on the country, update it once per country pulse, and project after recalculation. Otherwise UI and country values can tick twice or in different orders.
- The UI calls it Activism, but its native current-value accessor is `political_movement_radicalism`; `political_movement_activism` is not a script accessor. Verify display adapters against installed script/API examples and Tiger, not only a test fixture that could repeat the same invented spelling.
- Clamp Institutional Reach after combining deductions: Local Police's negative deduction offsets modernization, but cannot exceed the ceiling. Explicit institutional exits are separate from the arithmetic.
- Native `add_journal_entry` bypasses normal eligibility; check eligibility at the caller. An invalidated institutional JE must not emit a completed faction result or reset its retained registry/seed flag on re-entry. Engine delivery remains pending DP.
- A revolutionary opponent's movement is not an absent constituency. Track the specific constitutional conflict and its actual countries; suppress peaceful consolidation until that conflict has a real result. Use current-country identities after revolution, not an assumed `c:ZUL` survivor.
- Keep coup leader and intended beneficiary separate. Civilian chiefs use only applicable native coup-strength components. Do not add Prerogative resistance twice when legitimacy already feeds the native formula. Installed 1.14.5's `commander_coup_strength` gives its unassigned +2 outside the general/admiral gates, and regional ownership uses `root.owner`; calling it for a civilian from a country-root callback is therefore unsafe. SB guards the entire rank/location group and captures the actual character in a temporary scope. Script-derived tests cover civilians, deployed/unassigned commanders and foreign roots; engine coup delivery remains pending DP.
- Character allegiance to an incumbent or claimant is distinct from native loyalty and from constitutional ideology. Count each following through one representative; native agitator attraction must not be duplicated by a scripted claimant/network bonus.
- Permanent incorporation rewards belong to the beneficiary country as entitlements; state modifiers are their current ownership-dependent application. Reapply/remove on ownership changes without giving a new reward or starting an expiry.
- Earlier entries about a ten-year uSuthu deadline describe the retired implementation. The current Chiefdoms contest has no deadline and no instant activism-threshold takeover. Preserve that historical debugging evidence without reintroducing its obsolete mechanics.


## Court transitions, prices and initial traits (25 October 2026)

- A scripted-effect parameter is substituted where it is used. Passing `PATRON = ruler` into a helper that then enters a character loop no longer refers to the country’s ruler. Capture that character in a scope before the loop. A source-executed foreign-root test caught this in campaign recruitment; test the resulting patron identity, not just the effect’s presence.
- An explicit template trait list does not alone suppress Vanilla’s initial random trait generation. Override `trait_generation` only on the authored templates and retain native experience/Child bookkeeping. Do not shadow the global default to stabilise thirteen people. Static template checks do not prove later engine ageing.
- A long-delayed conditional event can lose eligibility between scheduling and delivery. Keep the selected deck card and due timer on the country, choose live participants at delivery and revalidate those same people before effects. The original stale-price confirmation requirement was superseded by the later 25 October instruction: keep the opening cash quote, while revalidating the named participants.
- Native Pop Attraction is exposed by `political_movement_pop_attraction_mult_desc`, not an invented `concept_political_movement_pop_attraction`. Use the established nested modifier tooltip when no game concept exists. Tiger caught the invented concept; engine tooltip rendering still needs DP.

## Historical identities and IG appointments (28 October 2026)

- A matching first name is not an existing historical identity. Sigananda kaZokufa of the amaCube is distinct from SB's fictional Sigananda Zulu in the Mbuyazi fallback line. Check lineage, dates and constituency before reusing a template; preserve separate identities where those differ.
- Native IG leadership already contributes +25 Prominence in the installed build. Do not add a second scripted office bonus or equate the IG's Clout with its leader's following. Appointment, constitutional alignment, present allegiance and future pledge remain separate records. Source checks cover registration and arithmetic; actual appointment selection remains a DP engine check.

## Dated descendants and release evidence (28 October 2026)

- A dated character template is not a birth scheduler. Dinuzulu and Solomon had templates and roster readers but no ordinary creation path. Trace template → eligible creation → exported character handle → registration/recognition. Guard known births with `is_template_used`, not merely absence of a living local character, so death or exile cannot recreate an identity. Record generated-newborn receipts on the parent rather than blocking every subsequent ruler of the country.
- Recognition of a minor and eligibility as an adult claimant are different checks. Allow designation without counting a newborn's Prominence or admitting every unrecognised child to a claimant war. Reuse the named identity and existing regency.
- Post-war autosaves cannot establish the original recruitment split. A reunited state's military Pops and buildings can reflect native employment, migration and AI construction after the event. Preserve dated snapshots around preparation and rebel creation before attributing an apparent mismatch to the transfer effect. DP approved live activation here while leaving that particular engine check pending.
