# Zulu glossary pilot: four terms and safe contexts

**7 November 2026 · Research proposal reviewed by the main agent · Research checkpoint before implementation**

The revised definitions and preferred contextual links have passed main-agent
research review. See the [review record and Vanilla comparison](zulu_glossary_review_2026_11_07.md)
for accepted scope, corrections and verification limits.

DP subsequently authorised implementation of these four definitions and links.
The [implementation record](../compatibility/1_15_0_zulu_glossary_pilot_2026_11_07.md)
tracks the delivered files and checks; this brief retains the research evidence
and period limits. Existing review classifications remain in force.

## Executive summary

The four terms can support a small historical glossary, provided that the definition of a word is kept distinct from the identity of the actor to which a link is attached.

- **Amabutho:** explain age groupings, including the men's military and labour service. The wider institution included female groups; a definition confined to a standing male army would mislead. [1, manuscript pp. 2–5]
- **amaKhosi:** explain the plural of *inkosi*, a chief or ruler. “Great Chiefs” is SB's movement label, not an exact translation of the bare word. [2, senses 1a and 2]
- **uSuthu:** explain Cetshwayo's following and its later association with Dinuzulu. The sources do not establish its use as a timeless name for every royalist movement from 1836. [3, pp. 105–106, 121 n. 9]
- **Umkhosi:** the short name is attested for the first-fruits festival. A definition explicitly about the nineteenth-century Zulu royal ceremony fits the intended royal gathering; it should not describe every chiefly assembly or imply uninterrupted institutional continuity through 1936. [4], [5, pp. S32–S34], [6, p. 64 n. 4]

Prefer a few contextual links: Amabutho in the institutional explanation, amaKhosi where the chiefly movement is explained, uSuthu in the existing Cetshwayo–Mbuyazi event branch, and “first fruits” in the royal gathering's description. The glossary itself can remain readable in any game year. Historical availability of a reference entry does not justify applying its name to an incompatible present actor.

## Introduction

This brief supports a decision on four proposed entries and their first link locations in *Spes Bona*. Its historical horizon is **1836–1936**, with earlier context only where it clarifies a word. It does not redesign movements, court laws, succession, Prerogative or the existing Thirteen Chiefdoms concept. All tooltip drafts below are original proposals.

The working assumption is a **Zulu-context pilot**, not a common glossary for every southern African institution. Current source is narrower than the generic filenames suggest: `common/scripted_triggers/sb_institutions_triggers.txt:2–3` admits the Zulu dynasty or its stored profile. `common/scripted_triggers/sb_firearms_triggers.txt:12–19` includes ZUL and NGN only when the latter has inherited Zulu content. The profile is copied into constitutional rebels at `common/scripted_effects/sb_court_constitutional_war_effects.txt:21` and dynastic rebels at `common/scripted_effects/sb_court_dynastic_effects.txt:417`. These are Zulu-content successor contexts, not evidence that another culture historically possessed identical institutions.

## Research approach

This was a **targeted review on 7 November 2026**, not a systematic survey. Two independent discovery routes were used: scholarly publisher/institutional repositories, and the historical *Dictionary of South African English* (DSAE), followed by inspection of edited oral testimony through UCT's Emandulo archive. Web searches combined the four terms and spelling variants with *regiment*, *labour*, *Cetshwayo*, *Dinuzulu*, *first fruits* and *revival*. Searches also checked later uses and the evidential basis of origin claims.

Pivotal source passages were read in full text. Search snippets and inaccessible works supplied leads only. DSAE establishes documented English usage of isiZulu loans; it is not a complete historical isiZulu corpus. Its *ibutho* entry documents the plural and an 1836 usage, while *Usutu* distinguishes a battle cry from a noun for royal adherents. [7, sense 1], [8, senses A–B] The Stuart materials require particular care: African testimony, a colonial recorder's questions and notes, translation, and subsequent editorial organisation all contribute to the published text. [9, pp. 144–146]

