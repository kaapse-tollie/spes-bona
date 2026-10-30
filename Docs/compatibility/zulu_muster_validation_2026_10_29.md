# Zulu civil-war muster: validation record

29 October 2026. Checkpoint: **`1a3d7c3`**, `Checkpoint SB 0.20.2 before civil-war muster rework`. Implementation follows that checkpoint and remains uncommitted. No push or game launch was performed.

## Provisioning follow-up

DP selected temporary wartime provisioning after the Klip River famine replay. The follow-up passes **87 focused tests**, including the newly pinned Food Security modifier, native relief precedent, buy packages and price range; both recipients and winners; abandoned-war cleanup; and exclusion of native one-state splits and foreign roots. Runtime-script, stale-symbol and unused-symbol checks pass. Localisation validation retains the same unrelated review drift and obsolete queue row detailed below; the new Wartime Provisions key is covered. Diff whitespace checks pass. The full unit discovery below predates this small follow-up and was not rerun.

The new modifier is +1.5 Food Security until the scripted muster is cleared. [Investigation, native calculation and limitations](zulu_muster_famine_2026_10_29.md). Existing wars are not migrated. Engine replay remains pending.

Fresh advisory Tiger output is unchanged: 0 fatal, 1,074 errors, 149 warnings, one untidy and one tip, with no diagnostic referencing the provisioning/muster scripts or modifier file. The tool's 1.13.5 schema limitation still applies; this is not a clean Tiger pass. Follow-up logs: `/private/tmp/sb-muster-provisions-focused.txt` and `/private/tmp/sb-muster-provisions-tiger.txt`.

## Source validation

| Check | Result |
|---|---|
| Pre-change claimant suite | 73 passed |
| Final claimant and muster suites | **85 passed** |
| Complete unit discovery | 893 run; **one failure, eight skips** |
| Full validator | **15/17** passed, warned or skipped; two gates report the same localisation review issue |
| Final installed-contract check | Passed, including current land-unit manpower definitions |
| Compatibility, override inventory, maps and naval connectivity | Passed |
| Diff whitespace check | Passed |

The full suite preceded the final internal donor-refill correction and its additional regression. The final 85 focused checks include that correction: a multi-state donor must retain its required civilian reserve in the recruitment state after exporting surplus. No claim of a subsequent complete-suite run is made.

The existing localisation review failure concerns reviewed text/size drift in `sb_klip_river_county.060`, `sb_klip_river_county.080` and `sb_natal_crisis.050`, plus the dangling review-queue key `sb_swazi_frontier.098.prerogative_after_blood_river`. Those event texts and approvals were not altered by this implementation. The validator reports this once through unit discovery and once through its localisation gate. The two new muster labels have their own review-queue entries.

The full suite reports eight skips. Historical-input checks retain their conditional skip policy; current-target compatibility checks passed. CMF release network synchronisation was explicitly skipped with `--skip-cmf-sync`; the pinned release and installed compatibility checks passed. Existing deferred gates remain BC-20, BC-22, CP-07, QUAL-09 and SUP-05.

## Advisory Tiger check

Final standalone result: **0 fatal, 1,074 errors, 149 warnings, one untidy and one tip**. The installed Tiger targets 1.13.5 while the game is 1.14.5, and reports unsupported current interfaces throughout the repository. No final diagnostic references the new muster files or the changed force-split/dynastic script paths. This is an advisory result, not a clean Tiger pass or proof of engine behaviour.

An initial missing-BOM warning on the new common files was corrected before the final check. The remaining repository-wide findings were not expanded into unrelated fixes.

## Reproduction and evidence

From the repository root, using the configured Python runtime:

```sh
python -m unittest tests.test_zulu_contested_crown tests.test_zulu_court_muster
python -m unittest discover -s tests
python tools/validate.py --skip-cmf-sync --tiger --game-root "$SB_GAME_ROOT"
```

`SB_GAME_ROOT` is the installed Victoria 3 `game` directory. Original run logs are in `/private/tmp/sb-muster-focused.txt`, `/private/tmp/sb-muster-full-unit.txt`, `/private/tmp/sb-muster-validator.txt` and `/private/tmp/sb-muster-tiger-final.txt`; these temporary logs are not durable project evidence. The [native contract](zulu_muster_native_contract_2026_10_29.md), pinned source hashes and saved disassembly excerpt preserve the relevant inspection evidence in the repository.

All engine scenarios in the [numbered DP matrix](../zulu_civil_war_muster_runtime_matrix_2026_10_29.md) remain **pending**. Start before answering the claimant challenge, with one-state and multi-state Zulu checkpoints. In particular, verify native recruitment, officer hiring, AI mobilisation, suppression of duplicate conscription and both winners' cleanup. Source tests do not establish these outcomes.
