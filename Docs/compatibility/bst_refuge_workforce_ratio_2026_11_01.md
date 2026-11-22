# Lesotho refugee workforce ratio: implementation trial

## Playtest follow-up — 3 November 2026

DP reports **“Okay works”** after testing the balanced refugee workforce trial.
Record this as working in the reported playtest and remove the immediate famine
blocker from the active testing priorities. Retain the current implementation;
no further population or relief increase is requested.

The individual population-accounting, metadata and ten-year-expiry checks below
were not separately reported. They remain verification details for the wider
pre-release balance pass, rather than grounds to repeat the successful trial now.
Codex has not launched the game or independently inspected a new replay.

## Implemented decision — approved and implemented on 1 November 2026

DP approved trying a **50:50 worker/dependant arrival cohort**, keeping the
mountain retreat at **5,000 people**. The earlier feasibility assessment is
preserved below. Engine replay was pending at handoff; DP's subsequent result is
recorded above. No game launch or save edit was performed by Codex.

The retreat option now calls `sb_bst_transfer_mountain_refugees`. It validates
BST's mountain-only retreat, BST ownership of Drakensberg, and an eligible
Sotho donor of at least 5,000 in the current frontier actor's Vrystaat territory.
The source is debited by exactly 5,000 and the destination receives **2,500 workers
and 2,500 dependants**. A receipt on BST prevents repeated delivery. All work
remains inside the existing hidden effect; reviewed event text is unchanged.

The native move does not expose a household-ratio override, so this is a
replacement rather than `move_partial_pop`:

1. Record the selected donor's culture/religion/profession, wealth and literacy.
2. Find an absent destination staging culture before removing anyone.
3. Remove 5,000 from the matching source-state culture/religion/profession group.
4. Create the 50:50 cohort in BST-owned Drakensberg, isolated under that temporary
   culture. Restore donor wealth without loyalty reactions, and donor literacy.
5. Restore Sotho culture last, allowing normal merging with existing residents.

The source removal can span several Pops of the same identity; wealth/literacy
are copied from the selected donor, not averaged across that removal group.
The arrival profession follows the inspected native move: peasants become
labourers, slaves become labourers where slavery is banned, and other installed
professions retain their type. The debit always uses the **original** profession.
No setters are applied to resident Pops after a merge. A merged Pop's displayed
worker share will be a weighted average, not necessarily 50%.

The Mountain Refuge retains DP's current **+30% in-kind Subsistence Output for
ten years**. The +50% subsistence-farm throughput line remains commented out.
This trial changes no laws, military setup, hiring protections, food modifiers
or total refugee count.

### Limits

Creation does not clone qualifications, IG support or the full political state
of the removed people. Filtered source removal uses native death cleanup,
including proportional loyalty/radical accounting; it is not recorded as a
normal native migration. Downstream death statistics have not been exhaustively
verified. Staging protects residents from direct metadata setters, but normal
merging may still change their combined averages. No claim of a perfect Pop
clone or a cure for starvation is made.

The 50:50 share is an **arrival condition**, not a permanent demographic rule.
Growth, casualties and migration can change it. Workers still need employment,
qualifications where required, and sufficient income/food supply.

### Validation and DP replay

- Source-executed focused checks cover population conservation, the exactly-5,000
  source boundary, filtered removal, native profession conversion, faith
  preservation, donor wealth/literacy restoration without loyalty reactions,
  merging, absent-culture fallbacks, ownership/eligibility failures, a foreign
  event root, and repeated/re-entrant delivery.
- Independent Sol 6.1 Max review caught the native profession conversion and
  wealth-setter loyalty flag; both corrections are included.
- Focused refugee/remediation suite: **29 passed**, repeated after the final
  encoding correction and independently run by the reviewer.
- Full validator: **15/17 gates passed, warned or skipped**. Unit discovery ran
  **1,041 tests: 1,032 passed, 8 skipped, 1 failed**. The failure and the separate
  localisation gate are the pre-existing dangling Swazi `.098` review row plus
  reviewed-prose/baseline drift in Klip River `.060`/`.080` and Natal `.050`.
  No localisation was changed by this trial. CMF integrity, override comparison,
  map/naval checks, runtime contracts and delayed-event checks passed.
