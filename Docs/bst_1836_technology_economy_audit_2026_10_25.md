# Basotho starting technology and economy: 1 January 1836

Research audit for DP · 25 October 2026 · SB 0.20.2 / installed Vanilla 1.14.5 / installed Community Mod Framework

## Executive summary

**BST already starts with a minimal technological package.** Its five explicitly granted technologies are identical to Vanilla: Enclosure, Standing Army, Urbanization, International Trade and Rationalism. Removing all five would confuse missing industrial institutions with missing agricultural, military and commercial capabilities. Rationalism is the strongest candidate for reconsideration, but removing it requires a deliberate replacement for the current religious-law and education assumptions.

The clearest historical problem is elsewhere: SB creates a binding British treaty on 1 January 1836 with transit rights, merchant-marine supplies and a power-bloc embassy. Missionary contact and existing African trade do not establish that diplomatic package. The available scholarship dates Moshoeshoe's British treaty to **1843**. Economic balancing also needs live employment evidence: the source contains two ranch levels and one trade centre, but their existence does not prove productive operation.

## Introduction and approach

This is a bounded audit of the authored 1836 start, not a demographic reconstruction or an implementation proposal. Country history was followed through inherited helpers, buildings, production methods, population initialisation, treaties and startup effects. CMF was checked for relevant overrides; Vanilla is the engine-version comparator. Hail Columbia's bespoke Cherokee literacy and Gates of the Bosphorus's tier-six native starts were consulted as implementation examples, not evidence about Basotho society.

Historical routes were independent: Casalis's missionary account; a recent scholarly trade history; research using Morija mission archives; and an environmental historian's university-hosted manuscript. Relevant full-text sections were inspected. Dates and retrospective scope matter more here than apparent precision. No game was launched, no save was inspected and no gameplay files were changed.

In Victoria 3, technologies are bundles of permissions and modifiers. Their European labels need not describe the historical institution literally. A building level is an employment and production capacity; production methods determine its labour and goods requirements. Subsistence buildings also represent agriculture and household manufacture. Consequently, neither “no industrial building” nor “no commercial crop farm” means an absence of productive knowledge.

## Findings: effective scripted baseline

SB [BST country history, lines 10–34][bst] calls the native tier-six technology helper, then adds International Trade and Rationalism. The [native helper, lines 132–141][tech-helper] grants only Enclosure, Standing Army and Urbanization; no relevant SB/CMF replacement was found. [Vanilla BST, lines 3–14][vanilla-bst] has the same five grants. No additional BST technology grant was found in the inspected startup chain. These are the resolved **scripted grants**: a fresh save remains necessary to verify engine handling, including whether prerequisite technologies are silently supplied. International Trade names `tech_bureaucracy` as a prerequisite; this audit does not silently count it as researched.

| Technology | Actual relevant function | Assessment for 1836 |
|---|---|---|
| Enclosure | Enables commercial agricultural buildings, including the authored ranches; [ranch definition, 133–158][ranch-def]. | **Retain**, high confidence as a game capability. It does not prove English enclosure or private freehold existed. |
| Standing Army | Barracks gate; also enables cavalry. [Military technology, 3–12][mil-tech]. | **Retain**, medium-high confidence. The name overstates professionalisation, but the chiefly levy and irregular units carry that distinction. |
| Urbanization | Population-based infrastructure +2, its cap +40, construction-sector cap +10 and weekly construction-progress cap +10; gates urban centres/construction sectors. [Society technologies, 3–19][soc-tech]. | **Retain**, medium confidence as settlement/construction access, not a claim of industrial cities. |
| International Trade | Required by active Mercantilism; [trade laws, 5–18][trade-law]. A trade centre has no direct technology gate: its normal construction condition excludes Isolationism. [Building, 236–263][trade-building]; [trigger, 34–40][trade-trigger]. | **Retain**, high confidence for external exchange; scrutinise the actual trade infrastructure and treaty separately. |
| Rationalism | School institution maximum +1 and `state_education_access_wealth_add = 0.01`; [technology, 42–56][rationalism]. Required by Freedom of Conscience and Religious Schools. [Religious law, 353–394][religion-law]; [education law, 43–45][school-law]. | **Conditionally retain pending replacement**, medium confidence. Missionary presence supports contact and small-scale instruction, not nationwide Enlightenment institutions. |

