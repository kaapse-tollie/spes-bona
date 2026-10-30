# Post-war return of Natal and Zululand population

Status: implemented; source-level checks passed; native reunion and employment checks pending DP.

## Requested result

After an authored claimant civil war involving both Zululand and Zulu-owned Natal, restore the regions' population proportions from before the scripted muster. Preserve wartime deaths: the saved proportion is applied to the population that survives, rather than restoring old population counts. Do not change starting population history.

The snapshot is taken by `sb_court_prepare_dynastic_forces` before its first recruitment-building relocation, only in the existing multi-state branch. It is copied to both actual factions. Native one-state wars, including a Zululand-only split after Klip River, retain the engine's distribution and receive no scripted population return. Existing checkpoints without this snapshot receive no fallback migration.

## Calculation and scope

```text
saved Natal share = owned Natal population / (owned Natal + owned Zululand population)
target Natal population = saved Natal share × surviving combined population
```

If Natal is above its target, move the surplus fraction of every current Natal Pop to the winner's largest owned Zululand state. If it is below target, move the corresponding fraction in the other direction. All owned portions in each region contribute to the calculation; state IDs need not survive native reunion.

The calculation includes workforce and dependants through native state population. `move_partial_pop` retains the existing people, culture and religion; no `create_pop`, forced profession conversion or casualty replacement is used. Native employment and profession reassignment remain engine behaviour. The restored ratio is approximate because script fixed-point arithmetic and per-Pop integer rounding can leave small discrepancies.

Only states owned by the actual winning country are scanned. Other countries' Natal land and unrelated regions are excluded. The helper never assumes the winner is `c:ZUL` or that an event's `root` changes with a country scope.

## Resolution and bounded delivery

The existing exact-war winner dispatcher owns the return. Its first attempt requires both owned regions and no relevant region portion still belonging to the recorded defeated faction. This avoids prematurely measuring a winner that already owns a portion of both regions before the final reunion.

If ownership is not ready, a separate country receipt survives the ordinary court cleanup. Hidden event `sb_court_population_return.001` retries after one day, at most twice. Restoration or exhaustion clears the ratio, opponent reference, retry counter and scratch values. Cancellation before victory discards the unused snapshot. Repeated victory callbacks and stale receipts cannot move the population again. There is no monthly or global population scan.

## Source evidence and limits

- Installed Vanilla `common/on_actions/00_code_on_actions.txt` documents that `on_civil_war_won` follows `on_revolution_end`. This does **not** prove state-merge timing. Nearby Vanilla revolution logic also uses a one-day follow-up where a former rebel capital can still belong to a dead country during the end callback.
- Gates of the Bosphorus uses native partial-Pop movement in `common/scripted_effects/3-01_turkfm_tanzimat_effects.txt`; Hail Columbia uses `population_ratio` with existing population values in `common/scripted_effects/usfp_scripted_effects.txt`. The return follows SB's existing muster style using this same native effect.
- Tests inject native split and ownership-merge results. They exercise shipped scripts, not the game's state-transfer, employment or mortality implementation. A successful source test is not an engine-verification claim.

## Verification

`tests/test_zulu_population_return.py` covers both movement directions, both actual winners and both player-side choices, lost population, a delayed reunion surviving court cleanup, partial ownership, third-country Natal land, unrelated regions, state ID changes, cancellation, repeated callbacks, absent snapshots, one-state bypass and zero-population arithmetic.

The focused population-return, muster and Contested Crown suites passed **97 tests**. The delayed-event lifecycle registry passed with the hidden return receipt registered. A parallel read-only review found no blocking issue.

## DP checks — all pending

1. Before the first two-region claimant war, record population in Zulu-owned Natal and Zululand; after either victor reunites them, confirm the pre-war ratio is recovered to ordinary rounding tolerance while total losses remain.
2. Check the day of victory and the following two days for correct ownership, once-only movement, missing-scope errors and the absence of population creation.
3. Inspect Pop professions, employment, food access and military manpower after the return. Native reassignment is not simulated in static tests.
4. Repeat after Klip River with ZUL owning only Zululand: the native one-state allocation must remain unchanged.
5. Confirm independent NAL-owned Natal and unrelated states retain their Pops throughout. Test interruption/cancellation before a split and a missing-region result without fallback migration.

No game launch, save migration or starting-population changes were performed for this work.
