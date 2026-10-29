# Zulu opening character traits: an independent historical assessment

**Research date:** 25 October 2026. **Historical cut-off:** 1 January 1836. **Status:** recommendations for review; no gameplay or localisation changes. This is a targeted research brief, not a systematic review.

**Subsequent comparison:** the [Vanilla package review](zulu_vanilla_character_packages_2026_10_25.md) sets out the likely rationale and full ruler/commander/IG effects of the inherited packages. The sparse recommendations here are not an approved balance replacement: in particular, removing Ndlela's Tactful/Elder package also removes material military benefits. Final packages remain under DP review.

## Decision

Use a sparse, deliberately authored baseline. Give a temperament only where a relevant early description or attributable oral tradition supports it; assign skills separately, as interpretations of demonstrated work. An unspecified temperament means that the evidence is insufficient, not that the person lacked a personality or ability. Existing packages were treated as absent when forming these recommendations.

The preferred packages are **Reserved + Basic Political Operator for Dingane**, **Elder + Experienced Political Operator for Mkabayi**, and **Imposing + Brave for Zulu/Komfiya**. Most other established officials need only one skill. Leave Mpande and Gqugqu's temperament unspecified, and give the three opening children no adult career accomplishments. The evidence and its limits are set out below.

Dingane's requested despised opening position should be represented partly by an explicitly authored political-reputation modifier. Permanent campaign achievements can then improve his reputation without changing his temperament or pretending that a king's victory proves personal battlefield bravery. Exact popularity targets are design decisions, not measurements recoverable from the historical record.

## 1. What actually exists at the opening

The ZUL character-history file explicitly creates thirteen named characters. The SB dynasty and court templates, together with inherited vanilla templates, resolve the identities below. No additional named historical opening character was found in that creation list. Later availability templates and randomly generated names are not additional historical opening identities. In particular, the later Masiphula, Maphitha, Mnyamana, Hamu, Godide, Sekethwayo, Dunn and Zibhebhu templates should not silently expand this review's opening cast. [1]

| Character | Authored age/state on 1 January 1836 | Template identity |
|---|---|---|
| Dingane | 41; ruler | `ZUL_dingane` |
| Mpande | 38; explicitly made a politician; no opening heir designation | `ZUL_mpande_zulu` |
| Gqugqu | 28; adult claimant | `ZUL_gqugqu_claimant` |
| Mkabayi kaJama | 76; Landowners leader | `ZUL_mkabayi` |
| Ndlela kaSompisi | 50; Armed Forces leader and general | `ZUL_ndlela_kasompisi` |
| Zulu kaNogandaya / Komfiya | 35; general | `ZUL_zulu_kanogandaya` |
| Dambuza kaSobadli | 45; explicitly made a politician | `SB_ZUL_dambuza` |
| Mawa kaJama | 55; explicitly made a politician | `SB_ZUL_mawa` |
| Nongalaza kaNondela | 40; explicitly made a politician | `SB_ZUL_nongalaza` |
| Sotobe / Sothobe kaMpangalala | 40; explicitly made a politician | `SB_ZUL_sotobe` |
| Cetshwayo | 9; child | `ZUL_cetshwayo_heir` |
| Mbuyazi | 8; child | `ZUL_mbuyazi_heir` |
| Uthumbu | 8; explicitly authored alternate history, `historical = no` | `ZUL_uthumbu_claimed_son` |

These are **template ages**, not newly verified birth dates. Several are approximations, and the native Cetshwayo template itself says his precise birthday is unknown. A template name containing `heir` does not establish the active heir role: the opening history deliberately blocks an opening heir. Uthumbu receives no invented historical biography in this brief. [1]

## 2. Recommendation matrix and intrinsic arithmetic

The installed native definitions are the authority for game effects, never for historical characterisation. Define **Q** as the sum of `character_popularity_add` in the proposed traits' universal `character_modifier` blocks; **R** as the sum of their direct `character_prominence_add`; and **E = R + 0.25Q** as an *uncapped analytical contribution* using the installed popularity-to-prominence coefficient. E is not a prediction of the displayed opening prominence: roles, other modifiers, the prominence cap, engine treatment of negative values and ordering still matter. [2]

The matrix excludes age traits and role modifiers. Confidence refers to the historical-to-game mapping, not merely whether the person held office. **High** means a directly attested early role; **medium** means a reasonable, bounded interpretation; **low** means evidence insufficient for that specific trait. Historical facts can be high-confidence while the proposed skill level remains an interpretation.

