# Chiefdoms prominence pressure and Natal AI implementation

15 November 2026. DP approved the [design](../zulu_chiefdoms_prominence_design_2026_11_15.md).
**Source implemented; engine verification pending.** Target remains Victoria 3
1.15.1 / CMF 1.67.3 + sb-1.15.1-r1, all DLC. No game launch, save rewrite,
dependency edit, commit or version bump was performed.

## Resulting behaviour

The court's existing house pass now counts two additional political totals from
full represented house weights. Each eligible member contributes once through
the selected head's alignment, including local agitators. The existing
attraction totals retain their local-agitator exclusion and coefficients.
Both JE backing labels read the political totals.

The royal movement receives one owned modifier:

`clamp(0.001 × (royal political backing − chiefly political backing), −0.30, +0.30)`

That is 0.1 percentage point per prominence advantage, bounded at ±30 points.
The modifier adjusts the native Activism **target**; it neither assigns current
Activism nor adds a fresh increment each month. Native radical/loyalist, law and
intervention contributions remain separate. The 100% actual-Activism endpoint
and its existing claimant/settlement guards are unchanged.

The existing court recalculation updates the modifier after its totals are
rebuilt, covering monthly maintenance and the existing bribe/return recalculation
paths. Replacement first removes only the feature's own modifier from the live,
origin and rebel countries, then applies it to the actual royal faction's
movement. A tie leaves no modifier. Terminal cleanup runs before those country
handles or the container are discarded. Missing movements are not recreated.
An existing campaign initialises the new derived totals on its next court
calculation; no saved values are guessed or rewritten.

Dynamic AI reads **radicals among Natal's Zulu Pops**, continuing the population
scope discussed with DP:

| Condition | Claimant action AI chance | Refugee action AI chance |
| --- | ---: | ---: |
| Radicals below 20% | 0 | 0 |
| Radicals at least 20%, current claimant not returned/present | 25 | 0 |
| Radicals at least 20%, current eligible claimant returned and present in ZUL | 25 | 25 |
| Strict Historical, JE younger than 1,095 days | 0 | 0 |
| Strict Historical, JE at least 1,095 days | 25 | 25 |
| Off | 0 | 0 |

These are AI weights, not a guarantee of immediate execution. Existing action
visibility and possibility still apply: a returned claimant cannot be returned
twice, and Shepstone locks/absence still prevent offloading. The extra claimant
ordering applies to Dynamic AI, not human action availability or the retained
Strict delay. The current claimant must satisfy the living/adult royal-candidate
predicate, have the character return receipt, be owned by ZUL and be neither
exiled nor in the void. Natal's old country receipt alone is insufficient.
Returning the claimant can reduce radicals below 20%; offloading then waits
until the live condition is met again. Successor returns retain the prior
once-only loyalist-reward and Boer-appeal protections.

## Verification

- Before editing: **74 focused tests passed**.
- After editing: **113 focused tests passed** across court accounting, prices,
  the contest, claimant/constitutional handoffs, prominence modifiers and AI gates.
- New source-executed cases cover a locally returned agitator remaining counted
  once; house-head alignment; death and alignment changes; positive, negative,
  zero and exact-cap inputs; non-stacking replacement; preservation of volunteer
  modifiers; both native split orientations; one house not counting in both
  courts; cleanup before container destruction; and absent backing/movements.
- AI cases cover 19.99%/20%, Natal versus ZUL/TRN and non-Zulu radicals, the
  current character versus old country receipt, foreign/exiled claimants,
  a live drop below 20% after return, the three-year boundary and Off.
- The first full run exposed 24 errors across six Hamu test cases: their fixture
  assigned its contest flag after parent construction, which now checks contest
  status during court recalculation. Initialising the fixture as pre-partition
  before parent setup fixes the ordering; the six Hamu cases and nine new
  prominence/AI cases pass together. This was a fixture correction, not a new
  gameplay workaround.
- Negative control: restoring the former representative counter makes the new
  returned-agitator political-backing check fail; the implemented counter passes.
- Full validator rerun: **15 passed, 2 warnings, 0 failures**. The warnings remain
  the five deferred release gates and Tiger 1.19.0's incomplete 1.15 schema;
  Tiger was not used as a target validator. Local documentation links and
  anchors resolve; the task diff preserves unrelated inputs.

These fixtures execute the shipped scripts while supplying native fields.
They do not simulate native target recalculation, actual Activism convergence,
AI dispatch, character movement attachment, population recruitment or rendering.
DP should run the [current replay checks](../zulu_thirteen_chiefs_runtime_matrix_2026_11_10.md#15-november--political-backing-and-natal-ai).

The input snapshot, focused/full validation output, link checks and task diff
are retained under `generated/chiefdoms_prominence_2026_11_15/`. Historical reports
and unrelated working-tree changes are preserved.
