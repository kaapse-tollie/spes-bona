# Testing Checklist

Use fresh `1836` starts unless a test explicitly needs a save mid-chain. This file is meant to reflect the current live branch, not the older Phase 1 release-candidate checklist.

## Core Startup

- `vic3-tiger` stays at `0 fatals / 0 errors / 0 warnings / 0 untidy`
- no duplicate JE warnings on startup
- no travel-connection, route-strip, treaty, missing-scope, or military-formation debugger spam on startup
- `ORA` and `TRN` rulers stay valid as commander-rulers after time passes
- Boer IG naming and trait swaps apply correctly after startup
- `NG Kerk` gets its intended trait package instead of vanilla fallback traits
- `ORA` keeps its corridor arrangement with `GBR`

## Cape Politics

- `CAP` starts with `je_sb_cape_politics`
- the balance bar uses the centered `-100 -> 100` logic correctly
- threshold text and status text match the current drift model
- Albany sanction and refusal branches both work
- London answer branches both work
- Cape law and drift changes still feel legible in play
- `CAP` / `ABY` flags, names, and map colors still look right

## Great Trek Core

- `ORA` and `TRN` both start with `je_sb_great_trek`
- stage 1 completes independently of stage 2
- `ORA` stage 2 completes from full Vrystaat control even if GDP is still low
- `ORA` only renames to Oranje once the full JE completes
- `TRN` stage 2 keys off West Transvaal rather than the whole old macro-state
- `TRN` can complete the JE without first owning East or Northern Transvaal
- Great Trek completion text matches the current requirements

## MTB And Frontier War

- `MTB` gets `Mzilikazi's Host` only when `TRN` or `ORA` is player
- otherwise `MTB` gets `Native warbands`
- `TRN` gets `sb_trek.004`
- `ORA` gets `sb_trek.005`
- ORA support joins the war correctly
- ORA refusal behaves correctly
- `TRN` win fires `sb_trek.002`
- `MTB` retreat now transfers West and North Transvaal to `TSW`, and East to `PDI`
- `TRN` gets the frontier reward only once

## Transvaal Split

- West, East, and Northern Transvaal all load correctly on the map
- clicking the three Transvaal states no longer jumps to bad coordinates
- state names switch correctly between native and European owners:
  - West: `Gauteng` / `Potchefstroom`
  - East: `Mpumalanga` / `Lydenburg`
  - North: `Limpopo` / `Zoutpansberg`
- `TRN` starts with claim on West only
- `SWZ` starts with a claim on East Transvaal
- `TRN` agrarian/frontier route gains an East claim from the republic-choice event
- West/East/North capitals and hub names are no longer obviously wrong

## ZPB And LYD

- Cape liberalization can spawn `ZPB`
- `ZPB` gets full hidden Boer republic setup on spawn
- player can choose to switch to `ZPB`
- `ZPB` uses the shared Potchefstroom flag
- `ZPB` starts with `law_slave_trade`
- `LYD` still spawns only from the Transvaal centralizing line
- player can choose to switch to `LYD`
- `LYD` uses the Dutch-style starting flag
- both splinter tags get the expected ruler, IG, and government setup

## Natal / Zululand / Britain

- Retief grant branch works and founds `NAL`
- Retief killed branch reaches the revenge handoff properly
- `TRN` support event fires properly after the revenge choice
- Blood River victory branch founds `NAL` correctly
- ZUL guns-for-land branch works on both accept and reject
- Dingane victory branch works and the Port Natal raid follow-up appears correctly
- British answer to the Port Natal raid uses `dp_annex_war`
- British victory in that coastal war creates the Natal Colony correctly
- `NAL` ultimatum only fires after the port-and-delay setup
- if `NAL` backs down, it becomes a British protectorate and then a crown colony through the defeat event
- if `NAL` resists and loses, the same protectorate -> crown colony path happens
- refugee migration after British takeover goes to one random inland Boer tag, not both
- if any of `NAL`, `ORA`, or `TRN` is player, the chain forces the resistance/support route

## Firearms Modernization

- `ZUL`, `SWZ`, and `GZA` have the JE on day `0`
- `ZUL` also starts with the Zulu kingdom JE on day `0`
- no duplicate `je_sb_adopt_firearms` or `je_sb_zulu_kingdom` warnings appear
- progress text is readable and player-facing
- a qualifying small-arms transfer treaty advances progress
- a `90%` staffed arms industry advances progress
- both routes now complete after `24` cumulative months
- the iron-age malus starts at roughly `-96%` kill and recovery
- the malus shrinks month by month while progress is active
- the temporary military-research malus stays until completion
- the completion event fires and grants the temporary `new tactics` reward

## ZUL / GZA AI Army Hack

- if `ORA` or `TRN` is player and `ZUL` enters the relevant play while still on the firearms JE, ZUL gets its emergency barracks bump
- otherwise ZUL only gets that bump on the intended `20%` fallback
- if `GZA` enters a diplomatic play involving a player while still on the firearms JE, it gets the emergency barracks bump
- `ZUL` no longer deletes its entire army at the start of the frontier war
- `GZA` no longer strips down unexpectedly when the JE is active

## Frontier And Regional Setup

- `STATE_DRAKENSBERG` exists and has its mountain defense trait
- `BST` capital localization is correct
- Moshoeshoe stays valid in the Basotho setup
- split Xhosa tags behave correctly at start
- `BST` / `PHL` / `WBL` startup behavior still makes sense after the state work
- Hereroland and Albany setup still initialize cleanly
