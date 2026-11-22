# SB 1.15.0 implementation — 5 November 2026

**7 November closure:** DP accepted the core rebase after the gameplay and fresh-start
smoke passes and approved the remaining localisation reconciliation. The full
validator now reports **15 PASS, two WARN, zero FAIL**. See the
[closure record](1_15_0_closure_2026_11_07.md) for approval, evidence and the
separate release gates and unitemised engine coverage.

**Original 5 November implementation record:** the approved port was implemented
in the working tree; DP engine checks and the pre-existing localisation review
gate were pending at that checkpoint.
No game was launched, no commit or publication was made, and SB's release version
remains **0.20.3**. Fresh campaigns with all DLC are the target; old-save migration
is excluded.

**7 November dependency update:** the active installation is now CMF **1.67.2**
plus `sb-1.15.0-r2`. See the [patch report](cmf_1_67_2_patch_2026_11_07.md) for
current hashes, the two additional corrections and fresh-start verification.
The original 5 November input identities and results below remain historical.

## Read by task

| Need | Evidence |
| --- | --- |
| Current acceptance and remaining limits | [7 November core closure](1_15_0_closure_2026_11_07.md) |
| Scope and deferred decisions | [Approved plan](1_15_0_implementation_plan.md), [design](1_15_0_rebase_design_2026_11_05.md), [open register](../audit_issues_open.md) |
| CMF installation, patch and political/territorial integration | [CMF report](1_15_0_cmf_implementation.md) |
| Raster, spline, locator, world-history and resource reconstruction | [Map report](1_15_0_map_implementation.md) |
| Journal outcomes, bars, conclusions and CMF interfaces | [JE report](1_15_0_je_implementation.md) |
| Remaining override dispositions | [Reviewed source contracts](evidence/1_15_0_implementation/override_review.json) |
| Contested-crown source dependencies and native callback limits | [Current contract review](zulu_contested_crown_1_15_0_contract_review.md) |
| Once-only event decisions | [321-event inventory](evidence/1_15_0_implementation/once_only_inventory.json), [source regression](../../tests/test_1_15_once_only.py) |
| Verification results and remaining gates | [Verification record](evidence/1_15_0_implementation/verification.json), [DP runtime matrix](1_15_0_runtime_matrix.md) |
| Launch errors and subsequent source corrections | [First launch](1_15_0_launch_debug_2026_11_05.md), [retest and impassable-coast correction](1_15_0_launch_retest_2026_11_05.md) |
| First-six-month scope errors and Riograndense HQ warning | [Correction, save evidence and replay limits](1_15_0_first_six_months_2026_11_05.md) |
| Live playtest notes through 1850 | [Preview/hover findings, Natal requests and deferred JE extensions](1_15_0_playtest_1850_2026_11_07.md) |

## Fixed inputs and preservation

The target remains Victoria 3 **1.15.0**, Steam build **26453692**, public branch,
core manifest **7727600027425614094**. The
[current-target evidence](evidence/1_15_0_implementation/current_target.json)
pins the installed manifest and 146 selected source payloads. This proves the
audited sources against that manifest, not a byte audit of every installed game
file. Historical manifest and spline checks keep their historical identities.

The original CMF input was **1.67.1**, commit `f2dea1dde7b87098b504d120b2b20e963e1d4fb6`,
with archive SHA-256
`8c7030df04c13ff47e9ade339abb3d96796c53122f73f0a0e2f3bb67e145264b`.
That installed `sb-1.15.0-r1` tree hash was
`5cd2ff82fb47384da257da22db0907ca9521245d4f8724ffbb34b222b54139b7`.
Repeated verified installation and rollback/rejection tests are recorded in the
CMF report. The original patch contained only the ideology-category and dynamic-bar
payloads; older patch directories remain historical evidence.

Before editing, all 1,092 tracked/untracked source files were copied to
`generated/rebase_1_15_0/before/`, with a hash index and the original Git binary
diff. The full previous CMF installation is retained beside it in `cmf_before/`.
All backup file hashes were [reverified](evidence/1_15_0_implementation/baseline.json).
These ignored local backups preserve unrelated edits and permit comparison with
the actual starting working tree rather than a clean-HEAD assumption. The
[implementation diff manifest](evidence/1_15_0_implementation/implementation_diff.json)
records the files changed by this task; the corresponding local binary patch is
`generated/rebase_1_15_0/implementation.patch`.

## Implemented behaviour

The map starts from native 1.15. Only 2,225 authored SB raster pixels are applied;
11,857 upstream pixel changes survive, with no overlaps. Exact old spline bytes
were recovered, six authored strip-ID collisions were remapped, and upstream
routes outside the declared delta remain intact. Terrain and locator changes
have explicit reconstruction evidence. New native states, Russian formations,
movements, treaties and untouched regional populations are restored while SB's
authored partitions and demographics remain.

Copper is native: Namaqualand **6**, Zambia **18**, Katanga **30**. Northern Cape's
eight copper-proxy lead levels are removed; Hereroland's ten and Namaqualand's
provisional two lead levels remain. Cold bounds follow matching native geography
or custom-state parents as intensities. The resource audit remains `RES115-01`.

All **27 JEs** now use **54 native outcomes**. Four obsolete bar styles use native
textures/markers while all fifteen bars retain their calculations, direction and
CMF indices. Shared settlement, existing cleanup, persistent institutions and
disabled Highveld content retain their contracts. Four general conclusion lines
are newly marked `TO REVIEW` and listed in the review queue.

