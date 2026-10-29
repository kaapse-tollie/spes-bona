# Zulu court playtest follow-up — 25 October 2026, 18:30

Source fixes and tuning for DP’s Retief-stage playtest. New campaigns remain the supported baseline. No launch, save migration or dependency change was performed.

## Changes

- Claimants receive +20 native Prominence while eligible, with the existing adult/renunciation/accession/exit lifecycle.
- All court costs based on reserve capacity are doubled. Pledges cost 40/62.5/100/130/160% at 10/25/50/75/100 Prominence. Incident discredit, dispute settlement and royal firearms cost 20/30/40%. Initial and renewed incident quotes now use the same value. Fixed non-reserve costs and native character interactions are unchanged.
- The pledge payment tooltip contains the cash price and the represented prominence of backing. Its body emphasises the price in bold. Purchase still changes present allegiance, not prominence or future succession promises.
- The gathering explicitly reports no changes. Changed rows use the current `THIS` character scope, following installed Spain’s list-tooltip pattern, instead of attempting to create localisation scopes during preview.
- Court roster filters use the JE country as their valid root and guard the optional character. Expired character handles cannot enter a character-typed root before eligibility checks.
- Retief’s internal watchdog scheduling is hidden. Container-dependent operations wait until the receipt exists; this is a preview guard, not a new gameplay condition. Actual dispatch and recovery times are unchanged.
- Coalition comparisons branch on an existing future pledge before comparing it with the current patron. Present and future support for the same prince still count once.
- DP approved native noble status for established dynasts and hereditary chiefly families. See the [cast assignments](../zulu_court_cast_roster_2026_10_19.md). Advisers, personal clients and procedural councillors are not automatically ennobled. Grant Peerage remains native. Fictional royal branches retain their explicit fictional provenance.

## Evidence and limits

The retained launch log contains 577 invalid-right-side comparisons and 289 missing refusal-container errors, with corresponding unset-container messages. Both failures reproduce against the pre-edit scripts in the focused preview harness and disappear with the corrected scripts. This checks script routing, not engine execution.

The latest save was dated 1 May 1838. Its annual-check marker was present and neither changed-house list was populated, supporting an explicit unchanged result. DP confirmed that the save’s several noble advisers received peerage during coalition testing; these flags do not establish an authored starting assignment.

The template, noble-status and court changes preserve existing identities, broad ideologies, allegiances and future pledges. Noble status is a game mapping, not a claim to European peerage titles or a new historical genealogy. No generated characters are assigned ancestry.

## Verification

Focused checks: **97 passed** (91 existing court checks plus six follow-up regressions). These exercise missing RHS scopes, expired roster handles, both report lists empty/populated, actual ORA-owned refusal receipts under a ZUL event root, doubled initial/renewed costs, payment invalidation and scoped noble assignments. Template flags are checked independently of player-granted flags in the save.

Complete discovery: **660 tests; 651 passed, eight historical-input skips, one pre-existing failure, no errors**. The failure is the unchanged reviewed-localisation baseline mismatch for `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`. Their localisation file is byte-identical to this turn’s pre-edit snapshot; no approval records were regenerated.

Full static validation: **14/16 gates passed, warned or skipped**. The unit and localisation gates both report the same existing prose mismatch. CMF payload verification, all five refreshed SB template pins, remaining override contracts, maps, naval connectivity, runtime script contracts and delayed-event lifecycle pass. Dependency release synchronisation was explicitly skipped; no dependency files changed.

Advisory Tiger: **0 fatal, 1,067 errors, 146 warnings, 1 untidy, 1 tip**. Compared with the previous complete run, the sole added diagnostic is the known older-schema rejection of `container_exists` for the new preview guard. Its 1.13.5 schema remains advisory for the installed 1.14.5 game. Engine execution remains pending DP.

The pre-edit source archive and log copy are under `/private/tmp/sb-court-1830-2026-10-25-before`. [Evidence hashes](evidence/zulu_court_playtest_2026_10_25_1830.json) retain the input, changed-source and validation-report fingerprints. Historical compatibility reports remain unchanged.

## DP replay

All current-source engine scenarios remain **pending**:

1. Fresh ZUL: check native noble status, +20 claimant prominence and ordinary Grant Peerage for eligible advisers.
2. Confirm a pledge and one paid incident: bold amount, compact payment tooltip, doubled initial and renewed price, insufficient-cash refusal.
3. Run an unchanged annual gathering and one with changed present/future commitments: body and tooltip report the appropriate result.
4. Open every court roster section before and after death/exile/succession, then hover repeatedly: no invalid-character errors.
5. From before Retief’s response, repeatedly hover Kill Retief: no watchdog schedule list, missing-container error or invalid RHS; selecting it still delivers the ordinary ORA response after 21 days. Existing recovery/expiry checks remain in the main matrix.

[Full runtime matrix](../zulu_court_runtime_matrix_2026_10_19.md). The same-constitution dynastic-war prototype and other previously deferred engine checks remain outside this fix.
