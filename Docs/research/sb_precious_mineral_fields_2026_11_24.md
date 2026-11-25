# Where gold and diamonds appear in Spes Bona

24 November 2026 · Victoria 3 1.15.2, SB 0.21.0 working tree

## Executive summary

**Northern Transvaal gets one gold-field level and British Bechuanaland gets two when a territorial owner has Nitroglycerin.** SB adds both as usable capacity [1, lines 7–35]. The October 1885 campaign actually has the northern field, established on 5 January 1872, and fields in the Tswana and Cape portions of Bechuanaland, established on 31 August 1872 and 20 January 1885 respectively [2, building manager, states 16777254, 1152 and 50331660]. Northern Transvaal has a good period analogue at Eersteling in 1871 [3, “Gold rushes of the 19th century”, note 34]. SB's British Bechuanaland allowance represents the Amalia–Kraaipan belt. The documented Tati diggings belong with the separate Botswana state in SB's geography [4, Bechuanaland and Botswana rows], [5, Bechuanaland and Botswana rows], [3, “Gold rushes of the 19th century”, notes 27–28].

The core region has **92 configured gold levels** across seven states and **115 designed diamond levels** across nine [1, seven gold grants], [6, Botswana and Zambezi resource blocks], [7, deposit register], [8, Kimberley opening and remaining potential]. These totals combine different things. Native gold reserves, immediate gold capacity, diamond survey finds and Kimberley's opening mine follow four separate paths [1, lines 7–35], [6, Zambezi], [7, survey delivery], [8, Kimberley opening].

## Scope and method

This targeted audit covers the 17 states in SB's Southern Africa geographic definition [9, `geographic_region_southern_africa_old`]. I also checked the whole sub-Saharan map override and report its two additional gold-bearing Mozambican states separately [6, Moçambique and Zambezia]. I searched the live map, buildings, resource effects, discovery callbacks and campaign databases on 24 November, and used geological studies, mining history, a provincial museum and the mine operator for the historical comparison. A level measures game capacity. A building's establishment date dates that building in this campaign.

## Gold inventory

A territorial owner with the required technology can satisfy a scripted gate at game start, on research or when acquiring a share of the state. Each grant is recorded globally once for that geography [1, gold blocks], [10, game start, acquired technology and owner change]. A native gold field requires Prospecting, auto-places and can deplete into gold-mine capacity where the map specifies the replacement [11, `building_gold_field` and `bg_gold_fields`], [6, native gold blocks]. The seven technology grants use `change_resource_potential`. They add to the capped amount, and do not populate the undiscovered counter or supply a missing depletion target [1, gold blocks], [12, “Native evidence and implementation choice”], [2, persistent resources for Bechuanaland and Northern Transvaal].

| State | Campaign opening | Later trigger | Configured gold |
|---|---|---|---:|
| West Transvaal / Witwatersrand | No reserve | Dynamite +25, Pumpjacks +50 [1, lines 53–66, 98–112] | 75 |
| Eastern Transvaal | No reserve | Dynamite +4 [1, lines 68–80] | 4 |
| **Northern Transvaal** | No reserve | Nitroglycerin +1 [1, lines 23–35] | **1** |
| **British Bechuanaland** | No reserve | Nitroglycerin +2 [1, lines 8–22] | **2** |
| Botswana | 1 undiscovered | Native discovery under Prospecting [6, Botswana], [11, gold field] | 1 |
| Zambezi / Zimbabwe | 1 undiscovered | Native discovery for the first level, Pumpjacks +4 capped [6, Zambezi], [1, lines 113–126] | 5 |
| Transorangia / Vrystaat | No reserve | Pneumatic Tools +4 [1, lines 142–155] | 4 |
| **Core total** | **2 undiscovered** | **90 capped** [1, gold blocks], [6, Botswana and Zambezi] | **92** |
| Moçambique, outside the core | 2 undiscovered | Native discovery and depletion [6, Moçambique] | 2 |
| Zambezia, outside the core | 1 discovered, 4 undiscovered | Native discovery of the remaining four and depletion [6, Zambezia] | 5 |

