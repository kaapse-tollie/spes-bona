# Resource Balance Executive Summary

SB's Southern African resource caps begin with a reproducible research model, then apply explicit state-split and gameplay corrections. The complete workbook, evidence tables, scripts, and audit reports are archived outside the mod at `../References/Resource rework/resources/` so release validation does not depend on a large research package.

## Method

The archive combines historical production anchors, modern geological and agricultural comparators, state-footprint mappings, chronology gates, and documented exceptions. Arable land, forestry, rubber, and quantity resources use separate calibrated paths rather than one universal denominator. Every published row records whether it is formula-driven, quantitatively adjusted, constrained to zero, or retained as an explicit exception.

The live state file remains authoritative. Research outputs are advisory whenever later map splits or observed gameplay require a documented balance adjustment.

## Accepted Live Differences

- **Cape Colony:** `42` arable land and `12` fishing reflect the reduced post-split Western Cape footprint and a conservative coastal balance pass rather than the archived `44/15` recommendation.
- **Northern Cape:** `6` arable land, `3` fishing, and `8` lead represent the narrowed coastal/base-metal remainder. Kimberley, the iron belt, and their associated capacity moved out with the Griqualand West and Bechuanaland splits.
- **Griqualand West and Bechuanaland:** these new states were created after the original 14-state workbook surface. Griqualand West carries `5` arable land and the initial iron slot, with later iron unlocked by technology; Bechuanaland carries `6` arable land and no capped mine resource.
- **West and East Transvaal:** the live logging additions support the split Highveld economy and AI buildout. The archived undiscovered-gold rows are not currently applied.
- **Vrystaat/Transorangia:** the live logging slot is an accepted gameplay correction after the state and economy revisions.
- **Namaqualand:** `4` arable land supersedes the archived `2` after starvation testing in SAN, Oorlam, Herero, and Rehoboth fragments.

These differences are deliberate and should not be treated as accidental data drift. The archived test command therefore exits nonzero while the accepted live-cap mismatch remains; it must not print an unconditional success result.

## Deferred Research

Only the Transvaal and Orangia gold allocation remains an unresolved resource-design item. Reassess those undiscovered-gold caps during the next relevant content block, when discovery timing and regional event mechanics can be evaluated together. No other accepted live difference requires reopening the resource model.