| Character | Preferred authored adult package | Basis and confidence | Q | R | E |
|---|---|---|---:|---:|---:|
| Dingane | `reserved`, `basic_political_operator` | Explicit pre-1836 reserve; established decision-making and negotiation. Medium temperament/skill mapping. [3], [4] | −25 | +5 | −1.25 |
| Mpande | None specified | Early evidence does not securely establish a particular temperament or specialised skill; reject the lazy/cowardly stereotype as a baseline. [5] | 0 | 0 | 0 |
| Gqugqu | None specified | Later rival power is insufficient to establish an ambitious or imperious personality at launch. [5] | 0 | 0 | 0 |
| Mkabayi | `elder`, `experienced_political_operator` | Senior royal authority and sustained political brokerage; medium mapping, stronger than a generic ambition label. [6] | +25 | +15 | +21.25 |
| Ndlela | `basic_political_operator` | Directly attested senior councillor and gatekeeper in 1835. High office confidence; medium skill mapping. [4] | 0 | +5 | +5 |
| Zulu / Komfiya | `imposing`, `brave` | Identified son's oral account of bearing, wounds and martial reputation; medium, with temporal caveat for bearing. [7] | +25 | +5 | +11.25 |
| Dambuza | `basic_political_operator` | Directly attested council, negotiation and access-control work in 1835. High office confidence; medium skill mapping. [4] | 0 | +5 | +5 |
| Mawa | `elder` | Senior royal woman with an established regimental establishment; medium standing-to-skill mapping. [8] | +25 | +5 | +11.25 |
| Nongalaza | `basic_political_operator` | Named military-town head and participant in royal deliberation in 1835. High office confidence; medium administrative-skill mapping. [4] | 0 | +5 | +5 |
| Sotobe / Sothobe | `basic_diplomat` | Actual 1828 envoy work; high confidence in the assignment, medium in translating practice into proficiency. [9] | +10 | 0 | +2.5 |
| Cetshwayo | No adult traits or skills | Preserve childhood; no adult achievements at launch. [1], [2] | 0 | 0 | 0 |
| Mbuyazi | No adult traits or skills | Preserve childhood; no adult achievements at launch. [1], [2] | 0 | 0 | 0 |
| Uthumbu | No adult traits or skills | Authored child; any future temperament is alternate-history authorship, not recovered evidence. [1], [2] | 0 | 0 | 0 |

### Age and role effects kept outside those totals

Native `trait_child` independently adds **Q = −25, R = −25**, giving **E = −31.25** before roles and other modifiers. Thus the preferred *adult package plus childhood* totals for **each** of Cetshwayo, Mbuyazi and Uthumbu are −25 popularity and −25 direct prominence. The child trait also supplies ruler authority −15%, ruler prestige −5%, and IG attraction −25% if those roles apply. This age state must not be mistaken for a historical claim that these children were unpopular. [2]

Native role modifiers include ruler **+100** direct prominence, heir **+50**, politician **+10**, and IG leader **+25**; the inspected general role has no direct prominence bonus. SB separately defines royal-claim **+5** and junior-status **−10** prominence modifiers. These are not intrinsic personality. Do not automatically sum every role label without confirming the character's actual roles, and do not add an heir bonus merely because a template is called `*_heir`. The native maximum prominence is 100. [1], [2]

Consequently, prominence-based faction strength will not reproduce the matrix's ordering mechanically. The ruler's large role contribution and the cap can dominate trait differences. A +30 popularity achievement has a nominal **+7.5** popularity-derived prominence contribution; it is not a direct +30 prominence award, nor a guaranteed +7.5 change in the displayed, capped value. [2]

## 3. Historical reasoning and alternatives

### Dingane: reserve is early evidence; universal hatred is not

Isaacs's original 1836 second volume describes Dingane as extremely reserved, weighing words before speaking, but becoming fluent and pointed once he had assessed his interlocutor. This portrait derives from his earlier residence, including the 1830–1832 return, rather than an episode after Blood River. It is direct evidence for an observer's experience of reserve before the opening date. Isaacs was an interested colonial trader writing through racial and civilising assumptions; his interpretation of motives cannot simply be treated as access to Dingane's mind. `reserved` is therefore a defensible medium-confidence translation, with its native −25 popularity a mechanical consequence rather than evidence that reticence caused general unpopularity. [3, pp. 280–282]

Gardiner's 1835 narrative also shows a king negotiating, referring questions to councillors and governing through them. That supports a basic political skill independently of the temperament choice. Gardiner's 28 May account reports Dingane saying his people had hated him because he had refused chiefs' requests to attack refugees at Port Natal; Nongalaza and other chiefs reportedly assented. This is a staged political conversation recorded by a missionary involved in returning those refugees. It establishes a reported dispute, not a representative poll, and its criticism concerns restraint rather than a simple picture of subjects uniformly rejecting cruelty. [4, pp. 34–37, 137–140, 160–163]

African praise and testimony must be considered on their own terms. Ndlovu reads the quiet, “mouthless” contrast with Shaka as comparatively amicable, while showing that the same archive also represents Dingane as dangerous, destructive and generous. The record contains competing political evaluations. The precise composition date of that praise passage was not established here, so it is corroborative context rather than the evidence that dates `reserved` to 1836. Isaacs supplies that earlier chronological anchor. [10, pp. 8–20] Okoye's publisher extract independently identifies the entrenched hostile stereotype as the problem of his reappraisal; the full article was not inspected, so it is not used to certify particular counterclaims. [11]

