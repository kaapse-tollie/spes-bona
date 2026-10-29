# Claimant stall and experimental army division — 28 October 2026

## Latest replay

Read-only copies of the June, July and August 1839 autosaves contain the same pending Gqugqu challenge and no native civil-war object. The latest, **1 August 1839**, has:

- Actual claimant activism **100%** and Gqugqu attached as its agitator.
- Armed Forces **−20 Approval / Angry**, the named temporary modifier and the intended crisis ideology. This is a fresh process, unlike the earlier missing-modifier reload.
- **6.338%** of Armed Forces political strength backing the movement, distinct from their **5.961%** national clout.
- A verified Contested Crown demand, live participants and the weekly polling receipt. There is no organising-war receipt for SB to advance.
- Frozen backing of **177 for Dingane and 334 for Gqugqu**. The original country still owns both states and all **four regular / seventeen conscript** unit records.

[Input hashes and bounded observations](evidence/zulu_claimant_rebuild_2026_10_28.json) preserve this replay separately from the earlier successful split and Landowner trial. The saves and logs were not modified.

## What the missing pressure label establishes

The movement explicitly prohibited all IG pressure. It now permits **only Armed Forces**. The installed native pressure/influencing threshold is **10%** internal backing, with three influencing slots and a retention preference; the separate revolutionary-sponsorship threshold is **5%**. The saved AF clears the latter, not the former. Native `HasInterestGroupSupportForRevolution` considers all IGs rather than requiring membership in the influencing list.

Consequently, “no pressured IG” is explained, but does **not** establish the sole cause of the missing war. The saved angry Royalist AF also appears compatible with the current crisis ideology. No saved country immunity, single-province restriction, recent-war cooldown or claimant script error explains the remaining gate. **The precise native refusal remains unresolved.** Do not claim that changing the pressure rule alone guarantees creation, or increase activism again as a substitute for diagnosing eligibility.

A separate recruitment error is corrected: the movement copied ordinary Absolutist attraction from the **incumbent's** Popularity, monarchic law and childhood. Dingane's −100 Popularity therefore reduced his opponent's recruitment to the inherited 0.2 floor. Recruitment now uses the named claimant's Popularity, retaining the bounded `clamp(1 + Q/100, 0.2, 1.8)` factor; Gqugqu's saved zero gives 1.0. This is a justified attraction correction, not proof that insufficient support caused this replay's stall. Other native constituency weights and CMF hooks remain.

## Authorised rebuilding trial

DP explicitly approved rebuilding and dividing the forces for testing, accepting lost manpower and experience. This supersedes the earlier no-redistribution boundary. The new effect runs **once after the actual native split**, after identifying both contender countries; it cannot create the missing revolution itself.

1. Count completed barracks and conscription-centre levels across both actual countries before deleting anything.
2. Allocate each service separately: claimant `round(total × R/(I+R))`; incumbent receives the exact remainder. Use the frozen two-coalition quote, without uncommitted/third-party backing, Popularity or the Prerogative discount. The 10–75% native territorial clamp remains separate.
3. Remove those military buildings and recreate each side's quota in its most populous actual state. Preserve each service's training method from its largest existing centre, including SB's customary conscription method. Leave naval and economic buildings alone.
4. Reserve the reset before deletion. Repeated callbacks cannot rebuild again; resolution/cancellation removes the receipt. Subsequent recruitment and construction remain native.

For the retained **177:334** quote, the intended rebuilding is **Dingane: 1 regular / 6 conscripts; Gqugqu: 3 regular / 11 conscripts**, regardless of which contender occupies the original country. No extra recruitment levels are awarded.

Installed `create_building` raises existing levels; reducing them requires removal/recreation. Native `CreateOrRemoveUnitsIfNeeded` gets or creates the country's default formation, validates its building/owner/formation and creates replacement combat units. An unspecified type is chosen through `CalcUnitTypeForNewUnit`. This is **not a transfer of the old troops**: manpower, experience and the previous unit composition are lost. Both side-selection options disclose the reset and recruitment requirement. Vanilla `destroy_barracks` and Hail Coloumbia's Reconstruction provide removal precedents, not lossless relocation.

Native conscription caps, recruitment staffing, formation composition and callback timing can still affect the practical result. Building-level conservation in source tests does not demonstrate retained available battalions or a military advantage. No combat modifier, daily quota enforcement, global define, dependency change or save migration is included.

## Verification and next replay

All **49 focused checks pass**, covering claimant recruitment, rounded quota conservation, both side choices, either initial military geography, multi-state totals, preserved production methods/naval/economic buildings, no reset before a split, duplicate callbacks and cleanup. Full discovery: **804 passed, eight historical skips, one unchanged reviewed-localisation failure, no errors** (813 tests). Full validator **15/17**; both failed gates concern the existing `.060`/`.080`/`.050` approved-prose drift. Compatibility/maps pass. Advisory Tiger is unchanged at **1,073 errors / 149 warnings** with its older schema; no diagnostic names a changed claimant file. Full reports are retained in `/private/tmp/sb-claimant-rebuild-2026-10-28/` and hashed in the evidence record.

**Pending DP:** fully restart and use a disposable checkpoint before the crisis/side choice. First verify the demanded law, AF internal support, its pressure label and creation of the exact organising war. If creation still fails, retain the pre-split save; the current changes must not be reported as an established engine fix.

After a real split, compare recruitment levels, unit types, manpower, experience, commanders and available battalions immediately, after a week and after a month. Repeat both choices and 25/50/75% backing, including one-state Zulu and uneven multi-state barracks. Confirm conscription caps do not undo the division and that duplicate callbacks do not erase replenished units. These are runtime matrix **99–102**. Automatic activation remains disabled until native creation and meaningful military influence are demonstrated.