- Advisory Tiger uses a **1.13.5** schema against **1.14.5**. It reported 0 fatal,
  1,892 errors and 150 warnings. Exactly 816 errors are repeated expansion of
  its unsupported `working_adult_ratio` schema field; the installed native
  parser/execution evidence verifies this field. The remaining 1,076 errors
  are outside the new helper. Its one new warning was the missing UTF-8 BOM,
  corrected after that run; the other 149 warnings are outside this change.
  Do not remove the native ratio setting merely to satisfy the older schema.
- `git diff --check` passes. Static checks do not execute the game engine.

[Machine-readable validation record](evidence/bst_refuge_cohort_validation_2026_11_01.json).
Full local output: `/private/tmp/sb-bst-refugee-validation-20261101.txt`.

DP should restart with the updated scripts and load a checkpoint **before the
mountain-retreat option**, or use a new campaign. Already-delivered refugees are
not retroactively modified.

1. Compare immediately before/after: eligible source group −5,000;
   BST-owned Drakensberg +5,000; world population conserved, excluding normal
   elapsed-time growth/deaths.
2. Confirm the arrival increment is +2,500 workers/+2,500 dependants, allowing
   native merging. Verify no temporary culture remains and no unrelated resident
   Pop was overwritten by the restoration setters.
3. Check donor faith, mapped profession, wealth/literacy and once-only delivery.
4. Run 8–12 weeks and compare employment, grain supply, income, Food Security
   and starvation with the prior trial. DP subsequently reports the trial works;
   detailed timings and economic measurements were not separately supplied.

## Historical feasibility assessment — before implementation

1 November 2026. Read-only proposal assessment; no gameplay/save changes or game
launch. DP suggested making the existing 5,000-person mountain retreat cohort
50% workers and 50% dependants, or more worker-heavy.

## Economic comparison

The current transfer's ratio at the retreat is unknown; all retained checkpoints
are later. A normal 25% worker share is a comparison, not a reconstruction of
that transfer. In the latest October save, the remaining Transoranje Sotho
labourers, farmers and peasants have aggregate worker shares of 25.47%, 26.04%
and 24.79% respectively. Selecting a normal civilian profession alone would not
guarantee 50% workers.

| Hypothetical 5,000-person cohort | 25% workers | 50% workers |
| --- | ---: | ---: |
| Workers | 1,250 | 2,500 |
| Dependants | 3,750 | 2,500 |
| Consumption weight, dependants at half needs | 3,125 | 3,750 |
| Weekly in-kind income if employed as peasants under Serfdom +30% | £93.75 | £187.50 |

The workforce doubles while consumption weight rises 20%. The in-kind income
calculation is workers × 3 × 1.30 / 52. This does not predict income for other
professions or guarantee employment/food security. The 50% ratio applies to
the new cohort only; merging it with existing residents gives a weighted average.

## Installed 1.14.5 interface

- `move_partial_pop` accepts destination, total population or population ratio.
  It preserves the source Pop's actual worker/dependant ratio, subject to rounding.
  There is no supported ratio override or separate worker selection in its parser.
- Runtime `create_pop` supports `working_adult_ratio = 0.5`, as does the installed
  history example. Native execution initialises approximately 2,500 workers and
  2,500 dependants when total size is 5,000. This creates people; it is not a
  modification of the existing transfer.
- A replacement transfer would therefore require source removal and destination
  creation with preserved total headcount and deliberate treatment of culture,
  religion, occupation and inherited attributes. Creation initialises literacy
  and political support; it does not clone the full original Pop. A clean,
  attribute-preserving replacement has not been implemented or engine-tested.
- `state_working_adult_ratio_add` changes the wider state's demographic target
  and growth calculations. It is neither cohort-local nor an instant ratio setter.

See [native findings and reproduction commands](evidence/bst_refuge_cohort_1_14_5_arm64/FINDINGS.md).
The installed script example is `common/history/pops/100_pops_example.txt:85`.
Native inspection also verifies runtime support, avoiding an assumption that
history and runtime creation accept identical syntax.

## Proposal limits

Use 50:50 as an initial cohort target if a replacement-transfer approach is
chosen; no higher value is justified by this comparison. Normal growth,
casualties and migration may change the ratio afterwards.

Additional peasants can staff subsistence production, but Serfdom's protected
employment floor still blocks their recruitment into commercial farms below
the floor. This is a demographic alternative to test, not an established cure
for the famine. The effects on donor population, arrival attributes, employment
and subsequent Food Security require engine verification by DP.

Independent Sol 6.1 Max review verified the transfer/creation distinction and
state-modifier scope. Arithmetic checked locally; gameplay remains unchanged.