There is also substantial early evidence of coercion. Gardiner describes witnessing the execution of a royal brother he calls Goujuana and two servants in 1835. He explicitly treats the alleged conspiracy as uncertain; his explanation of Ndlela's pressure is reported information, and destruction of the dead man's dependent settlements is relayed through a participating official, not personally witnessed. `ruthless` is a credible alternative emphasis on coercive politics, with lower confidence in treating such acts as an enduring psychological disposition. Do not silently identify this Goujuana with the Gqugqu whose death is placed in 1843. [4, pp. 44–47], [5]

The preferred two-trait package selects the comparatively precise early behavioural description and a modest skill. A coercion-centred package is also defensible; it is not required merely to make the popularity number negative enough. The Retief killings belong to 1838, and later reconstructions distinguish contemporaneous observation, subsequent testimony and disputed motives. They must not become an unexplained 1836 personality diagnosis. [12]

Avoid loading `hedonist`, `imperious` or `cruel` merely from hostile adjectives. Isaacs's account of dance, women and pleasure requires particular caution about moral and cultural framing. `cruel` also imposes a national −1 standard of living when the character rules: it makes a substantial claim about play outcomes, beyond representing a negative reputation. [3, p. 282], [2]

### Mpande and Gqugqu: position does not establish temperament

Shamase challenges representations of Mpande as indolent, inept or cowardly and places his early subordinate position in the context of his status as an umsizi prince. This supports refusing a negative caricature; it does not prove `honorable`, `compliant`, `cautious` or a specialised skill in January 1836. The neutral recommendation is evidentiary restraint, not a judgement that he was incapable. [5]

For Gqugqu, the strongest material inspected describes his threatening dynastic position, following and establishment in **1843**. Those facts matter for a later succession crisis, but cannot automatically become an already mature 1836 faction or an `ambitious`/`imperious` personality. A basic political skill is possible only as an explicitly modest adult-prince abstraction; it has weaker direct support than the same skill for the documented councillors. [5]

### Mkabayi: authority and brokerage before a temperament label

Mkabayi's political experience is the strongest justification for a higher skill tier. Shamase's oral-history study presents her senior royal authority, regency and interventions in succession, and discusses praise about access and mediation. Its interpretive and sometimes romantic language should not be converted wholesale into psychology. [6, pp. 15–22] Ndlovu likewise discusses praise representing both brokerage and destructive power, and her authority at ebaQulusini under Shaka and Dingane. Those accounts overlap in oral materials; they are not two independent contemporary observations. [10, pp. 23–24]

`elder` represents recognised senior standing; `experienced_political_operator` represents sustained practice. Neither means she was universally loved or politically harmless. `tactful` is a reasonable alternative reading of mediation, but less direct than the evidence of political work. Decline to infer `ambitious` merely because a powerful woman intervened in succession. The exact birth year and some biographical details remain uncertain. [6]

### Ndlela and Dambuza: attested political work, unspecified temperament

Gardiner encountered both as senior decision-makers in 1835, required to approve access and major business. He describes Dambuza acting as spokesman. This supports `basic_political_operator` for each, or `basic_diplomat` if the design emphasises negotiation. Gardiner's praise of Ndlela's appearance and hostile judgement of Dambuza's face are physiognomic judgements, not adequate evidence for contrasting moral personalities. The author's frustration at being unable to bypass them is part of the encounter. [4, pp. 34–37, 48–50, 93–94, 137–140]

Ndlela's general role can represent his command position without proving a particular defensive doctrine. Dambuza's later identification with Nzobo and accounts of 1838 planning require care about name variants, testimony dates and motive. The 1838 reconstruction is useful for that later episode; it does not establish an opening temperament. [12] Neither councillor needs an unsupported bravery, cruelty or ambition tag to have political weight.

### Zulu kaNogandaya / Komfiya: a genuine oral identity, with a chronology limit

The edited testimony of **Mkehlengana kaZulu**, recorded in April 1905, identifies his father Zulu with **Komfiya kaNogandaya**. It relates an intimidating presence, martial distinction under Shaka, wounds and recognition for prowess. This supports `brave` more directly than a ruler's mere possession of victorious armies; `imposing` represents the remembered personal bearing. [7, pp. 210–212]

The son was born around 1851, so his account of the Shaka campaigns is transmitted family history, not eyewitness testimony. His personal recollection of bearing concerns a later period: applying that to 1836 is a continuity inference. `imposing` therefore has a weaker chronological anchor than the earlier campaign reputation. A stricter opening alternative is **Brave alone**; **Imposing + Scarred** instead emphasises the reported wounds while retaining that continuity inference. Do not assign advanced planning or mass popularity from this evidence. The chronology of residence/exile also remains unresolved. [7]

