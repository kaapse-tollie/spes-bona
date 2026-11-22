# Chiefdoms review date and compact bars

12 November 2026. Target: Victoria 3 1.15.1 / CMF 1.67.3 + sb-1.15.1-r1.
Scope: presentation correction; no dependency payload, contest, timer or save
migration changes. The input campaign began on 1.15.0 / CMF 1.67.2 and was loaded
during the Anglo-Zulu war.

## Evidence

The inspected `autosave.v3` is dated 1 May 1880 (written 12 November at 13:51).
Journal 83 is the Chiefdoms situation, added on 22 April 1880. Its saved bar
values are 2 Activism and 0 Boer Commitment. Global `sb_chiefs_state_scope`
references container 67108864, whose name is `sb_zululand_chiefdoms_state` and
which holds the clock-started receipt and review timer. The timer is present;
the failure is not evidence of a lost alias or absent setup in this checkpoint.

The current `error.log` consists of repeated failed date-expression evaluation
and `sb_chiefs_status_review` localisation errors. The original expression
passes a global container reference into `GetVarTimeRemaining`.

The replacement reads `.VarRemaining('sb_chiefs_review_wait_var')` directly on
that scope and passes the resulting integer to the same date formatter. The
1.15.0 scripting digest declares `Scope.VarRemaining` as `int32`; installed
Morgenröte uses this accessor/formatter pairing in
`localization/english/curtiss/curtiss_schneider_trophy_l_english.yml:4`.
This avoids the failing nested helper call without duplicating a timer.
The precise engine evaluation failure and successful rendering of this
container-based expression remain **pending DP replay**; the global helper is
not established to be removed or restricted to countries.

The compact renderer uses the native bar's style, while SB's expanded journal
uses its own widget. The native Chiefdoms definition still had the former
red/green balance textures and moving marker. It now uses `default_bad`, with
the full widget selecting `IsDefaultBad`. Both consume the same unchanged
0–100 Activism projection. The green Commitment bar is unchanged; an empty
bar matches the saved zero. CMF's compact renderer intentionally omits text.

## Separate timer risk — not resolved by this presentation change

The save still records `tick=3650` on the review wait and `tick=6` on the weekly
receipt, despite nine calendar days since the JE opened. Independent inspection
of the installed executable found a decrementing saved-variable counter but no
script-container traversal in its principal saved-variable update task. Another
update path has not been excluded. Together these are evidence of a possible
frozen container timer, not proof that changing the date accessor repairs it.

Retain saves at least a week apart: compare the same container's two counters,
the displayed review date and weekly contest evaluation. A date that moves
forward with the calendar, or a permanently present six-day receipt, requires a
timer-lifecycle fix. Do not certify the ten-year review from the successful
rendering check alone. This pass does not reset or migrate that state.

## Verification

Source comparison checks the installed CMF compact `IsDefaultBad` branch and
the expanded SB widget. No game launch was performed. See scenario 2 in the
[runtime matrix](../zulu_thirteen_chiefs_runtime_matrix_2026_11_10.md) for the
date, advancing-time, compact/full-bar and clean-log retest.

- 51 focused Chiefdoms, settlement, house and journal-migration checks pass.
- The migration regression accepts only this bar's authorised style change;
  its historical arithmetic hash remains unchanged.
- Full validator: **15 PASS, 2 WARN, zero failures**, including complete unit
  discovery, installed CMF integrity, override comparison, localisation and map
  checks. [Output](evidence/chiefdoms_presentation_2026_11_12/static_validation.txt)
- The warnings are the five existing deferred release gates and Tiger 1.19.0's
  incompatible pre-1.15 schema; Tiger was not run as a current-target validator.
- Independent Sol 6.1 Max review found no further actionable issue in these
  edits and flagged the separate timer risk above. Rendering is still pending.
