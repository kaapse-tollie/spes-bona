# Victoria 3 1.15.0 — fresh smoke test and Bolivia HQ warning

**Fresh-start smoke: DP observed pass.** DP completed the requested new-campaign
check after the [resumed-campaign playtest](1_15_0_playtest_1870_2026_11_07.md)
and reported nothing SB-related apart from the question about Bolivia's HQ.
The captured debug log reaches **5 May 1837**. The error log has **zero
script-system errors**, five Bolivia HQ warnings, two SB encoding warnings
corrected below, and the previously recorded replacement/unused/orphan/filewatcher
messages. This closes the fresh-start smoke request; it does not manufacture
coverage for individual stress cases not itemised in the runtime matrix.

## Bolivia's coastal access

The warning occurred at **16:52:41, 16:52:47, 16:52:50, 16:52:52 and 16:53:02**,
naming naval HQ **643**, country **203** (`BOL`) and `region_andes`.
The January autosave was written at **16:52:57**, between the last two warnings;
the February checkpoint followed at **16:53:05**.

| Checkpoint | Antofagasta (state 1075) | Naval HQ 643 |
| --- | --- | --- |
| 1 January 1837 | Owned by Bolivia; occupation record explicitly says controller 205 (`CHL`), fraction 1 | Present, Bolivia, Andes, naval |
| 1 February 1837 | Owned by Bolivia; still fully occupied by Chile | Present |
| 1 March–1 May 1837 | Owned by Chile | Absent |

In January, the state's 25 provinces, including saved port province **34061**,
are within Chile's control theatre. Bolivia is fighting Chile and Argentina in
two wars. Its coastal state is occupied; this is not a case of a confirmed
Bolivian-controlled port failing despite an otherwise intact peace-time route.

The source comparison supports **wartime loss of controlled coastal access**:

- Antofagasta's native state definition and Andes strategic region are inherited
  unchanged; neither SB nor CMF shadows those South American files.
- SB's Antofagasta state-history block matches Vanilla exactly.
- Port **`x2000F0`**, locator **362**, its paired spline anchors and an entire
  native sea route are preserved. The locator record is byte-identical.
- All **six coastal harbour nodes and their sea edges** match Vanilla after
  accounting for SB's index remapping when 15 unrelated impassable African
  harbour leaves were removed. Raw node numbers alone are not a valid comparison.
- The existing source-access validator passes Antofagasta against both native
  and effective SB naval graphs. This is a source check, not engine travel proof.

The warning's missing-connection wording does not establish a damaged SB map.
The saved occupation directly supports its earlier statement that Bolivia has
no controlled coastal destination. No map, port, spline or gameplay change is
justified for this report. The exact native lookup at each warning timestamp
was not captured, so this is a strongly supported diagnosis rather than a
reproduced Vanilla-engine defect. Reopen it if the same warning occurs while
Bolivia actually controls its coast.

## Two startup encoding corrections

The log also requests UTF-8 BOM encoding for
[`sb_law_journal_readiness_triggers.txt`](../../common/scripted_triggers/sb_law_journal_readiness_triggers.txt)
and [`sb_law_journal_events.txt`](../../events/sb_law_journal_events.txt).
Both files now have the three-byte BOM prefix; **every pre-existing byte is
unchanged**. No trigger, event, timing or law behaviour was altered. All five
existing law-journal readiness/delivery tests pass. Log confirmation that the
warnings disappear belongs to the next normal restart, not another requested
full gameplay replay.

## Evidence and verification

The [machine-readable record](evidence/1_15_0_fresh_smoke_bolivia_2026_11_07.json)
contains hashes, the five warning lines, source comparisons, exact occupation
records and verification results. Three logs and all five January–May saves
were copied unchanged and were stable during capture under
[`generated/bolivia_hq_2026_11_07/`](../../generated/bolivia_hq_2026_11_07/).
The installed CMF **1.67.2 + sb-1.15.0-r2** passes its read-only integrity check.
The agent did not launch the game, edit a save or certify native travel behaviour.

Final target-aware validation ran **1,113 tests: 1,104 passed, eight skipped and
one pre-existing localisation-review failure**. There are no new failures.
The validator reports **15/17 rows passed, warned or skipped**; its two failed
rows are the unit aggregate and the same localisation gate. Map/naval network,
override inventory/comparison, runtime contracts, delayed-event lifecycle and
dependency checks pass. Automatic CMF synchronisation was skipped; the separate
read-only installed-integrity check passes. Tiger 1.19.0 still lacks the required
1.15 schema and was not used for target validation.

The existing failure is the dangling Swazi `.098.prerogative_after_blood_river`
review-queue row and reviewed prose/size drift in `sb_klip_river_county.060`,
`sb_klip_river_county.080` and `sb_natal_crisis.050`. No localisation or approval
baseline was changed. The five separate deferred release gates remain recorded;
this smoke test does not close them. The [full log](../../generated/bolivia_hq_2026_11_07/full_validation.txt)
and its hash are retained with the evidence.