### Mawa: senior institutional standing, without backdated faction loyalty

Hughes identifies Mawa as Jama's daughter and Senzangakhona's sister, with charge of Ntonteleni's regimental establishment under Shaka. That supplies an early basis for an authoritative royal elder. Her allegiance to Gqugqu and flight with a substantial following belong to **1843**. They demonstrate later political capacity without establishing that she must start 1836 in an anti-Dingane faction. [8, pp. 53–54 in the author-reformatted text]

`elder` is a medium-confidence status interpretation, not a reward for merely being aged 55 in the template. If its built-in +25 popularity overstates what the evidence can bear, use `basic_political_operator` alone for institutional experience. No particular temperament is securely established here. [8]

### Nongalaza: an opening office is documented

Gardiner explicitly names Nongalaza as chief induna of the principal military town in the Clomanthleen district in 1835. He also places him in royal deliberations about refugees. This is sufficient to avoid treating him as someone whose importance begins only in Mpande's later campaigns. `basic_political_operator` here denotes running an important establishment and participating in the court, not a claim that he was a particularly cunning intriguer. [4, pp. 140, 161–162]

His tactical speciality and personal temperament remain unspecified. Later victories may justify later military advancement; they should not automatically give him a skilled offensive-planning package at launch. Gardiner also mentions a companion simply called “Zulu”; that bare name is insufficient to identify this person as Komfiya. [4, p. 140]

### Sotobe / Sothobe: use the actual embassy

Peires reconstructs the mission sent by Shaka in April 1828, including Sotobe kaMpangalala, through oral evidence and colonial documentation. The securely relevant point is real envoy work before 1836. This supports a basic diplomatic skill; it does not establish expert success, an affable personality or a stable later faction allegiance. [9, section on the 1828 embassy]

The author's explanation for the mission's frustration is a historical argument about intermediaries and colonial policy, not a reason to penalise the envoy's ability. The printed template age of 40 is not independently established here; descriptions of seniority in the embassy literature deserve a separate age check. Do not conflate a projected approach to Britain with proof that Sotobe personally reached London. [9]

### Cetshwayo, Mbuyazi and Uthumbu: leave the future open

At their authored opening ages, none needs adult political, diplomatic or military credentials. Later accession, civil-war leadership or famous battles cannot justify childhood `basic_diplomat`, `basic_political_operator` or advanced command skills. For the two historical princes, any launch temperament would need evidence about the child, rather than a reading backwards from the adult. No such sufficiently specific evidence was established in this search. Uthumbu is explicitly authored alternate history and must be described as such. [1]

Use the native childhood state and allow the unfolding campaign to supply later accomplishments. This is a design recommendation, not an assertion that historical childhood personalities were unknowable in principle.

### Candidate alternatives: complete intrinsic totals

These are **replacement packages**, not additions to the preferred row unless expressly stated. All totals are derived from installed native universal character modifiers. [2]

| Character / interpretation | Complete alternative package | Q | R | E | Appraisal |
|---|---|---:|---:|---:|---|
| Dingane, coercive politics | `ruthless`, `basic_political_operator` | −15 | +10 | +6.25 | Defensible from early acts; enduring temperament remains an inference. |
| Dingane, both strands | `reserved`, `ruthless`, `basic_political_operator` | −40 | +10 | 0 | Defensible but less lean; use only if both emphases are wanted. |
| Dingane, office only | `basic_political_operator` | 0 | +5 | +5 | Strongest restraint if the behavioural interpretation is rejected. |
| Mpande or Gqugqu, modest princely experience | `basic_political_operator` | 0 | +5 | +5 | Low-confidence abstraction; weaker than directly attested office. |
| Mkabayi, lower skill tier | `elder`, `basic_political_operator` | +25 | +10 | +16.25 | Conservative proficiency calibration. |
| Mkabayi, mediation emphasis | `elder`, `tactful` | +25 | +5 | +11.25 | Medium inference from brokerage; drops the explicit political skill. |
| Mkabayi, experience only | `experienced_political_operator` | 0 | +10 | +10 | Avoids interpreting senior standing as native popularity. |
| Ndlela or Dambuza, negotiation emphasis | `basic_diplomat` | +10 | 0 | +2.5 | Based on their 1835 diplomatic business; no personality implied. |
| Zulu/Komfiya, wounds and bearing | `imposing`, `scarred` | +10 | +5 | +7.5 | More tangible condition; bearing still extrapolated backwards. |
| Zulu/Komfiya, strict earlier reputation | `brave` | +25 | 0 | +6.25 | Omits the later bearing inference and any unproven command speciality. |
| Mawa, office only | `basic_political_operator` | 0 | +5 | +5 | Avoids assuming an Elder popularity premium. |
| Nongalaza, office without a skill inference | None specified | 0 | 0 | 0 | Appropriate if a military-town appointment alone is judged insufficient. |
| Sotobe, chiefly administration | `basic_political_operator` | 0 | +5 | +5 | Less specific than the documented envoy role; no diplomatic popularity bonus. |
| Each opening child | No adult tags; inherited `trait_child` only | −25 | −25 | −31.25 | Combined age-state totals, unlike the adult-only zero rows above. |

