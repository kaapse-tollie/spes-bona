# Zulu playtest follow-up — 30 October 2026

Targeted source changes; current game/CMF baseline retained. No game launch, save migration, dependency change or wider country rollout. Existing unrelated working-tree changes and reviewed prose are preserved.

## 1. Dunn acceptance crash and guns presentation

The latest crash directory, `victoria3_01260930_173447`, ends with `Could not find widget 'event_window_1char' in file 'gui/eventwindow.gui'`. Its exception stack runs through GUI data-context setup and `CEventWindow::Setup`. Accepting `.001.a` immediately opens Dunn's delivery event `.002`, which named that absent window. It now uses the installed `event_window_1char_tabloid` with the existing saved Dunn portrait. The same absent window was also used by three Hamu offer/funding events from the preceding batch; those now use the supported single-character window too. A regression resolves every visible Dunn/Hamu window against installed Vanilla and checks the delivery portrait scope.

The arrival description and delivery description/tooltips now highlight Small Arms and the existing two-week reward. Event mechanics, prices and annual cadence are unchanged. Reopening `.001` and accepting `.a` from a checkpoint is **pending DP**; static checks cannot certify native GUI rendering.

## 2. Two-state barracks restoration

The original cleanup removed the temporary Wartime Muster but retained regular barracks at the wartime location. Preparation could itself move one regular level to Natal before the revolution formed.

The multi-state path now opens a relocation receipt before preparation and measures the net change in Natal regular levels around each actual scripted operation. Construction or demolition during the waiting period is not counted as scripted movement. Both real participants carry the receipt. Either winner reverses that relocation after actual reunion, through the existing bounded population-return receipt. Cancellation before the split reverses preparation without moving people.

Surviving total capacity is preserved: if the original layout is 4 mainland / 0 Natal, the war makes it 3 / 1, and another level is built in Natal, cleanup produces 4 / 1. Demolished capacity is not recreated; restoration is capped at surviving donor levels. Ordinary barracks merge all levels, so a level demolished and later replaced at the donor has no separate provenance and can still be relocated. A missing receipt is not guessed; older saves already past preparation require an earlier checkpoint to test restoration. One-state origins and foreign-owned portions are excluded. Repeated callbacks consume no second restoration.

Native downsizing still requires removal/recreation of the affected donor building, so its surviving units can lose manpower, experience and composition. Destination expansion retains its existing production methods. Building-level conservation is not military equivalence. DP must inspect actual post-war units and employment as well as counts.

## 3. Mbuyazi and confrontation eligibility

Answering either Two Brothers choice or The Other Brother grants Mbuyazi **Innovative**, if absent. The trait is previewed on the choice and is not granted on opening. Its native character modifier is empty: it adds no Popularity or Prominence. As ruler, it gives +10% technology spread; its other native role effects remain native. No authored Expert Political Operator package was found on Mbuyazi, so generated skill traits were left alone.

A claimant who currently supports the ruler cannot be confronted or purged. The shared requirement is checked when opening the action and again when answering, so a change of allegiance while the popup is open cannot consume Prerogative, Authority or an attempt. Future-successor pledges remain distinct: supporting a different future heir does not make a present loyalist a purge target.

## 4. Journal presentation

Institutional Reach retains its existing 0–50 calculation. Its tooltip now names the active laws that change the score, shows Local Police as +5, groups unchanged laws into the base 50, states the Social Mobility restriction, and displays actual live court modifiers. New research penalties have **not** been applied.

The Firearms JE adds a visible current-effects panel using the active Iron Age Weapons timed modifier's native description. It does not duplicate the staged penalty numbers or change progress. All existing stages share the displayed name used to select the modifier. Layout, actual translated names and zero/completed states remain DP rendering checks.

## 5. Expected ordinary court-event interval

The six-card deck draws a uniform integer delay from **6 through 24 months** after the previous choice closes. Therefore:

- Mean delay: **15 months**; median: 15; standard deviation: about 5.48.
- Probability of a delay of 12 months or less: **7/19 = 36.84%**.
- Six eligible cards, without suspension: **90 months (7.5 years)** between complete deck cycles, plus popup time.
- Monthly delivery, institutional inactivity, war/confrontation reservations and other open court episodes can delay delivery further.

The annual First Fruits report and dated story events are outside that deck. Their combined popup frequency is therefore higher. No cadence was changed in this pass. A modest alternative for review is **12–30 months** (mean 21, about 29% fewer ordinary episodes per year); **18–30** gives mean 24, about 38% fewer.

## 6. Lesotho famine: evidence and limits

The retained autosaves cover **1 December 1854–1 April 1855**, after BST's annexation. In the latest, Drakensberg is ORA-owned, with its last ownership change dated **29 September 1854**. There is no living BST to inspect and no active famine entry for that state.

Latest Drakensberg has **38,354 people**, including **8,972 workers**. There are **787 military workers (8.77%)**, 4,917 peasants, one regular barracks, one livestock ranch, two maize farms, one logging camp and five subsistence levels across eight arable slots. This is a post-annexation snapshot, not proof about BST's earlier retreat or wartime staffing.

