# Spes Bona - A Southern Africa Flavour Pack

Spes Bona is a Victoria 3 regional flavor mod for greater Southern Africa built around the Community Mod Framework. The current branch is a Phase 1 v1 release-candidate line focused on making the 1836 start solid, readable, and historically flavored across the Cape, the Boer republics, Natal, and the southeastern frontier.

## Current Scope

- `CAP` replaces start-date `SAF`
- `XHO` is split into `XHG`, `XHR`, and `XHT`
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

- Victoria 3 `1.12.5`
- Community Mod Framework

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

The live repo docs are now the source of truth:

- [docs/current_state.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/docs/current_state.md)
- [docs/testing_checklist.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/docs/testing_checklist.md)
- [docs/flag_texture_scaffolds.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/docs/flag_texture_scaffolds.md)

## Validation

Current standard validation command:

```sh
vic3-tiger -c --unused --no-color \
  --game '/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3' \
  --workshop '/Users/depro/Library/Application Support/Steam/steamapps/workshop/content/529340' \
  'Spes Bona - A Southern Africa Flavour Pack'
```

Current target state:

- `0 fatals`
- `0 errors`
- `0 warnings`
- `0 untidy`

## Current Priority

This branch is in stabilization mode.

What still matters most:

- fresh-save gameplay verification
- debugger cleanup if any new issues appear
- AI balance and branch reliability
- small presentation and content polish
