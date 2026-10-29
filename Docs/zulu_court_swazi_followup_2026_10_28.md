# Court event destinations and Swazi demands — 28 October 2026

## Changes

**Court events.** The first and alternative princes in `.210`, and the destination prince in `.214`, now use the existing harvest attraction curve: `clamp((Popularity + 100) / 200, 0, 1)`. Each eligible prince's chance is their weight divided by the eligible total. For example, +25 versus 0 Popularity gives approximately 55.6% versus 44.4%; +100 versus 0 gives 66.7% versus 33.3%. Prominence is not counted again in this draw.

The two `.210` candidates remain distinct. Zero-weight princes cannot beat a positive-weight candidate; if every eligible candidate has zero weight, the draw is uniform among them. Existing eligibility still excludes dead/ineligible princes. Selection happens once when the episode opens, so changing Popularity while reading the popup does not change the displayed destination. `.212` retains its incumbent and `.213` retains the named house's existing patron. Campaign consequences which intentionally select the strongest coalition remain unchanged.

**Swazi demands.** The opening handler already replaced SWZ's initial conquest with humiliation, but nothing prevented a later conquest addition. SB now replaces the effective `conquer_state` definition, preserving the installed CMF 1.66.0 + `sb-1.14.3-r1` body except for one scripted guard in `possible` and `valid`. It applies only to SWZ targeting ZUL in the recorded authored frontier play (or its exact launch lease). ZUL's conquest, unrelated plays/countries and other goal types keep their existing behaviour.

Recovering the originally attacked Swazi state remains eligible. This preserves Vanilla's claim-aware territorial mirrors after a timer transfer; the restriction must not erase legitimate recapture demands. Infamy, enforcement, timers, AI scoring and the CMF land-grab hook are unchanged. The compatibility inventory pins the new override against current Vanilla; full installed-CMF verification and a byte-for-byte object-parity test cover the dependency body. No dependency files or patch revision changed.

**Mobilisation.** The recurring ORA assistance helper previously called `fully_mobilize_army` on every army each month. It now requires `is_mobilized = no`, matching the native mobilisation UI's visible-state guard. The one-time force floor and existing AI/war/recipient checks remain. The native effect still needs replay confirmation; source validation cannot reproduce native mobilisation eligibility.

**Warnings.** Removed the obsolete `sb_court_play_rebels_var` cleanup. Kept `sb_court_pledged_share_var` (court percentages) and `sb_court_annual_weight_var` (frozen harvest-report Prominence): both are read by localisation, which the engine explicitly excludes from its unused-variable analysis. No dummy reads or altered UI values were added.

## Evidence and validation

- Stable save copy and input metadata: `/private/tmp/sb-court-swazi-followup-2026-10-28/`. The copied save is dated 1 September 1839 and contains no active authored ZUL–SWZ play. It cannot demonstrate which goals were added in the reported earlier attempts.
- 104 focused source tests pass: weighted draws/order independence, zero weights, distinct candidates, frozen destinations, existing patrons, exact-play and launch boundaries, territorial recovery, unrelated-country controls and repeated mobilisation.
- Compatibility inventory passes: 39 same-path files, 122 keyed overrides and 18 changed state-region blocks. Installed CMF payload remains verified.
- Full validator: 15/17 gates pass, warn or skip. Full discovery ran 855 tests: 845 passed, eight historical skips and two failures. One was the old expected override count (121); corrected to 122 and the complete affected test module rerun successfully alongside the new follow-up tests (24 checks). The remaining failure is the pre-existing reviewed-localisation drift, also responsible for the separate localisation gate: `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`. No reviewed text or approval baseline was changed. The full suite was not repeated after the count-only test correction.
- Current-target compatibility, map/naval connectivity, source contracts and other mandatory gates pass. The five existing deferred release gates remain recorded by the validator.
- Advisory Tiger reports 1,074 errors and 149 warnings with its older 1.13.5 schema. The one additional diagnostic is `mirrored_wargoal` in the new override: this is an unchanged, required Vanilla 1.14 field. There are no other diagnostics in this task's changed scripts. The pre-existing extra blank line in `events/sb_zulu_court_events.txt` remains outside this change; touched-file whitespace checks pass.

## DP replay

Scenarios 123–125 in the court runtime matrix cover weighted event previews/choices, Swazi's later demands and timer recovery, and repeated ORA mobilisation. No game was launched and no save was modified. Runtime checks remain pending.
