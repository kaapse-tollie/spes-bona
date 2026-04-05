# Current State

This file is the repo-local reference for the live Phase 1 v1 branch. It is meant to stay short and track the actual scripted content in the current mod folder.

## Status

- branch goal: Phase 1 v1 release candidate
- current focus: debugging, polish, AI balance, and fresh-save verification
- validation target: `0 fatals / 0 errors / 0 warnings / 0 untidy`

## Tag Model

- `CAP` is the live Cape Colony at game start
- `SAF` is reserved for later formable use
- `ABY` is the Albany outcome tag
- `XHO` is split into `XHG`, `XHR`, and `XHT`
- `ORA` and `TRN` are live Boer republic starts
- `NAL` forms through the Natal chain
- `ZUL`, `SWZ`, and `GZA` run the firearms-acquisition JE
- `ORL` exists in Hereroland
- `STATE_DRAKENSBERG` is a separate Phase 1 frontier state with a defensive mountain trait

## Live Branch Reference

### Cape Politics

- `CAP` starts with `je_sb_cape_politics`
- the JE is a liberal-versus-settler balance bar
- Albany pressure events fire at the dominance thresholds
- the JE resolves in one of five ways:
  liberal resolution
  settler resolution
  compromise
  Albany secession branch after London answers
  failure in `1880`

### Great Trek

- `ORA` and `TRN` share `je_sb_great_trek`
- stage 1: reach `GDP >= 100000`
- stage 2: control the full homeland state region
- completion settles the republic, removes the frontier expedient government setup, and ends the trek migration pull

### TRN / MTB Frontier

- `MTB` opens the early war lane against `TRN`
- `TRN` gets `sb_trek.004`
- `ORA` then gets `sb_trek.005` and can aid or refuse
- if `TRN` wins, `sb_trek.002` fires
- that event now has a single live outcome:
  `MTB` withdraws north into the Rozvi-space lane
  `TRN` gets `sb_trek_frontier_drive` for `5` years

### Natal / Zululand

- `ORA` can open the Natal question by sending Retief
- `ZUL` currently has three live responses:
  grant the southern strip
  kill Retief and seize the frontier
  sell the southern strip for guns

- grant branch:
  `NAL` forms
  player can choose to switch to `NAL`
  Dingane is politically weakened

- Retief-killed branch:
  `ORA` can back down or vow revenge
  revenge calls `TRN`
  `TRN` can support or refuse
  Boer victory leads into the Blood River / Natalia founding path
  Dingane victory leads into the ZUL triumph path and can escalate into a Port Natal raid

- guns-for-land branch:
  `ZUL` offers land in exchange for firearms
  `ORA` can accept and found `NAL` peacefully while supplying guns
  or reject and push the chain back into war

- British coastal intervention:
  if Dingane raids Port Natal and Britain answers, the response uses `dp_annex_war`
  British victory creates the Natal Colony

- later Natalia branch:
  after `NAL` has an operating port, Britain can send the Natal ultimatum after a long delay window
  `NAL` can submit or refuse
  refusal seizes Port Natal and can call `ORA` and `TRN`
  if Britain wins that later war, Boer refugee events fire inland
  TODO: add a dedicated Natalia Great Trek / coastal republic JE once the Natal chain is fully stable

## Firearms Modernization JE

- `ZUL`, `SWZ`, and `GZA` start with `je_sb_adopt_firearms`
- the JE models the shift away from the `sb_iron_age_weapons` malus
- progress comes from either route:
  an active small-arms transfer treaty with a country that runs an arms industry
  an arms industry at at least `90%` occupancy
- both routes now complete after `12` cumulative months
- the malus decays month by month while either route is active
- the flat military-research malus stays until the JE completes
- completion fires a `new tactics` reward event and gives a temporary military-research bonus

## Other Important Live Setup

- `CAP` and `ABY` flags, names, and map-color behavior are in the accepted Phase 1 v1 state
- `ORA` keeps its vanilla trade-through connection with `GBR`
- startup treaties are additive again, rather than relying on a full vanilla treaty override
- the repo-local pop research handoff lives outside this mod folder and is not part of the runtime mod payload

## Current Known Soft Spots

- AI balance still needs live playtime, especially in the frontier and Natal branches
- the Cape, Natal, and firearms lanes have the most branch interaction and are the most important fresh-save checks
- repo docs should stay small; if a note stops helping current testing or maintenance, move or remove it
