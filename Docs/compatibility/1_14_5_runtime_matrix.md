# 1.14.5 fresh-game runtime matrix

Target: SB 0.20.2; game 1.14.5, build 25629520, branch 1.14-openbeta,
core manifest 5521822647051867164; CMF 1.66.0 + sb-1.14.3-r1.

DP performs all launches and engine verification. Use a new campaign on this
exact stack; for Klip River, save a checkpoint **before the punitive play starts**.
Historical observations do not certify this build. No old-save migration or
character reconstruction is included. All rows start pending, including cases
carried forward from the 1.14.3 matrix and the existing story-war matrix.

Use the installed beta's expiry rules: no goal is dropped before the war has
lasted 24 months; a goal can expire after 12 months without contest since creation
or its last contest, with three months' warning. This is not a fixed deadline
for every war to end. Do not use the announced 1.15 reversal
as the expected behavior. Record notifications, goal ownership, timers, callbacks
visible in logs, peace outcome, actual territory/subject type and reward delivery.

| ID | Scenario and acceptance condition | Result |
|---|---|---|
| B145-01 | Fresh launch/new 1836 campaign; verify versions and audit fresh error/warning logs. Save/reload within this campaign. | **Engine pending — DP** |
| B145-02 | Annex/Conquer/Return infamy uses GDP/population shares; compare consequential/inconsequential states, claims and intended story exemptions. | **Engine pending — DP** |
| B145-03 | Native timers, territorial mirrors, recapture, reversal and split-state reconstitution; conquest radicalization reverses when land is retaken. | **Engine pending — DP** |
| B145-04 | Uncontested goal expiry, resulting war behavior and capitulation with pending/expired demands. Only actually enforced, unreversed demands produce story outcomes; no expired or partial demand grants missing territory, subjects or rewards. | **Engine pending — DP** |
| B145-05 | ORA–BST: occupy BST's Vrystaat while leaving Drakensberg unoccupied; record both timers, any expiry and transfers. | **DP retest, 2026-10-17: issue persists; workaround ON HOLD** |
| B145-06 | Revoke Claim remains assent-only; diplomatic demands resolve correctly. | **Engine pending — DP** |
| B145-07 | Klip setup: allied Make Protectorate (GBR may become holder after play leadership changes) and NAL Return State on ZUL-owned Natal are both primary; ZUL's Return State is secondary. Zulu backdown concedes both allied demands; British backing persists. | **Saved primary/secondary setup confirmed 2026-10-17; backdown pending — DP** |
| B145-08 | Klip negotiated victory, capitulation and timers in either order: record the actual allied victory before government choices, including a GBR protectorate awaiting handoff. Government event waits for the NAL handoff and occurs once. Partial enforcement, expiry, reversal, defeat and white peace grant no missing demand. Unrelated wars do not block settlement. | **Saved false `.081` confirmed; source correction 2026-10-17, engine replay pending — DP** |
| B145-09 | All three Klip government options: direct annexation; chiefdom puppet/Zibhebhu/CAP exile; Crown preserving actual king/heir and protectorate. Crown gives ZUL +15 relations with NAL and GBR, retains NAL's +10% Zulu loyalists and gives no loyalist bonus in ZUL. Check the three concept-linked option tooltips and Pop Attraction hover. After each choice, recorded Klip victory survives monthly pulses without `.081` or duplicate government events. Exercise existing Chiefdoms/NRP paths without the deferred redesign. | **Chiefdoms false-result regression reproduced; Crown source update 2026-10-17; corrected engine replay/UI checks pending — DP** |
| B145-10 | Great Trek: ORA's qualifying MTB victory delivers sb_great_trek.002 once; partial/expired/reversed goals do not count as a qualifying victory. | **Engine pending — DP** |
| B145-11 | Blood River: opposing countries/Natal targets correct; Oranje victory delivers Natalia once, including guns-bargain route. Failed/reversed settlements grant no unearned formation event. Test Rally immediately and at three-month popup expiry while ORA still fights PHL/BST; unrelated ZUL conflicts must also not block it. | **Partial DP result, 2026-10-16 21:35: reached Natalia formation; remaining cases pending** |
| B145-12 | Post-Blood River ZUL–SWZ: ZUL demands conquest of SWZ; SWZ demands humiliation of ZUL, with correct target countries and once-only resolution. | **Engine pending — DP** |
| B145-13 | Existing story-war matrix: victory, defeat, white peace, backdown, timer enforcement/reversal and exact subject restoration. Terminal settlement occurs once; missing or expired goals do not fabricate success. | **Engine pending — DP** |
| B145-14 | Native AI incorporation: ≥50% primary culture; ≥25% with same-owner incorporated adjacency; homeland/year eligibility; ordinary population minimum; colonial region/adjacency/eligibility paths. Test each boundary and unrelated-country controls. | **Engine pending — DP** |
| B145-15 | Four SB priorities: NAL/Zululand, CAP/Bechuanaland and Griqualand West, ORA/Drakensberg. Human, wrong-owner and unrelated-state cases retain native behavior. | **Engine pending — DP** |
| B145-16 | Colonial claims: acquire-states regional objectives affect native AI scoring. Boer claims remain unavailable in SB's authored regions; other cultures/regions retain native eligibility. | **Engine pending — DP** |
| B145-17 | Scramble remains active during wartime loss of its qualifying African territory; after war, native failure applies if territory is still absent. SB growth modifier persists while active and clears on completion/failure. | **Engine pending — DP** |
| B145-18 | AI demands, play backing, treaty selection and state values inherit current Vanilla changes. Cultural-majority API remains valid, CAP exclusion retained. | **Engine pending — DP** |
| B145-19 | Eligible buildings hire; individual/bulk production-method controls remain usable with CMF's GUI customizations. | **Engine pending — DP** |
| B145-20 | Native European transport ships appear at start; Portuguese army redistribution/African formations persist. Naval transports complete, merge and honor return-home controls. | **Engine pending — DP** |
| B145-21 | AI CAP mobilized armies deploy to immediate fronts, including Natalia refusal; distinguish stationary mobilized armies from demobilization and record orders/transport availability. | **DP retest failed, 2026-10-17: deployment issue persists after Natalia refuses Britain** |
| B145-22 | Replay from before Boer country formation. NAL peaceful/Blood River/guns-bargain routes, TRN with Andries or Marthinus, ZPB and LYD each receive one intended commando and no empty default army; existing unit packages and final commanders remain correct. Also inspect KLR/NRP/SGO for extra formations. | **Engine pending — DP; source ordering corrected 2026-10-17** |
| B145-23 | Reported Natalia technology loss: ORA, NAL and TRN have identical completed sets including Academia. DP confirmed the technology was Academia, not Empiricism. This closes the reported bug, without claiming engine verification of every other founding route. | **Closed — DP correction, 2026-10-17; no inheritance fix required** |
| B145-24 | Convert Boer Natalia into British Natal, including the refusal/war outcome; also check direct British colony creation. Martin West remains ruler and AF leader after government refresh and beyond seven days even with stronger Landowners. No recurring reinstall; later legitimate succession remains available. | **DP observed replacement; source correction 2026-10-17, corrected engine replay pending** |
| B145-25 | Replay named Boer founding (NAL peaceful/Blood River/guns, TRN, ZPB, LYD, SGO), a Boer government refresh, Albany's transferred/created Godlonton, all three German SWA governor date branches, and Klip River's Spies. The appointed ruler survives the government refresh and remains after the seven-day guard expires; later normal succession works. Guards belong to the receiving country despite foreign event roots. Non-German SWA and Zulu retain their existing rules. | **Source guards applied 2026-10-17; engine replay pending — DP** |
| B145-26 | With grants made under the new scripts, replay NAL direct annexation: one fresh native movement after the disband callback, or immediate creation if absent. Initial Enthusiasm and both Shepstone attraction bonuses retain their remaining strength and expiry (whole-day precision), alongside a fresh +100% / twenty-year Annexation of Zululand bonus. Expired or removed bonuses stay absent. Check pending save/reload and delayed delivery, early Klip and later Anglo-Zulu, first-year survival, no duplicate renewal and no resurrection after later ordinary death. Old checkpoints without grant records cannot test preservation. | **A failed; DP reports early B works; three-modifier preservation implemented. Testing TODO — explicitly deferred by DP, 2026-10-17; no result claimed** |
| B145-27 | Fresh campaign. Give an eligible foreign investor Pumpjacks while West Transvaal's owner has only Prospecting. Expect zero discoveries. Give the owner Pumpjacks mid-year and check its regional anniversary, 0–364-day delivery, toast and capacity for a single Diamond Mines building. From a pending find, save/reload and transfer its province to an eligible and an ineligible owner in separate runs. Check split-state construction, one regional roll, reserve exhaustion at 20, the other seven budgets, De Beers and Kimberley's event-led 1 + 19. | **Engine pending — DP, annual owner-only surveys** |

