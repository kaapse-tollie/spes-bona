# State modelling, arithmetic and selection

Read when: Counters, projections, snapshots, rankings, arithmetic or random selection.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x and 1.15.0 builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="state-01"></a>

## STATE-01 — Use one authoritative value and deliberate projections

A journal bar
projected from country state must not also apply independent native drift.
Reset derived lists and totals before rebuilding them without overwriting
another actor's records. A "no change" notification policy must still record
that the periodic calculation ran.

<a id="state-02"></a>

## STATE-02 — An exclusion must survive both calculation and commit

Skipping an actor
in the calculation loop can leave no new value for the later commit loop.
Applying that absence as an empty result can reset or withdraw an actor who
was meant to remain unchanged. Carry the exclusion through application or
explicitly distinguish "not calculated" from an intentional empty result.
Test excluded actors alongside actors receiving real updates.

<a id="state-03"></a>

## STATE-03 — Keep distinct concepts in distinct records

Present allegiance, future
promises, constitutional preference and eligibility are not interchangeable.
Likewise, a target value, its current value, an entry threshold, progress and
an outcome describe different stages. A low target does not prove the current
threshold has been reached or that an attempt will succeed.

Percentage shares also need an explicit denominator. A displayed share of pledged
backing does not establish a threshold measured against all represented backing.
Use the agreed pool consistently in the trigger and its explanation; test a
case that passes one denominator but fails the other. A save can establish that
distinction without proving what a subsequent native war would do. See the
[retirement investigation](../compatibility/zulu_retirement_succession_2026_10_30.md).

<a id="state-04"></a>

## STATE-04 — Preserve the intended arithmetic order

Initialise an aggregate before
accumulating; a later `value =` assignment resets earlier additions. Clamp
after combining terms when the bound applies to their total. Sequential
effects may intentionally clamp at intermediate steps; moving those clamps
changes the result. Test signed inputs, zero, opposing adjustments and exact
boundaries; a negative multiplier can reverse a deduction. Recheck units when
scaling counters, caps, seeds, rewards, archives and UI projections. Existing
saved counters are not rescaled by a source edit.

Check numeric literals against the engine reader's precision before trusting
host-language arithmetic tests. A mathematically valid coefficient can fail to
load. After rounding a rejected literal, verify the original error tolerance and
retest parsing; Python's acceptance does not establish engine acceptance. See
the [1.15 launch evidence](../compatibility/1_15_0_launch_debug_2026_11_05.md).

<a id="state-05"></a>

## STATE-05 — Group totals and representative values have different uses

If one actor
represents a group, aggregate each eligible member once and rank by the value
the rule actually requires. Do not count native trait or office bonuses twice.
Several actors writing one state-level cache will overwrite one another unless
their contributions are aggregated first.

A total can also contain exclusions specific to one mechanic. A recruitment
pool may omit actors already contributing through native recruitment, while
political backing still needs those actors counted once. Reusing the former
can make a valid role change reduce apparent political strength. Keep the pools
explicit and test the transition with the same people before and after it.
The [Chiefdoms pressure implementation](../compatibility/chiefdoms_prominence_2026_11_15.md)
tests that accounting in source; native target convergence remains a separate check.

<a id="state-06"></a>

## STATE-06 — Keep unintended ranking feedback out of the inputs

A bonus or penalty
awarded by the previous ranking can entrench the previous winner or make
repeated recalculation oscillate. Where those rank-derived effects are not
intended to influence selection, compare the underlying values before
applying them. Test both a genuine change of rank and repeated recalculation
with otherwise unchanged inputs.

<a id="state-07"></a>

## STATE-07 — Relative values need their original context

An encoding meaning
"supports the incumbent" can change meaning after succession or a country
split. Save the referenced identity and rebase the relationship against the
receiving context. Physical host country and registered home need not be
the same.

<a id="state-08"></a>

## STATE-08 — Snapshot restoration can undo later valid changes

Restoring earlier
records can revive deliberately removed eligibility or erase newly acquired
commitments. Specify which fields are intentionally frozen and preserve valid
changes outside that snapshot contract, or reapply required terminal cleanup
after restoration. Test a valid change between capture and restoration,
including repeated restoration.

<a id="state-09"></a>

## STATE-09 — Scope once-only records to the entity they describe

A per-ruler attempt
allowance cannot be represented by only the most recent ruler: an A→B→A
sequence would reset it. Birth, adulthood and recognition receipts need the
relevant identity; a country-wide flag can wrongly block later generations.
Separate independent cooldowns and action allowances.

<a id="state-10"></a>

## STATE-10 — Reserve shared candidates before another operation consumes them

Two
rewards drawing from the same uncommitted pool can invalidate each other.
Reserve distinct eligible identities and preview that same set. Ranking alone
does not protect an identity from eventual selection.

<a id="state-11"></a>

## STATE-11 — Native random-list weights lose fractional precision

In the inspected
engine, evaluated factors are converted to whole-number weights; values such
as 0.05 and 0.50 both become zero. Scale all competing weights equally to retain
the required precision. Test the engine's truncation rather than substituting
floating-point selection, and define the all-zero case. The
[native weight-conversion evidence](../compatibility/evidence/zulu_random_list_weight_1_14_5_arm64.txt)
establishes truncation, not observed campaign choice frequencies.

<a id="state-12"></a>

## STATE-12 — Ordered-list positions can repeat the last item

An unavailable
`ordered_in_list` position caps at the last available entry. Iterate a bounded
list once for distinct choices, or exclude a selection before selecting again.
`check_range_bounds = no` permits a shorter list; it does not make repeated
positional lookups distinct. Test empty, short, full and oversized lists.

<a id="state-13"></a>

## STATE-13 — Unused-variable warnings do not identify all consumers

The engine does
not count localisation reads. Check GUI, localisation and dependency readers
before removing state; definition-only symbol checks do not audit variable
assignments. Remove genuine leftovers from a replaced implementation rather
than adding dummy reads.
