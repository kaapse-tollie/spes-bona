# 1.14.5 rebase verification — 16 October 2026

SB 0.20.2; game 1.14.5/build 25629520/core manifest 5521822647051867164;
CMF 1.66.0 + unchanged sb-1.14.3-r1. No game launch or engine case was performed.

| Evidence | Meaning |
|---|---|
| [full_validator.txt](full_validator.txt) | Complete validator with CMF read-only verification, unit discovery, map/naval checks, compatibility and Tiger. 15 PASS, two WARN, zero FAIL. |
| [focused_after.txt](focused_after.txt) | 68 focused cases: 65 pass, three historical skips. Current parity, boundary tests, approval regression, metadata, naval, CMF and Natal/Shepstone contracts. |
| [historical_skips.txt](historical_skips.txt) | Full suite discovery counts 487 cases. The validator's unit subprocess returned success but does not retain successful stdout. These eight specifically rerun historical cases record the exact skip reasons; current-target checks were not skipped. |
| [inventory_after.txt](inventory_after.txt) | Direct current build/manifest/payload and Vanilla/CMF inventory verification; zero drift. |
| [port_parity_before.txt](port_parity_before.txt) | Before the runtime ports, all three new claim/Scramble/formation parity checks failed as expected. |
| [ai_before.txt](ai_before.txt) | New incorporation parity/threshold tests reject the pre-rebase bodies: 12 test methods, eight failed assertions/subtests, no errors. |
| [tiger_edited_files.txt](tiger_edited_files.txt) | Diagnostics referencing the four edited runtime files. Seven errors are syntax copied from current Vanilla and verified by parity tests; formation warnings are native/unchanged content. See the rebase report for limits. |

Transcripts remove trailing whitespace only; all diagnostics are retained.
Before/after test sets overlap the full suite and their counts are not additive.
The full discovery includes the unchanged dependency tests for clean installation,
repeat sync, read-only rejection, hashes, original files and failed-install rollback.
The live dependency was not replaced.

Commands from the repository root:

```sh
python3 -B tools/build_1_14_5_depot_delta.py --game-root '/path/to/Victoria 3/game'
python3 -B -m unittest tests.test_1_14_0_rebase tests.test_1_14_3_compatibility tests.test_1_14_5_compatibility tests.test_1_14_ai_incorporation tests.test_1_14_naval_network tests.test_boer_conventions_review_approval tests.test_natal_zululand_gameplay_contract
python3 -B tools/check_override_inventory.py --game-root '/path/to/Victoria 3/game' --cmf-root '/path/to/Community Mod Framework'
python3 -B tools/validate.py --game-root '/path/to/Victoria 3/game' --cmf-root '/path/to/Community Mod Framework' --tiger
```

Current Python and Git came from the configured Codex dependency runtime; Tiger
was `/Users/depro/.cargo/bin/vic3-tiger`. The full validator reported a Tiger schema
target of 1.13.5 and a final summary of 0 fatal, 1,061 errors, 130 warnings, one
untidy, one tip. These diagnostics remain advisory and are not hidden or treated
as engine verification. DP's fresh-game cases are all still pending.
