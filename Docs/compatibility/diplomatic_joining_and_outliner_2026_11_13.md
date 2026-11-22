# Diplomatic participation and international-situation bar overlap

13 November 2026. Victoria 3 1.15.1 / CMF 1.67.3 + sb-1.15.1-r1.
DP reported both issues from a fresh campaign. No game launch, save migration,
dependency modification or reviewed-prose change was performed.

## Global diplomatic veto

The Chiefdoms joining predicate used a flat `NOT` around several conditions,
including `NOT = { sb_chiefs_contest_country = yes }`. Every foreign joining
country therefore supplied a true child. Native `CNotTrigger::EvaluateDerived`
rejects a block on its first true child: it is negated OR, not negated AND.
The old bounded test evaluator used `not all`, which concealed this defect.
The Swazi joining predicate had the same flat-negation mistake.

The corrected Chiefdoms rule requires an active test-mode contest, both stored
factions and the recorded war. Both proposed sides must match that pair, in
either order, before foreign participation is vetoed. Missing, inactive,
event-mode or unrelated state passes through to Vanilla's existing eligibility.
Swazi's veto now explicitly groups all of its existing conditions, retaining
the restriction on NAL joining the defending SWZ side of the exact authored
ZUL conquest play. Native strategic-interest, treaty and power-bloc rules are
unchanged.

The test-only status of native Chiefdoms wars remains unchanged. This correction
does not establish that automatic overlord participation is excluded in-engine.

## Confederation bars

DP clarified the problem as clipped/overlapping bars, not missing labels.
The 1 December 1856 autosave matches the screenshot: 2/5 subjects controlled
(40%) and 0/60 sea-access months. The progress values are correct.

CMF's international-situation row inherits Vanilla's `journal_entry`, whose
`journal_entry_scripted_progress_bars` child paints each bar at 70% of its
12-point row height. The frame adds three points on either side: about 14.4
points of painted height. CMF's empty `progressbars_spacing` override removed
Vanilla's four-point gap, allowing adjacent frames to overlap.

SB now overrides only `com_outliner_international_situation_entry`, preserving
CMF's complete definition except `progressbars_spacing = 4` in the existing
block override. No global bar type, dimensions, colours, labels, progress or
dependency files change. A parity test compares the copied type against the
installed CMF source and pins the native spacing. The 12 November note's
reference to the standalone CMF mini-bar helper did not establish the actual
consumer; this investigation traces the inherited native type instead.

## Attached log

The inspected log contains no `sb_` path or identifier. Its 54 amendment-owner
scope errors point to Vanilla's `00_ip4_victoria_scripted_triggers.txt:736–744`
and Iberian negotiation callers; those files are not overridden by SB or the
installed CMF tree. Six invalid `home_country` references point to Vanilla's
`revolution_events_01.txt:1387`. Other entries concern filewatcher directories,
the `interest_group_top` GUI animation, invalid unnamed country scopes and
unidentified saved key references. The latter cannot be attributed from this
log alone. No unrelated hotfixes were added.

## Verification and DP handoff

Before correction, the joining-rule regression reproduced 23 failing cases
across seven tests, including fresh Ottoman–Montenegrin previews. After correction,
35 focused checks pass: the joining truth table, fresh/unrelated plays, both
faction orders, missing state, Swazi controls, shared Chiefdoms behaviour and
GUI/native source parity. Independent Sol 6.1 Max review found no further
actionable issue in the changes.

Full validator: **15 PASS, 2 WARN, zero failures**, including complete unit
discovery, installed CMF integrity, override comparison, localisation and map
checks. Warnings remain the five deferred release gates and Tiger 1.19.0's
pre-1.15 schema; it was not run as a target validator.

- [Validation output](evidence/diplomatic_joining_and_outliner_2026_11_13/static_validation.txt)
- [Failing pre-fix reproduction](evidence/diplomatic_joining_and_outliner_2026_11_13/joining_before_fix.txt)
- [Native NOT evaluation](evidence/diplomatic_joining_and_outliner_2026_11_13/native_not_trigger_arm64.txt)

Pending DP:

1. Restart and preview Ottomans versus Montenegro. Third parties should again
   be governed by ordinary Vanilla rules, without a Zululand exclusion reason.
2. Check the authored ZUL–SWZ play: NAL cannot join the defending Swazi side;
   other countries/sides retain ordinary eligibility.
3. Compare the two Confederation bars in the sidebar at the reported UI scale.
   Their frames should be separated; values remain 40% and zero in the inspected
   checkpoint. Check the Chiefdoms sidebar too, which uses the same row type.
4. In an explicit native-Chiefdoms test only, check third-party and automatic
   overlord participation against both sides. This remains a release gate for
   that experimental route.