The [traditional-politics helper, 74–115][politics] supplies monarchy/autocracy, hereditary bureaucracy, Mercantilism, Serfdom, Guild System, Closed Borders and other baseline laws. BST explicitly substitutes Freedom of Conscience, Legacy Slavery and SB's Chiefly Levy, while keeping Traditionalism and Land-Based Taxation. No school institution is authored. These labels are coarse models of authority and labour relations, not demonstrations of European feudal tenure. Chiefly Levy restricts conscription to peasants and permits large mobilisation; its [definition, 4–19][chiefly-law] therefore matters more to military character than the Standing Army label alone.

| Economic component | SB authored start and comparison | Important qualification |
|---|---|---|
| Commercial buildings | One ranch in BST Vrystaat; Drakensberg has one ranch and one trade centre. [History, 2508–2523][vrystaat-buildings] and [2812–2864][drakensberg-buildings]. Vanilla has four ranch and five barracks levels across its different BST state allocation: [2398–2423][vanilla-zul-buildings], [2478–2503][vanilla-vry-buildings]. | SB is already substantially smaller. Different borders prevent a simple like-for-like productivity comparison. |
| Production methods | Both ranches use open-air stockyards, simple ranching, standard fences and no refrigeration; trade centre uses normal trade. | Per fully staffed ranch: 4,000 labourers +1,000 farmers, meat 10 and fabric 5. [PMs, 457–465 and 505–517][ranch-pms]. These are capacity coefficients, not observed output. |
| Trade employment/input | Per level: 800 clerks +200 shopkeepers; normal trade consumes merchant marine 4. [PMs, 345–362 and 409–418][trade-pms]. | Qualification shortages or input/connectivity failures can make a present building ineffective. |
| Subsistence and land | Both regions use subsistence farms. Drakensberg has eight arable levels; Vrystaat's 56 belong to the whole region, of which BST owns only a portion. [Map, 1257–1276][vrystaat-map], [1457–1477][drakensberg-map]. | Subsistence supplies grain, fabric, wood and services, with household clothing/furniture/liquor PMs. [PMs, 1–46][subsistence]. No separate crop farm does not erase cultivation. |
| Forces | One barracks level and six conscription-centre levels in Drakensberg; no-organisation and customary-muster PMs respectively. | Levels do not establish employed soldiers or deployed battalions. Default irregular infantry has no small-arms goods upkeep: [unit, 10–25][irregular]. |
| Authored pop sizes | SB: Sotho 10,030 in Vrystaat; Sotho 26,514 and San slaves 1,521 in Drakensberg: **38,065 summed `size` units**. [Pops, 3053–3059][vry-pops], [3408–3421][drak-pops]. Vanilla's corresponding authored BST sum is 135,096. [Pops, 3058–3068][vanilla-zul-pops], [3110–3115][vanilla-vry-pops]. | These are **not verified engine population, workforce or dependants totals**. No historical population conclusion follows from the sum. |

No university, industrial factory, government administration, construction sector or commercial crop farm is authored in these BST building blocks. Their absence supports a very limited formal economy; it does not imply that political administration, building work, weaving or farming were absent from Basotho life.

The inherited [BST population file, 1–7][population-init] applies low wealth and baseline literacy. The latter begins at 5%, then adds profession/stratum increments and halves literacy in unincorporated states: [helper, 292–336][literacy]. It is not a uniform 5% national literacy claim. Low wealth likewise assigns different values by class/profession, rather than a national income. Clerks' qualification growth depends on literacy and includes a severe peasant penalty under Serfdom: [pop type, 51–77][clerks]. A small trading workforce can therefore be a stronger constraint than the technology list.

The proposed Basotho highland-agriculture startup modifier is entirely commented out: [startup, 141–149][inactive-agriculture]. The active Highveld grasslands trait gives infrastructure +15 and ranch throughput +5% in Vrystaat; [trait, 88–95][highveld] and [assignment, 30–34][trait-start]. Neither proves ranch employment. Moshoeshoe's Innovative trait adds 10% technology spread, not research innovation: [character, 750–772][moshoeshoe] and [native trait, 697–712][innovative].

## Historical calibration

