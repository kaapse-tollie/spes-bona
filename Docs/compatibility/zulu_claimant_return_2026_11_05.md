# Claimant return, 5 November 2026

The five retained autosaves, 1 May–1 September 1881, record the return button
as completed. ZUL (16777921) identifies **Msushwana Mpungose (67111028)** as
its restoration claimant. He is alive in ZUL with the agitator role, but belongs
to the **Pro-Slavery Movement (16777410)**. The uSuthu movement (50333013)
has no attached character. These are post-partition saves: they do not establish
when Cetshwayo disappeared or which royal held the crown immediately before
annexation. [Extracted save observations](evidence/zulu_claimant_return_2026_11_05.json).

## Corrections

- The exact British–Zulu annexation goal already shelters the Mandlakazi chief.
  It now also captures the **current** ruler and heir at enforcement and moves
  those living identities into British custody before native country removal.
  The heir moves first to avoid succession changing the second accessor. A
  receipt prevents repeated enforcement from archiving a generated replacement.
- The existing GBR-to-NAL archive transfer now reads its captured British
  country, rather than the event root (which can be a diplomatic play).
  Recreated ZUL restores the captured identities before the government choice;
  partition still sends the royals to CAP. A reversed enforcement restores only
  the pair actually sheltered, including when NAL has not yet been created.
  A genuinely dead character is never recreated.
- The designated restoration claimant gets uSuthu character-support weight
  100,000 during this contest, rather than the ordinary 200. Other characters
  retain 200 and their existing ideologies. The special weight is disabled
  during a reserved dynastic crisis so its dedicated movement retains priority.
  The return helper establishes royal alignment before transfer.

The movement interface defines `character_support_weight` as the agitator's
choice between eligible movements. The retained [1.14.5 claimant-war investigation](zulu_contested_crown_2026_10_27.md)
records native `FindBestMovementForAgitator` selecting the greatest valid weight.
The installation inspected on 5 November additionally shows
`MOVEMENT_AGITATOR_STICKYNESS = 2.0`, favouring the current movement. That fresh
inspection belongs to **1.13.11**, including the reviewer’s `CheckCanExile`
inspection; it is not additional 1.14.5 evidence. A 200/200 tie cannot guarantee
the intended cause. Game attachment after the correction still requires replay.
The change does not create another movement or renew enthusiasm.

## Verification and handoff

The focused suite passes **80 tests**, including eight new tests. Source-executed
fixtures delete all characters still hosted by the annexed country, then check
restoration, partition, CAP exile and the once-only return of the original
claimant as an agitator without coronation. Other cases cover a foreign event
root, NAL's later creation, wartime succession, repeated enforcement, reversal,
natural death and movement-priority boundaries. The fixtures do not emulate
native succession callbacks or agitator recruitment timing.

Full validation on 5 November reports **13/17 gates passed, warned or skipped**.
The installed game now reports **1.13.11 (Matcha)** in
`launcher/launcher-settings.json`, Steam build **24799966**, branch **public**;
SB's compatibility target remains **1.14.5 / 25629520**. Current-target checks
remain mandatory and have not been repinned to this installation. The failing
gates are unit discovery, reviewed localisation, naval connectivity (the pinned
naval-network file is absent) and upstream override comparison. The latter two
are installation incompatibilities; the localisation findings predate this fix.
CMF verification, local override inventory, map data, runtime script contracts,
delayed-event lifecycle and on-action routing pass. Tiger remains advisory:
**0 fatal, 1,919 errors, 153 warnings, 1 untidy, 1 tip**, using its 1.13.5 schema
against this mismatched installation. No clean 1.14.5 integration result is claimed.

Final unit discovery runs **1,060 tests: 19 failures, five errors and eight
historical skips**. The 22 compatibility findings concern the installed payload,
upstream parity, missing beta assets or the spline input hash. The two existing
bookkeeping failures are the stale 123/124 override-count assertion and reviewed
localisation drift. One overly broad movement assertion was updated to permit
the designated agitator preference while continuing to forbid contest-based
suppression elsewhere; that case and the eight new claimant tests also passed
independent review. Logs: `/private/tmp/sb-claimant-return-20261105-validation.txt`
and `/private/tmp/sb-claimant-return-20261105-unit-final.txt`.

DP replay is **pending** from a checkpoint before Britain's annexation is
enforced: record ruler/heir IDs, choose Thirteen Chiefdoms, permit return and
inspect the same claimant under uSuthu. Also test early Klip partition, reversal,
a deceased claimant and both sides of a later constitutional war. Existing saves
whose historical people were deleted are not reconstructed or migrated.
