# Zulu court presentation, supply and save findings — 28 October 2026

## Changes

- **Courtly Politics**, **Co-operation with the Settlement** and **Co-operation of the Amabutho** now have existing Vanilla flag/rifle modifier icons. Their effects are unchanged.
- The live claimant movement is named **Dynastic Rivalry**. Its internal identifier remains `movement_sb_dynastic_test`.
- **Civil War Provisioning** gives AI participants in the tracked SB dynastic conflict **−50% Supply Consumption**, matching Vanilla's `barracks_boost_paraguay_quantity_modifier` magnitude. It starts at the actual territorial split, not when an organising movement is created. Both factions receive it in an AI-only conflict; neither prince is privileged by identity or by being the original country.
- War-end callbacks remove the assistance from both sides before the winner's notification. Cancellation and missing-war recovery also remove it. The existing monthly reconciliation updates eligibility after a change of player control. No new daily scan, military-strength bonus, organisation override or dependency change was added.

The −50% value is an initial tuning choice. Source tests establish modifier delivery and cleanup, not that the native AI will attack or that supply alone caused the reported behaviour.

## Save investigation

Read-only copies cover **1 September 1851 through 1 January 1852**. [Input hashes and extracted records](compatibility/evidence/zulu_court_save_followup_2026_10_28.json) preserve the evidence without committing whole saves. The inspected country records contain no active dynastic war, so these checkpoints cannot measure the new supply assistance.

### Cetshwayo

Cetshwayo is **alive and adult**, character **4480**, born **27 April 1826**, with the original `ZUL_cetshwayo_heir` template and historical flag. He belongs to the surviving ZUL country **33554570**, ruled by Mpande. This is not a missing or recreated character.

All five saves contain `sb_court_claim_renounced_var` on him. They also contain the timed `sb_court_renunciation_cooldown_var`, with 2,941 ticks remaining in September and 2,819 in January. Mbuyazi, character **4481**, has neither marker.

The court's candidate trigger deliberately excludes renounced claims. The successful renunciation action sets that flag and releases current/future backing. The cooldown belongs to an attempted renunciation, supporting that explanation rather than a rendering fault. An accepted claimant accommodation can also set the renounced flag, so the final records alone do not reconstruct every earlier choice. The character interaction is AI-enabled; the snapshots do not identify who issued the command. The ten-year cooldown governs another attempt, not automatic restoration of a successfully renounced claim.

No claim or saved character was reset. Restoring Cetshwayo's candidacy despite his renunciation would change the political outcome, rather than fix the list.

### Klip River

In all five saves, NAL **33554916** has:

- `sb_natalia_british_colony_resolved_var`;
- `sb_klip_river_county_resolved_var`;
- `sb_klip_river_boer_flight_started_var`.

There is no pending commission or punitive-play marker. ZUL still owns states **779** (`STATE_ZULULAND`) and **780** (its `STATE_NATAL` portion); NAL owns its separate Natal state **16777726**. The Klip chain has taken a terminal departure route; it is not waiting for its first event to become eligible.

There are multiple ways to reach those same final flags:

1. Natal's `.010.b`, **Ratify the present boundary**, schedules `.070` and does not send ZUL the `.020` demand. Ordinary AI can select it; the strict historical all-AI rule suppresses it.
2. Invalid initial or delayed setup schedules the standard departure `.075`. Setup checks include actual province ownership and ZUL's independence. A temporary territorial split could fail them, but these saves do **not** establish that this happened.
3. Other completed county/punitive outcomes also use the shared departure helper.

The shared helper clears the intermediate routing markers. No retained `.010`, `.070` or `.075` event reference distinguishes those paths here. Therefore the evidence establishes **resolved, not stuck**, but does not prove whether Natal chose to ratify or a fallback ran. A checkpoint from before the departure/colony settlement would be needed to determine that. No speculative routing change was made.

## Verification and handoff

- **90 focused tests pass**, including actual script execution for AI/player factions, both side selections, repeated reconciliation, unrelated callbacks, cancellation, both winners and missing-war recovery. Icons resolve to installed Vanilla assets; the existing institutional arithmetic test now ignores icon metadata.
- **Full discovery: 859 tests, 850 passes, eight historical skips, one pre-existing failure, no errors.** The remaining failure is reviewed-localisation drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`; neither their text nor the approval baseline was changed. The separate localisation gate reports that same drift.
- **Full validator: 15/17 gates pass, warn or skip.** Current CMF installation, override compatibility, map/naval checks and runtime script contracts pass. Five existing deferred release gates remain recorded; remote release sync was deliberately skipped. Advisory Tiger retains its previous **1,074 errors and 149 warnings** under its older 1.13.5 schema, with no diagnostics in this update's changed scripts. Full output is retained at `/private/tmp/sb-zulu-playtest-2026-10-28-evening/validation.txt`.
- DP scenarios **126–128** cover presentation, AI supply/organisation and the two save investigations. No game was launched and no save was edited.
