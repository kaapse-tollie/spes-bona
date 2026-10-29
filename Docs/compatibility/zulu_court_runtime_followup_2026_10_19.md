# Zulu court runtime follow-up — 19 October 2026

Source corrections complete; corrected engine behaviour remains pending DP. Game/dependency baseline remains Victoria 3 1.14.5 and CMF 1.66.0 + `sb-1.14.3-r1`. No dependency changes, game launch, save migration, commit or push.

## Findings and corrections

| Report | Evidence and correction |
|---|---|
| Recognise a Successor spams errors | The retained error log contains 397 missing `sb_court_candidate_index_var` fetches, 397 unset-scope errors and 398 invalid comparisons. Tooltip previews do not execute the initialisation inside `hidden_effect`. Both the increment and its dependent comparisons now sit behind a separate existence-guarded branch. The regression simulates preview traversal without mutations; ordinary candidate-selection coverage remains intact. |
| Court looks like a heading, then breaks the JE | The unstyled button opened a 780-pixel window inside the 504-pixel vertical flow. A popup layer did not remove its layout footprint; the raw scrollarea also lacked scrollbars. Replaced with Japan's native expand/collapse header and a bounded 504 × 560 scrollbox. Long text resizes vertically within 464 pixels; character names are proper buttons. The viewed JournalEntry country remains the context. |
| Orphan `.990` warning | This is the deliberately manual claimant-war probe. Declared `orphan = yes`, following Vanilla debug events; no production caller was added. The war path remains test-only. |
| Generated replacement heir | None of the three retained autosaves contains a current native heir, so the reported transient appearance cannot be established from those saves. The court now uses CMF's existing `no_heirs` facility while living authored dynasts remain, including children and exiles. Authored heir and regency appointments release the court-owned flag briefly; exit/exhaustion releases it normally. Another route's independently owned block is preserved. |
| Apparently consequence-free killings | The saved princes are alive: Mpande is in exile by February, Gqugqu is abroad as an agitator by March. Both confrontations took the failed-coercion/flight route. Neither prince has a represented following or pledged coalition in these saves. Added brief, named notifications for submission, capture, escape and resistance. Chances, followings and Prerogative balance are unchanged. |

The inline display is an explicit limitation against the original detached-modal design. No verified way of transporting an arbitrary viewed JournalEntry's context to a detached root popup was established; the native Japan JE pattern provides the scoped, usable alternative. Actual rendering still needs DP's check.

The log also contains six `interest_group_top`/`FindChild` animation errors without a court script location. These were not attributed to or altered by this patch.

## Saved political state

Manager-bounded records identify ZUL as country **481**, Dingane as **4477**, Mpande as **4478** and Gqugqu as **4480**. Native heir `4294967295` means unset in all three saves.

| Checkpoint | Prerogative | Cooperation | Target |
|---|---:|---:|---:|
| 1 February 1836 | 1.22314 | 10.87243 | 8.15432 |
| 1 March 1836 | 2.26281 | 10.87243 | 8.15432 |
| 1 April 1836 | 3.14653 | 10.87243 | 8.15432 |

Represented weight stays 341, incumbent weight 182 and weighted endorsement 18,200. The second exposure refreshes the same five-year −10 Popularity modifier rather than stacking another penalty. This explains the unchanged target and gradual Prerogative movement. It does not establish how another checkpoint's stronger coalitions would behave.

Raw inputs are retained in `/tmp/sb-court-runtime-2026-10-19/`; [checked-in evidence](evidence/zulu_court_runtime_followup_2026_10_19.json) records hashes and relevant observations without shipping saves.

## Verification

- **115/115 focused tests pass**, including court, institutions, frontier and content-smoke checks. The independent reviewer separately ran both court suites (**58/58**) and the institutional core (**19/19**).
- Full discovery: **621 tests; 612 passed, 8 historical skips, 1 existing failure**, no errors. The failure remains reviewed-localisation baseline drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`. Their prose and approvals were not altered.
- Full validator: **14/16 gates passed, warned or skipped**; the unit gate and localisation gate report that same existing drift. CMF read-only verification, override inventory, map/naval connectivity, runtime contracts, delayed-event lifecycle and Vanilla/CMF comparisons pass.
- Advisory Tiger: **0 fatal, 1,066 errors, 146 warnings**, unchanged totals from the preceding implementation; no diagnostics identify the changed court statements. Tiger targets 1.13.5 and reports known 1.14/CMF schema limitations. This is not an engine certification.
- The five existing deferred release gates remain BC-20, BC-22, CP-07, QUAL-09 and SUP-05.
- Validation logs: `/tmp/sb-court-runtime-focused.txt`, `/tmp/sb-court-runtime-validation-final.txt`; Tiger output is in `/tmp/sb-court-runtime-validation.txt` (its first unit run also records the now-corrected test-double adapter failure).

## DP replay and review rule

Use a fresh launch/campaign for the corrected setup. Hover Recognise repeatedly, open/close the court, scroll all rows and inspect another country's JE. Remove the current heir, then recognise an authored successor; also check minority regency and institutional exit. Verify the correct named notification after a confrontation and no repeat attempt against the same rival in one reign. All these corrected-source engine checks remain **pending** in the [runtime matrix](../zulu_court_runtime_matrix_2026_10_19.md).

`AGENTS.md` now requires the lead agent to run an independent **GPT-6.1 Sol, max reasoning** reviewer in parallel for every substantive repository task, obtain its final review and address or report material findings. Reviewer agents do not recursively spawn reviewers. This batch used that reviewer; counter-increment coverage, regency protection, wrapped content, notification wording and documentation precision were checked and corrected. No material source findings remain.