## 4. What the native traits actually do

`character_modifier` applies regardless of role; `country_modifier` applies when the character is ruler; `interest_group_modifier` when IG leader; `command_modifier` applies in the documented command context to fully mobilised units. A court politician does not automatically confer a trait's ruler or army effects. The native `possible` block controls random selection and does not invalidate an authored acquired trait. These facts explain applicability, not historical suitability. [2]

| Trait | Universal effects beyond Q/R | Material ruler effect | Material command effect | IG-leader effect |
|---|---|---|---|---|
| `reserved` | Health +0.05; careful-manoeuvre modifier +1 | None | Morale loss −10%; naval critical-hit chance −10% | None |
| `basic_political_operator` | None | Authority +5% | Coup strength +5% | Political strength +5% |
| `experienced_political_operator` | None | Authority +10% | Coup strength +10% | Political strength +10% |
| `elder` | None | Two native country blocks: see note below | Supply use −10%; offence/defence in owned provinces +10% | Government approval +2; opposition approval −2 |
| `imposing` | Aggressive-manoeuvre modifier +1 | Infamy decay −25% | Morale loss −10% | Government approval +1; opposition approval −1 |
| `brave` | Health −0.05 | Army/navy power-projection prestige +5% | Morale loss −10%; naval vulnerability +25%; naval critical-hit chance +15% | None |
| `basic_diplomat` | None | Influence +5% | Morale recovery +25% | None |
| `scarred` | Health −0.1 | None | None | None |
| `ruthless` | None | Authority +5%; piracy-income modifier +0.05 | No command block giving combat lethality | Political strength +15% |
| `tactful` | None | Improve-relations speed +20% | Defence +5 flat; morale damage −5% | Attraction +2%; approval +1 |

This table reports effects relevant to distinguishing the proposed characters' roles; agitator and company-executive effects are not a prediction of opening court behaviour. In particular, Ruthless has executive throughput/mortality effects, not an automatic army killing bonus. [2]

The installed `elder` definition contains two `country_modifier` blocks: one lists peasants' political strength +15% and farmers' +10%; another lists prestige −5%, infamy decay −50% and authority +100. Their runtime composition was not tested. Neither proposed opening Elder is a ruler, so this uncertainty does not change the preferred opening-role arithmetic. Elder is a **skill**, not an automatic age condition. Its popularity bonus is an interpretation of recognised standing. [2]

Three mechanical traps matter for later decisions. First, **Popular Commander gives no direct popularity**: it supplies universal command limit +20%, conditional ruler prestige +10%, IG political strength +2%, and agitator movement attraction +5%. Celebrity Commander does add +30 popularity, but its command-celebrity meaning and extra role effects make it a poor substitute for an ordinary victorious king's reputation. Second, Basic Offensive Planner and Basic Defensive Strategist each place their **+5 popularity inside `command_modifier`**, not the universal block. Their universal Q/R totals are 0/0; any applied command popularity would nominally contribute another +1.25 E, but that placement's runtime behaviour has not been verified. Third, neither speciality was established for the opening characters by the evidence inspected. If earned later, their offence +5% or defence +10% should reflect that later command history. [2]

An empty trait list is **not sufficient to guarantee an unspecified package**. The native default generation supplies random personality/skill traits to adults with zero trait value, adds `trait_child` to non-adults, and can add further skills to older characters. Implementation should deliberately control generation for these authored templates while preserving childhood and intended progression. That is an implementation requirement revealed by inspection, not a change made by this brief; a global default-template rewrite would exceed this task. [2]

## 5. Dingane's durable reputation arc

Represent campaign achievement as **earned political reputation**. A permanent character trait or permanent character popularity modifier for each victorious campaign is appropriate; the reward belongs to the surviving ruler whose campaign outcome was achieved. Its text should credit victory or restored authority, not a witnessed personal feat that the event never established. Keep the two campaign rewards identifiable and non-repeatable in implementation.

This need not add `brave`, `honorable`, a diplomatic skill or a commander-speciality trait. Those labels carry different historical claims. A political-operator promotion can separately express demonstrated coalition management, but its +5 direct prominence step supplies no universal popularity; it cannot by itself fulfil a positive-popularity promise. Retain supported temperament after success: a reserved ruler can become well regarded. [2]

For the preferred intrinsic **Q = −25**, the parent's provisional design of an authored **−25 contested-accession/reputation modifier**, cleared on the first victory, and **two permanent +30 popularity achievements** gives:

| State | Explicit arithmetic, before unrelated modifiers or bounds | Popularity subtotal |
|---|---|---:|
| Opening | −25 intrinsic −25 authored reputation | −50 |
| First of the two campaign victories | −25 intrinsic +30 earned; opening penalty removed | +5 |
| Both campaign victories | −25 intrinsic +30 +30 | +35 |

