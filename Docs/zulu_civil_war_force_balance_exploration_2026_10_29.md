# Zulu claimant wars: recruitment and geographical imbalance

29 October 2026. **Investigation and design exploration only. No gameplay change authorised or applied by this note.**

**Follow-up:** DP clarified that after Klip River the native civil war divides Zululand itself. The [two-map muster proposal](zulu_civil_war_muster_proposal_2026_10_29.md) develops the recommendation for both that internal split and the early Zululand/Natal division. No permanent Natal recipient is assumed, and territorial redesign is unnecessary for the later case.

## Recommendation

First verify that the existing transfer actually delivers the intended military workforce at the split. Then prototype a crisis-only mobilisation pool divided by the two coalitions, including the men who would otherwise be conscripted. Do not try to solve the whole imbalance with a flat 5,000-person transfer or a permanent change to the 1836 population distribution.

The intended outcome is that stronger backing produces a military advantage of the intended magnitude. It is not that every conflict becomes 50:50. Giving the stronger coalition mainland Zululand already advantages it geographically; access to virtually the entire recruitment base can multiply that advantage far beyond the coalition ratio.

## Evidence and its limits

The [bounded evidence](compatibility/evidence/zulu_civil_war_force_balance_2026_10_29.json) records copied-save hashes, dates, population/profession totals, military buildings, actual unit manpower and the inspected script hashes. Live autosaves were rotating; the analysis uses copies verified unchanged while copied, under `/private/tmp/sb-civil-war-balance-2026-10-29/`.

All five copies are **postwar**, 1 August–1 December 1842. They have one reunited ZUL, ruled by Mpande, with both state objects. They cannot establish the allocation immediately after creation, a failed transfer, or the cause of a particular battlefield defeat.

| Evidence | Zululand | Zulu-owned Natal/Klip River |
|---|---:|---:|
| Authored starting population | 268,000 | 2,000 |
| Population, 1 December 1842 | 259,183 | 15,590 |
| Total workforce, same save | 45,257 | 3,475 |
| Servicemen workforce, same save | 2,849 | 0 |
| Officer workforce, same save | 42 | 0 |
| Existing barracks levels, same save | 2 | 0 |
| Existing conscription-centre levels, same save | 10 | 1 |

The source totals are authored setup, not a new claim that these are accurate historical estimates. Source: `common/history/pops/04_subsaharan_africa.txt`, Zululand/Natal blocks. The save's 13 unit records contain only **1,940 actual manpower**, so neither a level count nor a unit-record count measures a field army.

Earlier retained wartime evidence corroborates the general staffing problem, but predates the latest floor and other changes: [28 October follow-up](compatibility/evidence/zulu_claimant_followup_2026_10_28.json), 1 September 1839, records 7,674 manpower for mainland country 481 and 480 for Natal country 16777220. Do not present that as a new test of today's code.

Current implementation:

- `common/script_values/sb_court_dynastic_values.txt` reserves one existing regular barracks level for the weaker side, divides the remainder by the frozen coalition ratio, and divides conscript levels by the coalition ratio.
- `common/scripted_effects/sb_court_force_split_effects.txt` moves existing soldiers and officers, separately, to match the integer **regular-barracks** allocation before rebuilding both countries' recruitment buildings. It does not add civilian recruits or instantly fill units. Unraised conscript capacity has no corresponding pool of already-employed soldiers to move.
- Vanilla's conscription centre is non-buildable and non-expandable; native capacity still matters. The installed `CONSCRIPTION_CENTER_LEVEL_POPULATION_DIVISOR` is 1,000 and army laws supply conscription modifiers. Creating a requested level count does not establish that the engine will retain it or find its recruits.
- Ordinary barracks' starting training PM uses 97 servicemen to 3 officers. SB customary conscription uses 99:1. Transferring only servicemen is incomplete, and qualification, employment and training need independent checks.
- Both AI participants already receive −50% supply consumption while the tracked war lasts. Increasing that again is not an established fix for missing recruits.

