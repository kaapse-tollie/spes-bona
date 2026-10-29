# Zulu result buttons, harvest rendering and missing claimant — 27 October 2026

## Applied changes

- Blood River `.080`/`.082` and Swazi `.097`/`.098` reserve their responsible ruler and named houses on opening. Their valid option applies Popularity, allegiance and Prerogative changes once. Firearms remain on Blood River's options, including neutral `.081`. Waiting over an open popup no longer grants political rewards early.
- Revalidate the frozen house selection at execution. Dead or newly committed houses are skipped, with no replacement drawn behind the displayed tooltip. A deceased patron's coalition is not redirected to a replacement. Existing receipts and result guards prevent repeat rewards; a Swazi opening receipt prevents a duplicate popup before acknowledgement.
- Blood River, Swazi and generic defeats now impose **−25 P**, subject to the existing −100 floor. Generic wars retain their terminal callback because no generic-result popup exists. No new event was introduced. Campaign Popularity remains permanently **−25** on defeat and **+40** on victory.
- Harvest `.200` selects its description through native `first_valid`. Each join, withdrawal and switch has a direct outer tooltip, with character names read there rather than inside nested custom localisation. Royal/chiefly title and flavour selectors still select literal prose. No annual probabilities or reporting cadence changed.
- Mpande and Gqugqu receive 100-year politician careers on creation, matching the existing protection for Cetshwayo and Mbuyazi. Mpande's role assignment now precedes the career extension in one template callback. Native mortality, disease and authored removal remain possible. Old saves are not rewritten or deleted characters recreated.

## Save and log evidence

[Bounded evidence](evidence/zulu_outcome_options_harvest_2026_10_27.json) records checkpoint hashes, dates, P and character careers. The complete local extraction is `/private/tmp/sb-27oct-harvest-options/`; saves were read only.

Mpande (ID 4478) is present on **1 October 1842**, aged 45, with syphilis and a politician career expiring **4 October 1842**. He is absent from **1 November**. This closely fits career expiry; these monthly snapshots do not prove that illness caused—or did not cause—the disappearance. Gqugqu's saved role expires in September 1848, so his authored claim needed the same protection.

P was already −59.30 in July and −62.51 in October, with an October target of −67.63. No coup/claimant-conflict reservation appears in these country records. After Mpande disappears, November's target rises to −10.31; losing his coalition from the active backing calculation materially changes P's direction.

The captured log repeatedly fails on nested `THIS.GetCharacter...` in `sb_court_report_*_named`. The screenshot's house names render in the outer rows while old/new patron names do not. Its royal description similarly loses a character reference inside a custom-localisation-selected string. Direct outer references remove these particular context handoffs; visual correctness still requires DP's replay.

## Civil-war limitation and Popularity

**−50 P is not currently a production claimant-war trigger.** It checks the legacy coup path at the monthly pulse. That path separately requires an eligible present opponent, strength at least 90% of native coup resistance, and no conflicting attempt/war/succession reservation. The same-constitution native war remains confined to explicit prototype events, as previously agreed. This change does not invent a foreign war, force a historical sequence or enable that unverified route.

The available snapshots do not explain conclusively why the legacy coup also left no attempt record. Mpande is present, opposes Dingane and belongs to Landowners with 78.378% clout in October. Those facts make “zero Popularity means no coup strength” an inadequate explanation: the formula also counts IG clout. Capture the actual live strength/resistance and exclusions at a monthly pulse before changing that gate. Runtime scenario 98 retains this investigation.

The locked opening packages give Mpande `tactful` + `basic_political_operator`, and Gqugqu `basic_political_operator`. Neither package grants Popularity; **0 is expected**, not a missing value. Native `tactful` gives command/diplomatic/IG effects; `basic_political_operator` gives Prominence, with its coup multiplier in the command block. No starting-trait or Popularity rebalance was made.

At Popularity 0, annual attractiveness is `(0 + 100) / 200 = 0.5`. If the best eligible patron is also at 0, an uncommitted record has a 10% annual chance to join; equal-popularity competing patrons give a committed record 0.75% withdrawal, 1% switching and 98.25% persistence. Destination choice still depends on the eligible candidates. The incumbent alone contributes Q/2 directly to the Prerogative target. Popularity zero is neither zero attractiveness nor a guarantee of no allegiance changes.

## Compatibility and validation

Only the local ZUL character-history hash and keyed Mpande template hash were refreshed after inspecting their role/career delta. Installed game 1.14.5 and CMF 1.66.0 + `sb-1.14.3-r1`, upstream hashes, maps and all other override pins are unchanged. Reviewed localisation approvals are untouched. Obsolete harvest helper keys and their queue entries were removed; replacement general text remains TO REVIEW.

**Final results:** 80 focused tests pass. Complete discovery: **761 tests — 752 pass, eight historical skips, one existing reviewed-localisation failure, no errors**. Full validator: **14/16 gates pass, warn or skip**. Its unit/localisation failures both trace to the unchanged reviewed-text mismatches in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`; no approvals were regenerated. Current-build, installed CMF, override, map/naval and delayed-event checks pass. Remote CMF release sync was skipped. The existing deferred gates remain BC-20, BC-22, CP-07, QUAL-09 and SUP-05.

Tiger is advisory against its older 1.13.5 schema: **0 fatal, 1,073 errors, 148 warnings, one untidy and one tip**. Comparing diagnostic/file pairs with the previous run yields no new diagnostics and one removed warning. This is not an engine pass. No game launch, save migration, dependency change, commit or push was performed.

DP scenarios 95–98 cover option timing, direct harvest names, claimant careers and the unresolved low-P path. All new engine scenarios remain pending.


Local verification artefacts:

- `/private/tmp/sb-27oct-harvest-options/focused-final.txt` — SHA-256 `1e234fbe6e594dbb9608904fbe6e6545013d387feb64abba0a1eab8e0a6c38b3`.
- `/private/tmp/sb-27oct-harvest-options/static-accepted.txt` — SHA-256 `b827bda6a1bd4de16a9f2f197771a7defba008b4be1873626c0d6e6b6bc94f85`.
- `/private/tmp/sb-27oct-harvest-options/tiger.txt` — SHA-256 `8777b8f6ab7f437176c22aaadd687e0e5ce3037a9e09439bd89cc5122c2bcc55`.
- `/private/tmp/sb-27oct-harvest-options/tiger-delta.json` — SHA-256 `051cbde1d9c18285a8f68e9dcf0fe07bb6e0185342b6dc53d273dff79ff4df70`.