For each executed case append a dated DP observation, exact setup/actions,
checkpoint name, actual outcome and log evidence. Leave unperformed cases
pending. Static parity and connected naval ports do not prove engine deployment,
timers or event delivery. The separate deferred-release gates remain open.

2026-10-16, B145-11: DP sent Retief, left `.050` unanswered, then selected Rally
when it repeated; neither launched Blood River while ORA fought PHL and BST.
The 20:57:40 error log reports no available default for `.050`. The 20:58
autosave (1838-12-01) contains ORA/PHL/BST in war 18, no Blood River launch
reservation, and a repeated `.050` created on 1838-11-14. Its refusal container
incorrectly stores ZUL (country 481) as both actors instead of ORA (474)/ZUL.

Source correction removes the blanket war/play gates, replaces the duplicate
Rally/requeue option with the existing internal launch retry, and binds both
route containers to their actual current country. No save was edited. DP should
restart with the corrected source and replay a checkpoint before Dingane's
Retief response (or before sending Retief), so the participant record is created
correctly. Verify immediate Rally and automatic expiry separately, once-only
launch, and the guns-bargain escalation. All corrected engine results remain
pending; the existing terminal-settlement checks above remain pending too.

Static verification: 99 focused tests passed across Blood River launch, story-war
routes, Natal interwar, frontier assistance, and Natal/Zululand contracts. Eight
validator checks passed: runtime script contracts, localisation, stale/unused
symbols, on-action routing, delayed-event lifecycle, release invariants, and
local override inventory. The new regression checks failed against the original
guards/actor bindings and pass with the correction; they do not simulate engine
play creation or event expiry.

