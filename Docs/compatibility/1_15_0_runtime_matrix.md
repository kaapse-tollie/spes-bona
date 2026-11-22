# Victoria 3 1.15.0 — DP runtime matrix

**Core rebase closed by DP, 7 November 2026.** The
[closure record](1_15_0_closure_2026_11_07.md) accepts the reported gameplay and
fresh-start smoke results and records the now-passing localisation gate.
Acceptance does not turn unrun scenarios into passes. The table retains exact
coverage limits; outstanding targeted checks and unattributed diagnostics remain
separate release-verification or diagnostic follow-ups.

Use a fresh campaign, all DLC, exact game build 26453692/core manifest
7727600027425614094, CMF 1.67.2 + sb-1.15.0-r2, and this SB working tree.
DP launches the game. Old 1.14 saves/logs do not certify this port. Keep checkpoints
before each affected transition. Record branch, country, date, observations and
relevant log excerpts; a clean launch does not close later gameplay rows.

## Evidence chronology

The following reports retain the observations and pending checks at each
checkpoint; the table below records their latest individual status.

The [CMF 1.67.2 update](cmf_1_67_2_patch_2026_11_07.md) retains the existing
ideology and dynamic-bar payloads and adds two narrow upstream corrections.
RT15-18 requires a fresh campaign on this dependency; the earlier observations
below remain evidence for the builds on which they were recorded.

DP's 5 November [22:33 launch confirmation](1_15_0_launch_retest_2026_11_05.md#launch-confirmation)
clears the 15 undocked-harbour and 15 coastal-graphics messages. Earlier JE schema,
survey parsing, encoding and rejected-anchor errors remain absent. The remaining
24 lines match the previously classified warnings. World review, journal
presentation, movement and survey delivery remain unverified. Other rows remain
unrun unless separately evidenced.

The [first-six-month report](1_15_0_first_six_months_2026_11_05.md) records a native
state-event AI scope correction awaiting replay and a Riograndense HQ warning
around country elimination. These are tracked separately in RT15-16/17; they do
not reopen the cleared launch diagnostics or certify later movement.

DP's [live notes through 1850, received 7 November](1_15_0_playtest_1850_2026_11_07.md)
report that the campaign otherwise seems fine, with Cape/Caledon preview issues,
a Prerogative hover error and requested Natal timer/intervention changes. This
is provisional feedback; individual unexercised rows remain open. That intake
changed documentation only; the captured autosave had advanced to 1851.2.1.
The [subsequent corrections](1_15_0_playtest_1850_fixes_2026_11_07.md) implement
the five fixes; their new engine scenarios remain pending after restart.

The [7 November crash investigation](1_15_0_crash_2026_11_07.md) identifies
premature JE activation during rebel law inheritance. CRASH115-01 guards the
shared institutional helper against the direct-law route missed by the earlier
on-action guard. Replay the preserved 1 November 1856 save through the actual
Zulu split; source tests alone do not close RT15-13.

The [wider law-callback audit](law_callback_readiness_2026_11_07.md) adds
CRASH115-02: native and SB JE creation is deferred only for unfinished countries,
with delivery-time eligibility and duplicate checks. Ready-country law changes,
new-country delivery and save/load remain engine checks under RT15-13/14.

The later [observer-transition crash](1_15_0_observer_crash_2026_11_07.md)
is CRASH115-03: construction/investment-pool tooltip rendering, with no law or
JE activation frame. Its existing-save replay is diagnostic and does not certify
fresh-start compatibility. No source correction is established; RT15-19 remains
open independently of the inherited-law checks.

DP's [run through 1870 and follow-up](1_15_0_playtest_1870_2026_11_07.md) confirms
a resumed campaign and reports chat checklist items 3–6 as fine: crash
regressions, journal/war behaviour, once-only events and map/resources. DP saw
no SB-related log errors. Intake captured a later 1 January 1875 checkpoint;
its other diagnostics remain unattributed under PLAY115-07, not established
SB regressions. DP subsequently completed the fresh-start smoke test below.

The [fresh smoke test and Bolivia investigation](1_15_0_fresh_smoke_bolivia_2026_11_07.md)
record DP's fresh-campaign pass through May 1837, with no script-system errors.
Bolivia's warning is strongly explained by complete Chilean occupation of its
coast in the January/February saves; local native port routes are preserved.
Two SB file-encoding warnings received BOM-only corrections. That checkpoint's
pre-existing localisation-review failure was subsequently resolved by DP's
approval and the [closure validation](1_15_0_closure_2026_11_07.md).
The encoding warnings await confirmation at the next normal
restart, without requesting a repeat of the gameplay checklist.

## Recorded coverage

**DP observed pass (resumed)** below records that playtest result. It does not
claim individually demonstrated coverage of every alternate outcome, deliberate
stress case or exact historical crash reproduction. The acceptance column
retains those verification limits; this status is distinct from an unrun check.

