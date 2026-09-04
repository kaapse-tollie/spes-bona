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

- Victoria 3 `1.14.0` Open Beta 1 (Steam build `25081502`, branch `1.14-openbeta`)
- Community Mod Framework `1.66.x`

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

## Validation

Run the validation suite from the repository root:

```sh
python3 tools/validate.py
```

Validation fetches GitHub's exact CMF `1.66.0` release tag, requires `release-1.66.0.zip`, verifies its pinned SHA-256, and only then synchronizes the canonical sibling directory `../Community Mod Framework`. It never follows a newer “latest” release during normal validation. Use `--skip-cmf-sync` only for an intentional offline run; `tools/sync_cmf.py --latest` is an explicit maintainer-only discovery mode.

When the proprietary dependencies are available, include explicit Vanilla/CMF comparison and Tiger validation:

```sh
python3 tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --tiger
```

Missing proprietary dependencies report `SKIP`; CI does not require them. Tiger is useful for parser validation, but cold-launch logs and fresh-start smoke tests remain authoritative. Do not rely on filewatcher hot reload for map-data or startup-history changes.

Release validation is pinned to CMF `1.66.0`, commit `807c32ff42b75714a3a0e090c0db3357b5e46ed7`, and GitHub asset SHA-256 `79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b`. The launcher dependency is `1.66.*`. During the 1.14 beta audit, the Workshop change log reported a reversion to its 1.13 payload, so use the exact GitHub asset until the Workshop copy is unambiguous.

On the primary development machine, the canonical GitHub release is installed without local edits at `/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Community Mod Framework`.

## Current Priority

This branch is in stabilization mode.

What still matters most:

- fresh-save gameplay verification
- debugger cleanup if any new issues appear
- AI balance and branch reliability
- small presentation and content polish