2026-10-16, 21:35: DP reports reaching Natalia's formation during continued
playtesting after the Blood River correction. This confirms that the played
route progressed to formation. The note does not distinguish manual Rally from
expiry or document the full war/goal setup, so it does not certify both launch
paths, the guns-bargain variant, or every once-only/negative scenario. Those
checks remain pending. Record the grain-laws, liberal-movement, extra-army
and GDP-polish follow-ups in the
[open issue register](../audit_issues_open.md#playtest-follow-ups--16-october-2026-2135).

2026-10-17, B145-22/23: read-only inspection of the retained 1839-11-01 autosave
confirms NAL's extra empty army. ORA/NAL/TRN have identical completed-technology
sets; ORA has not completed Empiricism. The [spawn audit](boer_spawn_setup_2026_10_17.md)
records the evidence, route coverage and source correction. No game was launched
and no save was changed. The ordering correction affects future formation only;
load a checkpoint before the country is created when verifying it. GDP polishing
remains TODO `PT-20261016-05`, with the current 25,000 gate unchanged.

DP subsequently confirmed that the completed technology was Academia and asked
to clear the technology-loss flag. `PT-20261016-04` is archived as a mistaken
observation; `B145-23` is closed. The army replay remains pending.

2026-10-17, B145-05/21: DP reports that both ORA–BST occupation and CAP's
deployment after Natalia refuses Britain remain problematic. No detailed new
timer/front telemetry accompanied the note; do not mark either case passed.
The ORA–BST workaround remains on hold.

2026-10-17, B145-07/08/09: the March–July 1850 saves show both allied primary
demands timer-enforced on 27 May, ZUL becoming GBR's protectorate, then transfer
to NAL and the Chiefdoms choice before Klip reconciliation. `.081` was incorrectly
created on 11 June. DP confirms the existing priorities should remain. The source
now recognises the British-held victory and reconciles Klip before the handoff
opens Natal's government choice. All 130 focused source tests pass, including
both update orders and all three choices; corrected engine delivery is untested.
Restart and replay from before victory/handoff (the retained 1 June checkpoint
is still unfinalized), or before the play for full setup/backdown coverage. Do not
use the already-resolved July outcome to assess this correction. See the
[evidence and implementation report](klip_punitive_handoff_2026_10_17.md).

2026-10-17, B145-24: latest autosave is 1848-06-01. British conversion happened
on 1848-05-15; the previous monthly save is before conversion. Martin West is
alive and leads the AF, but Landowner Marinus Vermaak is ruler. See the
[governor investigation](natal_governor_2026_10_17.md) for the native callback
and temporary protection. Restart with the correction and replay from before
conversion; the June save has already lost West's ruler role. No save was edited.