| Evidence | Text actually inspected | Quality and appropriate use |
| --- | --- | --- |
| [1] Van der Merwe and Pikirayi, 2019 | Institutional manuscript, especially numbered pp. 2–5; metadata checked against Pretoria's article record. | Peer-reviewed archaeological study combining excavation, historical and ethnographic material. Strong for institutional breadth; its summary is not proof that every local affiliation disappeared or that a fixed age/service rule applied uniformly. Manuscript pages are not journal pages. |
| [2], [4], [7], [8] DSAE entries | Complete entries, senses, forms and dated quotations. | Authoritative historical lexicography. Useful for meaning and spelling; quotations from later fiction are not independent evidence of nineteenth-century practice, and the earliest listed quotation is not an institution's foundation date. |
| [3] *James Stuart Archive*, vol. 3 | Mgidhlana, printed pp. 102–113; Mgqibelo and Nguna, pp. 119–121, including separately identified editorial notes. | Edited primary testimony with traceable dates. Retrospective and politically situated; multiple excerpts from this volume are not independent modern scholarship. |
| [5] Snedegar, 1998 | Publisher's full article obtained; discussion on pp. S31–S37 read, especially S32–S34. | Peer-reviewed comparative study. The author expressly combines Zulu and Swazi practices in part of the account: only explicitly Zulu material is used for the proposed entry. |
| [6] Rautenbach, 2011 / PDF edition 2014 | Full chapter available; relevant passages on pp. 64–65 and 75–77 inspected, particularly p. 64 n. 4 and p. 75 n. 84. | Scholarly legal/religious analysis of the modern revival. Useful as a warning against continuity assumptions; its historical footnotes do not establish a complete nineteenth-century chronology. |
| [9] Wright, 2015 | Full text available; methodological discussion pp. 144–146 and the colonial faction context inspected. | Specialist historical analysis by an editor of the Stuart archive. Strong on provenance and mediation; not independent of the archive it evaluates. |

Lawful public copies of [1], [3], [5] and [6], with extracted text and access notes, are retained in `generated/zulu_glossary_research_2026_11_07/agent/`. The Weir thesis used in an earlier SB investigation could not be retrieved during this pass; no new claim here depends on that earlier summary.

## Findings and proposed definitions

### Amabutho

**Attested meaning.** *Amabutho* is the plural of *ibutho*. In the Zulu kingdom the organisation brought together age groups for service, including men's warfare and labour. Female amabutho also existed; only some of their members resided in royal enclosures. [1, manuscript pp. 2–5], [7, sense 1] This supports explaining the wider institution while making the military modifier's particular relevance clear.

**Period and confidence.** High confidence for this bounded nineteenth-century meaning and its presence at the game's opening; DSAE's 1836 example is an attestation, not an onset date. [7] The evidence examined does not establish a uniform survival, abolition date or service regime throughout 1836–1936. Use a historical description; do not introduce a calendar cutoff or treat modern uses as the same institution.

**Name and aliases.** Preserve the existing display **Amabutho**; use *amabutho* in running prose. *ibutho* is the singular, not a different institution. DSAE records initial/medial capitalisation and older spellings; they are search variants, not a reason to change SB's display. [7]

**Proposed short tooltip:**

> ***Amabutho*** are regiments organised by age; the singular is *ibutho*.
>
> In the nineteenth-century Zulu kingdom, the men's regiments brought together recruits from different communities for military service and labour under the king. Women also formed amabutho within the wider system.

Basis: [1, manuscript pp. 2–5]. This definition does not assign a political alignment or reproduce the army law's effects.

| Candidate location, current line | Classification | Proposed treatment |
| --- | --- | --- |
| `localization/english/sb_institutions_l_english.yml:20`, `sb_institutional_reach_breakdown` | General, non-event/JE; existing general review tracking | Preferred body-text candidate: link the existing **Amabutho** in the final reform sentence. It explains an unfamiliar institution where the player reads about its removal. |
| Same file, line 7, `sb_prerogative_military` | General, non-event/JE | Alternative: link only **Amabutho** in the modifier name, subject to a readable nested glossary after implementation. Current application additionally requires `law_sb_amabutho_system` at `common/scripted_effects/sb_institutions_effects.txt:52–53`. Actual rendering and nested hover behaviour remain unverified. |

**Exclude/defer:** automatic links in unrelated countries' army laws or a future shared profile; a universal “African regimental system” definition; changed mechanics, obligatory service ages or an unsupported foundation date.

### amaKhosi

**Attested meaning.** DSAE gives *amakhosi* as a plural of *inkosi*, “chief or ruler”. It separately records *inkosi inkulu* as a great chief/king. Thus the bare plural does not itself mean “Great Chiefs”, identify a constitutional programme, or establish one permanent organised faction. [2, senses 1a and 2] The last point is a semantic inference, not evidence against particular chiefs acting together.

**Period and confidence.** High confidence in the lexical meaning. The entry includes nineteenth- and early twentieth-century *inkosi* attestations; it cannot demonstrate that chiefly offices had identical powers throughout the century. [2] Keep the entry lexical rather than defining SB's Chiefly Council or Federated Chiefdoms.

