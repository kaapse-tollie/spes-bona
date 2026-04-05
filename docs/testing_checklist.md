# Testing Checklist

Use fresh `1836` starts unless a test explicitly needs a mid-chain save.

## Core Startup

- `vic3-tiger` stays at `0 fatals / 0 errors / 0 warnings / 0 untidy`
- no duplicate JE warnings on startup
- no treaty, military-formation, or missing-scope debugger spam on startup
- `ORA` and `TRN` rulers stay valid as commander-rulers after time passes
- `ORA` keeps its trade-through connection with `GBR`

## Tag Sweep

- `CAP` fresh start
- `ABY` fresh start through its formation path
- `GBR` fresh start
- `ORA` fresh start
- `TRN` fresh start
- `NAL` fresh start through formation
- `ZUL` fresh start
- `BST` fresh start

## Cape

- Cape Politics JE appears correctly
- bar logic and status text look right
- dominance threshold events behave correctly
- Albany sanction and refusal branches both work
- London answer branches both work
- `CAP` / `ABY` flags, names, and accepted map-color behavior still look right

## Great Trek And MTB

- `ORA` and `TRN` Great Trek JE starts correctly
- stage 1 and stage 2 fire correctly
- `MTB` pressure lane opens correctly against `TRN`
- `TRN` gets `sb_trek.004`
- `ORA` gets `sb_trek.005`
- ORA support joins the war correctly
- ORA refusal behaves correctly
- `TRN` win fires `sb_trek.002`
- `MTB` withdraws north and `TRN` gets the `5`-year frontier reward only once

## Natal / Zululand

- Retief grant branch works and founds `NAL`
- Retief killed branch reaches the revenge handoff properly
- `TRN` support event fires properly after the revenge choice
- Blood River victory branch founds `NAL` correctly
- ZUL guns-for-land branch works on both accept and reject
- Dingane victory branch works and the Port Natal raid follow-up appears correctly
- British answer to the Port Natal raid uses `dp_annex_war`
- British victory in that coastal war creates the Natal Colony
- `NAL` ultimatum fires after the port-and-delay conditions, not immediately
- `NAL` submit branch works
- `NAL` refuse branch seizes Port Natal and can call `ORA` / `TRN`
- inland refugee migration after British victory works

## Firearms JE

- `ZUL`, `SWZ`, and `GZA` have the JE on day `0`
- no duplicate `je_sb_adopt_firearms` warnings appear
- progress text is readable and player-facing
- a qualifying small-arms transfer treaty advances progress
- a `90%` staffed arms industry advances progress
- both routes complete after `12` cumulative months
- the iron-age malus shrinks month by month
- the temporary military-research malus stays until completion
- the completion event fires and grants the temporary `new tactics` reward

## Frontier And Setup

- `STATE_DRAKENSBERG` exists and has its mountain defense trait
- `BST` / `PHL` / `WBL` startup behavior still makes sense after the state split
- Moshoeshoe stays valid in the Basotho setup
- split Xhosa tags behave correctly at start
- Hereroland and Albany setup still initialize cleanly
