# Zulu court rework — implementation and verification

19 October 2026. Source implementation against Victoria 3 **1.14.5**, Steam build **25629520**, core manifest **5521822647051867164**, and CMF **1.66.0 + sb-1.14.3-r1**. No dependency or baseline change, launch, save migration or wider Bantu rollout.

## Delivered source

- Country/character registry extended with independent successor pledges and one current representative per named following. Royal birth adds eligibility, not additional votes. Court support uses Q/2 and the existing IR/effect/lifecycle rules.
- Court modal replaces the inline list. It shows the actual viewed country, incumbent/heir, candidates, named pledge holders, uncommitted backing, current/future commitments, provenance and commanders separately.
- Contextual cash-only Secure a Pledge uses native reserve capacity. Confirming a stale price refreshes the quote without charging. Target/ruler changes, death, representative replacement and insufficient cash invalidate the purchase. Vanilla social interactions remain untouched.
- Annual constitutional alignment remains; annual personal acknowledgement affects only uncommitted present representatives. Privileges and council promises are separate named bargains. Present adherents and future pledges count once each in a confrontation coalition; peaceful succession considers the separate future pledges.
- Common death/retirement reservation captures outgoing commitments before native selection, refreshes living candidates and holds one popup until answered. Mpande's retirement is dated 1 December 1856. Actual pledges are reconciled on accession, without universal loyalty or a constitutional reward. A minor uses an adult pledged regent with normal mortality.
- Targeted lesser-rival confrontation/purge stores one attempt per ruler and target before rolling. Failed coercion causes the specified popularity/supporter consequences. Existing escape uses actual exile status; relatives are not purged as a group.
- Opening Dambuza/Mawa/Nongalaza/Sotobe, Mpande-era Masiphula, earlier Maphitha/Mnyamana/Godide/Hamu windows, and explicitly fictional Uthumbu are recorded in the [cast sheet](../zulu_court_cast_roster_2026_10_19.md).
- Five reserved annual event families `.210`–`.214` replace `.200`–`.203`; their old prose is preserved in [the retirement archive](../retired/zulu_court_200_203_2026_10_19.md). New text is TO REVIEW. The firearms benefit remains once-only.

## Native claimant-war blocker and boundary

The inspected native political-movement interface supplies revolutionary eligibility, attraction/activism, IG/state weighting and callbacks. It has not established a direct script effect that creates the required royal-versus-royal revolution while both candidates retain the same laws. Japan's separate-country diplomatic-play pattern is not this mechanism. High activism alone is not proof that the engine will create the desired conflict.

The explicit test event `sb_court_succession.990` enables a custom native movement probe. Its character support follows the actual named rival's current/future adherents. Scripts then track the returned civil-war scope and exact opponent, move registered people by their commitments, allow player switching only after the real split, and resolve the actual winner. No foreign play or random/event-only war winner is substituted. A dynastic victory calls no Thirteen Chiefs reward dispatcher.

**Unverified, therefore not a completed production path:** same-constitution mobilisation, province/army assignment, faction selection and winner callbacks. Automatic contested death/retirement and major-rival coercion remain dependent on that engine proof. A deferred contest keeps its records without blocking ordinary court interactions. Mpande does not retire through a fabricated peaceful result; native ruler selection after death is not presented as a verified custom claimant settlement. DP must test before this route is enabled automatically.

## Compatibility review before repinning

Only one exact-path payload changes: `common/history/characters/zul - zulu.txt`. The pre-turn SB replacement and current installed Vanilla file were compared before repinning. SB's existing Dingane, Mpande, Uthumbu, Gqugqu, Cetshwayo, Mbuyazi, Mkabayi, Ndlela and Zulu/Komfiya entries are unchanged. Four researched adults are added with politician roles; no Vanilla history is newly deleted. The inventory's upstream hash/version are unchanged; only this mod payload hash and explanatory intent change.

All other changes are SB-owned court presentation, scripts, source tests and records. The three old/new succession axes remain separate from character law ideology. Native character interactions, legislation, decrees, institutional thresholds, broad movements and CMF contracts are unchanged. The opt-in dynastic movement is never seeded by ordinary history or annual/monthly actions.

The delayed-event inventory drops exactly four retired `.200`–`.203` dispatches, from 441 to 437. The one-day `.900` death receipt retains its coalescing flag and now reconciles the reserved succession too. The replacement ordinary episodes are immediate reserved popups, not new delayed dispatches. The new hash records that semantic change, not a blanket inventory refresh.

NGN, constitutional coups/civil wars, early/later partition, NAL/TRN interventions, NRP, permanent incorporation entitlements and annexation-movement modifier preservation retain their existing contracts. Court suspension also clears new action/episode reservations so an old choice cannot apply after institutional exit.

## Verification record

Focused source-executing court tests pass: **53 tests**; together with the existing content-smoke module, the final focused run is **63/63 passed**. They cover weighted followings and Q/2, distinct future pledges, price boundaries and stale/invalid quotations, annual acknowledgement, dated retirement and duplicate pulses, dead nominees, institutional exit, deferred-war isolation, minor/regent continuity, council fulfilment/repudiation and non-repeatable coercion. Renunciation releases successor promises and removes the native heir role. A minor's coming of age preserves the same reign's once-only privilege concession.

| Final verification | Result |
|---|---|
| Full unit discovery | **616 run: 607 passed, 8 historical skips, 1 failure.** The failure is `test_repository_manifests_are_current`, which reports the existing approved-prose drift below. The replacement-event smoke failure found during implementation was corrected in the source; its test was not weakened. |
| Full validator | **15/17 gates passed/warned/skipped; 2 failed.** Both failing gates reflect the same localisation-baseline problem: unit discovery and localisation. |
| CMF | Release pin, read-only installed-tree check and compatibility pass; dependency staging/rollback tests are included in unit discovery. No payload change. |
| Compatibility and scripts | Local inventory, Vanilla/CMF comparisons, on-action routing, stale/unused symbols, runtime script contracts, 1.14.5 release invariants and delayed-event inventory pass. |
| Maps and naval network | Both pass. |
| Tiger, advisory | **0 fatal, 1,066 errors, 146 warnings**, plus one untidy and one tip in the repository-wide run. No diagnostics identify newly added court statements. Two warnings in a touched file refer to the unchanged `GetTimedModifier` localisation accessor; Tiger does not recognise that existing getter. The aggregate is not a clean engine-validation result. |
| Existing deferred release gates | BC-20, BC-22, CP-07, QUAL-09 and SUP-05 remain warned. |
| Working-tree whitespace | `git diff --check` passes. |

The eight historical skips cover unavailable 1.14.0/1.14.2/1.14.3 manifests and historical payloads not currently installed. Current-target checks remain mandatory and pass. The final focused rerun also covers the last regency privilege-preservation adjustment. Local raw output is retained at `/tmp/sb-court-validation-final.txt`, `/tmp/sb-court-smoke-final.txt` and `/tmp/sb-court-final-tiger.txt` for this session.

No successful static test establishes runtime rendering, native mobilisation, character survival through engine annexation or event delivery.

The pre-turn working tree already contains approved-prose regression drift in `sb_klip_river_county.060`, `sb_klip_river_county.080` and `sb_natal_crisis.050`, all in `sb_natal_crisis_l_english.yml`. That file and its approval baseline are unchanged by this batch. These failures must remain visible for DP rather than be silently approved or reverted.

Every engine scenario remains pending in the [compact DP matrix](../zulu_court_runtime_matrix_2026_10_19.md).