**Name and aliases.** Preserve SB's **amaKhosi** for this pilot. Record *amakhosi* and singular *inkosi* as lexical forms. Keeping the internal capital is our choice to preserve SB's current display; it makes no claim about a universal orthographic rule or a rank distinction. “Great Chiefs” should remain an explicitly separate SB label decision.

**Proposed short tooltip:**

> ***amaKhosi*** are chiefs or rulers in isiZulu-speaking communities. The singular is *inkosi*.

Basis: [2]. No movement programme is embedded in the definition.

| Candidate location, current line | Classification | Proposed treatment |
| --- | --- | --- |
| `localization/english/sb_institutions_l_english.yml:22`, `sb_court_movements_breakdown` | General, non-event/JE | Preferred: link the first **amaKhosi** while leaving the adjacent explanation clearly about SB's named movement. This makes the word's meaning available alongside the game's programme. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml:12`, `movement_sb_zulu_chiefly` | General, non-event/JE | Alternative: link only **amaKhosi**, retaining the current display “amaKhosi — Great Chiefs”. Inspect `_name` substitution at line 13 and widget wiring before implementation; test the displayed movement name and hover afterwards. |

**Exclude/defer:** treating all chiefs as federalists or opponents of a king; renaming the movement under cover of a glossary change; duplicating `concept_sb_zulu_chiefdoms` or the two law descriptions. A decision on “Great Chiefs” can be taken independently.

### uSuthu

**Attested usage.** Mgidhlana's account recorded on 23 February 1912 places the name's emergence during the quarrel between Cetshwayo and Mbuyazi under Mpande. It supplies no secure calendar onset. The 1907 Mgqibelo/Nguna account uses a related English form for adherents; the editors distinguish Cetshwayo and Dinuzulu's cause from Zibhebhu's in their note. [3, pp. 105–106, 119, 121 n. 9] DSAE also records a broader royal-house/adherent sense, with later attestations, alongside the battle-cry sense. That broader lexical use exists; it does not by itself establish that the name fits every ruler's adherents from 1836. [8, senses A–B]

**Period and confidence.** High confidence in the Cetshwayo/Dinuzulu association; moderate confidence in the retrospective account of the name's emergence. Do not turn 1852 into a verified first-use date or repeat an origin legend as established etymology. An entry about this historical following can be available before it arises; links naming a current faction need compatible actors and context.

**Name and aliases.** Preserve **uSuthu**. DSAE documents *Usutu*, *Usuthu* and *Usuto*; use those as spelling variants, not interchangeable names for all royalists. [8] The related place/homestead name *oSuthu* should not be an alias for the faction. [3, p. 121 n. 10]

**Proposed short tooltip:**

> The ***uSuthu*** were the political following of **Cetshwayo**, and later of his son **Dinuzulu**.
>
> The name was associated with Cetshwayo's struggle for the Zulu throne and continued to identify supporters of his royal cause.

Basis: [3, pp. 105–106, 121 n. 9], [8]. No biography or constitutional rules are needed.