The other ten core states have no configured gold. The two adjacent Mozambican entries take the whole regional map-file total, including the SB grants, to **99** [1, gold blocks], [6, all gold blocks], [9, core region]. The native base chance is 0.02% per day before modifiers. Depletion chance also depends on employed levels. A technology gate does not specify a calendar year [13, `BASE_RESOURCE_DISCOVER_CHANCE` and `EMPLOYMENT_RESOURCE_DEPLETE_CHANCE`], [1, gold blocks].

## Diamond inventory

| State | Mechanism and unlock | Designed levels |
|---|---|---:|
| Griqualand West / Kimberley | Annual story check. Mechanical Tools at the Kimberley province's owner, Dynamite in living CAP, Nitroglycerin in living ORA, or Dynamite in TRN after absorbing Oranje [14, `sb_can_discover_kimberley_diamonds`], [10, Kimberley yearly pulse] | 1 opening mine + 19 further potential [8, opening and seed helpers] |
| Transorangia / Vrystaat | Dynamite survey [7, deposit register] | 5 |
| Northern Cape | Pumpjacks survey [7, deposit register] | 4 |
| West Transvaal | Pumpjacks survey [7, deposit register] | 20 |
| Namaqualand | Pumpjacks survey [7, deposit register] | 14 |
| Northern Transvaal | Pneumatic Tools survey [7, deposit register] | 6 |
| Drakensberg | Pneumatic Tools survey [7, deposit register] | 6 |
| Botswana | Pneumatic Tools survey [7, deposit register] | 30 |
| Zambezi / Zimbabwe | Pneumatic Tools survey [7, deposit register] | 10 |
| **Total** | **Eight survey deposits plus Kimberley** [7, deposit register], [8, opening and seed helpers] | **115** |

**How a survey becomes a mine.** The first qualifying territorial owner starts an immediate roll and a 365-day cycle shared by all owners of the region. Each roll chooses one eligible state fragment and uses its owner's discovery modifier. A success schedules delivery to a province within 0–364 days. Delivery rechecks the province's present owner and consumes only the levels actually revealed. Ownership changes do not refill the reserve [7, registration, annual roll and delivery], [10, survey callbacks]. The unmodified annual chance is about **7.04%**. A find starts with 20% of the original deposit rounded, minimum one, plus a random whole-number bonus up to 50% rounded, minimum one for the maximum. The remaining reserve caps the result [13, discovery fractions], [15, annual chance and find size]. A successful survey opens construction of the ordinary Diamond Mine. Construction still requires Prospecting and, in a survey state, a territorial owner with the regional technology [16, `unlocking_technologies` and `possible`].

Kimberley follows its own events. The opening creates a mine in the state containing province `x68B5E8`. The one-time capacity helper adds 19 when potential already exists, or first registers potential and adds 18. That accounts for why the save may show a separately built mine and a regional `amount=19`. Adding together levels from every split owner is not a reliable way to measure a geological reserve [8, lines 233–303], [2, Griqualand West persistent resources]. No other core state has a diamond deposit in the current register [7, deposit register], [8, Kimberley helpers].

## What had actually opened by 1 October 1885

These are all the active gold-field, gold-mine and diamond-mine buildings in the 17 core states and the two additional Mozambican states. The levels are the buildings' current sizes. Establishment dates are recorded independently for each state's building [2, building manager, records 10342, 10421, 16787608, 10957 and 11633].

| State and owner | Building | Established | Levels in October 1885 |
|---|---|---|---:|
| Griqualand West, CAP | Diamond mine | 2 Jan 1871 | 13 |
| Northern Transvaal, TRN | Gold field | 5 Jan 1872 | 1 |
| British Bechuanaland, Tswana portion | Gold field | 31 Aug 1872 | 2 |
| Zambezia, POR | Gold mine | 21 Jul 1878 | 1 |
| British Bechuanaland, Cape portion | Gold field | 20 Jan 1885 | 1 |