That is an **85-point turnaround**, of which 25 comes from removing the opening modifier. The arithmetic illustrates the independent historical recommendation; it is not evidence for any of those authored reputation values. A label such as *Contested accession* should be understood as SB's political framing, not proof of unanimous historical rejection or a settled constitutional judgement that Dingane was a usurper.

The native threshold constants are −50/−25/+25/+50, with popularity bounded at −100/+100. They do not by themselves establish how exact equality is labelled in the UI. The parent reports that DP's earlier tooltip showed **Neutral (25)**; this research pass did not independently reproduce that observation. Therefore **do not certify +25 as Liked**. The +35 illustration leaves a margin above the positive threshold constant; DP still needs to verify the displayed category and other active modifiers in game. A −50 opening is likewise a subtotal at a boundary, not an independently verified guarantee of the displayed Hated label. [2]

For comparison, the earlier +25-per-victory proposal would give −50 → 0 → +25 and a 75-point turnaround, but sits on the disputed positive boundary. If the coercion-centred intrinsic alternative is selected, recalculate honestly: with Q = −15, the same −25/+30/+30 design gives **−40 → +15 → +45**; with Q = −40, it gives **−65 → −10 → +20**. The latter does not reach the +25 positive threshold constant after both victories. Do not select traits merely to make a reward schedule convenient.

A lasting defeat reputation penalty is also a coherent design interpretation of a failed campaign, rather than a forced change of personality. Under the parent's provisional −20 permanent popularity penalty per defeat, the preferred opening popularity subtotal becomes **Q = −90 after two defeats**, assuming the −25 opening penalty remains. The separately proposed **−10 immediate Prerogative P shock per defeat is not a popularity change**: it must not be added to Q. P then follows the court's own drift towards its recalculated target. No historical source supplies these magnitudes. The event implementation and Prerogative dynamics belong to the companion design work, not this historical recommendation.

## 6. Research method, source appraisal and access limits

The search was targeted to names, aliases, offices, childhood chronology, pre-1836 acts and oral characterisation. Representative concepts included Dingane/“reserved”/izibongo, Mkabayi/royal women, Gqugqu/1843, Mawa/Ntonteleni, Nongalaza/Gardiner, Sotobe/Sothobe/1828 embassy, and Zulu/Komfiya/kaNogandaya/Mkehlengana. English-language scholarship and English translations were inspected; isiZulu praise lines were read as presented by their editors and historians, without claiming a fresh philological translation.

Discovery used multiple routes: general web scholarly discovery to publisher/journal records (Cambridge, Springer, Taylor & Francis, SciELO, Inkanyiso); direct institutional searching and reading in UCT's eMandulo/FHYA and Killie Campbell/JSA material; public-domain editions and catalogue records through Internet Archive/Smithsonian; and an identified author upload for Peires. The four existing SB briefs dated 18, 19 and 24 October supplied discovery trails and identity leads only. They were not evidence that an existing trait was correct. Backward references led to the actual Gardiner, Isaacs and JSA passages; later historiographical work was sought to test hostile and favourable readings.

| Source group | Material actually inspected | Principal limitation |
|---|---|---|
| Isaacs and Gardiner [3], [4] | Public-domain full texts; relevant passages and bibliographic material closely read, not every page analysed | Early witnesses, but interested colonial authors; distinguish observation, reported speech and speculation within each account |
| Shamase on Mpande and Mkabayi [5], [6] | Full journal texts, with targeted reading | Later synthesis of mixed sources; interpretive confidence and exact genealogical/date claims vary |
| Mkehlengana in JSA [7] | Full edited entry and volume front matter | Recorded 1905, edited/translated for the 1982 volume; earlier campaigns transmitted, later bearing personally recalled |
| Hughes [8] | Institutional author-reformatted thesis; relevant chapter and notes | Author explicitly warns that reformatting changed pagination; cited pages refer to that deposited text |
| Peires [9] | Publisher metadata/abstract and identified author-deposited full text | Author-uploaded early version has different pagination; detailed motive argument remains interpretation |
| Ndlovu thesis [10] | Full institutional PDF; introduction and relevant early chapters/passages closely read | Many oral statements accessed through the thesis, not independently in original notebooks |
| Okoye [11] | Publisher bibliographic record and extract only | Used solely for the stated historiographical challenge; no claim to have read full article |
| Grobler [12] | Full SciELO article | Retrospective reconstruction of 1838; includes moral judgements and evidence of unequal proximity |
| Ndlovu's later book chapter [13] | Publisher metadata and abstract only | Supports the existence/scope of the later multi-perspective treatment; no detailed claims borrowed from unseen book text |

