# Institutional reach and reform in Zulu, Swazi, Gaza and Basotho societies

**30 October 2026 — targeted research and design assessment; no gameplay edits.**

## Executive summary

**A reusable reform journal is defensible, but the current Zulu political journal is not yet that reusable component.** Its initialisation and monthly work directly invoke the Zulu court, dynasty, claimant and constitutional-movement systems. Adding SWZ, GZA or BST to its profile trigger would carry those systems with it. Keep the generic reform calculation and its lifecycle separate from the Zulu political layer. [1]

The starting technologies are not an industrial package: ZUL, SWZ and GZA explicitly receive Enclosure, Standing Army, Urbanization and International Trade; BST additionally receives Rationalism. These bundle useful basic capabilities with imperfect historical labels. The existing country audits identify literacy assumptions, employment scale, ownership and territorial control as stronger review targets than deleting all four basic technologies. [1], [2]

The historical fit varies. Zulu rulers could mobilise specialised production; Swazi consolidation strengthened royal institutions; Gaza exercised different forms of control over different communities; Basotho agricultural development did not require the disappearance of chiefly government. These are not successive positions on one institutional ladder. [3]–[6]

**Do not make every Society technology automatically remove five points of political Institutional Reach.** Research unlocks, enacted laws, funded institutions and productive adoption are different outcomes. A maximum −25% Society/Production research modifier is a possible authored balance trial, but the evidence cannot validate that number or the same starting severity for all four countries. Prefer a small, explicit reform progression based on operating educational and administrative capacity, and assess Production separately from Society.

Basotho land loss is relevant to food security, but it does not establish inevitable permanent famine immediately after retreat. The historical economy could still export grain after the territorial losses. [6, p. 3]

## Introduction

The decision is whether to extend a common institutional-reform challenge from ZUL to SWZ and GZA, and potentially BST, without duplicating Zulu claimant politics. The principal period is **1836–1870**; a limited later comparison tests whether the Basotho retreat implies permanent food incapacity. This brief assumes the intended obstacle concerns the acquisition and practical use of the game's institutional and production packages, rather than an absence of indigenous knowledge.

Three meanings need separating:

| Concept | Meaning relevant to the mod |
|---|---|
| Reach of the customary political order | How strongly government depends on personal, chiefly, dynastic and regimental arrangements. This is closest to the existing IR calculation. |
| Administrative reach | How consistently the ruler can govern, extract revenue or mobilise resources across territory and communities. Strong customary institutions can increase this. |
| Capacity to adopt new techniques | Access to instruction and exchange, suitable skills, capital, buildings, inputs and institutions that make an unlocked technique usable. |

The same change can increase one and reduce another. Calling all three “Institutional Reach” would make the player's reform choices difficult to interpret.

## Research approach

This is a targeted review, not a systematic survey. Before fresh research, the four **25 October technology/economy audits** and the **18 October institutional design exploration** in `Docs` were read. Their claims were treated as leads and their code descriptions were checked against the current working files. [1]

