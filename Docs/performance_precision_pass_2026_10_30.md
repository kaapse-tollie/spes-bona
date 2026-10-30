# Precision performance pass — 30 October 2026

This pass follows DP's cumulative-time caller review. It retains Victoria 3
1.14.5 and CMF 1.66.0 + `sb-1.14.3-r1`. Source comparisons establish equivalent
requirements and ordered effects; engine timing gains remain unmeasured.

## Changes

| Caller | Avoided work | Preserved behaviour |
|---|---|---|
| Nguni decision `possible` | Check Nationalism and the existing land requirement before the global story-safety scan. | Every requirement and named tooltip predicate is intact. Nationalism and land appear earlier in the requirement list. All 227 checks inside the shared safety helper remain unchanged. |
| Frontier colonisation `can_enact` | Try the existing Boer-republic exception before the geographical alternatives. | Identical eligibility for every country; all three complete alternatives are unchanged. Other countries incur the cheap exception check first, so a global timing improvement is not assumed. |
| Cape monthly settler ideologies | Check whether Rural Folk needs either ideology operation before scanning owned states. | The same removal and addition occur, in the same order, for the same eligible owners. Already-correct or absent groups receive no effects. |
| Cape yearly assimilation | Remove three population existence pre-checks whose predicates exactly duplicate the following population filters. | The three passes, country/state scope, filters, target cultures, ordered native calls and 2% conversion rates are unchanged. |
| Cultural-majority pop support | Skip the Reactionary/Fascist movement search when `pop_radical_fraction` is exactly zero. | The omitted multiplier is exactly one. Every nonzero fraction retains the original search and calculation. DP explicitly accepted that the neutral loss tooltip contribution may disappear for zero-radical pops. |

Pulse frequency, routing, RNG-bearing effects and all numerical gameplay values
remain unchanged. The movement's eligibility and additional-radicalism blocks
are untouched. No cache or dependency edit is introduced.

## Verification

The existing focused baseline passed all 65 tests before editing.
`tests/test_performance_precision.py` adds:

- fingerprints of complete pre-pass predicates, including tooltip contents;
- all truth combinations of the Nguni decision's unchanged top-level gates;
- Boer-exception controls for the four eligible tags and unrelated countries;
- ordered monthly ideology effects, with missing groups, completed repairs,
  unrelated cultures, split-region ownership and a foreign root;
- ordered yearly conversion calls with empty and mixed populations, excluded
  cultures, different religions and reversed population order; and
- full cultural-majority weight/breakdown comparisons against CMF for zero,
  tiny positive, negative and positive radical fractions, competing movement
  combinations, suppression/bolstering, pop types and ANZ compatibility branches.

Pre-pass fingerprints prevent the reconstructed predicates from silently
changing alongside the implementation. The yearly test records native conversion
calls rather than claiming to emulate population splitting. The complete CMF
movement contract permits only the new exact-zero guard alongside the previously
approved deltas, then compares the remaining token stream.

Only the frontier-law and cultural-majority SB object hashes and intents are
repinned. Upstream hashes and installed dependency pins are preserved.

Validation completed:

- The five new regression tests pass, including 450 full cultural-majority
  weight/breakdown cases. The existing focused baseline remains passing.
- Reversing only the authorised edits reproduces the complete pre-edit syntax
  trees of all four runtime files. UTF-8 BOMs are preserved. The inventory diff
  contains only the two SB object hashes and their intent descriptions.
- Full validation: **965 passed, eight skips, one existing failure** across
  974 tests. The failure is the existing localisation-review gate: reviewed drift
  in `sb_klip_river_county.060`, `.080`, `sb_natal_crisis.050`, and the dangling
  `sb_swazi_frontier.098.prerogative_after_blood_river` queue row.
- **15/17 validator gates passed, warned or skipped.** Both failing gates report
  that same localisation issue. Compatibility, override inventory, routers,
  runtime contracts, delayed lifecycle and naval connectivity pass. The five
  existing deferred release gates remain.
- Advisory Tiger: **0 fatal, 1,076 errors, 149 warnings**. Compared with the saved
  29 October deeper-pass output, the only added diagnostic is an unsupported
  `container` prefix in the untouched `sb_hamu_bargain_triggers.txt`. None is new
  on the edited scripts. Tiger targets 1.13.5; this is not clean engine validation.
- Whitespace checks pass. Installed CMF was verified without modifying it.

No game was launched. DP's engine timing comparison remains separate from static
parity verification. Requirement-list ordering and the accepted neutral tooltip
omission are the presentation changes described above.

Validation evidence:

- `/private/tmp/sb-precision-validation-2026-10-30.txt`
- `/private/tmp/sb-precision-source-audit-2026-10-30.txt`
- `/private/tmp/sb-precision-tiger-delta-2026-10-30.json`

Pre-edit sources are preserved at
`/private/tmp/sb-performance-precision-before-2026-10-30-gx3lz9kc/`.
