# Claimant demand and recruitment — 28 October 2026

## Two newest autosaves

The latest replay remains stalled before native war creation. Stable read-only copies preserve these observations separately from the preceding August checkpoint:

| Observation | 1 August 1839 | 1 September 1839 |
|---|---:|---:|
| Actual claimant activism | 100% | 100% |
| Armed Forces' internal support for the movement | 6.312% | 8.178% |
| Attached agitator | Gqugqu, 4479 | Gqugqu, 4479 |
| Native civil war for ZUL | None | None |
| SB's verified-demand receipt | Absent | Present |

Both saves retain original ZUL 481, claimant movement 33554979, an angry Armed Forces with the named −20 Approval modifier, and frozen backing of 177 for Dingane and 334 for Gqugqu. No split has occurred, so the experimental military rebuild has not run. The fresh-process logs contain no claimant script error explaining this stall. [Input hashes and bounded evidence](evidence/zulu_claimant_demand_attraction_2026_10_28.json).

## Does approving Monarchy prevent the demand?

The evidence does **not** support that explanation. The crisis ideology approves Monarchy but **strongly approves Contested Crown**. The September receipt is set only after the script verifies the actual `most_desired_law` and the claimant's movement attachment. It is evidence of that check, not a separately serialised desired-law field.

Read-only inspection of installed `CalcMostDesiredLawToEnact` confirms that it accepts an eligible candidate law whose stance is strictly higher than the active law's; it does not require the active law to be disliked. The existing stance pair also preserves compatibility with Royalist Armed Forces leadership. Leave it unchanged for this trial.

Neither save clears the separate **10%** internal-backing threshold for the pressure label. Revolutionary sponsorship uses **5%** and other native requirements, so the missing label alone does not establish why no war exists. The precise remaining creation failure is still unresolved. No source test or disassembly observation is being treated as successful engine creation.

## Change for the next test

Add **+100% Political Movement Pop Attraction** to the existing `sb_court_claimant_mobilisation` modifier, following Vanilla's `modifier_birth_of_the_liberation_army` precedent. This is a first test magnitude for DP's requested recruitment boost. It applies to the reserved claimant movement, does not stack on weekly polls, and clears with cancellation or resolution. It changes recruitment over time, not current support immediately, the frozen house quote or the troop quota. Keep 25-point weekly activism, AF sponsorship and ideology stances unchanged.

**Pending DP:** fully restart and replay from before the crisis/side choice. Confirm the attraction modifier, growth in internal AF backing, the actual demanded law and eventual organising-war object. Check cleanup and unrelated movements. Once a split exists, continue the already approved military-division checks in runtime scenarios 99–102. Automatic activation remains disabled; no launch or save modification was performed.

## Validation

- **50 focused claimant checks pass**, including movement-only attraction, repeated polls without stacking and cancellation cleanup. The new regression failed before the modifier was added.
- Full discovery: **814 tests; 805 passed, eight historical skips, one existing reviewed-localisation failure, no errors**.
- Full validator: **15/17 gates passed, warned or skipped**. Both failed gates still report reviewed-text drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`. No localisation was edited here. Compatibility, map/naval, script-contract and delayed-event gates pass; CMF release sync was explicitly skipped.
- Advisory Tiger, using its older 1.13.5 schema: **1,073 errors / 152 warnings**. The three warnings added to the preceding report concern inference of the existing `no_heirs` flag; none concerns the attraction change. This is not a clean Tiger result.

Reports and read-only extraction remain under `/private/tmp/sb-claimant-demand-2026-10-28/`; hashes are recorded with the evidence. Historical reports remain intact.