| ID | Scenario | Acceptance | Status |
| --- | --- | --- | --- |
| RT15-01 | Fresh 1836 startup | World/new native states and SB ownership, population, buildings and political starts load; no new related errors | DP observed fresh-start smoke pass through May 1837; two BOM-only warning corrections applied afterwards |
| RT15-02 | Active and concluded journal panels | Headers, artwork, long text, four translated bars, tooltips and CMF dynamic widgets render; hidden groups remain appropriate | PLAY115-03/04 implemented; DP observed pass (resumed) |
| RT15-03 | Completing, invalidating and timing-out JEs | Correct terminal effects, conclusion and cleanup; persistent institutions stay active; Highveld remains disabled | DP observed pass (resumed) |
| RT15-04 | Bechuanaland shared JE, both outcomes and participant perspectives | Shared settlement once, correct winner, late replies handled and container cleanup preserved | DP observed pass (resumed) |
| RT15-05 | Zulu, Basotho and Trek introductions | Each valid country receives its introduction and original option effect once, including default answer | DP observed pass (resumed) |
| RT15-06 | Boer constitutional choice for two qualifying countries | Each country may receive its own event once; both alternatives preserve effects; no world-wide lock | DP observed pass (resumed) |
| RT15-07 | Delagoa notifications | Actor and gateway receive their separate country-local notices; original completion/relations/bonuses remain at answer | DP observed pass (resumed) |
| RT15-08 | Once-only queue and recovery | Repeated dispatch before delivery, held popup, failed trigger, cancellation and save/load do not duplicate or lose required effects; exercise changed owner/retag where applicable | DP observed pass (resumed); individual queue/retag stress cases not itemised |
| RT15-09 | Repeatable and shared negative controls | Gaza can progress in a later valid episode, diamond surveys recur, Kimberley settles across opener routes once, and settlement retries remain available | DP observed pass (resumed) |
| RT15-10 | Map movement | Map/splines load; land and sea deployment through Cape, Natal and Lourenço Marques works, including split ownership and market/trade access | Earlier map launch fixes retained; DP observed pass (resumed) |
| RT15-11 | Copper/lead and discoveries | Native copper capacities and provincial shares appear; Northern Cape proxy lead is absent; genuine lead, diamond discovery and production methods remain correct | Survey parser fixes retained; DP observed pass (resumed) |
| RT15-12 | Territorial wars | Swazi restriction, British–Zulu pre-annex character handoff, enforcement, reversal and peace receipts preserve their contracts | PLAY115-05/06 implemented; DP observed pass (resumed) |
| RT15-13 | Succession, recruitment and relief | Zulu actors/promises and both conflict outcomes work under Monarchy and Social Monarchy; verify restoration and native callback side effects (`anti_monarchist_revolution`, `ai_gendarme_revolutionary_regime_var`, unintended abolition JE) using the [claimant contract limits](zulu_contested_crown_1_15_0_contract_review.md#verification-limits). Basotho's previously accepted relief/cohort behaviour survives | CRASH115-01 correction applied; DP observed pass (resumed); exact historical split replay not itemised |
| RT15-14 | Non-SB politics/character control | Russian branches, movement eligibility, socialist character classification, retirement locks/conversion and native decree behaviour survive; law-triggered JEs activate once after country creation and retain normal reform/restoration behaviour | Law/JE behaviour: DP observed pass (resumed); other native controls not individually reported |
| RT15-15 | Text and portrait | Quoted concept/function text renders without format errors; Fodo loads with intended appearance; four new conclusion lines receive DP review | Engine pending |
| RT15-16 | Paralegal-discrimination state-event choices | AI options evaluate country-only radical preferences on the state owner; ordinary and French-path cases retain native weights and state effects without scope errors | Two-call source correction and regression pass; restart and replay pending DP |
| RT15-17 | Riograndense wartime port access and HQ retirement | Observe port control around country elimination; distinguish loss of a valid destination from a missing map connection, using an immediate save and native control if it recurs | Warning observed; source parity and May/June saves recorded; cause/replay open |
| RT15-18 | CMF 1.67.2 + r2 fresh campaign and journal/outliner rendering | No new related parser or scope errors; ordinary and dynamic bars, Bechuanaland and Imperial Confederation widgets, and the Zulu Prerogative marker render correctly when active | DP observed journal-rendering pass (resumed) and subsequent fresh-start smoke pass; no new script-system errors in the captured smoke log |
| RT15-19 | Construction tooltips and observer transitions | Compare ordinary construction hover, both observer-toggle directions, and closed/open tooltip conditions in the preserved August 1855 checkpoint; distinguish persisted state with fresh SB/CMF and separate Vanilla controls if reproducible | DP observed pass (resumed), no new issue reported; CRASH115-03 cause remains unresolved |

Source tests do not model an assumed native once-only consumption point. If a
migrated candidate fails the lifecycle-equivalence check, retain its previous
occurrence bookkeeping and record the failed scenario before certification.
Performance is a separate measurement under PERF-20261028-01; fewer variables
alone are not a measured speed-up. Existing SUP-05 spline release verification
and other unrelated deferred gates remain open.

[Implementation report](1_15_0_implementation.md) · [Approved plan](1_15_0_implementation_plan.md)
