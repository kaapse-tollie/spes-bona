# Overrides, rebases and performance

Read when: Overrides, dependency updates, copied definitions or performance.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="upstream-01"></a>

## UPSTREAM-01 — Inspect the effective definition, including dependencies

A Vanilla body
may already be replaced by CMF, and a copied DLC mechanic may depend on external
journal, scoring or maintenance code. Trace nested calls and every caller of
a shared helper before changing it. Copying a modifier does not copy the
surrounding mechanic.

<a id="upstream-02"></a>

## UPSTREAM-02 — Review semantics before refreshing hashes

Exact-path shadows, keyed
replacements, GUI types and localisation overrides have different load
behaviour. Compare the complete affected body, preserving dependency hooks and
untouched branches. A matching filename inventory or new hash is not a
semantic compatibility check.

<a id="upstream-03"></a>

## UPSTREAM-03 — Override mechanisms are not interchangeable

Customisable-localisation
functions do not accept `REPLACE:` prefixes in the inspected build. A partial
`INJECT` cannot overwrite an already-read trigger section. Use the supported
mechanism and inventory any required full shadow rather than assuming a
familiar prefix works everywhere.

<a id="upstream-04"></a>

## UPSTREAM-04 — Rebase every effective layer

Updating a dependency does not update the
mod's own copy of the same definition. Keep compatibility patches reproducible
and distinguish patched dependencies from immutable upstream releases so
normal synchronisation cannot erase the patch.

<a id="upstream-05"></a>

## UPSTREAM-05 — A depot delta covers only its exact endpoints

Missing historical inputs
can prevent reproducing an old comparison without implying current corruption.
Keep historical reproduction separate from mandatory current-build, manifest
and payload checks. Verify every pinned override against its actual baseline.

<a id="upstream-06"></a>

## UPSTREAM-06 — Profiler attribution is not implementation ownership

A replacement's
time includes inherited code, and a router includes its children. Separate
total time, call count and individual spikes before identifying a bottleneck.
Source operation counts are not engine benchmarks.

<a id="upstream-07"></a>

## UPSTREAM-07 — Prefer equivalent cheap guards before cadence changes or caches

A country-level `has_state_in_state_region` check can reject non-owners before
a state scan; retain the original filter for split ownership. Preserve effect order, RNG calls, scope paths, optional references,
arithmetic and tooltip breakdowns. Compare old and new results rather than
asserting only that faster-looking syntax exists.

<a id="upstream-08"></a>

## UPSTREAM-08 — Recalculation is not automatically idempotent

Role changes, native caps
and callbacks can alter later projections even when one visible variable
changed. Cache only values whose invalidation is understood; do not remove a
refresh because a simplified test model omits those side effects. Measure
runtime gains from comparable checkpoints.