Complete native conquest and annexation bodies retain the Swazi restriction and
British–Zulu handoff. Seven movement overrides retain CMF's new branches and SB's
authored exclusions. Remaining overlays restore native retirement conversion,
Russian law and Armed Forces branches, decree gates and AI incorporation routing.
Highveld temporary-immortality grants/revocations follow their native event phases.
Fodo receives the documented neutral `gene_asian_east` DNA field.

PHL retains native Adam III regnal numbering; this preserves the new native
definition rather than implementing the deferred ZUL numbering extension.
The 35 authored character-template overrides remain deliberate replacements.
Thirty omit native `home_region`, which is optional and also omitted by native
templates. Copying native parent geography onto SB's redrawn states was not
justified; regional exile/character design remains deferred. SAF names and the
disabled native buttons likewise retain their deliberate authored replacements.

## Native once-only adoption

These six country-owned occurrence records now use `fire_only_once = yes`:

- `sb_zulu_dynasty.001`
- `sb_bst_frontier.001`
- `sb_great_trek.003`
- `sb_boer_republics.130`
- `sb_delagoa.020`
- `sb_delagoa.021`

Only their redundant occurrence guards/writes were removed. Captured pre-port
body contracts verify that eligibility, resource guards, gameplay effects and
their original phases remain unchanged. No global once-only flag was introduced.
The reduction is six occurrence reads and seven writes across the six events
(Boer normalisation previously wrote the same record in either option).
Kimberley's shared pending/discovered/resource state, resettable Gaza episodes,
recurring surveys, delivery receipts and settlement recovery retain their state.

Native delivery/consumption timing is **not established by source tests**. DP must
exercise duplicate queued dispatch, held popups, normal/default answers, failed
eligibility, cancellation, save/load, a second country and relevant retag/recreation
cases. A candidate that fails equivalence must return to its previous tracking
before certification. Reduced bookkeeping is recorded without claiming a speed-up.

## Localisation boundary

The required escaping edit adds **88 `|q` substitutions on 58 lines in 14 files**.
Removing those additions reproduces each pre-edit file exactly: substantive prose,
review markers and namespace classifications are preserved. The
[syntax evidence](evidence/1_15_0_implementation/localisation_syntax_changes.json)
records the edits. Only the previously clean reviewed namespace
`sb_martinus_confederation.020` needed its syntax hash refreshed; its previous hash
is retained. Existing unrelated reviewed drift was not reapproved.

## Verification and limits

The independent pre-port unit run used the immutable source backup and recorded
**1,060 tests, 18 failures, six errors and eight skips**. Missing historical ignored
fixtures account for some errors; it was not a clean 1.14 runtime baseline. A first
validator run overlapped implementation and is explicitly excluded as a reliable
before/after baseline. The final suite ran **1,081 tests: 1,072 passed, eight
skipped, one failed, zero errors**. Its sole failure is the unchanged localisation
review gate listed below. The full validator records **12 PASS, two WARN, one
SKIP and two FAIL**; both failed gates report that same pre-existing issue.
CMF sync was explicitly skipped in the offline aggregate and passed separately
through `tools/sync_cmf.py --check`. Exact results and log hashes are recorded in
the linked verification JSON.

The integration run also caught two stale verification assumptions. The claimant
checks now use a separately reviewed 1.15 fixture, preserving the historical one.
The delayed-dispatch scanner now ignores comments: a disabled native Scramble
example had been counted as a new call. The live before/after dispatch multisets
are identical at 444; their original lifecycle manifest hash remains unchanged.

The known pre-existing localisation gate remains open for:

- the dangling Swazi `.098.prerogative_after_blood_river` queue row;
- reviewed-text/size drift in `sb_klip_river_county.060`,
  `sb_klip_river_county.080` and `sb_natal_crisis.050`.

The original backup produces exactly those same localisation diagnostics. They
are preserved unrelated failures, not an approval to change reviewed wording.

The task-specific binary patch applies cleanly to the captured starting files.
Documentation checks resolve the changed files' local link destinations. Two
unchanged Basotho follow-up anchors in the open register were already stale in
the backup and are recorded separately. Diff whitespace checks report 14 native
state-history indentation lines and 38 unchanged upstream CMF GUI lines; all are
preserved source formatting, not newly authored whitespace.

The repaired naval checker passes 31 of 33 SB coastal-access cases and 29 of 31
unmodified native controls. The remaining Benin and Bas Congo cases are unchanged
native river ports and are explicit runtime warnings. Missing, invalid,
out-of-state and disconnected port fixtures fail. Coastal graph reachability does
not prove building-port or river access in the engine.

Installed **Tiger 1.19.0** lacks the new JE outcome and native once-only fields;
its source schema hashes are recorded in the
[coverage evidence](evidence/1_15_0_implementation/tiger_schema.json).
The validator reports it as unsupported rather than interpreting its diagnostics
as target errors or a pass. No replacement schema was silently assumed.

Every engine row in the [runtime matrix](1_15_0_runtime_matrix.md) remains pending,
including rendering, localisation, portraits, political movement lifecycle,
territorial callbacks, succession/recruitment, Basotho relief and land/naval
movement. The existing performance and spline release gates remain open. The
glossary, JE extensions, character work and release artwork/music retain their
agreed follow-up destinations in the open register.

The [7 November playtest corrections](1_15_0_playtest_1850_fixes_2026_11_07.md)
implement Cape/Caledon previews, context-safe Prerogative naming, Natal objective
timers and the Natalia/SWZ joining restriction. See that report for the task diff,
updated validation and post-restart engine gates.