Oral tradition is historical evidence, not a synonym for invention. Attribution, transmission, genre and audience matter: izibongo can praise, criticise, warn and negotiate authority within the same composition. A son's family account, a court praise performance and a late interview provide different kinds of access. Colonial written witnesses also mediate language, pursue interests and repeat hearsay. Agreement between two historians who use the same oral passage is not independent corroboration. Ndlovu's later chapter explicitly frames the archive through multiple African perspectives; only its abstract was available here. [13]

Publisher and repository records verified the listed titles, authors, dates and identifiers. No authorised institutional subscription session was available; inaccessible full texts were not bypassed. No shadow-library copy was used. The chapter DOI and e-book ISBN below are attached to the correct 2017 book, not substituted for the 2001 thesis. Original 1836 editions have no contemporary ISBN; no later reprint ISBN is attached to them.

## 7. Open gaps and verification boundary

1. **1836 public opinion cannot be quantified.** Neither “despised” nor any positive score is an empirically measured share of supporters. Distinguish king, court factions, ordinary subjects and later narrators.
2. **Gqugqu's early personal record is thin.** His later succession strength should not determine an opening personality or a fully mobilised 1836 faction. Verify name/parentage before joining similarly rendered princes in early travel accounts.
3. **Exact ages remain uncertain.** Sotobe's seniority, Mkabayi's birth year and the approximate added-court ages deserve a dedicated chronological check if portraits or age-dependent mechanics become central.
4. **Komfiya's 1836 location and the dating of his bearing are unresolved.** The son establishes the identification and transmitted martial reputation; he cannot personally witness a pre-birth campaign. Brave alone is available if the later bearing inference is considered too strong.
5. **Military specialisation needs its own evidence.** Office, courage, bodily wounds and successful armies are not interchangeable evidence for offensive planning, defensive doctrine or personal combat.
6. **Several oral originals remain uninspected.** The source chain for each mediated statement is stated; a future deeper pass should compare the relevant isiZulu texts and Stuart notebooks/edited entries directly, rather than treating later English summaries as identical testimonies.
7. **Numbers are statically verified, not engine-tested.** The brief inspects installed files and checks package arithmetic. It does not establish live trait generation, modifier composition, rounding, threshold equality or final court-role totals. No game was launched and no gameplay sources were changed.

The practical next step is to choose among the expressly bounded packages, then implement deterministic template generation and the separate reputation arc. Historical uncertainty should remain visible in the design record instead of being replaced with extra traits.

## References

[1] Spes Bona, “Zulu opening character history and authored templates,” local working tree, inspected Oct. 25, 2026. [Opening history](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/history/characters/zul - zulu.txt>), [dynasty templates](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/character_templates/sb_zulu_dynasty_characters.txt>), [court templates](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/character_templates/sb_court_characters.txt>), and [court modifiers](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/static_modifiers/sb_court_modifiers.txt>). Inherited identities checked against Paradox Interactive, [installed `country_zul.txt`](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_templates/country_zul.txt>). Implementation evidence only.

[2] Paradox Interactive, *Victoria 3*, installed character-definition files, inspected Oct. 25, 2026. [Personality traits](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_traits/personality_traits.txt>), [skill traits](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_traits/skill_traits.txt>), [condition traits](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_traits/condition_traits.txt>), [trait scope documentation](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_traits/character_traits.md>), [defines](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt>), [automatic roles](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_roles/00_auto_assigned_roles.txt>), [appointment roles](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_roles/01_appointment_roles.txt>), and [default trait generation](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_templates/00_default_template.txt>). Local version inspected; engine behaviour not inferred beyond the stated limits.

