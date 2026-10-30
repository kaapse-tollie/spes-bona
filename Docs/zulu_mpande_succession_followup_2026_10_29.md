# Mpande's consolidation and the rival sons — 29 October 2026

Implemented in the existing 0.20.2 maintenance batch; current game/CMF pins are unchanged.

- **Purge Gqugqu:** Strict/Dynamic Historical AI Mpande prioritises the existing character interaction and purge option once eligible. It waits for the normal 50-P requirement, costs and once-per-ruler limit, rather than renouncing him first. Human play, Off and the sons' protection retain their rules.
- **Preferred heir:** Mbuyazi:Cetshwayo weights are now 66:33 in all twelve recognition slots and the brothers' birthday choice. Mbuyazi is also that event's timeout default. Other recognition eligibility is unchanged.
- **Rival support:** a passed-over Cetshwayo is topped up to two eligible outside houses; Mbuyazi retains one. Frozen targets are ranked by combined house Prominence and revalidated, with no stolen pledges or double-counted junior members. Reserve those houses before the recognised heir receives ordinary royal backing. This changes future-successor pledges, not current allegiance or constitutional alignment.
- **Prose:** `.006`/`.007` use paired portraits and concrete rival-following scenes. The early variant avoids backdating the later faction names; from 1852 the Cetshwayo-opposition variant names uSuthu and iziGqoza. The historical basis and authored numerical defaults are separated in the implementation spec. New and rewritten text remains TO REVIEW.
- **Dunn:** [event and evidence record](zulu_dunn_mbuyazi_event_2026_10_29.md). A once-only November 1856 visit pledges his existing house to Mbuyazi on acknowledgement, and a valid pending visit reserves scheduled retirement. Existing losing-coalition rules remain: no historical escape exception was added.
- **Retirement:** once Mpande leaves sovereignty, remove his claim and claimant bonus without killing him. Apply this at peaceful installation and actual contested split, and prevent snapshot restoration from returning his claim.

## Validation

- 139 focused source-execution tests passed across recognition, adulthood, Dunn, coercion, retirement and claimant wars.
- Independent reviewer found no blocking defects; independently ran 24 brothers/Dunn tests successfully.
- Full discovery: **907 tests; 898 passed, 8 skipped, 1 existing failure; no errors**.
- Full validator: **15/17 gates passed/warned/skipped**. The unit-test and localisation gates report the same pre-existing review-register issue: reviewed drift in `sb_klip_river_county.060`, `.080`, and `sb_natal_crisis.050`, plus the dangling `sb_swazi_frontier.098.prerogative_after_blood_river` row. No approvals regenerated.
- CMF release/installed compatibility, override inventory, map/naval checks, runtime script contracts, unused symbols and delayed-event lifecycle passed.
- Tiger remains advisory: its 1.13.5 schema is older than installed 1.14.5. The new Dunn files' missing-BOM warning was corrected. The final recheck verified SB/CMF loading and returned WARN: 0 fatal, 1,074 errors, 149 warnings, matching the prior baseline; no diagnostics name the changed court files.
- Repository diff whitespace check passed. No game launched, save migrated, dependency patched, commit made or push performed.

Raw run output: `/private/tmp/sb-mpande-court-tests.txt`, `/private/tmp/sb-mpande-court-focused.txt`, `/private/tmp/sb-mpande-court-validation.txt`; post-BOM Tiger output: `/private/tmp/sb-mpande-court-tiger.txt`.

DP's unperformed engine checks are [runtime scenarios 138–141](zulu_court_runtime_matrix_2026_10_19.md): AI purge scheduling, both preferred-heir branches, named backing/tooltips, Dunn's dated arrival and retirement reservation, and peaceful/contested loss of Mpande's claim. Use checkpoints before each event; consumed events are not replayed.
