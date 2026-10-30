# Small simulation performance pass — 29 October 2026

Status: source changes implemented; engine timing comparison pending DP. This is
the first limited follow-up to `PERF-20261028-01`, not completion of that audit.
Game 1.14.5 / CMF 1.66.0 + `sb-1.14.3-r1` remain unchanged.

## Evidence and boundaries

DP reported these script timings over three months in 1843. These are the supplied
totals, not measurements independently reproduced by Codex. The country and call
counts for each movement entry were not supplied. File labels on keyed overrides
cover the full effective Vanilla/CMF definition, not just SB's additions. Totals
and a single invocation are not interchangeable and must not be summed into a
claimed percentage of overall tick time.

| Reported location before this pass | Reported time | Assessment / action |
|---|---:|---|
| `zz_sb_absolutist_override.txt:409` | 954 ms total | Full inherited additional-radicalism calculation. Retained; no safe major reduction established in this pass. |
| `zz_sb_cultural_majority_movement_override.txt:452` | 631 ms total | Check insurrection before matching neighbouring movements' cultures. Keep every factor and scope. |
| `zzz_sb_cape_political_movement_overrides.txt:732` | 239 ms total | Inherited Liberal additional-radicalism calculation; retained. |
| `zz_sb_armed_forces_override.txt:233` | 165 ms total | Short-circuit acceptance/incorporation guards; exclusive wage branches; share the existing in-government guard. |
| `zz_sb_absolutist_override.txt:12` | 147 ms total | Check cheap disband conditions before movement scans. Also combine creation's two exclusion scans after country/law checks. |
| `sb_on_actions.txt:43` | 143 ms for one fire; others around 100 ms | This is the router, not an individual handler. Keep routing/cadence. Add narrow Cape ownership and NGI/ZUL handler guards. |
| `zz_sb_cultural_minority_movement_override.txt:832` | 123 ms total | Full inherited additional-radicalism calculation; retained. |

The cultural filenames in the timing notes contained `culutral`; the table uses
the actual repository paths. Line numbers will shift after editing.

## Changes and preserved behaviour

- **Absolutists:** identical creation/disband truth conditions; one explicit
  alternative-movement scan instead of two. Cheap exclusions precede it. Authored
  Zulu exclusion, surviving Traditionalists, constitutional-monarchist conversion,
  Carlist/Miguelist exceptions, Japan, France and all CMF hooks remain.
- **Cultural majority:** insurrectionary status precedes the cultural predicate
  inside the existing neighbour movement iterator. Peaceful movements need no
  cultural lookup. The country/`prev`/movement scopes and numerical contributions
  are unchanged. No new neighbour iterator or country cache is introduced.
- **Armed Forces:** populations failing acceptance skip the social-hierarchy
  lookup; incorporated states skip colonial-law checks. Soldier wages use an
  `if`/`else_if` chain because only one wage level can apply. Two existing
  in-government multipliers share their guard, retaining arithmetic order and
  separate tooltip descriptions. Imperial Administration's attraction stays.
- **Cape monthly maintenance:** the existing country-owned state scan is preceded
  by native `has_state_in_state_region = STATE_EASTERN_CAPE`. Countries without
  a portion of Eastern Cape skip the scan. Split ownership, resistance traits,
  Xhosa cleanup and all monthly effects remain unchanged. No `root` substitution
  or new saved scope is used.
- **Nguni tribute:** a top-level NGI/ZUL guard prevents entering the effect for
  unrelated countries. Every original effect branch already requires one of
  those two countries. Link creation, destruction and tombstone repair are intact.

No court formula, movement attraction, activism, war allocation, event delay,
pulse frequency, localisation or dependency payload changes are included.

## Verification

`tests/test_performance_pass.py` executes the shipped predicates/arithmetic
against their previous Vanilla/CMF expressions. Coverage includes:

- Absolutist creation/disband truth tables across laws, country exceptions,
  authored constituency, voting, history flags and competing movements.
- Majority culture matching for insurgent/peaceful majority, minority and
  unrelated movements, including shared and different cultures.
- Armed Forces scores and ordered breakdown entries across five pop types, all
  five wages, government/opposition/missing IG, acceptance, incorporation, three
  army laws and both Imperial Administration modifier values.
- Eastern Cape ownership/trait checks with a foreign root and another owner's
  matching state; unrelated-country tribute controls.

Source traversal examples: the explicit Absolutist alternative-movement checks
visit 12 unrelated movements once instead of twice; a French creation exclusion
visits none instead of 24. A country with 200 states and no Eastern Cape portion
visits none instead of 200 in that resistance check. These are synthetic traversal
counts, **not engine benchmarks or a measured percentage speed-up**.

The existing complete-CMF Absolutist contract now proves logical equivalence for
the two changed predicates and still requires token parity for every other field.
Only the three affected SB override hashes/intents were repinned; upstream and
installed dependency hashes remain unchanged. Current Vanilla's geography trigger
and Sepoy Mutiny JE demonstrate native region ownership checks; Gates of the
Bosphorus and Hail Columbia retain country-triggered feature handlers, as SB does.

Validation completed:

- Focused run: **48 passed, three historical skips**. Independent parallel review
  found no remaining issue and separately reran the affected contracts.
- Full discovery: **926 passed, eight historical skips, one existing failure**
  (935 tests, no errors). The failure is the existing localisation manifest gate:
  reviewed drift in `sb_klip_river_county.060`, `.080`, `sb_natal_crisis.050`, and
  the dangling `sb_swazi_frontier.098.prerogative_after_blood_river` queue row.
  This pass changes no localisation or approvals.
- Final validator without repeating Tiger: **14/16 passed, warned or skipped**;
  its two failing gates both report that existing localisation problem. Current
  compatibility/inventory, map/naval, router and lifecycle checks pass.
- Advisory Tiger on the same runtime changes: **0 fatal, 1,075 errors, 145
  warnings**. No new diagnostic is attributable to these edits; the existing
  schema/compatibility limitations remain. This is not a clean engine validation.
- Whitespace check passes. CMF release sync was disabled and the installed
  dependency verified without modification. No game was launched.

Local logs: `/private/tmp/sb-performance-focused.txt`,
`/private/tmp/sb-performance-validation-final.txt`; advisory Tiger output is in
`/private/tmp/sb-performance-validation.txt` (its earlier unit run also includes
three now-updated exact-order/hash contract failures). Pre-edit source copies are
under `/private/tmp/sb-performance-before-2026-10-29`.

## DP repeat measurement

1. After a fresh launch loading these source changes, repeat the same three-month
   1843 checkpoint at the same speed, profiling settings, DLC and load order.
2. Compare elapsed time for the complete period and per-block totals **and call
   counts**. Repeat if possible; isolated maxima are noisy.
3. Spot-check movement activism breakdowns, Armed Forces attraction, Cape/Xhosa
   resistance and Nguni tribute. Their values and timing should match.
4. If monthly spikes remain, capture the child-handler timings beneath
   `sb_on_actions.txt:43`. The router total cannot identify which child dominates.

All four checks remain pending. The broad pre-release performance investigation
stays open, particularly inherited neighbour scans and any sustained court work
not isolated by this profile.


## DP feedback and deeper pass

DP subsequently confirmed that tick speed was noticeably faster and waived further
measurement of this first pass. That is qualitative runtime confirmation, not a
measured percentage improvement. The deeper pass is recorded separately in
[performance_deeper_pass_2026_10_29.md](performance_deeper_pass_2026_10_29.md).
The repeat-measurement list above remains a future pre-release profiling protocol;
it is not a prerequisite requested of DP before continuing playtests.