| Candidate location, current line | Classification | Proposed treatment |
| --- | --- | --- |
| `localization/english/sb_court_succession_l_english.yml:52`, `sb_court_succession.007.d.usuthu` | **TO REVIEW event namespace** `sb_court_succession.007`, marker at line 44 | Preferred: link the existing **uSuthu**. `events/sb_court_succession_events.txt:218` selects this branch for a Mbuyazi heir and year ≥1852; lines 242–247 then identify the opposing brother as Cetshwayo. This is a context match, not historical validation of that date gate. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml:10`, `movement_sb_zulu_royal`; `localization/english/sb_institutions_l_english.yml:17–18,21–22` | General, non-event/JE | **Defer links.** These use uSuthu as a continuing general royal movement, including circumstances that need not concern Cetshwayo or Dinuzulu. The sources do not validate all those applications. A historical tooltip would not resolve this potential period/context mismatch. |

**Exclude/defer:** any silent rename or new date gate; extending the label without further evidence to Dingane's supporters, every rival prince's following, or every counterfactual royal movement. Decide the generic movement's naming separately. No claim is made that the term vanished on a particular date or could never carry a broader royal-house sense.

### Umkhosi

**Attested usage.** DSAE supports *Umkhosi/Umkosi* as a first-fruits festival, including an 1887 example. [4] Snedegar treats the Zulu royal ceremony's agricultural, ritual and political dimensions, including a specifically identified account of Cetshwayo's regiments in the 1870s. His surrounding reconstruction partly combines Zulu and Swazi evidence; the tooltip therefore omits its detailed ritual sequence. [5, pp. S32–S34]

**Period and confidence.** High confidence for a nineteenth-century Zulu royal first-fruits referent. Snedegar dates the last **full** Zulu observance to January 1879; this is a source claim, not proof that every related practice ceased then. [5, p. S32] Rautenbach reports interruption and revival, and distinguishes earlier little/big ceremonies from the modern form. [6, p. 64 n. 4, p. 75 n. 84] Continuity across 1879–1936 is insufficiently established for a timeless present-tense description or automatic cutoff.

**Name and aliases.** Retain **Umkhosi** as the existing attested short label, with **royal first-fruits festival** specifying the entry's sense. *Umkosi* is an attested spelling variant. [4] “First fruits” may be the displayed link text in this event, not a global alias for every harvest festival. Longer labels such as *Umkhosi Ukweshwama* occur in modern scholarship; this pilot does not establish a historically uniform full name requiring replacement of SB's title. [6]

**Proposed short tooltip:**

> ***Umkhosi*** was a royal first-fruits festival in the nineteenth-century Zulu kingdom.
>
> The king and his regiments gathered for rites marking the new harvest and affirming royal authority.

Basis: [4], [5, pp. S32–S34]. The glossary does not authenticate the event's particular system of allegiance declarations.

| Candidate location, current line | Classification | Proposed treatment |
| --- | --- | --- |
| `localization/english/sb_zulu_court_l_english.yml:4`, `sb_zulu_court.200.d` | **TO REVIEW event namespace** `sb_zulu_court.200`, marker at line 2 | Preferred: link the existing **first fruits** to this entry. This is the royal description; `events/sb_zulu_court_events.txt:9–10` gives Federated Chiefdoms a separate description. |
| Same file, line 81, `sb_court_gathering_royal` | General, non-event/JE, despite being selected by an event-title getter | Alternative: test a link on **Umkhosi** in “Umkhosi: Before the King” after implementation; retain it only if the title and hover render correctly. `common/customizable_localization/sb_court_custom_loc.txt:91–100` selects chiefly text for Federated Chiefdoms and otherwise the royal text. A getter does not confer the event namespace's review classification on this key. |

**Exclude/defer:** the “Gathering of the Chiefs” title and `.200.d.chiefs`; an equation with the Reed Dance or every Nguni ceremony; a fixed ritual calendar; retrospective use of modern revived practice as proof of nineteenth-century continuity. Other countries/regimes and post-conquest continuations require their own presentation decision.

## Discussion and implications

The useful distinction is between **reference prose**, **a live actor's name**, and **SB's rules**. A historically bounded entry may explain an older institution during an alternative history without asserting that the real institution survived in that form. It does not resolve whether an actor's label fits its period and context. This requires a separate decision for the generic uSuthu movement, as does the “Great Chiefs” translation implied by the chiefly movement's display.

The proposed definitions use the direct meaning followed by short context. The parent review owns the detailed installed Vanilla/CMF comparison and final wiring choice. These entries neither replace `common/game_concepts/sb_zululand_concepts.txt:1` nor explain its settlement mechanics. Prefer one useful initial link per entry over adding the same link to every numerical readout and choice tooltip.

Review classifications above follow the complete localisation policy: event markers classify exact event namespaces only. General keys remain general even when interpolated into events. Any accepted new glossary prose is general prose requiring `# TO REVIEW (non-event/JE keys)` tracking and a review-queue entry. Main-agent research acceptance is **not DP localisation approval**.

## Limitations and evidence gaps

The review does not establish a precise first-use date for uSuthu, a continuous history of ceremony practice through 1936, or one orthographic standard across historical and modern isiZulu. DSAE's English quotations are selective. Colonial observers and retrospective oral accounts must not be treated as transparent inventories of a timeless society; source mediation is particularly visible in the Stuart archive. [9, pp. 144–146] The short definitions deliberately omit disputed origins, numerical service rules and detailed ceremonial actions.

The UP manuscript was retrieved from its public institutional endpoint after the web reader failed; publisher copies similarly supplied the ceremony texts. Weir's thesis returned HTTP 403 and was not used substantively. No subscription access, shadow-library copies, gameplay run or rendered-tooltip validation is claimed. Source URLs, local copies, printed-page locators and access failures are recorded in the research scratch log.

## Recommendations

1. **Accept or revise the four draft definitions first.** They describe bounded historical referents and avoid introducing mechanics. Confidence is high for their core meanings; uSuthu's exact onset and later ceremonial continuity remain open.
2. **Select one placement per accepted entry.** Prefer the four body-text candidates above. Before implementation, verify source references, intended wording, event branches and widget/getter wiring. These source checks cannot certify rendered behaviour.
3. **Keep the naming questions separate.** Record the generic uSuthu movement's unvalidated period/context applications and “Great Chiefs” gloss as design decisions; do not quietly retrofit labels or date gates during the pilot.
4. **Only after main review, implement the accepted scope under the localisation policy.** Preserve review markers, track new general keys and run proportionate static checks. After implementation, DP must inspect the actual displayed wording, hover activation and nested tooltips in the game; those checks remain pending until then. Leave game launch to DP.

