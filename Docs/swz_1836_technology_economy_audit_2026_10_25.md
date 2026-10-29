# Swazi technology and economy on 1 January 1836: source and historical audit

**25 October 2026 — research only; no gameplay, configuration or test changes.**

## Executive summary

**SWZ does not start with an industrial technology package. Retain its four explicitly authored technologies provisionally, and scrutinise the economic and military abstractions around them before deleting technologies.** SB grants Enclosure, Standing Army, Urbanization and International Trade, exactly the explicit Vanilla package. It authors one maize-farm level and two livestock-ranch levels, predominantly basic production methods, and a small irregular formation. Neither authored building capacity nor a researched technology establishes employed production, GDP or a functioning overseas trade connection.

Sobhuza's polity combined agricultural production, cattle wealth, coercive extraction, military organisation and exchange. Its institutions were still developing; the stronger territorial administration associated with Mswati must not be projected backwards. Bonner's reconstruction particularly distinguishes Sobhuza's conquest arrangements from subsequent consolidation. [[1, pp. 8–10]](https://hdl.handle.net/10539/8432) Limited exchange with Delagoa Bay supports trade capability, but not an industrial economy or widespread firearm adoption. [[2, p. 33 preview]](https://www.jstor.org/stable/j.ctt8171d)

The highest-value review targets are the inherited occupational literacy rates, the unsupported precision of 2,500 Tsonga slaves, and SB's additional pre-firearms penalties. The current evidence does **not** support replacing the entire package with “no technology”.

## Introduction

This audit concerns the playable **SWZ country and its owned East Transvaal slice on 1 January 1836**, under Sobhuza, rather than every community later included within Eswatini or the wider nineteenth-century Swazi sphere. “Technology” means a Victoria 3 unlock and modifier package. “Industrial” means production organised around the game's manufacturing, mining, machinery and associated institutions; it is not a synonym for intelligent, skilled or politically organised.

The baseline is the live SB checkout declaring version **0.20.2**, installed Vanilla **1.14.5**, and the installed Community Mod Framework. The source analysis follows country history, shared helpers, population and building history, production methods, and the opening firearms journal. A search of CMF's `common` tree found no SWZ history, starting-technology-helper or population-helper replacement. No game was launched and no fresh SWZ save was inspected.

## Research approach