The retreat option in `sb_bst_frontier.020` moves **5,000 people including dependants**, not 5,000 workers. It selects one Sotho Pop in Boer-owned Vrystaat with at least 5,000 people; fragmentation into smaller eligible Pops means no transfer. It does not require that selected Pop to be peasants. The outcome flag is recorded when the popup opens, while the move occurs on the option.

Conditional AI frontier assistance can restore **14 conscription levels** for BST (against six in its initial Drakensberg setup). Capacity is not actual mobilisation, but full staffing at the normal 1,000 jobs per level would compete heavily with the remaining civilian labour pool. The present save cannot establish whether that helper ran, whether the transfer completed, or the famine's immediate cause. These are investigation leads, not a confirmed diagnosis.

The existing 1836 audit finds 26,514 authored Sotho size plus 1,521 San in Drakensberg, and 10,030 Sotho in Vrystaat; these source values alone do not establish the post-retreat workforce or a historically correct total. The new [regional research brief](institutional_reach_regional_reform_research_2026_10_30.md) finds historical land loss and food vulnerability alongside later Basotho grain exports. No unsupported population or arable-land increase is applied.

**Needed checkpoint:** before the mountain retreat, after answering it, and during the famine. Compare population/profession/qualification, actual mobilisation, subsistence vacancies, Food Security, grain supply, prices and market access. If military employment is the cause, a population-sensitive assistance cap or demobilisation/provisioning is a more direct candidate than adding arbitrary population.

## 7. Institutional reform proposal

See the [research and arithmetic brief](institutional_reach_regional_reform_research_2026_10_30.md). SWZ and GZA fit a reusable reform layer with country-specific objectives; BST requires its own agrarian/mission/land context. Existing helpers directly invoke Zulu court content and must not simply be enabled for those tags.

The proposed research-only ceiling would be `−25% × IR / maximum IR`. At the current maximum 50, IR 50/25/0 gives −25%/−12.5%/0. At 75% of an otherwise unchanged research rate, research takes one third longer. Industry Banned already contributes −25% Production research and spread; stacking must be considered separately.

For `clamp(100 − law deductions − 5 × Society technologies, 0, 100)`, twenty counted technologies eliminate IR with no law reform. Native Society counts are 18/15/13/10/8 by era. ZUL explicitly starts with two Society grants (ancestor granting still needs verification), so at least those credits must be defined before selecting the scale. Counting every technology both rewards cheap unrelated discoveries and overlaps law unlocks. Recommendation for further design: keep Zulu politics separate and choose a few practical education/administration objectives for the reusable layer. No new numeric model is authorised or implemented here.

## 8. Verification and DP checks

Focused source execution covers both victors and side choices, delayed reunion, cancellation, construction after split, reverse relocation, demolished capacity, missing receipts, loyal claimant protection, held-popup invalidation, Mbuyazi option timing and installed Dunn windows. Final focused run: **143 passed**. Complete validator discovery: **981 tests, 972 passed, one pre-existing failure, eight historical-input skips**. The failure is the existing localisation baseline/queue issue: dangling `sb_swazi_frontier.098.prerogative_after_blood_river` and reviewed-text drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`. No unrelated approval was regenerated.

The validator reports **15/17 gates passed or warned**, with unit discovery and localisation both reporting that same existing issue. CMF installation/pin/compatibility, override inventory/comparison, map/naval checks, on-action routing, unused/stale symbols, runtime contracts and delayed-event lifecycle pass. Tiger remains advisory: its supported 1.13.5 target is older than installed 1.14.5; the report has zero fatal diagnostics and existing unsupported-engine diagnostics. No new barracks helper or Firearms widget diagnostic remains. Five deferred release gates remain open.

An independent Sol 6.1 Max reviewer found and reproduced two intervening-construction/demolition cases, which were fixed. Its recheck passed 69 focused tests plus a replay with replaced state objects, different destination training and a foreign root. No blocking source finding remains. `git diff --check` passes. Full output is retained at `/private/tmp/sb-playtest-validation-final-20261030.txt`; final focused output is `/private/tmp/sb-playtest-focused-final-20261030.txt`.

All new engine scenarios are **pending DP**:

1. Accept Dunn's arrival and gun delivery; inspect highlighted guns and reward.
2. End a two-state war as either side, including delayed reunion and extra regular construction; inspect barracks, manpower, training and returned population.
3. Cancel a claimant crisis before the split; verify original regular geography and unchanged people.
4. Inspect IR and Firearms live-effect panels at several levels and after institutional/Firearms completion.
5. Open confrontation against an opponent, make him loyal before answering, and confirm no cost or roll; present loyalists must not be selectable.
6. Answer `.006` in either direction and `.007`; verify Mbuyazi receives Innovative once, with no new Popularity/Prominence.
7. Retain a pre-annexation BST retreat/famine checkpoint for the separate diagnosis.
