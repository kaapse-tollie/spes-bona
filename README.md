# Spes Bona - A Southern Africa Flavour Pack

Spes Bona is a Victoria 3 regional flavor mod for greater Southern Africa built around the Community Mod Framework. The current branch is a Phase 1 v1 release-candidate line focused on making the 1836 start solid, readable, and historically flavored across the Cape, the Boer republics, Natal, and the southeastern frontier.

## Current Scope

- `CAP` replaces start-date `SAF`
- `XHO` remains unified; the 7th, 8th, and 9th Xhosa Wars model separate frontier phases
- `ORA`, `TRN`, `NAL`, `ZUL`, `SWZ`, `GZA`, `BST`, `ORL`, `ABY`, and the frontier minors all have custom startup work
- the live build covers the Cape constitutional struggle, the Great Trek, the Natal question, the MTB pressure lane, and the firearms-modernization lane for selected kingdoms

## Live Feature Set

- Cape Colony:
  liberal vs settler balance JE, Albany petition branch, London answer branch, ECSL and Cape Liberal movement pressure
- Boer republics:
  two-stage Great Trek JE, trek migration pull, MTB war opener, post-Vegkop frontier reward, custom Boer government setup
- Natal / Zululand:
  Retief diplomacy, Retief-killed revenge branch, Blood River branch, ZUL guns-for-land bargain branch, British ultimatum and annex-war follow-through
- Firearms modernization:
  day-0 JE for `ZUL`, `SWZ`, and `GZA`, with monthly malus decay through imports or domestic arms production
- Startup setup:
  custom pop, state, country, military formation, and building history for the Phase 1 Southern Africa scope

## Requirements

- Victoria 3 `1.13.10`
- Community Mod Framework `1.61.x`

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

- [Audit issue register](Docs/audit_issue_register.md)
- [Override manifest](Docs/compatibility/override_manifest.md)
- [Third-party compatibility notes](Docs/compatibility/third_party_compatibility.md)
- [Cross-tag event travel times](Docs/cross_tag_event_travel_times.md)
- [Bechuanaland map-connectivity exception](Docs/bechuanaland_map_connectivity.md)
- [Resource-balance executive summary](Docs/resource_balance_summary.md)

## Validation

Run the validation suite from the repository root:

```sh
python3 tools/validate.py
```

Validation queries GitHub for CMF's latest stable release and synchronizes the official release payload to the canonical sibling directory `../Community Mod Framework` before running compatibility checks. If GitHub publishes a newer CMF minor release, it is installed and validation then fails with a rebase-required error until SB's pinned CMF baseline is updated. Use `--skip-cmf-sync` only for an intentional offline run.

When the proprietary dependencies are available, include explicit Vanilla/CMF comparison and Tiger validation:

```sh
python3 tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --tiger
```

Missing proprietary dependencies report `SKIP`; CI does not require them. Tiger is useful for parser validation, but cold-launch logs and fresh-start smoke tests remain authoritative. Do not rely on filewatcher hot reload for map-data or startup-history changes.

Release validation is pinned to CMF `1.61.0` commit `9b999e3`. The launcher dependency is `1.61.*`, so patch releases are accepted while each new CMF minor line requires an explicit compatibility review.

On the primary development machine, the canonical GitHub release is installed without local edits at `/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Community Mod Framework`.

## Current Priority

This branch is in stabilization mode.

What still matters most:

- fresh-save gameplay verification
- debugger cleanup if any new issues appear
- AI balance and branch reliability
- small presentation and content polish
