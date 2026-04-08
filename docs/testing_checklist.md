# Testing Checklist

Use fresh `1836` starts unless a test explicitly needs a mid-chain save. This file should track the current live branch, not the older Phase 1 milestone checklist.

## Smoke Pass

- `vic3-tiger` stays at `0 fatals / 0 errors / 0 warnings / 0 untidy`
- no duplicate JE, duplicate loc, missing scope, treaty, or formation warnings appear on startup
- no travel-connection, route-strip, invalid-object, or teleporting-unit map bugs appear on startup
- the Southern Africa countries load with the intended colors, flags, and dynamic names
- a fresh observe run does not immediately break `ZUL`, `TRN`, `ORA`, `NAL`, `ZPB`, or `LYD`

## Core Startup

~~- Boer IG naming and trait swaps apply correctly after startup~~
~~- `NG Kerk` gets its intended trait package instead of vanilla fallback traits~~
~~- `ORA` and `TRN` rulers stay valid as commander-rulers after time passes~~ 
- commandant upkeep no longer fights vanilla retirement logic after age `60`
~~- `MTB` gets `Mzilikazi's Host` only when ~`TRN` or `ORA` is player~~
~~- otherwise `MTB` gets `Native warbands`~~`
~~- `ZUL`, `SWZ`, and `GZA` start with `je_sb_adopt_firearms`~~
~~- `ZUL` also starts with `je_sb_zulu_kingdom`~~
~~- `CAP` starts with `je_sb_cape_politics`~~
~~- `ORA` and `TRN` both start with `je_sb_great_trek`~~

## Map And State Split

~~- West, East, and Northern Transvaal all load correctly on the map~~
~~- clicking the three Transvaal states no longer jumps to bad coordinates~~
- units do not route into the South Pacific or other invalid fronts
- West / East / North dynamic state names switch correctly between native and European owners:
  - West: `Gauteng` / `Potchefstroom`
  - East: `Mpumalanga` / `Lydenburg`
  - North: `Limpopo` / `Zoutpansberg`
~~- `TRN` starts with claim on West only~~
~~- `SWZ` starts with a claim on East Transvaal~~
~~- `ZPB` scope is the full Northern Transvaal state~~
~~- `LYD` scope is the East Transvaal state~~
- East / North / Drakensberg capital and hub names are no longer obviously wrong
- European city naming for Drakensberg works as intended

## Cape Politics

~~- the Cape bar uses the centered `-100 -> 100` model correctly~~
- `sb_cape.020` only fires while the Cape politics JE is active
- `sb_cape.020` gives the intended liberal bar shift, liberal strength, and ECSL activism effect
~~- Albany sanction and refusal branches both work~~
~~- London answer branches both work~~
~~- the JE still has the `1880` failure timeout~~
- compromise, liberal, settler, and Albany outcomes all still resolve correctly
- the custom CAP liberal citizenship law `law_sb_non_racialism` is only available after the liberal win path
- CAP responsible-government hooks remain stable even if the wider CAP content pass is still deferred

## Responsible Government

~~- the responsible-government action appears only on valid colony subjects~~
~~- the request resolves as its own responsible-colony subject relationship, not as a plain crown colony~~
~~- a granted colony can use ordinary non-colonial government types~~
~~- a British grant maps monarchy to parliamentary republic as intended~~
- a non-British monarchical grant maps to monarchy and keeps the parent dynasty ruler setup
~~- `concept_sb_responsible_colony_desc` and the no-icon loc render correctly~~
~~- the subject does not snap back into crown-colony behavior after a day tick~~
~~- the granted subject can pursue its own diplomacy as intended~~

## Great Trek Core

- stage 1 completes independently of stage 2
~~- `ORA` stage 2 completes from full Vrystaat control~~
~~- `TRN` stage 2 keys off West Transvaal rather than the whole old macro-state~~
~~- `TRN` can complete the JE without first owning East or Northern Transvaal~~
~~- Great Trek completion still hands off into `A Republic Established`~~
- AI weights on `A Republic Established` remain `75%` normal republic and `25%` frontier republic
- the AI-only trek battalion bonus only applies while both `ORA` and `TRN` are AI and the JE is active

## MTB And Frontier War

- `TRN` gets `sb_trek.004`
- `ORA` gets `sb_trek.005`
- ORA support joins the war correctly
- ORA refusal behaves correctly
- `TRN` win fires `sb_trek.002`
- `MTB` retreat transfers West and North Transvaal to `TSW`, and East to `PDI`
- `TRN` gets the frontier reward only once
- `TSW` inherits the intended MTB lands in both west and north

## ZPB And TRN

- Cape liberalization can still spawn `ZPB`
- `ZPB` gets full hidden Boer republic setup on spawn
- player can choose to switch to `ZPB`
- `ZPB` uses the shared Potchefstroom flag
- `ZPB` starts with `law_slave_trade`
- the Boer migration event into `ZPB` visibly fires
- after Great Trek completion, `TRN` gets the Sand River Convention
- after Great Trek completion, `ORA` gets the Bloemfontein Convention
- accepting either convention grants recognition, renews the `GBR` truce, grants transit rights, and bans slavery
- refusing either convention queues delayed British anti-slavery pressure
- recognized `TRN` with an independent slaveholding `ZPB` gets `Lawlessness in Northern Transvaal`
- the `Bring order` branch adds the claim and starts `je_sb_zpb_crackdown`
- completing the crackdown JE by taking North Transvaal resolves the crisis cleanly
- timing out the crackdown JE strips `TRN` recognition and queues British pressure on `ZPB`
- the `true frontier spirit` branch gives the pact with `ZPB`, restores slavery in `TRN`, and queues British pressure
- the anti-slavery British response opens `dp_ban_slavery` against the intended target and does not loop forever

## LYD And TRN

- `LYD` still spawns only from the Transvaal centralizing line
- player can choose to switch to `LYD`
- `LYD` uses the Dutch-style starting flag
- `LYD` receives real Boer population through migration / transfer from `TRN`
- `je_sb_transvaal_unity` appears when `LYD` exists
- the JE shows the visible conservative-stability requirements properly
- the cumulative 5-year progress logic still works
- successful completion reunifies `LYD` with `TRN` and incorporates East Transvaal

## Natal / Zululand / Britain

- Retief grant branch works and founds Boer `NAL`
- Retief killed branch reaches the revenge handoff properly
- `TRN` support event fires properly after the revenge choice
- `TRN` can now also refuse support
- Blood River victory branch founds `NAL` correctly
- the migration from `CAP` to `NAL` fires on the normal Boer-founding path
- ZUL guns-for-land branch works on both accept and reject
- Port Natal / Durban content now runs through the current decision/event flow correctly
- British answer to the Port Natal raid uses the intended war path
- British victory in the early coastal war creates a proper British Natal colony on the same `NAL` tag
- the early British Natal colony owns the intended full footprint and does not snap back to independence
- the later `NAL` ultimatum only fires after the port-and-delay setup
- if `NAL` backs down in the diplomatic play, it still becomes and remains a British colony
- if `NAL` resists and loses, the same British colony finalizer happens
- after British submission/defeat, Pretorius is exiled and no longer rules Natal
- refugee migration after British takeover goes to one random inland Boer tag, not all of them
- the colony law stack, culture swap, and treaty cleanup all apply on British takeover

## Zulu Dynastic Stability

- the JE bar drifts downward under Dingane's starting setup
- the JE can be pushed upward through victories and positive choices
- at `100`, the secure-dynasty event fires and installs the intended heir
- at `0`, the current claimant usurps, the old heir is removed, a new heir is installed, and stability resets to `33`
- the `Enforce Dynastic Claims` toggle appears on the JE
- turning it on applies the authority drain and positive stability drift
- turning it off removes the modifier cleanly
- Retief outcomes move dynastic stability in the intended direction
- Blood River win/loss moves dynastic stability correctly
- Blood River outcomes also advance firearms progress
- the Swazi chain only appears under Dingane and uses the intended later frontier timing
- Swazi victory gives positive stability
- Swazi defeat gives a major stability hit and meaningful collapse pressure
- generic non-special war victories and defeats apply the `+20/-20` stability swings only once
- the random dynastic events fire and present meaningful tradeoffs

## Firearms Modernization

- no duplicate `je_sb_adopt_firearms` or `je_sb_zulu_kingdom` warnings appear
- progress text is readable and player-facing
- a qualifying small-arms transfer treaty advances progress
- a `90%` staffed arms industry advances progress
- both routes now complete after `24` cumulative months
- the iron-age malus starts at roughly `-96%` kill and recovery
- the malus shrinks month by month while progress is active
- the temporary military-research malus stays until completion
- completion fires and grants the temporary `new tactics` reward
- `ZUL` completion also gives dynastic stability and the intended ruler trait
- `SWZ` and `GZA` completion also grant their intended ruler trait reward

## ZUL / GZA AI Army Support

- if `ORA` or `TRN` is player and AI `ZUL` reaches the Retief buildup endpoint while still on the firearms JE, it gets the direct extra units
- if neither `ORA` nor `TRN` is player, ZUL instead uses the intended random fallback path
- if `GZA` enters a diplomatic play involving a player while still on the firearms JE, it gets the intended emergency support
- `ZUL` no longer deletes its entire army at the start of the frontier war
- `GZA` no longer strips down unexpectedly when the JE is active

## Formables, Tiers, Names, And Presentation

- starting country tiers match the intended Southern Africa override list
- Great Trek completion gives `ORA` / `TRN` their principality-status fallback modifier
- Transvaal Unity upgrades `TRN` to its grand-principality fallback status modifier
- `TRN` name ladder works:
  - early: `Potchefstroom`
  - normal mature: `Transvaal Republic`
  - full consolidation: `Suid-Afrikaanse Republiek`
- `NGU` is formable on the new tag
- `NGU` requires the intended four-state footprint at `80%`
- `NGU` gets the intended name, adjective, flag, and monarchical setup
- `SAF` and `NGU` present correctly as the kingdom-tier formables

## Frontier And Regional Setup

- `STATE_DRAKENSBERG` still exists and keeps its mountain defense trait
- Basotho setup still initializes cleanly
- `BST`, `PHL`, and `WBL` startup behavior still makes sense after the state split and treaty work
- `CAP` still guarantees `WBL` independence at start
- Hereroland, Albany, and the split Xhosa tags still initialize cleanly
- `SWZ`'s East Transvaal claim meaningfully slows immediate TRN colonization pressure

## Suggested Save Anchors

- clean `1836` startup smoke save
- post-`MTB` war save
- pre-Blood River ORA save
- post-Boer `NAL` founding save
- post-British-Natal ultimatum save
- post-Great-Trek-completion `TRN` save
- post-`ZPB` spawn recognized `TRN` save
- post-`LYD` split save
