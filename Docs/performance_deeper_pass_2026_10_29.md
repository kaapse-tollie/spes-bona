# Deeper performance pass — 29 October 2026

DP confirmed noticeably faster ticks after the first pass and requested a deeper
pass without changing behaviour. This follow-up retains Victoria 3 1.14.5, SB
0.20.2 and CMF 1.66.0 + sb-1.14.3-r1. It changes no gameplay values, pulse cadence,
RNG calls, localisation, historical commitments or dependency payload.

## Changes

| Surface | Avoided work | Preserved behaviour |
|---|---|---|
| Court house selection | Rank each shared house once per recalculation, rather than once per member; reject a different house before nested eligibility checks. | Same native ranking, tied head choice, rank penalties, member summation order and final saved scopes. Links are rebuilt each call. |
| Court tallies | Check representative/weight markers before nested country-membership checks. | Same eligible representatives, coalition totals, future pledges, recruitment contributions and foreign-home handling. |
| Imperial Confederation involvement | Evaluate eligibility once per country in each maintenance pass. | Same involved countries and ordered add/remove operations, including missing GBR/JE cases. Eligibility does not depend on involvement itself. |
| Southern formation safety | Combine two global existence scans; check local route flags before nested state snapshots. | All 227 original flags, containers and state markers retain their scope and blocking meaning, including damaged-save snapshots. |
| Cultural minority activism | Check neighbouring movement insurrection before its culture lookup. | Same optional-culture semantics, iterator scopes, factors and annexation recreation hooks. |
| Claimant challenge eligibility | Reject high Prerogative and existing reservations before checking native civil wars. | Same thresholds, concurrency protection and challenge timing. |

The house selection uses the original ordered iterator. The first ranked member
becomes the head; all matching members receive that reference during the same
traversal. Later outer-loop visits reuse that per-call reference. Unaffiliated
characters retain their original treatment. No cache survives a recalculation.

Installed ARM64 code inspection by the independent reviewer confirms that
`COrderedInScriptedListEffect::ExecuteWithArray` invokes `OrderList` before
choosing positional selection or full traversal. `OrderList` uses stable sorting;
full traversal's first result is therefore the former `position = 0` selection,
including ties. This evidence is specific to the installed baseline.

## Deliberately retained work

The full post-drift backing refresh remains. A challenge callback can change the
rival's agitator role and therefore Prominence. Native Prominence is capped at
100, so repeated rank/modifier refreshes cannot simply be assumed idempotent.
Skipping this work would require broader behavioural proof.

The inherited large neighbouring-state scans remain. Replacing them with a new
country cache would require reliable invalidation for borders, cultures and
movement lifecycles. No new cache, polling schedule or global cadence change is
part of this pass. Permanent-modifier replacement behaviour is also unchanged.

## Verification

The source-executed parity checks compare pre-pass expressions against the shipped
ones, including complete country/character/movement projections and final saved
scopes. Coverage includes tied and capped Prominence, singleton/shared houses,
reversed and duplicate roster entries, minors, deaths, exiles, foreign homes,
leadership changes, repeated calls, institutional exit/re-entry, missing journals,
retagged route holders, optional movement cultures and challenge boundaries.

Illustrative source counts, **not engine timings**:

- A 39-character grouped-house fixture uses 13 sorts instead of 35 and 153 nested
  representative-eligibility checks instead of 1,481.
- A singleton-house fixture retains 35 sorts, with eligibility checks falling
  from 1,481 to 151.
- A clear 300-country formation fixture visits 300 countries instead of 600.
  An active route holder can also avoid the state traversal entirely.

The minority override's SB object hash and intent are repinned. Its complete CMF
contract canonicalises only the equivalent reordered neighbour predicate, then
requires token parity for every other field apart from the two existing authored
annexation hooks. Upstream and installed dependency hashes are unchanged.

Focused validation: **191 tests passed**. Independent Sol 6.1 Max review found no
blocking issues and separately exercised monthly/court parity, including native
Prominence cap variants.

Full validation (`tools/validate.py --skip-cmf-sync --tiger`):

- **935 passed, eight historical skips, one existing failure** across 944 tests;
  no unit errors. The failure is the pre-existing reviewed-localisation manifest
  drift in `sb_klip_river_county.060`, `.080`, `sb_natal_crisis.050`, plus the
  dangling `sb_swazi_frontier.098.prerogative_after_blood_river` queue row. No
  localisation or approval was changed by either performance pass.
- **15/17 validator gates passed, warned or skipped.** Both failing gates report
  that same localisation issue. Installed CMF, override compatibility/inventory,
  map/naval, routers, runtime contracts and delayed lifecycle pass.
- Advisory Tiger: **0 fatal, 1,075 errors, 149 warnings**. Error diagnostics are
  unchanged from the first pass. Its four added warnings concern unchanged CMF
  international-situation illustration scopes, not edited performance bodies.
  Tiger still targets 1.13.5 while this mod targets 1.14.5; this is advisory
  validation with existing limitations, not clean engine validation.
- Five existing deferred release gates remain: BC-20, BC-22, CP-07, QUAL-09 and
  SUP-05. Whitespace validation passes. Dependency release sync was skipped;
  installed-payload verification ran without modifying CMF.

No game was launched. DP's qualitative confirmation applies to the first pass;
engine timings for this deeper pass remain unmeasured. The broader pre-release
performance audit stays open; no additional benchmark is required before DP
continues ordinary playtesting.

Evidence and recovery inputs:

- `/private/tmp/sb-performance-deeper-focused.txt`
- `/private/tmp/sb-performance-deeper-validation.txt`
- `/private/tmp/sb-performance-deeper-before-2026-10-29/`
- `/private/tmp/sb-deeper-perf-court-before-2026-10-29/`
- `/private/tmp/sb-performance-monthly-before-2026-10-29/`
