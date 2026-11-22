# Time, modifiers and reversible effects

Read when: Durations, decay, repeated grants or modifier cleanup.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x and 1.15.1 builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="mod-01"></a>

## MOD-01 — Duration units belong to the field, not the surrounding story

Country
event `duration` is measured in months in the inspected build. Script duration
arithmetic uses 30-day months and 365-day years; calendar boundaries and pulse
counts are different. Use a native age value or a timed marker on an object whose
expiry is established, and define precedence when success and expiry coincide.
Date comparisons use `game_date`; the plausible-looking `current_date` was
rejected by the target validator.

A duration parsing and appearing in a save does not establish that its holder
participates in native expiry. In the [1.15.1 container investigation](../compatibility/chiefdoms_playtest_2026_11_14.md#review-clock),
two script-container counters stayed unchanged across 120 days while country
counters decayed. Both a displayed deadline and a deduplication receipt can
freeze this way. Prefer the JE's native `journal_entry_age` for a JE-age deadline;
compare repeated saves before trusting a custom holder's timers. Test the old
frozen state too. Static fixtures that manually remove the marker do not prove
engine expiry, and source corrections still require native replay.

<a id="mod-02"></a>

## MOD-02 — Duration fields have their own parser

`add_modifier` duration fields
accept a number or named script value, not a bare `var:` link. Put dynamic
duration arithmetic in a named script value and test that syntax, not only
its intended numerical result. The [parser diagnosis and verification limits](../compatibility/zulu_institutions_launch_2026_10_18.md#corrections)
distinguish observed load errors and native inspection from pending replay.

<a id="mod-03"></a>

## MOD-03 — Guard optional removals

Removing an absent timed modifier logs an error.
Use `has_modifier` where absence is normal, including neutral recalculation
and repeated cleanup.

<a id="mod-04"></a>

## MOD-04 — Same-key grants are not automatically independent commitments

Reapplying a timed modifier can refresh its duration instead of stacking a
separate expiry. Verify its stacking contract. When independent obligations
require separate accounting, preserve each expiry while displaying the correct
aggregate; expiry must not depend on the original participant remaining valid.

<a id="mod-05"></a>

## MOD-05 — Replacing an object destroys its modifiers, not its owner's flags

A country-level "already granted" marker can survive movement replacement and
prevent restoration. Preserve only the unexpired remainder of known grants,
including decay, without resetting their original one-use flags or granting a
fresh full duration. An aggregate modifier total cannot reconstruct individual
grants; untracked old-save expiries cannot be recovered exactly. The inspected
`modifier:` value link does not support political-movement scope, so do not
assume it exposes those grants. Record necessary expiries when granting them.

<a id="mod-06"></a>

## MOD-06 — Distinguish entitlement from current application

A permanent country
reward may apply state modifiers only while the beneficiary owns those states.
Ownership changes should update the application without awarding the reward
again or starting an unintended expiry.

<a id="mod-07"></a>

## MOD-07 — Undo only changes owned by the feature

Snapshot relevant pre-existing
penalties, roles and locks before temporary changes. Cleanup must preserve
earlier native penalties and unrelated grants; a missing snapshot is not
permission to clear them all.
