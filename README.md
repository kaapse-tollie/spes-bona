# Spes Bona - A Southern Africa Flavour Pack

Spes Bona is a Victoria 3 regional flavor mod for greater Southern Africa built around the Community Mod Framework. The current branch is a Phase 1 v1 release-candidate line focused on making the 1836 start solid, readable, and historically flavored across the Cape, the Boer republics, Natal, and the southeastern frontier.

## Current Scope

- `CAP` replaces start-date `SAF`
- `XHO` remains unified; the 7th, 8th, and 9th Xhosa Wars model separate frontier phases
- `ORA`, `TRN`, `NAL`, `ZUL`, `SWZ`, `GZA`, `BST`, `ORL`, and the frontier minors all have custom startup work; `ABY` is an emergent mid-game tag (Albany secession) with lifecycle scripting rather than startup work
- the live build covers the Cape constitutional struggle, the Great Trek, the Natal question, the MTB pressure lane, and the firearms-modernization lane for selected kingdoms

## Live Feature Set

- Cape Colony:
  liberal vs settler balance JE, Albany petition branch, London answer branch, ECSL and Cape Liberal movement pressure
- Boer republics:
  two-stage Great Trek JE, trek migration pull, MTB war opener, post-Vegkop frontier reward, custom Boer government setup
- Natal / Zululand:
  Retief diplomacy, Retief-killed revenge branch, Blood River branch, ZUL guns-for-land bargain branch, British ultimatum and protectorate-play follow-through
- Firearms modernization:
  day-0 JE for `ZUL`, `SWZ`, `GZA`, `BST`, and `NGN`, with monthly malus decay through imports or domestic arms production
- Startup setup:
  custom pop, state, country, military formation, and building history for the Phase 1 Southern Africa scope

## Requirements

- Victoria 3 `1.15.2` (Steam build `26763837`, branch `public`), all DLC
- Community Mod Framework `1.67.9` with patch `sb-1.15.2-r1`

The working tree targets 1.15.2 and carries SB release version **0.21.1**.
The [port report](Docs/compatibility/1_15_2_implementation.md) records the game
and CMF changes. DP’s [fresh-campaign replay](Docs/compatibility/1_15_2_runtime_matrix.md)
covers subjects, parties, mobilisation, battle casualties, journal rendering and the map.
The [1.15.0 core closure on 7 November](Docs/compatibility/1_15_0_closure_2026_11_07.md)
remains historical acceptance; separate release gates remain open.
The [1.14.5 rebase](Docs/compatibility/1_14_5_rebase.md) and earlier checkpoint
reports remain historical evidence. The approved Zulu institutional and court redesign is now implemented for DP verification; wider country profiles remain deferred. See the [implementation and pending engine matrix](Docs/zulu_institutions_implementation_2026_10_18.md).

## Compatibility

Spes Bona is not a light overlay. It changes Southern Africa startup data heavily, including:

- country history
- pops
- buildings
- state regions
- diplomacy
- journal entries and events
- modifiers, laws, and subject setup

It will conflict with other mods that substantially rewrite Southern Africa in 1836.

## Documentation

The live repository documentation is the source of truth:

- [Open audit issues](Docs/audit_issues_open.md) · [Completed audit issues](Docs/audit_issues_completed.md)
- [Override manifest](Docs/compatibility/override_manifest.md)
- [Third-party compatibility notes](Docs/compatibility/third_party_compatibility.md)
- [Cross-tag event travel times](Docs/cross_tag_event_travel_times.md)
- [Bechuanaland map-connectivity exception](Docs/bechuanaland_map_connectivity.md)
- [Resource-update contributor and maintainer guide](Docs/resource_update_guide.md)
- [Resource-balance executive summary](Docs/resource_balance_summary.md)

Current port target: **Victoria 3 1.15.2**, fresh campaigns with all DLC.
See the [core closure and remaining limits](Docs/compatibility/1_15_0_closure_2026_11_07.md)
and [current DP runtime checks](Docs/compatibility/1_15_2_runtime_matrix.md). Static checks
are not engine certification.

## Validation

Run the validation suite from the repository root:

```sh
python3 tools/validate.py
```

Validation checks the pinned CMF `1.67.9` + `sb-1.15.2-r1` installation without changing it. Install or repair the canonical sibling directory `../Community Mod Framework` with `python3 -B tools/sync_cmf.py`: it verifies the exact release archive, applies the pinned patch in staging, verifies the resulting tree, and installs with rollback. `--check` is read-only; `--force` retains the patch; `--latest` is rejected for this pinned dependency. `--skip-cmf-sync` omits the synchronizer check but retains the installed-tree integrity check.

When the proprietary dependencies are available, include explicit Vanilla/CMF comparison and Tiger validation:

```sh
python3 tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --tiger
```

Missing proprietary dependencies report `SKIP`; CI does not require them. Tiger is useful for parser validation, but cold-launch logs and fresh-start smoke tests remain authoritative. Do not rely on filewatcher hot reload for map-data or startup-history changes.

SB's naval graph removes obsolete native harbour leaves on its impassable coast.
`python3 -B tools/check_naval_network.py` checks its exact derivation without
writing. After an upstream graph or impassability change, rebuild explicitly with
`--write-network`, review the node/edge delta, then update the inventory and map
hashes. See the [launch retest evidence](Docs/compatibility/1_15_0_launch_retest_2026_11_05.md).

Release validation is pinned to CMF `1.67.9`, commit `9103c9cb4130d46cb18204d588def1266e5c1555`, and GitHub asset SHA-256 `2c702bbf99fd96804366896521832d18519a6a33e94519d49160de0ece7e04ae`. The launcher dependency is `1.67.*`. During the 1.14 beta audit, the Workshop change log reported a reversion to its 1.13 payload, so use the exact GitHub asset until the Workshop copy is unambiguous.

On the primary development machine, the verified release plus the pinned compatibility patch is installed at `/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Community Mod Framework`.

## Current Priority

This branch is in stabilization mode.

What still matters most:

- fresh-save gameplay verification
- debugger cleanup if any new issues appear
- AI balance and branch reliability
- major pre-release balance pass for BST, SWZ, ZUL and GZA starting technologies, economies and literacy: [TODO and saved research briefs](Docs/audit_issues_open.md#major-pre-release-balance-todo--bantu-starting-positions)
- small presentation and content polish

The current dependency is the verified CMF release **plus** `sb-1.15.2-r1`; an unpatched release is unsupported. Install with `python3 -B tools/sync_cmf.py`. `--check` verifies the complete patched file tree without modifying it. See the [1.15.2 dependency review](Docs/compatibility/1_15_2_implementation.md#community-mod-framework).