This was a targeted English-language review on 25 October 2026, not a systematic review. Independent discovery routes were scholarly publisher/repository records (Cambridge Core, Wits WIReDSpace, SOAS, UEA, JSTOR and SciELO) and primary-source/library collections (Smithsonian, Internet Archive and UCT's Five Hundred Year Archive). Searches combined **Sobhuza/Ngwane/Swazi**, **1830s/1836**, and **cattle, agriculture, iron, trade, military organisation, literacy**. Bibliographies and publisher chapter links supplied follow-up leads.

Gardiner's public-domain 1836 text and Bonner's Wits seminar paper were downloaded through their public repositories and read directly. Gardiner's report was checked against Bonner's criticism, rather than accepted as a census. Bonner's paper is explicitly provisional and requests permission for quotation; it is paraphrased here, without quotations. The Cambridge chapter summary, Crush's displayed opening chapter excerpt and Moffett et al.'s repository abstract have narrower evidentiary uses, identified below. The SOAS thesis text could not be retrieved; no detailed claim relies on it. Earlier SB research notes were discovery leads, not independent historical authority.

## Findings and evidence synthesis

### 1. Effective source setup and Vanilla comparison

The following are **authored inputs or source-derived expectations**, not measurements from a settled game economy. Linked lines are the inspected checkout's line numbers.

| Component | SB source finding | Vanilla comparison / verification limit |
|---|---|---|
| Country and technology | [SWZ history, lines 10–32][S1], calls tier 6 then adds `international_trade`; [native helper, lines 132–141][S2], grants `enclosure`, `standing_army`, `urbanization`. | [Vanilla SWZ, lines 2–10][S3], grants the same package. These are four **explicit grants**. [Trade's native prerequisite, lines 142–151][S33], is `tech_bureaucracy`; this audit does not assume whether the engine automatically completes prerequisites. Check the completed-research list in a fresh save. |
| Constitutional/economic laws | Traditional helper supplies State Religion, Autocracy, Hereditary Bureaucrats, Subjecthood, Traditionalism, Right of Assembly, Closed Borders, Guild System, Monarchy, Mercantilism, Serfdom, Land-Based Taxation and No Workers' Rights for this unrecognised country; SB substitutes Amabutho for Peasant Levies and explicitly activates Legacy Slavery. [Helper, lines 74–115][S4]; [SWZ, lines 20–32][S1]. | Vanilla uses Peasant Levies and Slave Trade. Closed Borders is the migration law; it does not make the trade policy Isolationism. Unmentioned law groups should be checked in the fresh start rather than inferred from this helper. |
| Agriculture and ownership | [Building history, lines 2780–2808][S5], purges selected inherited buildings, then requests **1 maize farm** and **2 livestock ranch levels**, with manor-house ownership; each creation uses `reserves = 1`. | [Vanilla, lines 2548–2585][S6], has 1 millet farm, 2 ranch levels and 2 barrack levels. SB's farm change is a crop/building substitution, not a demonstrated productivity increase. Ownership levels are not a count of historical estates. |
| Production methods | Farm: simple farming, no secondary crop, tools disabled. Ranch: open-air stockyards, simple ranch, standard fences, unrefrigerated. [SB history][S5]. | Native base PMs have no industrial input requirement. “Tools disabled” means no additional game-goods tools input, not that cultivators had no hoes. [Agro PMs, lines 1–14, 167–169, 457–465, 505–517, 587–589, 626–628][S7]. |
| Subsistence and territory | State region uses `building_subsistence_farm`, **35 arable land region-wide**, malaria, and agricultural/resource potentials. SWZ owns seven of the region's twenty authored provinces. [Region, lines 1480–1496][S8]; [ownership, lines 9152–9182][S9]. | Do not give SWZ all 35 arable land, all regional mine capacity, or assume proportional allocation by province count. Its generated subsistence levels and allocated capacities require a save. No producing mine is authored here. |
| Population | After clearing existing pops, the authored `create_pop.size` inputs are **47,500 for Swazi** and **2,500 for Tsonga slaves**: a sum of **50,000**, with the latter 5% of that input total. [Pops, lines 3350–3360][S10]. | [Vanilla, lines 3161–3165][S11], authors `size = 64396` for Nguni without an explicit slave pop. These inputs are neither observed engine inhabitants nor an established historical census. |
| Wealth and literacy | SB retains [native population history, lines 1–5][S12]: low wealth and baseline literacy. The literacy helper sets 5%, adds 45 percentage points for bureaucrats/academics/clergymen/engineers, 15 for upper strata, and 5 for clerks/shopkeepers; an unincorporated-state multiplier halves the result. [Helper, lines 292–336][S13]. | These are occupation-dependent inputs, **not a verified national literacy rate**. Low-wealth settings yield, for example, peasants 7, labourers 8, middle strata 17, upper strata 25 and slaves 1, before subsequent economic adjustment. [Wealth helper, lines 120–168][S14]. |
| Military | [Formation history, lines 97–115][S15], creates `swazi_emabutfo`: **1 regular irregular-infantry unit and 4 conscript irregular-infantry units**. | Do not add Vanilla's two barracks to that formation. Actual staffing, supporting buildings and mobilised conscripts are runtime questions. Later AI wartime force-floor repairs are conditional, not extra peacetime starting troops. [Repair, lines 62–104][S16]. |

The three agricultural levels imply **15,000 full-staffing jobs** under the native PM definitions: 4,000 labourers and 1,000 farmers per level, before ownership and military employment. That is a capacity calculation, not evidence that 15,000 people are working there. The **50,000 sum of authored `create_pop.size` inputs** does not establish the engine's total inhabitants or available workforce; those runtime quantities are needed before judging whether this job capacity can be staffed. Serfdom also reserves incorporated subsistence capacity/employment and multiplies peasants' farmer-qualification growth by 0.2. [Land law, lines 51–57][S17]; [farmers, lines 75–103][S18]. Agriculture can therefore be limited by labour and institutions even when its technology is present.

Subsistence supplies grain, fabric, wood and services; its home-workshop method supplies clothes, furniture and liquor, while its Serfdom method adds grain and subsistence output. [Subsistence PMs, lines 1–45 and 132–145][S19]. Consequently, “no textile mill”, “no logging camp” or “no food industry” does not mean no clothing, fuel, woodwork or food processing. Conversely, these abstract outputs are not an inventory of Swazi crafts.

### 2. What the historical evidence supports

Gardiner recorded a conversation in 1835 with Umkolwani and other Ngwane visitors at the Zulu court. It describes iron obtained from eastern neighbours for spearheads and unfamiliarity with guns among those visitors. It also alleges tiny population, almost no cultivation and loss of all cattle. These are translated, politically situated reports, not Gardiner's inspection of Swazi production; his missionary judgements further complicate interpretation. [[3, pp. 167–171]](https://library.si.edu/digital-library/book/narrativeofjourn00gard) Bonner explicitly disputes the demographic compression and distinguishes the conquest zone from more extensive southern settlement. His reconstruction locates much of the later administrative and regimental systematisation under Mswati. [[1, pp. 8–10]](https://hdl.handle.net/10539/8432)

**The practical inference is to retain a cereal-and-cattle economy while treating its exact scale as uncertain.** Gardiner's alarming description cannot justify deleting cattle husbandry or farming country-wide. Neither the consulted passages nor SB's comments establish the exact maize-to-sorghum/millet balance or two commercial ranch equivalents. A maize building may be a workable representation of cereal cultivation; it is not proof of maize monoculture, fencing or production mainly for sale.

Crush's chapter opening describes limited pre-mid-century trade in iron goods and calico with the Portuguese, followed later by hunters and traders exchanging cattle, ivory and skins for horses and guns. Only that displayed opening was available. [[2, p. 33 preview]](https://www.jstor.org/stable/j.ctt8171d) It supports keeping access to exchange while rejecting automatic inference of widespread 1836 firearms, a large trade centre, or domestic gun manufacture. The claimed **1834 blockade** in SB's comment was not independently established by the accessible passages; treat that date as awaiting a pinpoint source.

Regional archaeological work identifies iron-bladed hoes as significant agricultural tools, traded objects and stores of value before industrial copies spread. Its repository abstract supports that regional proposition, not an 1836 Swazi furnace count. [[4, abstract]](https://doi.org/10.1007/s10437-017-9247-1) The sound distinction is **iron use and specialist metal skills versus the game's industrial tooling and shaft-mining packages**. Imported iron also does not establish that all smithing was imported. No consulted source establishes the industrial production system that would justify a blanket Manufacturies or Shaft Mining grant.

The literacy baseline is substantially harder to defend as history. Van Wyngaard places the Allison/Giddy mission and its reading-and-writing classes in **1844**. His article is a church-history synthesis; its early chronology relies on earlier works and is not a literacy survey. [[5, “The first missionaries in Swaziland”]](https://doi.org/10.4102/hts.v74i1.4785) This does not prove that every person was unable to read in 1836. It does mean that 5% for ordinary occupations, 20% for upper strata and 50% for indigenous religious specialists cannot be treated as measured historical values. Oral political, religious and technical expertise must be distinguished from alphabetic literacy.

SB allocates 95% of its summed `create_pop.size` inputs to `swazi`, compressing a changing political identity. Bonner's published chapter summary describes Sobhuza incorporating Sotho, Tsonga and Nguni chiefdoms into the reconstructed polity. [[6, chapter summary]](https://doi.org/10.1017/cbo9780511563027.006) That supports heterogeneity, but supplies no proportions for SB's particular slice. **No inspected source establishes that exactly 2,500 Tsonga people there were chattel slaves.** Captivity, tributary subordination and the game's slave profession require separate evidence. The history comment itself mentions avoiding later demographic effects: that is a gameplay rationale, not historical verification.

### 3. Technology labels and the additional SB penalty

| Package | Actual material dependency | Assessment for SWZ |
|---|---|---|
| Enclosure | Farms and ranches require it. [Building definitions, lines 81–149][S20]. Native flavour describes private enclosed fields. [Localisation, line 416][S21]. | **Retain provisionally.** The flavour fits imperfectly, but removing the unlock removes a useful way to represent productive agriculture. Do not infer private freehold from the tech. |
| Standing Army | Enables barracks. [Technology, lines 3–12][S22]. | **Retain provisionally** for organised armed service; Amabutho and the regular/conscript mix describe the institution more closely. This is not evidence of a modern salaried standing army. |
| Urbanization | Adds population infrastructure, construction-sector capacity and weekly construction allowance. [Technology, lines 3–19][S23]. | **Retain pending a dependency-aware alternative.** Removing it is a transport/construction nerf as well as a statement about urban settlement. |
| International Trade | Is the installed Mercantilism prerequisite. [Trade law, lines 5–23][S24]. The current trade-centre building has **no technology gate**: government/private construction calls `trade_center_construction_allowed`, whose conditions concern trade laws. [Building, lines 236–263][S34]; [construction trigger, lines 1–41][S35]. The technology's “Unlocks Trade Center” comment is stale. | **Retain.** Limited exchange is compatible with weak market integration. An external obstruction is not voluntary Isolationism. No operating trade route follows merely from ownership of this tech. |
| Manufacturies, Shaft Mining, Military Drill and later industrial/military technologies | Not explicitly granted; mining and manufacturing unlocks are broader than individual metalworking skills. | **Do not add on the evidence reviewed.** Military Drill additionally gates Professional Army in SB. [Army override, lines 128–143][S25]. |

The opening firearms journal is a material departure from Vanilla. It seeds SWZ at **zero** import and industry progress, then applies the base weapons modifier. [JE, lines 54–102][S26]; [seed effect, lines 75–99][S27]. That modifier supplies **−50% offence/defence, −0.75 additive kill/recovery rates, −50% military wages, and −25% military technology research speed**. [Modifier, lines 5–12][S28]. The additive rate fields must not be reported as simple percentage reductions to final battle outcomes.

Limited firearm access supports an adoption challenge; it does not independently establish all these values. In particular, general recovery, military learning and wage reductions do not follow automatically from spear armament. Balance should assess this package alongside irregular-unit statistics and the law, avoiding repeated penalties for the same limitation. Amabutho already adds 0.30 conscription rate, changes dependent wages and military experience/morale, and strengthens aristocrats/officers. [Law, lines 5–22][S29]. Ordinary army-law reform is also locked behind firearms completion. [Reform trigger, lines 1–9][S30]. These are substantive gameplay dependencies, not historical measurements.

## Discussion and implications

“Closer to ancient than industrial” is useful only as a narrowly specified comparison of productive resources. A household farming economy using cattle, human labour and iron implements differs materially from a steam-powered industrial economy. It does not follow that it lacked agriculture, exchange, technical specialisation or institutions, nor that its politics reproduced a particular ancient society. The game has no single archaeological-age variable: its technologies bundle concrete capabilities with broad European historical labels.

The most defensible approach is therefore **capability by capability**: retain productive cultivation and exchange, constrain industrial production and firearm adoption, and avoid equating low literacy with absent knowledge. A historical correction to literacy also needs a qualifications review: native engineer growth requires literacy above 20% and excludes peasants under Serfdom; officer growth also interacts with literacy, status and occupation. [Engineers, lines 52–68][S31]; [officers, lines 39–68][S32]. An unexamined zero-literacy change could disable advancement for reasons unrelated to the intended history.

## Limitations and evidence gaps

The review does not establish GDP, household consumption, effective market access, employed outputs, treasury, average literacy, exact arable allocation or actual battalion manpower. It does not certify an historical total population, slave percentage, crop mix or commercial herd size. Bonner's two consulted texts are not independent corroborating historians; Gardiner is a mediated contemporary report, and the archaeological abstract concerns a wider region. Crush's full book and Bonner's SOAS thesis were inaccessible through the available routes. These limits favour bounded recommendations over precise replacement numbers.

## Recommendations

| Priority / decision | Proposed action | Confidence and implementation condition |
|---|---|---|
| 1 — **Retain** | Keep the four explicit tech grants and the absence of industrial/mining/firearm upgrades for this iteration. | **Medium–high.** Verify the engine's completed-tech list, especially Trade's prerequisite handling. Audit unlocks before any later removal. |
| 1 — **Replace after review** | Replace the generic occupational literacy profile with an explicitly justified SWZ starting profile. Treat religious and practical expertise separately from reading. | **High** that present percentages lack demonstrated support; **low** for any exact substitute. Check officer/farmer qualifications, hiring and attainable reform first. |
| 1 — **Defer numerical claims** | Label the summed 50,000 `create_pop.size` input and its 2,500 Tsonga-slave component as calibration assumptions; commission focused evidence for status, geography and proportion before revising them. | **High** that the current exact values are unverified. Do not replace them with a guessed zero or make later slave-raiding evidence prove 1836 prevalence. |
| 2 — **Retain provisionally** | Keep basic cereal/cattle production and subsistence. Defer crop-type and level changes until employment and crop evidence are available. | **Medium** for the economic mix; **low** for exact levels. Do not infer industrial productivity from ownership levels or all regional resources. |
| 2 — **Review / remove unsupported justification** | Review the firearms penalty's research-speed, recovery and wage components individually; retain the distinction between imported guns and domestic industry. | **High** that historical evidence does not quantify these values; **low** for a replacement balance. Test survivability and reform access without presuming that a universal technology downgrade improves fidelity. |
| 3 — **Verify in DP's playtest** | Capture the opening tech list, active laws/modifiers, population by occupation/literacy, subsistence and agricultural employment, goods output, market access and regular/conscript staffing. | Compare the same fresh setup before economic changes. An employed-output and qualifications check is more decision-useful than a speculative GDP estimate. |

## References

[1] P. L. Bonner, “Classes, the mode of production and the State in pre-colonial Swaziland,” African Studies Institute Seminar Paper no. 046, University of the Witwatersrand, Johannesburg, Sep. 13, 1976. [Repository record](https://hdl.handle.net/10539/8432); [institutional PDF](https://wiredspace.wits.ac.za/bitstreams/8d33c1c7-0b9f-459d-895a-0dfacc204d25/download). Full paper consulted; provisional argument; no direct quotation used.

[2] J. Crush, *Struggle for Swazi Labour, 1890–1920*. Montreal: McGill-Queen's University Press, 1987. Electronic ed., ISBN 978-0-7735-6118-2, doi: [10.1515/9780773561182](https://doi.org/10.1515/9780773561182). [JSTOR record and displayed chapter opening](https://www.jstor.org/stable/j.ctt8171d), ch. 2, pp. 33–48. Only the displayed opening excerpt, not the whole chapter, consulted. Metadata checked against the publisher's distribution record.

[3] A. F. Gardiner, *Narrative of a Journey to the Zoolu Country, in South Africa*, 1st ed. London: William Crofts, 1836. [Smithsonian catalogue and digitisation](https://library.si.edu/digital-library/book/narrativeofjourn00gard); [public-domain text](https://archive.org/download/narrativeofjourn00gard/narrativeofjourn00gard_djvu.txt). Relevant printed pp. 167–171 inspected in the digitised text. No ISBN assigned to this edition.

[4] A. J. Moffett, T. Maggs and J. van Schalkwyk, “Breaking ground: Hoes in precolonial South Africa—Typology, medium of exchange and symbolic value,” *African Archaeological Review*, vol. 34, pp. 1–20, 2017, doi: [10.1007/s10437-017-9247-1](https://doi.org/10.1007/s10437-017-9247-1). [UEA repository](https://ueaeprints.uea.ac.uk/id/eprint/90140/). Abstract and metadata consulted; full text unavailable there.

[5] A. van Wyngaard, “The Dutch Reformed Church Mission in Swaziland – A dream come true,” *HTS Teologiese Studies/Theological Studies*, vol. 74, no. 1, 2018, doi: [10.4102/hts.v74i1.4785](https://doi.org/10.4102/hts.v74i1.4785). [SciELO full text](https://www.scielo.org.za/scielo.php?pid=S0259-94222018000100004&script=sci_arttext). Full article consulted, particularly “The first missionaries in Swaziland”.

[6] P. Bonner, “The conquest state 1820–1838,” in *Kings, Commoners and Concessionaires: The Evolution and Dissolution of the Nineteenth-Century Swazi State*. Cambridge: Cambridge University Press, 1983, ch. 3, pp. 27–46, doi: [10.1017/cbo9780511563027.006](https://doi.org/10.1017/cbo9780511563027.006). Publisher chapter summary consulted; full chapter unavailable through Cambridge access.

### Local primary-source links

All local sources were inspected on 25 October 2026; their line numbers are not immutable version identifiers.

[S1]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/countries/swz - swaziland.txt:10>
[S2]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_inventions.txt:132>
[S3]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/countries/swz - swaziland.txt:2>
[S4]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_political_setup.txt:74>
[S5]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/buildings/04_subsaharan_africa.txt:2780>
[S6]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/buildings/04_subsaharan_africa.txt:2548>
[S7]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/production_methods/02_agro.txt:1>
[S8]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/map_data/state_regions/04_subsaharan_africa.txt:1480>
[S9]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/states/00_states.txt:9152>
[S10]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/pops/04_subsaharan_africa.txt:3350>
[S11]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/pops/04_subsaharan_africa.txt:3161>
[S12]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/population/swz - swaziland.txt:1>
[S13]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_literacy.txt:292>
[S14]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_wealth.txt:120>
[S15]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/military_formations/07_military_formations_subsaharan_africa.txt:97>
[S16]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/scripted_effects/sb_frontier_force_effects.txt:62>
[S17]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/laws/01_land_reform.txt:51>
[S18]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/pop_types/farmers.txt:75>
[S19]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/production_methods/12_subsistence.txt:1>
[S20]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/buildings/02_agro.txt:81>
[S21]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/inventions_l_english.yml:416>
[S22]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/20_military.txt:3>
[S23]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/30_society.txt:3>
[S24]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/laws/01_trade_policy.txt:5>
[S25]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/laws/zz_sb_customary_army_reform.txt:128>
[S26]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/journal_entries/1-04_sb_firearms_acquisition.txt:54>
[S27]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/scripted_effects/sb_firearms_effects.txt:75>
[S28]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/static_modifiers/sb_firearms_modifiers.txt:5>
[S29]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/laws/03_sb_amabutho_system.txt:5>
[S30]: </Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/scripted_triggers/sb_institutions_reform_triggers.txt:1>
[S31]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/pop_types/engineers.txt:52>
[S32]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/pop_types/officers.txt:39>
[S33]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/30_society.txt:142>
[S34]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/buildings/11_private_infrastructure.txt:236>
[S35]: </Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_building_triggers.txt:1>
