# One-state recruitment trial: annual membership bottleneck

31 October 2026. **Active trial failed to converge. Investigation only; no gameplay
source or saves changed, no game launch.**

The investigation below records the failed replay. **Subsequent authorised
implementation on 31 October:** bounded native membership refreshes are now in
source; see the follow-up at the end. The recorded saves and failed trial evidence
are unchanged. This does not mark the replacement trial as engine-verified.

## Finding

The controller activated and applied its attraction modifier correctly. It could
not recruit the required 57.275% within 26 weekly samples because ordinary native
Pop political membership updates run on an annual cohort, rather than weekly.
Each visit moves at most 10% of a Pop's political participants into or out of a
movement, with a minimum change allowance of ten individuals for small Pops.

This was an incorrect timing assumption in the trial design. The support gate
prevented another weak rebellion; it did not accelerate recruitment. By the March
save the trial had exhausted its budget and set `sb_court_recruitment_failed_var`.
Waiting with the April save cannot clear that flag or permit this war.

## Replay evidence

The five autosaves written around 12:07 cover December 1856 through April 1857.
Hashes, exact movement records, country variables and logged support components
are retained in [evidence](evidence/zulu_recruitment_stall_2026_10_31.json).

- Frozen coalitions remain Mbuyazi 248 versus Cetshwayo 185; backing Cetshwayo
  gives actual rebel Mbuyazi the correct 57.275% target.
- The recorded actual rebel is character 4481, Mbuyazi. The immediate debug
  line's character name fails to render, but the saved identity is valid.
- The attraction factor rises from 9.164 to 13.746, 20.619, 30.9285 and the cap
  of 32 by week four. The movement retains the recruitment modifier at multiplier
  30, alongside the existing +100% mobilisation modifier.
- Logged combined support remains around 10%. The last retained sample, week 17,
  is 10.693%: 9.313% popular, 13.386% military and 9.426% wealth support. Later
  cached percentages are not serialised; DP observed about 11% in April.
- Saved sample counts are 14, 18, 23, 26 and 26. Failure is present in March and
  April. The debug log retains only samples 1–17, so the later count/failure comes
  from saves, not an invented log reconstruction.
- Activism reaches 100% in February. All five movement records lack a civil war;
  `last_failed_civil_war_start_date` remains `1.1.1`. This is failure to qualify
  under the support gate, not an observed failed native territorial allocation.
- Movement members rise only from 6,657 to 7,364 over December–April. Aristocrat
  Pop 18767 has 345 workforce and exactly 35 claimant supporters throughout;
  its other movement memberships are also unchanged over those snapshots.

The current error log has 339 repeated Vanilla AI-strategy errors at
`common/ai_strategies/00_default_strategy.txt:2535`; no recruitment-script error
accounts for the stalled support. Earlier rotated launch logs contain other
existing warnings and are not represented as clean.

## Native cause and verified API

[Installed-engine excerpts](evidence/zulu_pop_recruitment_cadence_1_14_5_arm64.txt)
include exact symbols and reproduction commands:

1. The ordinary `CPopManager::UpdatePopsInterestGroupsAndMovements()` calls
   `CollectPopsForDailyUpdateOnceEachYear`, selecting an annual ID/day cohort.
2. `CPop::AdjustPoliticalMovementSupport` derives the desired share from modified
   attraction relative to competing movements, then applies the per-update
   10%/minimum-ten adjustment limit from Vanilla's defines.
3. Movement creation calls the country-specific updater once. That provides an
   initial adjustment; subsequent ordinary membership updates are annual.
4. The Pop Attraction modifier is part of the native weight calculation. No
   fixed 11% recruitment ceiling was found. Modifier add/remove invalidates the
   cache; no evidence supports the alternative theory that weekly replacement
   continually postpones modifier activation.

There is a supported country effect: **`recalculate_pop_ig_support = yes`**.
Vanilla's church/state laws use it, and its native implementation calls the same
country-specific updater. Despite the name, it updates movements too. It performs
one normal bounded adjustment; it does not directly set this movement's support.
It also updates **all other movements and IG memberships in that country**.

## Recommended next trial, not implemented here

Retain the frozen target and actual-support gate. Add a limited number of targeted
country recalculations during pending one-state recruitment, with native update
boundaries between attraction changes, membership recalculation and subsequent
support sampling. Do not read a same-block cached support result as a fresh one.
Stop refreshing once qualified or invalidated; do not run this globally or during
the active war. Keep an explicit budget and measure the other IG/movement effects.

Removing the support gate would restore the known one-province risk. Raising
attraction above 32 cannot remove the annual membership bottleneck. Recreating
movements repeatedly would refresh unrelated creation state and is unnecessary
given the existing recalculation effect.

This targeted refresh is the smallest supported next experiment, not proof of
convergence, province balance or staffed military strength. An already failed
episode is not a suitable checkpoint without an explicitly designed recovery;
the supported baseline remains a restart before the side choice.

Independent Sol 6.1 Max review confirmed the saved controller arithmetic, annual
native update path, adjustment limit and country-scoped recalculation API. No
gameplay tests were rerun for this read-only investigation; existing static passes
do not establish native convergence.

## Authorised follow-up: bounded refresh implemented

The existing weekly `.991` delivery now samples and logs support, attempts
qualified advancement, and checks expiry before requesting any membership update.
For a still-valid pending one-state episode outside its support band, samples
1–25 perform one `recalculate_pop_ig_support` call in that country. Sample 26
can still advance a qualified war; otherwise it expires without another refresh.

The next attraction factor is calculated before recalculation, but applied to the
movement **afterwards**. The native update therefore uses the previous week's
settled modifier. Its support is sampled on the following weekly delivery; there
is no same-delivery advancement based on an assumed fresh cache. Ready, failed,
cancelled, advanced, active-war and multi-state episodes receive no refresh.
Other movements and IGs in the pending country also receive native updates.

This is a bounded recruitment experiment, not a direct support assignment or an
army split guarantee. Replay from before side selection. The failed March/April
episode remains failed, and no saves or dependency payloads are changed. Runtime
case 155 covers the added timing, side effects and performance checks.

Validation of this follow-up:

- 109 focused recruitment, claimant-conflict and muster checks pass. Independent
  Sol 6.1 Max review passes 149 related checks and reports no blocking finding.
  The native refresh stub records the request and its input modifier; it does not
  invent a new support value or simulate recruitment convergence.
- Full discovery: **1,006 tests; 997 passed, eight existing historical skips,
  one existing localisation-review failure, no errors**.
- Full validator: **15/17 gates passed, warned or skipped**. The unit/localisation
  failures both reflect the existing dangling Swazi
  `.098.prerogative_after_blood_river` queue entry and reviewed prose drift in
  Natal `.050` and Klip `.060`/`.080`. No localisation is changed in this follow-up.
- CMF installation/integrity, compatibility inventory, map/naval checks and
  script contracts pass. Advisory Tiger: **0 fatal, 1,076 errors, 147 warnings,
  one untidy, one tip**. Error identities match the preceding run; the warning
  difference concerns scope deduction in unrelated Bechuanaland/story helpers.
  No diagnostic names the recruitment files. `git diff --check` passes.

Full output: `/private/tmp/sb-recruitment-refresh-acceptance-20261031.txt`.
No launch was performed. Convergence, native outbreak, staffed forces, wider
local political changes and tick cost remain pending DP.