This is consistent with Vanilla's geographical model: revolutionary states bring their economic and military infrastructure with them. [Paradox's original revolution explanation](https://www.paradoxinteractive.com/games/victoria-3/news/dev-diary-41-revolutions) establishes that design principle; current installed files and retained native investigations, rather than that older diary, govern the beta's precise behaviour.

## Why “5,000 peasants” needs a unit

On 1 December 1842, Zululand's peasant group contains 29,954 workers and 145,770 dependants. Moving a proportion of that group moves both:

- **5,000 people:** approximately 852 workers at this snapshot's ratio.
- **5,000 workers:** approximately 29,332 people including dependants.

These are examples from this save, not universal workforce ratios. A move cannot promise 5,000 fighting men just because it moves 5,000 population.

`change_poptype` exists and Vanilla uses it for whole-pop profession changes, for example in `events/soi_events/00_ep1_persia_events.txt`. It is not an instant army-manpower setter. A bounded partial-pop conversion, destination employment and retention would still need validation; `move_partial_pop` does not expose the newly split destination pop as a selectable result. Avoid converting an entire large peasant group accidentally.

## Alternatives

| Approach | What it fixes | What remains / cost | Assessment |
|---|---|---|---|
| **A. Crisis recruitment transfer** | Move an amount of existing military/civilian workforce sufficient to staff the weaker side's intended force, including officers or officer recruitment. Conserves population. | Native conscription capacity can still reject the proposed levy allocation. Families also relocate; native hiring/training still take time. Persistent demographic effects are possible. | Best small experiment; use a measured shortfall, not an unconditional 5,000. |
| **B. Change the starting population split** | Gives Klip River a larger tax base, civilian workforce, recruitment capacity and replacement pool throughout the campaign. | Changes Natal's economy, territorial payoffs, Blood River/Klip River outcomes and historical setup even when no claimant war occurs. Modest changes may still leave a huge imbalance. | Reserve for independently justified population rebalance. |
| **C. Coalition-based wartime mobilisation pool** | Divide an agreed combined army budget, rather than letting each resulting state's civilian pool determine most of its army. Transfer enough existing people to support that budget. | Larger intervention: temporary recruitment buildings, wages, qualifications and end-of-war demobilisation must work. Staffing remains engine-tested, not guaranteed by scripting a quota. | Preferred design to test if A cannot make native conscription deliver the intended split. |
| **D. Give both sides substantial territory within Zululand** | Distributes recruitment and economic resources at their source, rather than leaving one side with the peripheral county. | Requires a different territorial-split design and verification of province/pop/building allocation. Could disrupt the now-working native conflict routing. | Potentially cleaner geographically, but a larger separate project. |

### A — smallest staffing experiment

Snapshot each side's actual allocation and eligible workforce at the split. Transfer only a deficit from the other side, with the same total people and intended army size. Include officers; do not assume soldiers alone are sufficient. The role of a peasant supplement is to supply recruits and replacements when the already-military population is too small.

Measure the result after native employment updates. Only then decide whether a short recruitment/training aid is needed. Do not add combat bonuses, extra free population or recurring automatic top-ups. Population movement is not automatically reversible: occupations, migration, births and casualties prevent pretending the original households can simply be restored unchanged.

### C — preferred fuller model

At the reserved crisis, quote the combined regular force plus an explicitly bounded levy pool, and divide it by the two competing coalitions. Preserve the agreed weaker-side regular minimum. Uncommitted houses and third princes remain outside this two-faction ratio.

If the small state cannot retain its native conscript quota, prototype representing the allocated wartime levies through **temporary barracks**. Existing building creation can express this; it is a proposed change from the current conservation of each building category. It must not silently become a permanent standing-army grant.

Move enough existing military and eligible civilian workforce for the resulting jobs, with the appropriate officer share. Observe military wages, goods availability, organisation and recruitment. Budget or supply assistance should answer an observed shortfall; the current AI supply modifier already exists. Do not claim that converting occupations or creating buildings instantly creates trained, supplied battalions.

On resolution, remove only the additional temporary capacity, retain the intended regular army and let demobilised people enter civilian employment. Do not duplicate old units or force nonexistent prewar people back into existence. The combined levy budget, recruitment aid and cleanup rules require agreement before implementation.

This is more work than A, but addresses both initial staffing and the much larger mainland conscription pool. The first test should be an equal coalition, followed by 60:40 and 75:25: a near-even political split should not turn into a tenfold military gap merely because one side holds Klip River.

## Validation needed before balance conclusions

Capture a checkpoint before the split, immediately after it, and after four and eight weekly employment ticks. For each actual faction record:

1. Frozen coalition share, current ruler, state ownership and Prerogative.
2. Intended versus surviving barracks/conscription levels and training PMs.
3. Soldiers/officers: total workforce, employed workforce, unemployment and relevant qualifications; transferred workers and dependants separately.
4. Regular/conscript manpower, organisation, supply, recruitment, casualties and reinforcements.
5. Military wages, treasury balance, goods shortages and whether the AI has actually raised its conscripts.

Compare both player choices, equal and unequal coalitions, and early/later wars. A late postwar autosave cannot replace this evidence. No engine test was performed in this investigation.

## Decision register

| Status | Decision |
|---|---|
| Existing requirement retained | Coalition backing must produce meaningful military strength; native war, identity routing and both playable sides remain. |
| Verified in source | Starting population is 268,000 versus 2,000; the current force-split code attempts to redistribute existing military workforce, not a civilian levy pool. Successful delivery at the split still needs verification. |
| Provisional recommendation | Verify the existing staffing transfer, test A, and use C if native conscription remains the decisive bottleneck. |
| Open | Whether to author a unified wartime levy pool; its size, temporary employment support and cleanup. |
| Deferred | Starting demographic rebalance without independent historical justification; territorial/map redesign. |
| Not selected | Flat 5,000-person grants, broad combat bonuses or repeated automatic recruitment top-ups. |

## Work performed

Read-only source/save investigation and arithmetic verification; this design record and its evidence only. No event, law, modifier, population history, save, dependency or game binary was edited, and no game was launched.
