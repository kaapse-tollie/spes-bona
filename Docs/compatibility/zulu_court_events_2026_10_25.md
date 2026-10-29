# Zulu court: annual allegiances, incidents and campaign reputation

25 October 2026. **Implemented in source; engine verification pending DP.** Authorised by DP’s final “code it up and I’ll test”. Baseline remains SB 0.20.2, Victoria 3 1.14.5 build 25629520, and CMF 1.66.0 + `sb-1.14.3-r1`. No launch, save migration, dependency patch or wider country rollout.

## Implemented behaviour

The thirteen opening character packages now follow the [locked trait baseline](../zulu_character_package_proposal_2026_10_25.md). Per-template initial generation retains experience and native Child bookkeeping without extra random opening traits. Later native ageing and earned traits remain intact. Mkabayi, Ndlela and Komfiya require three additional keyed template contracts; their installed Vanilla sources are pinned. The inventory therefore contains 121 keyed overrides, previously 118.

January, first in 1837, runs the selected annual [model B](../zulu_court_transitions_and_event_deck_2026_10_25.md). Current allegiance and future succession pledge are distinct snapshots and rolls. A house counts once through its representative; prominence changes the consequence, not the probability. The incumbent retains self-support, princes retain their own succession claims, and existing minor pledges remain under the regency controller. Reserved accession/civil-war/coup commitments do not reroll. Constitutional movement alignment remains separate. Umkhosi reports actual current/future changes and named house prominence; it adds no incident or extra recruitment roll.

The six ordinary portrait scenes are .210 succession undertaking, .211 service and reputation, .212 chiefly bargain, .213 change of patron, .214 disputed award and .215 firearms contacts. Eligible unused cards are drawn uniformly, with one saved integer delay of 6–24 months. Participants are selected at delivery. An invalid reserved scene can be replaced at the same due time. A shown card is consumed; completion/default/cancellation schedules the next draw once. A three-month event window has a four-month recovery lease. Institutional suspension preserves pending cards/due dates; no unrelated-war restriction is introduced.

Paid choices revalidate the named participants and current reserve-capacity quote. Changed quotes require a fresh confirmation of the same scene; review itself costs nothing. The character pledge price is now 20/31.25/50/65/80% of maximum reserves at prominence 10/25/50/75/100. Payment guarantees current co-operation immediately; ordinary annual persistence applies afterwards. Native character interactions remain separate.

Bargains bind the specific current or future commitment. Voluntary departure ends only the matching unfulfilled promise. A granted Council or recruitment concession is not reversed as a refund. Council repudiation releases still-bound supporters and produces one ruler reaction, regardless of the number of affected houses. Chiefly movement concessions retain their original expiry if the movement disappears and returns naturally; they do not recreate it or refresh initial enthusiasm.

Blood River and Swazi victory each grant the actual result sovereign permanent +40 Popularity, remove Usurper if present, and recruit up to two neutral houses. Each outright defeat grants permanent −20 Popularity, a −10 P shock, and up to two neutral houses to the strongest eligible rival. Rewards are applied by terminal result handling before acknowledgement popups. White peace/stalemate, incomplete demands and generic-war exclusions retain their distinct existing routing. The generic coordinator changes its political reward to one neutral house; it still tracks one ordinary play at a time and does not claim new coverage of every concurrent or auxiliary war.

Retief and Klip River political choices now use the agreed personality, named-house, succession-pledge and chiefly-concession effects. Obsolete direct P rewards and temporary victory reputation are removed. Existing military, territory, firearms and settlement mechanics remain. New opposition ranks the eligible rivals by current backing, excluding future-only promises; ties use a stable authored candidate order, without creating an extra following.

## Boundaries and prose

The automatic historical defeat-sequence crisis remains deferred. The existing same-constitution claimant-war prototype remains test-only; this work does not claim to solve native revolutionary delivery. Q/2, λ = 0.25, Institutional Reach, incorporation entitlements, NRP and the annexation-movement preservation work are retained.

New court prose is TO REVIEW, with general keys in the review queue. No reviewed event/JE text or approval snapshot was regenerated. Three pre-existing reviewed-localisation regressions remain in `sb_natal_crisis_l_english.yml`: `sb_klip_river_county.060`, `.080`, and `sb_natal_crisis.050`. That entire localisation file is byte-identical to the pre-edit snapshot for this revision.

Reviewed narration in `sb_natal_crisis.080` and the existing Swazi victory narration `.097` names Dingane, whereas the revised mechanics correctly credit whoever actually ruled at the result. This wording is retained for DP review if an alternative ruler reaches those outcomes. Obsolete unused general Klip dynasty tooltips remain historical prose; the active choices use new, queued tooltips.

## Verification

- New source-executed package checks: **19 passed**. These cover probability bounds, annual snapshots, separate commitments, zero-attraction fields, minors/dead candidates, reserved conflicts, deck cycling/delays/re-entry, invalidated scenes, revised quotes, timed concessions, breach handling and actual credited sovereigns. New opposition selection explicitly distinguishes present backing from future promises.
- Complete discovery: **654 tests; 645 passed, 8 historical-input skips, 1 pre-existing failure, no errors**. Dependency installation/rollback and existing institution/settlement checks are included. The sole failing test aggregates the same three reviewed-localisation regressions noted above; no approval was regenerated to clear it.
- Full validator: **15/17 gates passed, warned or skipped**. The unit and localisation gates both report that existing prose mismatch. Installed CMF verification, source contracts, override parity, maps, naval connectivity and delayed-event checks pass. Live CMF release sync was explicitly skipped in the final run; an earlier run verified the same installed payload without changing the dependency.
- Advisory Tiger: **0 fatal, 1,066 errors, 146 warnings, 1 untidy, 1 tip**, matching the prior baseline. Its 1.13.5 schema remains advisory for installed 1.14.5. No new court diagnostic remains.
- The eight skips concern unavailable historical manifests or non-installed historical 1.14.0/1.14.2/1.14.3/OB1 payloads. Current-target checks remain mandatory. The five existing deferred gates remain BC-20, BC-22, CP-07, QUAL-09 and SUP-05.

Static source execution checks probabilities, state changes and scope routing; it does not prove in-engine portraits, timer expiry, event defaults or annual report localisation. No reviewer agent was spawned: the repository’s mandatory-review policy remains explicitly suspended by DP.

The pre-edit snapshot is `/private/tmp/sb-court-2026-10-25-before/sources.zip`, with its file hash manifest alongside it. Source/validation hashes are retained in [the evidence record](evidence/zulu_court_events_2026_10_25.json). Earlier reports remain unchanged.

[DP runtime matrix](../zulu_court_runtime_matrix_2026_10_19.md): all current-source engine scenarios remain **pending**. Start a fresh ZUL campaign for the controlled opening traits, annual gathering, incident cadence and prices. Use checkpoints before the respective campaign/partition for results. Do not infer a successful claimant war from the court display or high activism alone.
