# Zulu harvest and war-outcome follow-up — 27 October 2026

## Findings and source changes

The retained autosaves span **1 November 1841 to 4 March 1842**. They contain annual patron snapshots, including Dingane 0.05, Mpande 0.50 and Gqugqu 0.55 attraction. They cannot reconstruct every year across DP's earlier starts. Original saves were read only; [hashes and extracted court state](evidence/zulu_harvest_war_2026_10_27.json) preserve the evidence.

Two execution faults explain why an apparently active annual system could remain silent:

1. The native random-list evaluator converts fixed-point factors to integer weights. All three patron weights above became zero. The sub-1% withdrawal branches also became zero. [The installed ARM64 evaluator](evidence/zulu_random_list_weight_1_14_5_arm64.txt) calls `GetRawFactor`, then divides its fixed-point result by 100,000 before returning an integer. Its optional min/max bounds default to −1 (unbounded), so scaling does not hit an implicit 100-point ceiling. Every competing court weight is now multiplied by 100,000 before this conversion. The probability model is unchanged.
2. Uncommitted people have no old patron. Optional equality did not protect a missing right-hand variable, producing the logged line-127 error. Patron selection, old/new change detection and council-promise release now test existence before comparing. The regression interpreter rejects absent right-hand links and reproduces native integer truncation.

Reports still appear only when current allegiance or future succession changes. The independent incident deck is unchanged.

## Current probabilities — no balance change

Let `a = clamp((Popularity + 100)/200, 0, 1)`.

- Uncommitted: join chance is `20 × best available a` percent annually. Conditional patron choice is proportional to each patron's `a`.
- Committed: withdrawal is `1 − 0.5a` percent; switching is `1 + 3 × max(best alternative a − current a, 0)` percent when a positive-attraction alternative exists. Otherwise switching is zero. The remainder stays committed.
- Current allegiance and future-succession records are separate; existing minor-pledge and conflict reservations remain.

For the saved attraction values:

| Record | Join / withdraw | Switch | Stay |
|---|---:|---:|---:|
| Uncommitted current allegiance | 11% join | N/A | 89% |
| Dingane supporter | 0.975% withdraw | 2.5% | 96.525% |
| Mpande supporter | 0.75% withdraw | 1.15% | 98.10% |
| Gqugqu supporter | 0.725% withdraw | 1% | 98.275% |

An uncommitted house's unconditional annual chances are 0.5% Dingane, 5% Mpande and 5.5% Gqugqu. These are the intended probabilities now represented by non-zero native weights, not newly raised coefficients.

## War outcomes

- Generic defeat recruits up to **two** eligible uncommitted houses into opposition; generic victory still recruits one.
- Blood River and Swazi defeat recruit up to **three** each. Campaign victory still recruits two. An exhausted neutral pool does not manufacture houses or convert existing supporters.
- Both permanent campaign defeat modifiers now give **−25 Popularity**. The otherwise unchanged opening Dingane package starts at −50, so the two defeats reach −100. Other traits/events can still affect the total.
- Swazi terminal handlers reserve `.097` for victory or new `.098` for defeat. The Zulu event applies the political result on opening, once; repeated callbacks and acknowledgement cannot repeat it. The responsible ruler is captured before delivery and a surviving current ruler supplies the portrait if needed.
- Existing Swazi victory claims/AI follow-up remain, now applied by the victory event. Its +40 Popularity, the defeat's −10 Prerogative shock, and the separate existing stalemate treatment are unchanged. Blood River's −25 Prerogative shock is unchanged.

The new defeat event follows the one-character DLC presentation used by `regency.2`/`.3`: a concrete public outcome followed by its personal/political consequences. The responsible sovereign is the visual focus; the verified native portrait window/icon is retained. `.098` is **TO REVIEW**. Reviewed prose is untouched; the shared −25 tooltip remains in the general localisation queue. Portrait rendering and prose wrapping await DP.

## Other reported diagnostics

- Concession duration: a bare variable was passed where `add_modifier.days` expects a number or named value. A named formula now reads the same remaining-days variable, preserving the original expiry after movement recreation.
- `sb_court_pledged_share_var` and `sb_court_annual_weight_var` are read by the court/harvest localisation. The engine explicitly excludes such reads from its unused warning; both are retained. The genuinely unread `sb_court_rival_share_var` calculation was removed.
- `enforced_by_timer`: installed 1.14.5 documents separate final and timer callbacks. Added a dedicated timer adapter, supplying a temporary marker only to the existing exact-play Klip/Bechuanaland trackers. It does not call accepted-demand bookkeeping. This corrects older documentation treating the marker as engine-provided. Current dependency payload and upstream pins are unchanged.
- The base Legitimacy/script-value errors occurred at 01:23:09–01:23:13 while the previous edit batch was in progress. Current definitions exist, and the March autosave contains `sb_prerogative_base_legitimacy`. This is consistent with incomplete hot-reload state; it is not evidence that the current source lacks the modifier. No speculative replacement was added.

## Popularity-weighting proposal only

No change was made to Q/2 or the 75%/25% target formula. To strengthen Popularity without reducing Prominence's coefficient, a possible later revision is `T = clamp(0.75H + 0.25M + 0.5Q, −100, 100)`. Away from clamps, Q currently contributes 0.375Q; this proposal makes a +20 Popularity improvement worth +10 target instead of +7.5. Keeping the existing H and M coefficients avoids trading away coalition influence; the final bound still limits gains near ±100. This also removes the earlier intermediate clamp, so it is a proposal for DP, not a silent tuning change.

## Validation and handoff

**122 focused checks pass.** Full discovery: **746 tests, 737 passed, eight historical skips, one existing failure**. The failure is the reviewed-localisation baseline in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`; those namespaces and their approvals were not changed. Full validation is **14/16 gates passed, warned or skipped**: unit/localisation gates both report that same existing drift. Current Vanilla/CMF compatibility, installed dependency checks, override inventory, maps, naval connectivity, on-action routing and the refreshed delayed-event inventory pass. Remote CMF release sync was deliberately skipped; the five existing deferred gates remain (BC-20, BC-22, CP-07, QUAL-09, SUP-05).

Advisory Tiger: **0 fatal, 1,073 errors, 149 warnings, one untidy and one tip**, identical diagnostic/category/path counts to the prior run against its older schema. No new diagnostic was introduced. The unrelated existing EOF whitespace finding in `events/sb_zulu_court_events.txt` is untouched.

Reports: `/private/tmp/sb-27oct-harvest-focused.txt`, `/private/tmp/sb-27oct-harvest-full-final.txt`, `/private/tmp/sb-27oct-harvest-tiger-final.txt`. Engine checks are **pending DP**, scenarios **88–92** in the [runtime matrix](../zulu_court_runtime_matrix_2026_10_19.md). No game launch, save edit/migration, dependency patch, or wider country rollout.