Independent discovery/access routes on 30 October were scholarly publishers and journal platforms (Cambridge Core, SciELO and RCAAP), institutional repositories (Wits WIReDSpace and the University of London's SAS-Space), and a museum's archaeological presentation. Searches combined the country names and rulers with institutions, tribute, regiments, agriculture, food, labour, missions, 1836 and 1865–1868. Publisher and repository records verified bibliographic details. Selected sections of full articles and a chapter were inspected; Eldredge was consulted through the publisher's ten-page introduction, not the whole book. Bonner's seminar argument is explicitly provisional and is paraphrased without quotation. No paywall was bypassed.

The current SB checkout declares version 0.20.2 and compatibility with Vanilla 1.14.5. Local source readings establish authored mechanics, not economic outcomes. No game was launched and no save was inspected for this brief. Hail Coloumbia and Gates of the Bosphorus supplied implementation comparisons only; they are not historical authorities for these societies.

## Findings and evidence synthesis

### 1. What the current system actually does

The current [IR calculation](../common/script_values/sb_institutions_values.txt) starts at **50**, subtracts law contributions and clamps to 0–50. Its economy deduction is zero for Traditionalism **and Industry Banned**. Local Police contributes a deduction of **−5**, which raises uncapped IR; No Police contributes zero. The army deduction is zero only for **Amabutho**, and five for every other army law, including BST's distinct chiefly levy. These are current source findings; the older design discussion's police schedule is not the current implementation. [1]

The current [institution effects](../common/scripted_effects/sb_institutions_effects.txt) and [journal](../common/journal_entries/1-03_sb_zulu_kingdom.txt) also:

- mark a country with the Zulu profile;
- ensure the Zulu court roster and create the royal, chiefly and traditionalist movements;
- calculate court cooperation and Prerogative;
- check claimant, succession and later princely events;
- scale a base legitimacy penalty and Prerogative's political/military effects.

There is **no generic Society or Production research penalty in the current institution modifiers**. The [Social Mobility decree override](../common/decrees/zz_sb_institutions_social_mobility.txt) already excludes countries with the active-institutions flag. Native Promote Social Mobility supplies +25 percentage points of education access and +25% qualification gain. Broadening the existing flag therefore changes education availability even without adding a new research modifier. [1], [2]

The [country histories](../common/history/countries) and native tier-six helper supply the basic technology packages described above. International Trade requires Bureaucracy in the research tree, although the histories do not explicitly add Bureaucracy. **The engine-resolved ancestor list needs a save check before counting starting Society technologies.** History grants must not be treated as a verified exhaustive researched-tech list. [1], [2]

### 2. Country fit

| Country | Historical evidence | Implication for an authored reform journal |
|---|---|---|
| **ZUL** | The recent synthesis describes royal mobilisation of specialist ironworking and deliberate engagement with outside knowledge, while acknowledging debate over military novelty and scale. Archaeology independently documents regimental accommodation, cattle enclosures and brass-working at Dingane's capital. [3, “Knowledge and Power in the Zulu Kingdom”], [7] | The court and regimental system can obstruct some changes while organising others. A challenge about new administrative, educational or industrial capacity fits; a general inability to innovate does not. Preserve the existing Zulu political story as its own layer. |
| **SWZ** | Bonner distinguishes Sobhuza's uneven conquest arrangements from later consolidation. Under Mswati, royal villages, age regiments and stronger regional supervision increased central control; regimental labour also supported royal cultivation. Regional opposition and external threats constrained those changes. [4, SAS-Space typescript, PDF pp. 4–6] | **Strong fit for a reusable institutional challenge, with different objectives.** Reforms can strengthen the monarchy and its capacity. An automatic fall in customary authority for each discovery would misrepresent this route. Do not project the later network fully into 1836. |
| **GZA** | Mathebula distinguishes directly governed areas, tribute relationships and raids, and challenges blanket ethnic/geographical accounts of Gaza rule. His reconstruction describes an unstable northern/southern sequence around 1835–1838. Separately, Farré documents southern Mozambican cultivation, diversification and food marketing, including women's participation. [5, “Migration of the Gaza into the vicinity of the Hlengwe”], [8, pp. 33–37] | **Good fit if the issue is converting uneven military/tributary control into reliable administration.** A uniform national research score cannot by itself distinguish the core from a tributary periphery. Do not infer economic ignorance from weak direct administration. Avoid calibrating the entire population as a single social unit. |
| **BST** | Eldredge identifies indigenous agricultural techniques and pre-existing surpluses, with high labour inputs and subsequent technical adaptation. Mission schools developed within arrangements negotiated with the king and chiefs; the mission presence did not replace customary landholding. [6, pp. 6–7], [9, “The Arrival of the Paris Missionaries” and “The Different Views on Land Occupation”] | **Conditional fit, requiring a distinct starting profile.** School provision and administrative adoption can be difficult without blocking agrarian learning behind constitutional reform. The chiefly levy must be recognised as a customary institution rather than automatically counted as a reformed army. |

These findings support different histories of incorporation, labour mobilisation and knowledge transfer. They do not supply comparable numerical research rates. The shared component should represent the particular constraint selected by the design, not claim that one polity was “five technologies” closer to another.

### 3. Starting knowledge and practical adoption

The basic technology labels should be read through their effects. Enclosure gates farms and ranches without itself enacting private freehold. Standing Army enables military buildings but does not imply firearms or a fully professional army. Urbanization bundles infrastructure and construction capacity with settlement-related unlocks. International Trade makes Mercantilism available; it does not create a route or guarantee supply. The native trade-centre definition has no direct technology gate, despite an old technology comment. [2]

Zulu metallurgical expertise is especially useful counterevidence to equating a short technology list with absence of technical knowledge. Beinart and Dubow describe royal attempts to extend production and control its distribution; their discussion spans decades and cannot establish a factory-equivalent output in 1836. [3] The right mechanical distinction is between a known practice, its scale and the organisation and inputs required by a particular production method.

The country's ability to hire and sustain a new building can remain weak after research succeeds. The existing audits flag the occupational literacy template, qualification requirements, subsistence employment, ownership and commercial job capacity as material limits. These should be measured before assigning all observed development to “too much starting technology”. [1], [2]

### 4. Why “100 minus five per Society technology” is a poor default

The arithmetic is straightforward: with no other deductions, `IR = max(0, 100 − 5N)` reaches zero after **20 counted technologies**. If the research modifier is `−0.25 × IR / 100`, each technology removes **1.25 percentage points** of the penalty. Ten counted technologies leave −12.5%; fifteen leave −6.25%. These are authored arithmetic, not historical calibration.

The installed native technology definitions contain **64 Society technologies**, distributed as follows. SB preserves the eras of its two Society overrides and adds the unresearchable `sb_namibian_coastal_access` marker in Era III. That marker should not be treated as an ordinary innovation. This is a definition count, not a claim that every item is available to every country or counted by a particular engine query. [1], [2]

| Era | Native Society technologies | Cumulative native total | SB addition |
|---|---:|---:|---|
| I | 18 | 18 | None |
| II | 15 | 33 | None |
| III | 13 | 46 | 1 unresearchable coastal-access marker |
| IV | 10 | 56 | None |
| V | 8 | 64 | None |

For a direct comparison, let **D** be the net deductions from laws and **N** the total counted Society technologies, including the starting grants. The following retains today's deductions unchanged. “Retained 50” uses only the current law score, `clamp(50 − D, 0, 50)`, with a proposed penalty of `−25% × IR/50`. The proposed 100-point model uses `clamp(100 − D − 5N, 0, 100)` and `−25% × IR/100`.

| Net law deduction D | Retained 50: IR / research penalty | Proposed 100 at N = 2: IR / research penalty | Total counted technologies needed for IR = 0 | Further technologies after ZUL's two explicit Society grants |
|---:|---:|---:|---:|---:|
| 0 | 50 / −25% | 90 / −22.5% | 20 | 18 |
| 10 | 40 / −20% | 80 / −20% | 18 | 16 |
| 25 | 25 / −12.5% | 65 / −16.25% | 15 | 13 |
| 50 | 0 / 0% | 40 / −10% | 10 | 8 |
| 75 | 0 / 0% | 15 / −3.75% | 5 | 3 |

ZUL's explicit Society grants are **Urbanization and International Trade**; Enclosure is Production and Standing Army is Military. If the engine also grants Bureaucracy as an ancestor, the effective starting count becomes three, and the final column falls by one. If the intended rule counts **only discoveries after entry**, it instead begins at N = 0 and requires the full total in the fourth column; it needs a separate baseline. [1], [2]

With no law reform and all starting technologies counted, completing **all 18 Era-I Society technologies** would still leave IR = 10 and a −2.5% penalty, requiring two further counted technologies to reach zero. A ten-point law deduction permits completion with 18 total. Twenty discoveries need not include every Era-I item: these are arithmetic thresholds, not proposed research orders, historical schedules or assertions that every law/technology combination is legally reachable. If the retained 50-point score also receives the same −5 per technology, technology alone ends it after **ten** counted items and removes **2.5 percentage points** of research penalty per item. Changing the range therefore changes considerably more than presentation.

The design has four problems:

1. **It counts availability as implementation.** Researching Bureaucracy does not demonstrate a staffed administration, and learning about schooling does not fund schools. It also gives unrelated Society discoveries the same institutional effect.
2. **It rewards a technology twice when the law it unlocks is also counted.** Democracy opens distribution-of-power options; Romanticism opens Agrarianism; Bureaucracy and Law Enforcement sit on administrative/police paths. A technology deduction followed by a law deduction can be intentional, but they should represent distinct outcomes rather than two rewards for the same assumed reform. [2]
3. **It couples progress to its own escape mechanism.** Research becomes slower until research removes the penalty. This can reward collecting inexpensive discoveries and discourage costly but relevant capacity. Native Rationalism already changes education access, Centralization changes tax capacity and incorporation, and literacy already raises the innovation ceiling and technology spread. [2]
4. **The starting and scale conventions become ambiguous.** Counting all explicit Society grants would give ZUL/SWZ/GZA two credits and BST three before checking ancestors. Counting only later discoveries requires a clearly defined baseline, including inheritance. Changing the existing cap from 50 to 100 without adjusting its `/50` consumers would also alter political modifier strength. Keeping all old law deductions unchanged would make each reform only half as large relative to the new maximum. [1], [2]

If technology must contribute, use a **short named list of relevant milestones**, explain what each establishes, and prevent technology alone from completing the journal. A completed research item should normally enable a practical objective. No source here establishes a historical reason to make every Society discovery erode royal or chiefly authority.

### 5. Penalty size and existing constraints

The proposed **−25% Society and Production research** is technically expressible with native category modifiers. It would be an explicit gameplay choice. In the simplified case where effective research speed becomes 75% of an otherwise unchanged rate, the same research takes approximately **33⅓% longer**, not 25% longer. Other bonuses, penalties, innovation limits and spread determine the actual campaign result. [2]

Check these interactions before selecting the magnitude:

| Existing mechanism | Interaction with the proposed penalty |
|---|---|
| Literacy | Native literacy increases the innovation ceiling and adds technology spread. Lower starting literacy plus another research penalty can represent two real constraints, but needs separate justification and measurement. [2] |
| Social Mobility exclusion | The existing institutional flag already withholds a substantial education-access and qualification boost. Adding a research modifier changes a third part of the development process. [1], [2] |
| Traditionalism | It already reduces investment efficiency and tax capacity and changes market-price effects. It has no direct native Production research penalty. These economic constraints can impede practical adoption even if research is available. [2] |
| Industry Banned | It already contributes **−25% Production research and −25% Production spread**. Current IR gives it the same economy deduction as Traditionalism. Another −25% Production research contribution would total −50% from these two sources. [1], [2] |
| Firearms challenge | It already contributes −25% Military research until completion. The **current** JE uses 260 qualifying weeks of small-arms market supply; imports and domestic output satisfy the same supply check. Slower Production research can delay domestic supply even if the military penalty is unchanged. The older audits' separate 24-month route description is superseded by the current working source. [1] |
| Army-law reform | Ordinary replacement of Amabutho/the chiefly levy requires the firearms-completion flag, and Professional Army also requires Military Drill. A second generic reform completion gate would add another obstacle to the same transition. [1] |

Research speed and technology spread are separate settings. Testing −25% research does **not** require simultaneously reducing spread, education access or literacy growth. Keep those changes separate so the comparison identifies what caused the result.

### 6. Basotho retreat, food and labour

Eldredge states that wars in the 1850s–1860s cost the Basotho **over half their arable land**. Nevertheless, they sold surplus grain and labour to Kimberley in the 1870s and early 1880s; long-run loss of food self-sufficiency came later. Her explanation connects shortages to war, dispossession, environmental stress and subsequent economic pressures. [6, pp. 3, 6–7]

**Modelling inference:** the retreat should test lost productive land, damaged assets, access to food markets and the placement of displaced households. Additional people provide potential labour but also need food and a productive place to work. Neither headcount alone nor a blanket “highland productivity” bonus establishes a viable settlement. Distinguish cultivable lowlands/foothills from high mountain areas, and distinguish a short war/harvest crisis from permanent national incapacity.

This review found **no defensible January 1836 workforce/dependants ratio, post-retreat population total or exact food-output multiplier**. It therefore does not recommend a population reduction, a famine timer or a free productivity bonus. Those require the save and map/allocation analysis being conducted separately. The historical check is that displacement should create a contingent, explainable food-security problem rather than predetermine permanent starvation.

## Discussion and implications

The most economical reusable design is a **country opt-in reform journal with a small common lifecycle and explicitly selected objectives**. It need not duplicate the entire court framework or introduce a universal registry. SWZ's likely emphasis is royal/regimental administration; GZA's is governing a heterogeneous conquest and tribute system; BST's is sustaining educational and administrative adaptation alongside a productive agrarian base.

The examples inspected favour authored country packages rather than a claim of one universal developmental stage. Hail Coloumbia's Apache setup pairs tier-six technology with its own native-law and conscription helpers. Gates of the Bosphorus pairs Kurdish country histories with a specific tribal journal; its Tanzimat progress separately reads legitimacy, literacy, political backing and administration. These are useful stylistic precedents for explicit inputs, not templates to copy wholesale or evidence that their formulas suit southern Africa. [10]

An institutional reform that strengthens an existing monarchy is a valid successful outcome. Research penalties should end because the relevant adoption obstacle has been overcome. A constitutional change, annexation, renamed tag or Society discovery should not by itself imply that schools, staff and productive inputs now exist.

## Limitations and evidence gaps

- Bonner's seminar paper uses an explicitly provisional theoretical interpretation. Its detailed reconstruction is valuable, but it does not yield modern administrative-capacity indices. Later royal institutions cannot simply be backdated to Sobhuza's 1836 polity.
- Mathebula presents a substantive challenge to broad Gaza claims, with contradictory earlier traditions discussed openly. It supports distinguishing control relationships; it does not settle every provincial boundary or population allocation.
- Eldredge's introduction supports the stated agrarian and land-loss conclusions; the full book's population tables and detailed famine chapters were not inspected in this pass. No precise population calibration is attributed to them.
- The mission study is a church/land history, not a literacy survey. A school founding date cannot establish national literacy or an investment level.
- Current scripts and older audits differ, especially in firearms progression. No fresh-start technology ancestry, qualification, research-rate, employment or food-balance result has been engine-verified here.

## Recommendations

1. **Extend a generic reform layer to SWZ and GZA, with BST conditional on its distinct profile.** First isolate its calculation, modifiers and cleanup from Zulu court, claimant and movement calls. Recognise BST's chiefly levy explicitly. Confidence: high on the separation; medium on the final shared objectives. [1], [3]–[6]
2. **Keep the basic starting technologies provisionally.** Review literacy inputs, commercial staffing, tenure representation and territorial administration against actual saves before removing unlocks that keep agriculture and exchange functional. Confidence: high in the dependency concern; lower in the exact starting values. [1], [2]
3. **Reject a universal −5 per Society technology as the primary reform measure.** Use two or three plainly explained practical objectives: for example, funded school provision, staffed administration and a sustained route for instruction/technical exchange. These are design candidates; their thresholds require calibration. Allow progress under monarchy and customary land arrangements.
4. **If testing −25%, treat it as a research-only trial ceiling and compare Society and Production separately.** Start from an unchanged-literacy control; record actual research times, spread, school access, qualifications and firearms supply. Check Industry Banned and army-law gates explicitly. Do not stack another military-reform gate onto firearms completion. [1], [2]
5. **Assess the Basotho retreat through land, employment and food access.** Preserve the possibility of recovery and export agriculture when the game's remaining resources support it. Do not infer a population or labour correction from the historical fact of territorial loss alone. [6]

## References

[1] Spes Bona contributors, *Spes Bona – A Southern Africa Flavour Pack*, working source snapshot, declared version 0.20.2, inspected Oct. 30, 2026. [Descriptor](../descriptor.mod); [IR values](../common/script_values/sb_institutions_values.txt); [institution effects](../common/scripted_effects/sb_institutions_effects.txt); [institution modifiers](../common/static_modifiers/sb_institutions_modifiers.txt); [eligibility](../common/scripted_triggers/sb_institutions_triggers.txt); [army-reform trigger](../common/scripted_triggers/sb_institutions_reform_triggers.txt); [army laws](../common/laws/zz_sb_customary_army_reform.txt); [firearms JE](../common/journal_entries/1-04_sb_firearms_acquisition.txt); [supply trigger](../common/scripted_triggers/sb_firearms_triggers.txt); [firearms modifiers](../common/static_modifiers/sb_firearms_modifiers.txt); [Society overrides](../common/technology/technologies/sb_society_technology_overrides.txt); [coastal-access marker](../common/technology/technologies/sb_namibian_coastal_access.txt). Prior research consulted: [ZUL audit](zul_1836_technology_economy_audit_2026_10_25.md), [SWZ audit](swz_1836_technology_economy_audit_2026_10_25.md), [GZA audit](gza_1836_technology_economy_audit_2026_10_25.md), [BST audit](bst_1836_technology_economy_audit_2026_10_25.md), [institution design exploration](southern_african_institutions_and_zulu_politics_2026_10_18.md). These are source/design records, not independent historical evidence.

[2] Paradox Development Studio, *Victoria 3*, installed game scripts, compatibility target 1.14.5, inspected Oct. 30, 2026. [Starting technology helper, line 132](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_inventions.txt:132>); [Society technologies](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/technology/technologies/30_society.txt:3>); [economic-system laws](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/laws/01_economic_system.txt:5>); [Industry Banned research effects, line 320](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/laws/01_economic_system.txt:320>); [literacy innovation/spread effects, line 831](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_code_static_modifiers.txt:831>); [literacy initialiser, line 292](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_starting_pop_literacy.txt:292>); [trade-centre definition, line 236](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/buildings/11_private_infrastructure.txt:236>). Source inspection does not establish resolved runtime values.

[3] W. Beinart and S. Dubow, “Scientific Governance and Colonial Institutions, c. 1800–70,” in *The Scientific Imagination in South Africa: 1700 to the Present*. Cambridge: Cambridge University Press, 2021, pp. 66–108, doi: [10.1017/9781108938198.004](https://doi.org/10.1017/9781108938198.004). [Publisher full chapter](https://www.cambridge.org/core/books/scientific-imagination-in-south-africa/scientific-governance-and-colonial-institutions-c-180070/C7C29B0CCCEBA5CB38085F6EAD33CF16). Section “Knowledge and Power in the Zulu Kingdom” inspected; later descriptions are not treated as 1836 measurements.

[4] P. L. Bonner, “Classes, the mode of production and the state in pre-colonial Swaziland,” African Studies Institute Seminar Paper no. 046, University of the Witwatersrand, Johannesburg, Sep. 13, 1976. [Wits institutional version and dated cover](https://wiredspace.wits.ac.za/server/api/core/bitstreams/8d33c1c7-0b9f-459d-895a-0dfacc204d25/content); [University of London SAS-Space parallel typescript](https://sas-space.sas.ac.uk/4059/1/P_L_Bonner_-_Classes,_the_mode_of_production_and_the_state_in_pre-colonial_Swaziland.pdf). Relevant historical passages checked in the SAS-Space version, PDF pp. 4–6; its pagination differs from the Wits version. Provisional seminar argument, paraphrased without quotation. No DOI verified.

[5] M. M. Mathebula, “Bounding the frontiers: An assessment of the Gaza’s relations with the Hlengwe of Zimbabwe (1835–1895),” *New Contree*, vol. 91, art. a247, Nov. 6, 2024, doi: [10.4102/nc.v91.247](https://doi.org/10.4102/nc.v91.247). [Publisher full text](https://newcontree.org.za/index.php/nc/article/view/247/986). Metadata and relevant historical sections inspected.

[6] E. A. Eldredge, *A South African Kingdom: The Pursuit of Security in Nineteenth-Century Lesotho*, 1st ed. Cambridge: Cambridge University Press, 1993. ISBN 978-0-521-44067-7. [Publisher introduction, pp. 1–10](https://assets.cambridge.org/97805214/40677/excerpt/9780521440677_excerpt.pdf); [publisher front matter and edition/ISBN verification](https://assets.cambridge.org/97805214/40677/frontmatter/9780521440677_frontmatter.pdf). Only the provided introduction was inspected in this pass.

[7] KwaZulu-Natal Museum, “Pieces of uMgungundlovu: Remembering iNkosi Dingane kaSenzangakhona’s capital,” online exhibition, undated. [Museum exhibition](https://www.nmsa.org.za/online-exhibition/pieces-of-umgungundlovu.html). Accessed Oct. 30, 2026. Archaeological presentation includes explicitly identified later recollections; no exact economic output inferred.

[8] A. Farré, “Las Mujeres y el Mito de la Agricultura de Subsistencia. De la exportación de alimentos a la dependencia alimentaria en el sur de Mozambique,” *Cadernos de Estudos Africanos*, no. 29, pp. 31–58, 2015, doi: [10.4000/cea.1777](https://doi.org/10.4000/cea.1777). [Official full PDF](https://revistas.rcaap.pt/cea/article/view/7973/5600). Historical sections, especially pp. 33–37, inspected. Regional and long-period evidence does not establish every Gaza community's position in January 1836.

[9] N. S. K. Tseuoa, “Church and Land in Basutoland: The Paris Evangelical Mission and its Implications,” *Studia Historiae Ecclesiasticae*, vol. 46, no. 2, pp. 1–16, 2020, doi: [10.25159/2412-4265/6773](https://doi.org/10.25159/2412-4265/6773). [Open full text](https://www.scielo.org.za/scielo.php?pid=S1017-04992020000200008&script=sci_arttext). Mission/land sections inspected; not a national literacy survey.

[10] Hail Coloumbia and Gates of the Bosphorus contributors, installed example-mod source snapshots labelled 1.13, inspected Oct. 30, 2026. [Hail Coloumbia Apache history](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Example Mods/hc - Hail Coloumbia [1.13]/common/history/countries/apc - apache.txt:1>); [Gates of the Bosphorus Kurdish history](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Example Mods/gotb - gates of the bosphorus [1.13]/common/history/countries/kur - kurdistan_tribes.txt:1>); [Gates of the Bosphorus Tanzimat values](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Example Mods/gotb - gates of the bosphorus [1.13]/common/script_values/3-01_turkfm_tanizmat_values.txt:140>). Implementation comparisons only.