## References

[1] R. H. van der Merwe and I. Pikirayi, “The organisation and layout of Zulu military homesteads (amakhanda),” *Azania: Archaeological Research in Africa*, vol. 54, no. 1, pp. 75–93, 2019, doi: [10.1080/0067270x.2018.1540218](https://doi.org/10.1080/0067270x.2018.1540218). [University of Pretoria record](https://repository.up.ac.za/items/b33ed121-c4be-4e87-a626-f9639ef78946); [repository manuscript inspected](https://repository.up.ac.za/bitstream/2263/74128/1/VanDerMerwe_Organisation_2019.pdf). Pinpoints in this brief refer to the manuscript's own numbered pages.

[2] Dictionary Unit for South African English, “Inkosi, n.,” *Dictionary of South African English*, 2025. [Online]. Available: [entry](https://dsae.co.za/entry/inkosi/e03298). [Accessed: Nov. 7, 2026].

[3] C. de B. Webb and J. B. Wright, eds., *The James Stuart Archive of Recorded Oral Evidence Relating to the History of the Zulu and Neighbouring Peoples*, vol. 3. Pietermaritzburg: University of Natal Press, 1982. Consulted through Emandulo's institutional reproductions: [Mgidhlana ka Mpande, pp. 102–113](https://emandulo.apc.uct.ac.za/collection/KCAL/3_VOL3/KCAL_JSAVol3_1982_edited_notes_Mgidhlana_ka_Mpande_079_p102_p113.pdf) and [Mgqibelo and Nguna, pp. 119–121](https://emandulo.apc.uct.ac.za/collection/KCAL/3_VOL3/KCAL_JSAVol3_1982_edited_notes_Mgqibelo_and_Nguna_082_p119_p121.pdf). An ISBN-13 for this exact scanned edition was not independently verified; a retailer's modern reprint identifier is not substituted.

[4] Dictionary Unit for South African English, “Umkhosi, n.,” *Dictionary of South African English*, 2025. [Online]. Available: [entry](https://dsae.co.za/entry/umkhosi/e07471). [Accessed: Nov. 7, 2026].

[5] K. Snedegar, “First Fruits Celebrations Among the Nguni Peoples of Southern Africa: An Ethnoastronomical Interpretation,” *Journal for the History of Astronomy*, vol. 29, Archaeoastronomy suppl. 23, pp. S31–S38, 1998, doi: [10.1177/002182869802902304](https://doi.org/10.1177/002182869802902304). [Publisher's full issue inspected](https://www.shpltd.co.uk/aa.pdf).

[6] C. Rautenbach, “Umkhosi Ukweshwama: Revival of a Zulu Festival in Celebration of the Universe's Rites of Passage,” in *Traditional African Religions in South African Law*, T. W. Bennett, ed. Cape Town: UCT Press, 2011, pp. 63–89; PDF edition 2014, ISBN 978-1-92054-123-1. Container doi: [10.58331/uctpress.28](https://doi.org/10.58331/uctpress.28). [Publisher record](https://openuctpress.uct.ac.za/uctpress/catalog/book/28), posted Apr. 8, 2022; [PDF inspected](https://openuctpress.uct.ac.za/uctpress/catalog/download/28/34/124?inline=1). The PDF copyright page distinguishes print 2011 from PDF publication 2014; repository posting is not the chapter's original date.

[7] Dictionary Unit for South African English, “Ibutho, n.,” *Dictionary of South African English*, 2025. [Online]. Available: [entry](https://dsae.co.za/entry/ibutho/e03157). [Accessed: Nov. 7, 2026].

[8] Dictionary Unit for South African English, “Usutu, interj. and pl. n.,” *Dictionary of South African English*, 2025. [Online]. Available: [entry](https://dsae.co.za/entry/Usutu/e07538). [Accessed: Nov. 7, 2026].

[9] J. Wright, “Socwatsha kaPhaphu, James Stuart, and Their Conversations on the Past, 1897–1922,” *Kronos*, vol. 41, no. 1, pp. 142–165, Nov. 2015. [Article](https://www.scielo.org.za/scielo.php?pid=S0259-01902015000100006&script=sci_arttext); [published PDF](https://scielo.org.za/pdf/kronos/v41n1/06.pdf). No DOI was verified in the journal metadata inspected.
