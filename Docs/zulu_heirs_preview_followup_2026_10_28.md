# Mpande's sons and the successor preview — 28 October 2026

## New replay evidence

The latest copied saves cover **1 September 1848 to 1 January 1849**, following DP's reload after the first civil war. They are a different replay from the previous September 1851–January 1852 investigation.

**Mbuyazi**, historical character **4481**, is alive, adult and still uses `ZUL_mbuyazi_heir`. He has `sb_court_claim_renounced_var` in every retained checkpoint. His ten-year renunciation cooldown falls from **3,236** to **3,114** ticks. Cetshwayo and Gqugqu have no renunciation marker in these saves. Mpande is the ruler; the selected rule is **Dynamic Historical**.

The missing candidacy therefore follows a surrendered claim, as Cetshwayo's did in the previous run. The cooldown establishes a renunciation attempt; the retained saves do not identify who initiated it or preserve the complete sequence of choices. No identity reconstruction or saved-flag reset was performed. [Hashes and extracted evidence](compatibility/evidence/zulu_heirs_preview_followup_2026_10_28.json).

DP reports that **Klip River fired after reloading the post-war checkpoint**. This confirms delivery in that replay; it does not recover which branch produced the previous run's shared terminal flags. No further Klip routing change was needed.

## AI target restriction

Under **Strict Historical** or **Dynamic Historical**, an **AI-controlled Mpande** may no longer target **Cetshwayo or Mbuyazi** with either renunciation or purge. Gqugqu remains eligible under the existing costs, odds and attempt limits. The change preserves the sons' later succession contest without forcing Gqugqu's defeat.

The shared target trigger is checked when offering the interaction and again when resolving the choice. An old quote cannot charge Prerogative/Authority or coerce a protected son after the country changes to AI control. Human decisions, the **Off** rule, other rulers, and actual civil-war outcomes are unchanged.

This is prospective behaviour. Retest from before the unwanted renunciation; the already-surrendered claim in the January 1849 save remains surrendered.

## JE scope error

The captured error log contains **864** copies of the collision at `sb_court_buttons.txt:9`, with no other SB-bearing diagnostic. The successor button's `possible` block attempted to save a temporary `sb_court_country` while the JE already held a permanent target with that name.

The preview now compares each candidate's home country with the list iterator's previous scope—the country displaying the JE. It preserves the same living-dynast, non-ruler and home-country requirements, including recognition of a child. It neither shadows nor changes the existing permanent target. Actual successor selection retains its established effect/event scopes.

## Verification

- **133 focused source tests pass.** Both historical rules protect both sons against both coercion choices; Gqugqu remains actionable. Player control, Off and another ruler remain valid negative controls. A stale quote after AI takeover incurs no cost. The button accepts an eligible adult or child, rejects an absent/renounced candidate, and leaves a deliberately foreign permanent target untouched.
- **Full discovery: 862 tests, 853 passes, eight historical skips, one pre-existing failure and no errors.** The failure remains reviewed-localisation drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`; the separate localisation gate reports the same drift. No approval baseline or reviewed text was changed.
- **Full validator: 15/17 gates pass, warn or skip.** Current CMF payload, compatibility, map/naval and script-contract checks pass. Five existing deferred gates remain; remote release sync was skipped. Advisory Tiger reports **1,074 errors and 148 warnings** under its older 1.13.5 schema, with no diagnostics in the changed button or trigger files. Output: `/private/tmp/sb-zulu-heirs-court-2026-10-28/validation.txt`.
- DP replay remains pending for the AI target menu/behaviour and repeated opening/hovering of the successor JE with a clean log. No game was launched or save edited.

## Parallel CAP review

DP separately requested a review of Cape's starting political and electoral setup. The [review brief](cape_starting_politics_review_2026_10_28.md) recommends retaining the unelected opening, fixing the Liberal Movement's Subjecthood creation mismatch, and testing a modest attraction modifier before changing character roles or adding an electoral amendment. No CAP gameplay changes are included in this fix.
