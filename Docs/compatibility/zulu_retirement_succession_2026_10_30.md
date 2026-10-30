# Mpande's retirement: succession shares and event presentation

30 October 2026. Source changes and save investigation; engine replay remains pending DP.

## Save diagnosis

The retained checkpoints run from 1 May to 1 September 1856. In `autosave_1.v3`, dated **1 August**, ZUL (481) still has Mpande (4478) as ruler and Mbuyazi (4481) as recognised heir. The court has **756 represented Prominence**, of which **596 is pledged to successors**.

| Prince | Succession backing | Share of pledged | Share of all represented |
|---|---:|---:|---:|
| Cetshwayo (4480) | 185 | 31.04% | 24.47% |
| Mbuyazi (4481) | 248 | 41.61% | 32.80% |

The old major-challenger test used the last column. Cetshwayo needed 189 Prominence, four more than he held. No rival qualified, so the controller selected the one-option peaceful accession `.001`. The **1 September** save has Mbuyazi ruling and the once-only Mpande retirement receipt. These observations explain the peaceful path; they are not evidence of a failed native revolution. The game never reached its movement/war creation stage for this succession.

[Bounded evidence and save hashes](evidence/zulu_retirement_threshold_2026_10_30.json) preserve the observation independently of later autosave replacement.

## Approved correction

DP approved **25% of succession-pledged Prominence** on 30 October. The trigger now uses the same share as the court display. The obsolete total-share projection is removed; total court Prominence remains available for the other calculations. Living challenges still use current allegiance and their existing threshold; succession uses future promises. The selected pair's force division excludes uncommitted and third-party backing as before.

A source-executed fixture with 756/596/185/248 opens `.004` once, with Mbuyazi and Cetshwayo and their actual pair weights. It does not create or verify an engine war. Acknowledging an old peaceful popup rechecks backing and the displayed nominee: sufficiently strengthened opposition opens the faction choice; an invalid or replaced nominee cannot be installed beneath the old portrait.

## Event changes

- **`sb_court_succession.001`:** one-character accession scene with explicit Mpande retirement title, description and flavour when he is the living outgoing ruler. Its acknowledgement previews accession and retirement. The tooltip states the contested-succession condition because native Prominence can change before the next cached court refresh. A stale choice offers reconsideration rather than installing the old nominee.
- **`sb_court_succession.004`:** retains the two-contender choice and adds a retirement-specific scene explaining Mpande's withdrawal and the divided household. No extra popup, forced war, scripted death or new deadline.
- **`sb_court_dunn.002`:** remove refusal, retain one distribution acknowledgement and the two-week reward. First delivery is scheduled **three days after accepting `.001.a`**; later annual deliveries keep their existing immediate dispatch. Reserve the trader/recipient before scheduling and revalidate on delivery and answer. No progress is granted merely by opening it.

The installed **`regency.2`** script and complete localisation supplied the resignation model: public explanation, concrete change of responsibility, portrait and decisive acknowledgement. The contested variant retains the actual princes' paired portraits. Both windows are native. New prose remains **TO REVIEW**; reviewed namespaces and unrelated historical evidence are preserved.

## Verification

**145 focused checks pass**, covering the saved distribution, 25% boundary, unpledged dilution, current/future separation, one retirement reservation, invalid or strengthened opposition, both war sides, delayed Dunn delivery, changed owner/death/completion and once-only gun progress. The independent reviewer found no remaining blocking source issue. None of these checks establishes engine delivery or UI rendering.

Full validation: **15/17 gates passed or warned**. Complete discovery ran **986 tests: 977 passed, one existing failure, eight historical skips**. The failing unit gate and localisation gate report the same pre-existing issues: the dangling `sb_swazi_frontier.098.prerogative_after_blood_river` review-queue entry and reviewed-text baseline drift in Klip `.060`/`.080` and Natal `.050`. This task does not alter those namespaces or their approvals.

CMF integrity/compatibility, override comparison, map/naval checks, runtime contracts, symbols and delayed-event lifecycle pass. Advisory Tiger remains at **0 fatal, 1,076 errors, 149 warnings, one untidy and one tip**, unchanged from the preceding pass; its installed version targets an older game baseline. `git diff --check` passes. Full output: `/private/tmp/sb-retirement-validation-20261030.txt`.

## DP replay

1. Restart and load **`autosave_1.v3` (1 August 1856)** or an earlier checkpoint before the retirement pulse. Confirm `.004` presents Mpande's withdrawal and both princes, then test either side through native mobilisation/split. The September save already completed the peaceful accession and is not a reproduction checkpoint.
2. Reduce the rival below 25% of succession-pledged backing. Confirm `.001` shows the peaceful retirement scene, an effect tooltip, living Mpande's retirement and only the promised allegiance conversions. Hold it open while backing changes and verify the contested route if the threshold is crossed.
3. Test earlier natural death and a minor successor: no living-retirement scene, no missing portrait/name, and the existing regency rules remain intact.
4. From before Dunn's arrival, accept him and advance three days. Confirm one delivery popup, one option, no early progress and exactly two weeks on acknowledgement. Check a dead/transferred trader and completed Firearms during the delay.

All four replay rows are **Pending DP**. No game launch, save migration or dependency change was performed.