Casalis describes skilled metalworking, well-made hoes, deliberate soil choice, fallowing, crop timing and grain storage. His observations support an economy with specialised craft and agricultural knowledge. They do not require an industrial steelworks, mechanised tools industry or commercial wheat estate. His 1861 account covers decades, however: statements about recently adopted wheat or substantial exports cannot be assigned automatically to January 1836. Its missionary and racial judgements also require critical reading. [1](https://archive.org/details/basutosortwentyt00casa)

The recent trade synthesis identifies pre-existing exchange in iron implements, copper goods, livestock, skins and other products. It places mission arrival in 1833, records failure of the first missionary wheat crop in 1835, and distinguishes expanding wheat trade in the 1840s from later commercial development. This supports retaining exchange capability and subsistence cultivation while avoiding a mature export-grain economy at start. Its later trading quantities are not 1836 calibration data. [2](https://doi.org/10.4102/aosis.2025.bk536.02)

Morija was founded in July 1833; schooling followed that year. This gives SB's Rationalism comment a real historical anchor. It does not establish a national literate workforce or a funded education institution. The same research stresses the mismatch between chiefly allocation of land for use and missionaries' assumptions about exclusive ownership. [3](https://doi.org/10.25159/2412-4265/6773) Casalis's early account of preparing translated lessons reinforces the small, developing character of this educational work. [1](https://archive.org/details/basutosortwentyt00casa)

**Rationalism should therefore be judged by its effects.** Religious toleration can be a defensible representation of Moshoeshoe's accommodation of missionaries without implying mass conversion or philosophical uniformity. The present technology is the game's gate to that law, but its wealth-based education bonus applies more broadly. A future design could separate toleration, modest local missionary education and general research capacity. Simply deleting Rationalism while leaving Freedom of Conscience in history would create an unresolved prerequisite inconsistency; it would also affect future Religious Schools eligibility and schooling capacity.

Horses were being acquired from the early 1830s, with further acquisitions in 1835–40. Swart's manuscript places widespread mounted society and horse exports substantially later. Early adaptation is therefore credible; the later Basotho mounted military reputation is not a ready-made 1836 baseline. [4](https://academic.sun.ac.za/history/downloads/swart/race_horses.pdf)

SB already models partial firearm adoption separately. The [JE immediate block, 54–102][firearms-je] seeds BST through [the helper, 75–99][firearms-seed]: treaty progress 9.6, industry zero. Multiplication by 2.5 produces 24 on the 60-point bar, **40% game progress**, not evidence that 40% of warriors possessed firearms. [Calculation, 279–357][firearms-calc]. The corresponding [tier-24 modifier, 245–253][firearms-penalty] still imposes substantial combat and military-research penalties. The precise fraction lacks historical validation in the material inspected. Retain partial adaptation provisionally; defer its numerical calibration. Completion needs a qualifying import treaty or industry and removes penalties; it does not itself grant a technology. [JE, 110–164][firearms-monthly].

## Discussion: the treaty is the strongest mismatch

SB's own [treaty history, 6–35][british-treaty] unconditionally creates a non-draft, 25-year GBR–BST agreement dated 1836.1.1: British transit provision, ten merchant-marine units supplied to BST, and a British power-bloc embassy hosted by BST. Lines 37–52 separately create PHL–BST transit rights. This is an SB addition: no BST treaty was found in installed Vanilla treaty history, and CMF has no corresponding treaty-history directory.

Normal negotiation of both [transit rights, 24–26][transit-article] and [embassies, 22–28][embassy-article] requires International Relations; the embassy also adds treaty leverage. Their history creation is not evidence that BST has researched that additional technology. SB's [goods-transfer article, 13–22][goods-article] requires International Trade and assigns maintenance to the source country. This is a further dependency to check before any technology removal.

The mission-history study dates Moshoeshoe's British treaty to **1843**, not 1836. [3](https://doi.org/10.25159/2412-4265/6773) Ordinary exchange and missionary access do not substantiate a British embassy and guaranteed maritime supply seven years earlier. The package may solve a landlocked trade mechanic, but that is a gameplay rationale requiring explicit acknowledgement. Replace or defer the formal British arrangement; preserve necessary commercial access through a historically narrower design. Removing it without checking merchant-marine availability, route connectivity and trade-centre employment could inadvertently disable the intended economy. Its merchant-marine transfer is not a firearms-import treaty.

## Recommendations and dependencies

| Priority | Decision | Confidence and condition |
|---|---|---|
| 1 | **Replace/defer** the 1836 British treaty and embassy package. | High confidence that current dating is unsupported; medium on the best mechanical replacement. Verify trade connectivity and input supply before implementing. |
| 2 | **Retain** Enclosure, Standing Army, Urbanization and International Trade. | High confidence in capability/dependency reasoning. Their removal would affect ranches, barracks/cavalry, construction/urban centres or Mercantilism, without better representing indigenous knowledge. |
| 3 | **Replace eventually; retain provisionally** Rationalism's bundled representation. | Medium confidence. Couple any removal to religious-law eligibility and deliberately calibrated education; do not infer national literacy from mission arrival. |
| 4 | **Retain provisionally** the small ranch/subsistence economy and partial firearm adoption; **defer** exact levels/progress. | Historical direction is plausible; employment, firearms prevalence and sustainable revenue remain unmeasured. Review crop options separately: generic subsistence grain can cover staples, while maize-only commercial options deserve a sorghum/millet check. |
| 5 | **Defer** population, slavery-share and army-size reductions until observed results exist. | High confidence in the need for evidence. Conditional AI war helpers can restore a 14-level conscription floor despite six authored levels: [effect, 62–108][force-effect], [values, 22–36][force-values]. |

## Limitations and playtest evidence needed

This audit establishes source instructions and historical plausibility, not engine success. Capture a fresh 1 January start and the first ordinary economic ticks: researched technologies; population/workforce/dependants separately; literacy by profession; actual subsistence levels; ranch/trade-centre employment and vacancies; qualifications; merchant-marine supply; market access; goods balances; treasury; and deployed versus potential troops. GDP, productivity and living standards should be reported from that save, never manufactured from building counts or source pop sizes.

The full texts consulted remain selective evidence. Casalis retrospectively covers 23 years; the trade chapter synthesises earlier scholarship; the mission article has an explicit theological perspective; Swart was consulted in author-manuscript pagination. The specialist Atmore–Sanders firearms article was accessible only as a publisher extract, so it supplies no quantitative 1836 claim here. [5](https://doi.org/10.1017/S0021853700011130) The evidence supports targeted corrections, not a universal ranking of societies on a technology ladder.

## References

[1] E. Casalis, *The Basutos; or, Twenty-three Years in South Africa*. London: James Nisbet & Co., 1861, especially pp. 58–59, 131–133 and 163–170. [Public-domain digitisation and full text](https://archive.org/details/basutosortwentyt00casa). Original edition predates ISBNs; title, publisher and year checked against [CiNii bibliographic record](https://cir.nii.ac.jp/crid/1971430859817552586). Relevant full-text sections consulted, not a contemporaneous 1836 census.

[2] N. E. Attah and S. Maliehe, “A history of international trade in Lesotho,” in *A Compendium on International Trade in Lesotho*, D. N. Yuni and T. Tsietsi, Eds. Cape Town: AOSIS Books, 2025, pp. 15–30, especially pp. 19–22. DOI: [10.4102/aosis.2025.bk536.02](https://doi.org/10.4102/aosis.2025.bk536.02). [Publisher record](https://books.aosis.co.za/index.php/ob/catalog/book/536); [open full volume](https://books.aosis.co.za/index.php/ob/catalog/view/536/839/10714-1). Chapter metadata and DOI verified in the downloaded publisher PDF.

[3] N. S. K. Tseuoa, “Church and Land in Basutoland: The Paris Evangelical Mission and its Implications,” *Studia Historiae Ecclesiasticae*, vol. 46, no. 2, pp. 1–16, 2020. DOI: [10.25159/2412-4265/6773](https://doi.org/10.25159/2412-4265/6773). [Open article](https://www.scielo.org.za/scielo.php?pid=S1017-04992020000200008&script=sci_arttext). Full text inspected, including mission establishment, land-use arrangements and the 1843 treaty.

[4] S. Swart, “‘Race’ horses—horses and social dynamics in post-Apartheid Southern Africa,” in *Under Construction: Race and Identity in South Africa Today*, N. Distiller and M. Steyn, Eds. Heinemann, 2004, pp. 13–24. Consulted version: [university-hosted author manuscript](https://academic.sun.ac.za/history/downloads/swart/race_horses.pdf), titled “‘Race’ horses—a discussion of horses and social dynamics in post-Apartheid Southern Africa,” especially manuscript pp. 9–10. Publication identity/year/pages verified in the author's [university CV, p. 5](https://academic.sun.ac.za/history/cv/swart.pdf?page=swart). No DOI verified; manuscript pagination is not published pagination.

[5] A. Atmore and P. Sanders, “Sotho Arms and Ammunition in the Nineteenth Century,” *The Journal of African History*, vol. 12, no. 4, pp. 535–544, 1971. DOI: [10.1017/S0021853700011130](https://doi.org/10.1017/S0021853700011130). [Publisher record/extract](https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/sotho-arms-and-ammunition-in-the-nineteenth-century1/DCCBA048A77FAED986FE50DA54BD4D07). Bibliographic metadata verified; full article inaccessible in this audit and not treated as inspected evidence.

Local primary evidence below refers to the working files inspected on 25 October 2026; line anchors may move with later edits.

[bst]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/countries/bst - basuto.txt:10>
[tech-helper]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_inventions.txt:132>
[vanilla-bst]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/countries/bst - basuto.txt:3>
[ranch-def]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/buildings/02_agro.txt:133>
[mil-tech]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/20_military.txt:3>
[soc-tech]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/30_society.txt:3>
[trade-law]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/laws/01_trade_policy.txt:5>
[trade-building]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/buildings/11_private_infrastructure.txt:236>
[trade-trigger]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_building_triggers.txt:34>
[rationalism]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/30_society.txt:42>
[religion-law]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/laws/00_church_and_state.txt:353>
[school-law]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/laws/01_education_system.txt:43>
[politics]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_political_setup.txt:74>
[chiefly-law]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/laws/04_sb_chiefly_levy.txt:4>
[vrystaat-buildings]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/buildings/04_subsaharan_africa.txt:2508>
[drakensberg-buildings]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/buildings/04_subsaharan_africa.txt:2812>
[vanilla-zul-buildings]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/buildings/04_subsaharan_africa.txt:2398>
[vanilla-vry-buildings]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/buildings/04_subsaharan_africa.txt:2478>
[ranch-pms]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/production_methods/02_agro.txt:457>
[trade-pms]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/production_methods/11_private_infrastructure.txt:345>
[vrystaat-map]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/map_data/state_regions/04_subsaharan_africa.txt:1257>
[drakensberg-map]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/map_data/state_regions/04_subsaharan_africa.txt:1457>
[subsistence]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/production_methods/12_subsistence.txt:1>
[irregular]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/combat_unit_types/00_land_combat_unit_types.txt:10>
[vry-pops]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/pops/04_subsaharan_africa.txt:3053>
[drak-pops]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/pops/04_subsaharan_africa.txt:3408>
[vanilla-zul-pops]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/pops/04_subsaharan_africa.txt:3058>
[vanilla-vry-pops]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/pops/04_subsaharan_africa.txt:3110>
[population-init]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/population/bst - basuto.txt:1>
[literacy]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_literacy.txt:292>
[clerks]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/pop_types/clerks.txt:51>
[inactive-agriculture]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/on_actions/sb_startup_on_action_handlers.txt:141>
[highveld]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/state_traits/sb_state_traits.txt:88>
[trait-start]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/global/sb_state_traits.txt:30>
[moshoeshoe]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/character_templates/sb_southern_africa_character_template_overrides.txt:750>
[innovative]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_traits/personality_traits.txt:697>
[firearms-je]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/journal_entries/1-04_sb_firearms_acquisition.txt:54>
[firearms-seed]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/scripted_effects/sb_firearms_effects.txt:75>
[firearms-calc]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/scripted_effects/sb_firearms_effects.txt:279>
[firearms-penalty]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/static_modifiers/sb_firearms_modifiers.txt:245>
[firearms-monthly]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/journal_entries/1-04_sb_firearms_acquisition.txt:110>
[british-treaty]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/treaties/sb_treaties.txt:6>
[transit-article]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/24_transit_rights.txt:24>
[embassy-article]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/treaty_articles/10_host_power_bloc_embassy.txt:22>
[goods-article]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/treaty_articles/13_goods_transfer.txt:13>
[force-effect]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/scripted_effects/sb_frontier_force_effects.txt:62>
[force-values]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/script_values/sb_frontier_force_values.txt:22>