[3] N. Isaacs, *Travels and Adventures in Eastern Africa, Descriptive of the Zoolus, Their Manners, Customs, etc. etc., with a Sketch of Natal*, vol. II. London: Edward Churton, 1836. [Online]. Available: [UCT eMandulo public-domain original](https://emandulo.apc.uct.ac.za/collection/FHYA%20Depot/Isaacs_Nathaniel_Travels_and_adventures_in_eastern_Africa_vol_2.pdf). Relevant original pagination: pp. 279–282. Residence chronology cross-checked with [HiPSA's edition description](https://hipsa.org.za/publication/travels-and-adventures-in-eastern-africa-by-nathaniel-isaacs-2/); the cited pages belong to the 1836 original, not that later edited edition.

[4] A. F. Gardiner, *Narrative of a Journey to the Zoolu Country, in South Africa. Undertaken in 1835*. London: William Crofts, 1836. [Online]. Available: [Internet Archive public-domain scan](https://archive.org/details/narrativeofjourn00gard_0), [full OCR consulted](https://archive.org/download/narrativeofjourn00gard_0/narrativeofjourn00gard_0_djvu.txt), and [UCT catalogue record](https://emandulo.apc.uct.ac.za/metadata/FHYA%20Depot/1188/1238/index.html). Page references use printed pagination, not OCR line numbers.

[5] M. Z. Shamase, “The nature and extent of the Zulu military engagements under Emperor Mpande,” *Military History Journal*, vol. 16, no. 4, Dec. 2014. [Online]. Available: [South African Military History Society full text](https://samilitaryhistory.org/vol164ms.html). No DOI verified.

[6] M. Z. Shamase, “The royal women of the Zulu monarchy – through the keyhole of oral history: Princess Mkabayi Kajama (c.1750–c.1843),” *Inkanyiso: Journal of Humanities and Social Sciences*, vol. 6, no. 1, pp. 15–22, 2014, doi: [10.4102/ink.v6i1.241](https://doi.org/10.4102/ink.v6i1.241). [Journal record](https://inkanyisojournal.org/index.php/ink/article/view/241); [full text inspected](https://inkanyisojournal.org/index.php/ink/article/download/241/347). The current journal platform also displays later migration metadata; the article and issue are dated 2014.

[7] Mkehlengana kaZulu, testimony recorded Apr. 18–21, 1905, in C. de B. Webb and J. B. Wright, Eds., *The James Stuart Archive of Recorded Oral Evidence Relating to the History of the Zulu and Neighbouring Peoples*, vol. 3. Pietermaritzburg and Durban: University of Natal Press and Killie Campbell Africana Library, 1982, pp. 210–221. ISBN 978-0-86980-287-8. [Online]. Available: [institutional edited testimony](https://emandulo.apc.uct.ac.za/collection/KCAL/3_VOL3/KCAL_JSAVol3_1982_edited_notes_Mkehlengana_ka_Zulu_092_p210_p221.pdf), [volume front matter](https://emandulo.apc.uct.ac.za/collection/KCAL/3_VOL3/KCAL_JSAVol3_1982_front_matter.pdf). Identity and martial passages: pp. 210–212.

[8] H. Hughes, “Politics and society in Inanda, Natal: The Qadi under Chief Mqhawe, c.1840–1906,” Ph.D. dissertation, University of London, Oct. 1995. [Online]. Available: [institutional author-reformatted full text](https://emandulo.apc.uct.ac.za/collection/Cele/publications/Politics_and_society_in_Inanda_Natal_the%20Qadi_chief_under_Mqhawe_%28HHughesPhD%29.pdf). Relevant pp. 53–54 refer to this reformatted version; its notice warns that pagination differs from the original thesis.

[9] J. Peires, “A buffalo on the banks of the Mzimvubu: The Zulu invasions of Mpondoland, 1824 and 1828,” *Journal of Natal and Zulu History*, vol. 34, no. 1, pp. 56–83, 2021, doi: [10.1080/02590123.2021.1994749](https://doi.org/10.1080/02590123.2021.1994749). [Publisher record](https://www.tandfonline.com/doi/abs/10.1080/02590123.2021.1994749); [author-deposited full text inspected](https://www.researchgate.net/publication/356887316_A_Buffalo_on_the_Banks_of_the_Mzimvubu_The_Zulu_Invasions_of_Mpondoland_1824_and_1828). Deposit identified as uploaded by Jeff Peires; the deposited pagination differs from final issue pagination.

[10] S. M. Ndlovu, “The changing African perceptions of King Dingane in historical literature: A case study in the construction of historical knowledge in 19th and 20th century South African history,” Ph.D. dissertation, University of the Witwatersrand, 2001. [Online]. Available: [institutional full text](https://emandulo.apc.uct.ac.za/collection/FHYA%20Depot/Theses%20and%20Dissertations/Ndlovu_Sifiso_The_Changing_African_Perceptions_ofKing%20Dingane.pdf). Relevant pp. 8–24. Original testimony quoted or analysed there remains mediated unless separately identified as inspected above.

[11] F. N. C. Okoye, “Dingane: A reappraisal,” *The Journal of African History*, vol. 10, no. 2, pp. 221–235, 1969, doi: [10.1017/s002185370000949x](https://doi.org/10.1017/s002185370000949x). [Publisher record and extract inspected](https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/dingane-a-reappraisal/16F30C648B56730FC0D957F534C30109). **Extract only.**

[12] J. Grobler, “The Retief Massacre of 6 February 1838 revisited,” *Historia*, vol. 56, no. 2, Nov. 2011. [Online]. Available: [SciELO full text](https://www.scielo.org.za/scielo.php?pid=S0018-229X2011000200007&script=sci_arttext). No DOI verified.

[13] S. M. Ndlovu, “Magolwane kaMkhathini Jiyane and Mshongweni: Izibongo and the construction of King Dingane's archive,” in *African Perspectives of King Dingane kaSenzangakhona: The Second Monarch of the Zulu Kingdom*. Cham: Palgrave Macmillan, 2017, pp. 33–62, doi: [10.1007/978-3-319-56787-7_2](https://doi.org/10.1007/978-3-319-56787-7_2). Book e-ISBN 978-3-319-56787-7. [Publisher chapter record](https://link.springer.com/chapter/10.1007/978-3-319-56787-7_2). **Metadata and abstract only; full book not inspected.**
