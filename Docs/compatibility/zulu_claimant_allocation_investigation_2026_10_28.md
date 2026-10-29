# Claimant war: military allocation and unreliable sponsorship — 28 October 2026

**Investigation only. The current implementation fails the military-allocation release criterion.** No gameplay source, dependency, save or game binary was changed, and no game was launched. Automatic activation remains disabled.

## Evidence and replay boundaries

Five autosaves and the current logs were copied read-only to `/private/tmp/sb-claimant-allocation-2026-10-28/`. The saves were stable while copied. [Bounded extraction, input hashes and verification](evidence/zulu_claimant_allocation_2026_10_28.json) identify each input. Installed native inspection uses the same 1.14.5 arm64 binary as the preceding investigation.

These are **different replays**, not one continuous chronology:

| Files | Game dates | Observation |
|---|---|---|
| `autosave_4.v3` → `autosave_3.v3` → `autosave_2.v3` | 1 June → 1 July → 1 August 1839 | Back Gqugqu; an organising war exists in June, and the split has completed by July. |
| `autosave_1.v3` → latest `autosave.v3` | 1 June → 1 July 1839 | Back Dingane; the claimant movement reaches 100% activism but no Zulu civil-war object exists. |

The claimant movement began on 7 May in the successful replay and on 3 May in the stalled replay. The saves do not establish that choosing a particular portrait causes success or failure.

## Military allocation: the coalition calculation survives, but does not divide the army

The frozen quote is **177 Prominence for Dingane and 334 for Gqugqu**. Gqugqu therefore has **65.362%** of the two represented coalitions. Backing him correctly inverts the rebel territorial target to **34.638%** for Dingane.

Before the split, the native organising war already contains:

```text
war 3
origin_country = 481
political_movement = 33554978
uprising_states = STATE_ZULULAND (state 779)
army = 21
conscript = 17
insurrectionary_igs = 1891 (Intelligentsia)
```

The native choice is a whole state. Zulu owns two state objects: Zululand and its Natal portion. **All military buildings are in Zululand**: barracks 6233 with four levels and conscription centre 6234 with seventeen slots. Natal has neither. After the split:

| Side | Country | Ruler | Land | Regular battalion records | Conscript records |
|---|---:|---|---|---:|---:|
| Player/original | 481 | Gqugqu 4479 | Natal 780 | 0 | 0 |
| Rebels | 16777220 | Dingane 4477 | Zululand 779 | 4 | 17 |

The twenty-one records are **not twenty-one fully staffed battalions**. On 1 July the rebels have 2,587 regular manpower and 3,991 conscript manpower; on 1 August, 3,668 and 10,122 respectively. The original country has none in both retained post-split saves. Before the split, the seventeen conscript records have zero manpower.

Installed native code corroborates the mechanism: `CalcStatePotentials` records each state's unit count and conscription capacity. `UpdateMilitarySetup` calls `ParseTransferedUnits`, which collects the army-unit records from military buildings in the receiving country's states; `TransferUnits` assigns those records to formations. It does not recalculate the frozen court Prominence ratio at that step. The saved June uprising plan already contains all twenty-one records, before SB's post-creation character routing. [Native excerpts and reproduction commands](evidence/zulu_claimant_allocation_1_14_5_arm64.txt).

Vanilla's army-support and IG-clout factors influence native state allocation; they are not an independent scriptable battalion-percentage setter. The current movement supplies `target_fraction_of_states` only. In this two-state arrangement, the selected one-state split gives the rebels all military infrastructure despite their smaller quoted coalition. A precise territorial percentage cannot divide a single concentrated barracks/conscription pool.

Named character routing is partly verified: Gqugqu rules original ZUL, Dingane rules the rebels, Mpande survives in original ZUL, and Ndlela is with Dingane. The recorded war identity persists through July and August. This does not validate every character, placeholder death, both winners or the opposite player choice. It also demonstrates that assigning commanders to their faction does not guarantee that faction receives troops.

## Sponsorship: two independent Landowner failures, plus an accidental sponsor

Latest save, 1 July 1839:

- Prerogative **−67.48287**; the same 177:334 quote remains reserved.
- Gqugqu is alive, is an agitator, and is attached to the exact claimant movement.
- The movement has **100% activism**, its mobilisation modifier and the demand-verified receipt. There is no exact preparing-war receipt, no advance receipt and no Zulu civil-war object. Its failed-start date is still the unset `1.1.1` sentinel.
- Landowners have the crisis ideology but **+9 Approval / Happy**.
- Only **3.667% of Landowner clout** supports the movement, below the native **5%** prerequisite. This is distinct from the Landowners' roughly 80.8% national clout and the prince's court coalition.

The saved Landowner modifier list contains `modifier=""`, starting at the crisis date, rather than `sb_court_claimant_landowners`. The session log reports that exact modifier missing from the database at **07:11:58**, during script reload. The current file on disk defines it correctly. The evidence is consistent with a partial live reload: the ideology/script changed while the new static-modifier definition did not load. **A full process restart and a checkpoint before the crisis are needed to validate the current package.** Reopening a save in the same running process is insufficient evidence that new database definitions loaded.

Even if the intended −30 Approval applies, the saved **3.667% backing still fails the separate 5% gate**. Merely changing the sponsored IG or increasing activism cannot guarantee creation.

The successful replay did **not** demonstrate Landowner sponsorship. Its native war records **only the Intelligentsia** as insurrectionary. In the June checkpoint they have **0.048% national clout**, but **5.769% of their own clout** backing this movement: one supporting individual, with six supporting political-strength points. They have −7 Approval and a Moderate leader. In the stalled replay, their national clout is saved as zero and there is no support record for the claimant movement. This makes the current route dependent on small, incidental native constituencies rather than the displayed house coalitions.

The previous [native eligibility evidence](evidence/zulu_claimant_ig_gate_1_14_5_arm64.txt) confirms that native IG eligibility precedes the scripted `revolution.possible` check. The proposed sponsor must satisfy population backing, approval and ideological agreement; a saved court endorsement or an agitator role is not an override. These snapshots prove that the intended sponsor is ineligible and that another IG sponsored the successful trial. They do not reconstruct every in-memory ideology definition or every weekly eligibility evaluation in this partially reloaded session.

## Other observed error

`sb_court_place_dynastic_member`, currently line 407, transfers eligible characters even when they already belong to the destination. The log reports `Can't transfer to the same country` at the split. This is a separate unnecessary transfer. The pre-split uprising plan and building-linked unit records establish that it is not necessary to explain the military imbalance. No fix was made during this investigation.

## Consequences for the next implementation

1. Verify sponsorship after a complete game restart, then address actual Landowner movement backing and the native eligibility gates. The label and Approval penalty alone do not provide reliable sponsorship. Keep other IGs' accidental participation distinct from successful validation of the intended sponsor.
2. Treat military allocation as a separate design requirement. More activism, a different sponsor, or another territorial fraction will not establish a fair division of this concentrated force. A reliable coalition-based split needs a separately verified means of allocating military infrastructure/units or a different supported split mechanism. Scripted redistribution remains outside the agreed implementation scope until DP changes that constraint.
3. Preserve the working named-ruler/original-country handoff. Correct the redundant same-country transfers in the next authorised fix, without using them as an explanation for the army split.

Scenarios 99 and 101 now record observed failures; 99b/99c/102 gain bounded positive observations. The repeated 25/50/75% trials, one-state allocation, both winners and cleanup remain pending. Do not enable automatic challenges on these results. No full static suite was rerun because gameplay source is unchanged; extraction assertions check identities, country ownership, all unit records, backing totals, modifier presence and repeat-snapshot consistency.