Bechuanaland illustrates the distinction. Two different owners have field buildings with different establishment dates. The regional resource record still holds `amount=2`, and the Nitroglycerin grant has one global receipt for the region [2, buildings 16787608 and 11633, Bechuanaland state-region record], [1, lines 8–22].

## Historical fit and implications

- **Northern and eastern Transvaal.** Eersteling is a specific reason to keep a small northern field. The eastern rush followed a different chronology. Pilgrim's Rest was proclaimed on 22 September 1873, Barberton had a profitable strike in 1884, and the major Witwatersrand discovery followed in 1886 [3, “Gold rushes of the 19th century”, note 34, and “Discovering and working the Lydenburg Goldfields”, final two paragraphs], [17, “Pilgrim's Rest”, opening paragraphs]. I would retain the separation and let local research affect timing.
- **Bechuanaland and Botswana.** SB's resource audit explicitly describes the British Bechuanaland allocation as a low-confidence border-area proxy [4, Bechuanaland row], [5, Bechuanaland row]. Geological sampling establishes gold-bearing rock at Kalahari Goldridge and Amalia [18, sec. 1, Figs. 1–2]. It cannot date a British Bechuanaland rush. The Tati find was reported in December 1867, in present-day north-eastern Botswana [3, “Gold rushes of the 19th century”, notes 27–28]. The operator dates the Orapa diamond discovery to 1967 and production to 1971 [19, “Discovery”]. I would retain the native Botswana gold level and describe its substantial diamond budget as a counterfactual late-game possibility.
- **Diamond chronology.** The regional synthesis dates the first South African finds to 1867, Zimbabwe's Somabula placer to 1903, Namibia's Lüderitz placers to 1908 and Lesotho's Kao discovery to 1958 [20, Table I]. Charles Payton, who visited the diggings, placed the Colesberg Kopje rush at Kimberley in early July 1871 [21, ch. IV, p. 22]. The regional synthesis distinguishes the much later northern Transvaal Venetia development from Kimberley [20, Fig. 1]. Free State, Namaqualand and the Transvaal have multiple distinct districts and mining dates [20, Table I and discussion following it]. An SB technology threshold represents access to a regional endowment. It can bring post-1936 deposits such as Orapa and Kao into the playable century [7, deposit register], [19, “Discovery”], [20, Table I].

## Limits and recommendation

I would keep the quantities pending a deliberate balance pass. The material implementation issue is **RES-DISC-01**. Decide whether the seven gold grants should remain immediate fields or become genuine prospecting followed by depletion. The older resource notes describe hidden reserves, while the native capacity investigation and the 1885 save agree on the capped entries [12, “Separate pre-existing finding”], [2, state-region manager], [22, RES-DISC-01]. A correction should preserve the seven budgets and thresholds, and test split ownership, construction, exhaustion and mine succession in fresh games [1, gold blocks], [22, RES-DISC-01]. Historical mineralisation and modern mine size alone cannot establish a nineteenth-century opening date.

## References

[1] Spes Bona, “Technology-gated resource potential,” working tree, 24 Nov. 2026. [Gold grants](../../common/scripted_effects/sb_resource_technology_gates_effects.txt).

[2] DP, *Suid-Afrikaanse Republiek*, 1 Oct. 1885, Victoria 3 1.15.2 checkpoint inspected 24 Nov. 2026. Rotating autosave, building and state-region managers. [Campaign file](../../../../save%20games/autosave.v3).

