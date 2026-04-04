# Spes Bona - A Southern Africa Flavour Pack

Spes Bona is a Victoria 3 regional flavor mod for greater Southern Africa built around the Community Mod Framework. The current build is a Phase 1 foundation pass focused on making the 1836 start work properly for the Cape, the Boer republics, the Xhosa frontier, and Natal.

## Current Build

This refresh currently includes:

- 2 custom journal entries
- 20 custom events
- 4 scripted buttons
- 2 custom political movements
- 21 custom character entries
- 1 custom amendment
- 1 custom subject type
- 1 formable country definition
- 2 custom state traits

### Current Gameplay Focus

| Area | Current content |
|---|---|
| Cape Colony (`CAP`) | Cape Politics JE, liberal vs settler tug-of-war, ECSL and Cape Liberal movements, faction buttons, frontier raid flavor |
| Transvaal / Orange Free State (`TRN` / `ORA`) | Great Trek JE, two-stage republic consolidation, trek migration pull, stage reward events |
| Natal / Zululand | Retief negotiation chain, refusal/war alternatives, Natalia formation, British ultimatum follow-through |
| Ndebele frontier | Early-game pressure on TRN through raids and a follow-up showdown event |
| Regional setup | `CAP` replacing start-date `SAF`, `XHG` / `XHR` / `XHT` split from vanilla `XHO`, `ORL` setup, pop/building/homeland/state history cleanup |

### What This Build Is Not Yet

This is not yet the later-century Southern Africa overhaul originally described in older docs. The current build does not yet include full Rhodesia content, the Boer Wars, a full Responsible Government chain, a full Basutoland chain, or a bespoke Union of South Africa narrative.

## Tag Model

- `CAP` is the live British colony at game start
- `SAF` is reserved as a formable
- `XHO` is split into `XHG`, `XHR`, and `XHT`
- `ORL` is represented in Hereroland
- `NAL` can form through the Natal chain

## Requirements

- Victoria 3 `1.12.5`
- Community Mod Framework

## Compatibility

Spes Bona is not a light overlay. It currently modifies:

- country definitions
- cultures
- state regions / map setup
- state, pop, and building history
- on_actions
- journal entries, events, scripted buttons, movements, and localization

It will conflict with other mods that touch Southern Africa startup data, the Highveld/Natal setup, or the same CMF-sensitive startup hooks.

## Installation

### Manual

1. Place the `Spes Bona - A Southern Africa Flavour Pack` folder in your Victoria 3 `mod` directory.
2. Enable both Community Mod Framework and Spes Bona in the launcher.
3. Keep CMF above Spes Bona if your load order requires dependency-first ordering.

## Development Status

Current status: Phase 1 refresh.

What is already done:

- startup architecture moved away from a brittle `SAF`/`XHO`-dependent overlay approach
- Southern Africa history refactored around `CAP`, split Xhosa tags, `ORL`, and Port Natal handling
- Cape Politics, Great Trek, Natal, and Ndebele Phase 1 content all exist in script
- mod text files normalized to UTF-8 BOM for Tiger/game compatibility

What still needs live verification:

- fresh 1836 startup logs after the latest stabilization pass
- Natalia formation and the delayed British ultimatum in live gameplay
- final tuning of Cape movement behavior and Ndebele pressure

## Validation

Current standard validation command:

```sh
vic3-tiger -c --unused --no-color \
  --game '/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3' \
  --workshop '/Users/depro/Library/Application Support/Steam/steamapps/workshop/content/529340' \
  'Spes Bona - A Southern Africa Flavour Pack'
```

As of the latest refresh pass this returns `0 fatals / 0 errors / 0 warnings`, with one remaining `unused-localization` untidy report that appears to be a Tiger false-positive bucket for automatically-resolved loc keys.

## Notes

- Live reference: [`../history.md`](../history.md)
- Live roadmap: [`../v1_roadmap.md`](../v1_roadmap.md)
- Live testing sheet: [`../test_runs/phase1_ingame_testing_checklist.md`](../test_runs/phase1_ingame_testing_checklist.md)
- Manual test log archiving is supported by [`../tools/archive_logs.sh`](../tools/archive_logs.sh).