[3] J. Carruthers, “Mount Anderson: South Africa’s forgotten gold rush in the first decades of the 20th century situated in regional historical and geomorphological context,” *New Contree*, vol. 93, art. a906, 2026. [DOI](https://doi.org/10.4102/nc.v93i0.906).

[4] Spes Bona resource audit, “State geometry crosswalk,” 24 Aug. 2026. [Geographic proxies](../../../References/Resource%20rework/sb_full_resource_audit_2026-08-24/data/input_snapshots/state_geometry_crosswalk.csv).

[5] Spes Bona resource audit, “Proposed precious mineral technology gates,” 24 Aug. 2026. The working tree supersedes its proposed quantities. [Technology schedule](../../../References/Resource%20rework/sb_full_resource_audit_2026-08-24/data/input_snapshots/proposed_precious_mineral_technology_gates.csv).

[6] Spes Bona, “Sub-Saharan Africa state regions,” 1.15.2 working map. [Regional resource blocks](../../map_data/state_regions/04_subsaharan_africa.txt).

[7] Spes Bona, “Regional diamond surveys,” working tree. [Register and delivery](../../common/scripted_effects/sb_diamond_surveys.txt).

[8] Spes Bona, “Griqualand West effects,” working tree. [Kimberley helpers](../../common/scripted_effects/sb_griqualand_west_effects.txt).

[9] Spes Bona, “Geographic regions,” working tree. [Core regional definition](../../common/geographic_regions/sb_geographic_regions.txt).

[10] Spes Bona, “Mineral discoveries on-actions,” working tree. [Discovery callbacks](../../common/on_actions/sb_mineral_discoveries_on_actions.txt).

[11] Paradox Development Studio, *Victoria 3*, v1.15.2, building and group definitions. [Gold field and mine](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/buildings/03_mines.txt>) · [Gold fields group](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/building_groups/00_building_groups.txt>).

[12] Spes Bona, “Diamond discovery,” native capacity investigation, 18 Oct. 2026. Its native-effect evidence covers the older build. The active diamond implementation is in [7]. [Investigation](../compatibility/diamond_discovery_2026_10_18.md).

[13] Paradox Development Studio, *Victoria 3*, v1.15.2, economy defines. [Per-day discovery and depletion](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt>).

[14] Spes Bona, “Mineral discovery and Griqualand triggers,” working tree. [Kimberley eligibility](../../common/scripted_triggers/sb_mineral_discoveries_triggers.txt).

[15] Spes Bona, “Diamond survey script values,” working tree. [Probability and find size](../../common/script_values/sb_diamond_surveys.txt).

[16] Spes Bona, “Diamond Mines,” working tree. [Construction eligibility](../../common/buildings/sb_diamond_mines.txt).

[17] Mpumalanga Department of Culture, Sport and Recreation, “Pilgrims Rest,” *Mpumalanga Museums*. [Provincial museum](https://museums.mpg.gov.za/pilgrims-rest/). Accessed 24 Nov. 2026.

[18] K. Adomako-Ansah, N. Q. Hammond, Y. Morishita and D. Ishiyama, “Evolution of Auriferous Fluids in the Kraaipan-Amalia Greenstone Belts: Evidence from Mineralogical and Isotopic Constraints,” *Minerals*, vol. 14, no. 11, art. 1171, 2024. [DOI](https://doi.org/10.3390/min14111171).

[19] Debswana, “Orapa,” mine profile. [Operating history](https://www.debswana.com/orapa/). Accessed 24 Nov. 2026.

[20] W. F. McKechnie, “Diamond exploration and mining in southern Africa: Some thoughts on past, current, and possible future trends,” *Journal of the Southern African Institute of Mining and Metallurgy*, vol. 119, no. 2, 2019. [DOI](https://doi.org/10.17159/2411-9717/2019/v119n2a4).

[21] C. A. Payton, *The Diamond Diggings of South Africa: A Personal and Practical Account*. London, Horace Cox, 1872. [Digitised edition, South African History Online](https://sahistory.org.za/sites/default/files/archive-files3/the_diamond_diggings_of_south_africa.pdf).

[22] Spes Bona, *Open audit issues*, working tree, entry RES-DISC-01. [Issue register](../audit_issues_open.md).
