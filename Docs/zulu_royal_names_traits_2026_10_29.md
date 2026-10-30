# Zulu royal names, the two brothers, and Hamu

**Decision record, 29 October 2026.** Scope: the current Zulu court implementation, period name generation and a historically defensible Cetshwayo balance adjustment. No new succession storyline, birth-date revision or save migration is included.

## Decisions

- Use documented patronymics for named historical royals, retaining their existing template identities. Use clan names for generated surnames, so a random courtier is not presented as a son of Mpande or Senzangakhona.
- Give Cetshwayo **Charismatic on reaching adulthood**, not in his childhood template. This is an interpretation of his ability to gather support; its +50 Popularity is a balance choice, not a measured historical quantity.
- Retain Mbuyazi's existing event-awarded Ambitious. Do not invent a negative personality package merely because he lost the succession struggle.
- Keep the existing Hamu kaNzibe identity and 1865 introduction. The current autosave is too early for this authored character; its two Hamus are generated namesakes.

## Evidence and trait judgement

Cetshwayo developed substantial support while Mpande favoured Mbuyazi. The rivalry became open conflict in 1856, with John Dunn assisting Mbuyazi. The broad outline supports differentiated coalitions, rather than making Mbuyazi personally incapable. SAHO's synthesis supports that comparison but contains chronological compression and should not supply every precise date. [1]

Shamase's oral-history study describes Cetshwayo's following among young men, royal regiments and important chiefs, including Masiphula and Maphitha. It also preserves competing accounts of the factions' origins and Mbuyazi's maternal support. These are evidence of networks and remembered political appeal, not an objective personality test. The account associates Cetshwayo's military reputation with the 1852 Swazi campaign: adding Brave to him as a child would backdate that achievement. [2, pp. 10–11]

| Character | Implemented judgement | What remains deliberately unasserted |
|---|---|---|
| Cetshwayo | Charismatic from the first adult court pulse; retain any Ambitious awarded by the brothers' event. | No childhood military achievement, automatic genius command trait or permanent claim that every Zulu supported him. |
| Mbuyazi | Keep the existing sparse childhood template and scenario-earned Ambitious. | Defeat does not establish Cowardly, Inept, Cruel or Unpopular. His father's preference and outside allies are represented by backing and events. |

Granting Charismatic at 16 is an **authored developmental timing choice**. The stronger historical evidence concerns the 1850s; the earlier grant gives DP the requested support advantage while the succession rivalry develops. It neither changes his constitutional allegiance nor forces a future civil-war result.

Cope's reassessment cautions against taking hostile colonial depictions of Cetshwayo's reign at face value. Its publisher abstract was inspected; the full article was not available in this pass. It supports caution over imported stereotypes, not a finding that Cetshwayo was uniformly benevolent. [3]

### Native effects checked against installed 1.14.5

These are the shipped definitions, not inferred from trait names. Role-specific effects apply when the character holds that role.

| Trait | Character | Ruler | Commander | IG leader |
|---|---|---|---|---|
| **Charismatic** | +50 Popularity | +5% Influence | +10% Morale Recovery | +20% Pop Attraction |
| Ambitious | +10 Prominence | +10% army/navy power-projection Prestige; −25% decree cost | +5% Offence; −0.05 recovery-rate addition; +25% ship critical-hit chance; +5% native coup strength | +10% Political Strength |
| Imperious | −35 Popularity; +10 Prominence | −20% decree cost; +10% movement Loyalists; −20% movement Radicals | −15% Morale Loss and Recovery; +100% aggressive-manoeuvre battle-condition factor; +5% native coup strength | +25% Pop Attraction |
| Basic Diplomat | +10 Popularity | +5% Influence | +25% Morale Recovery | N/A |

Vanilla's later `ZUL_cetshwayo` template contains Ambitious, Imperious and Basic Diplomat: **−25 net Popularity and +20 direct Prominence**. SB uses its existing `ZUL_cetshwayo_heir` identity instead. Copying the full later package would undermine the requested Popularity advantage and give the child an adult résumé.

Native `PROMINENCE_FROM_POPULARITY = 0.25` means Charismatic's +50 Popularity can also add **12.5 Prominence**, before native limits and other effects. The trait therefore changes both annual allegiance probabilities and the actual coalition weights; it is not a hidden fixed support modifier. Check both effects in the balance pass. It is incompatible with Reserved; the authored child template starts with neither.

Local sources: `game/common/character_templates/country_zul.txt`, `game/common/character_traits/personality_traits.txt`, `skill_traits.txt`, and `game/common/defines/00_defines.txt`. These were read from the installed game, not copied from an older wiki version.

## Historical display names and generated names

Zulu personal naming distinguishes a given name, lineage and clan association. A patronymic such as `kaSenzangakhona` identifies a parent; it is not an interchangeable generic surname. Ngubane and Thabethe explicitly discuss genealogical names and give historical naming examples. Their study also records names spanning the eighteenth to early twentieth centuries, which suits the campaign-wide pool but does not date every generated person's name to 1836. [4]

| Existing identity | Displayed name after this change |
|---|---|
| `ZUL_dingane` | Dingane kaSenzangakhona |
| `ZUL_mpande_zulu` | Mpande kaSenzangakhona |
| `ZUL_gqugqu_claimant` | Gqugqu kaSenzangakhona — already correct |
| `ZUL_cetshwayo_heir` | Cetshwayo kaMpande |
| `ZUL_mbuyazi_heir` | Mbuyazi kaMpande |
| `ZUL_dinuzulu_heir` | Dinuzulu kaCetshwayo |
| `ZUL_solomon_heir` | Solomon kaDinuzulu |
| `SB_ZUL_hamu` | Hamu kaNzibe — retained; explanation below |

“Zulu” remains a valid clan/dynastic identification. The change makes SB's historical **display convention** consistent with Gqugqu; it does not assert that every use of “Zulu” is erroneous. SAHO's genealogy corroborates the principal royal links, although its Cetshwayo birth date conflicts with its dedicated biography; no dates were changed from that list. [5] The published naming literature distinguishes Mbuyazi kaMpande from Henry Francis Fynn's Zulu name, Mbuyazi weTheku. [6, p. 48] Solomon's patronymic is also used by the Presidency and the National Archives catalogue. [7], [8]

### Pool construction

`REPLACE:zulu` changes only the four name arrays. Religion, heritage, language, colour, ethnicity, graphics and treaty seal retain their installed Vanilla values. Both noble and common surname arrays use the same twenty clans: **clan membership is not itself proof of nobility**. Historical template nobility is unchanged.

The clan pool is Biyela, Buthelezi, Chube, Hlabisa, Khoza, Langeni, Magwaza, Mbatha, Mchunu, Mdlalose, Mdletshe, Mpungose, Mthethwa, Ndwandwe, Ntombela, Nxumalo, Nyawo, Sibiya, Sibisi and Zungu. Guy's territorial and political survey supplies most of these, and period personal names including Dilikana, Mabhoko, Matshana, Mbopha, Mfanawendlela, Mfuzi, Mlandela, Mnqandi, Msushwana, Ndabankulu, Sigananda, Sitshaluza, Somfula and Vumandaba. The survey identifies particular lineages and leaders; using those names in a random pool is an engine approximation, not an assignment of their biographies. [9, pp. 60–63 and figures 7–8]

Ngubane and Thabethe supply Godlumkhonto, Gwala, Nyamakayishi, Sokwetshatha and Tshani, and support the Mehlokazulu and Senzangakhona spellings. [4] Shamase supplies female names including Bathonyile, Hloyisile, Langazana, Mawa, Mkabi, Mmama, Monase and Nomantshali, as well as Sibiya/Nxumalo affiliations. [2, pp. 1–4, 10] Existing suitable names are retained. The resulting arrays contain **39 male and 15 female given names**, plus **20 clan surnames**. Specific `ka…`/`wa…` parent references and the misspelt Buthelezei are removed from surname generation. Sekhukhune/Sikukuni are omitted from this Zulu pool; Mthethwa is retained as a clan rather than a female given name.

New localisation keys are separately marked for review. Existing narrative localisation and historical evidence are not rewritten. Template-name changes affect newly created characters; saved names are not migrated.

## Hamu: present source and present save

The James Stuart Archive editors identify Hamu as Mpande's biological son and the genealogical son of Mpande's brother Nzibe. This is an editorial clarification of recorded testimony, not a second person and not proof that Nzibe was his biological father. [10, p. 194, n. 9]

Knight explains the political consequence: Mpande assigned Hamu to Nzibe's house, constraining his ordinary royal succession position, while Hamu developed his own Ngenetsheni following and later opposed Cetshwayo. [11, pp. 3–4] His political aspirations can still matter without making him an automatically senior legitimate heir. The prior [oral-history cast brief](zulu_oral_history_cast_research_2026_10_19.md) records the 1865 evidence behind SB's availability gate. That gate remains unchanged.

**Read-only snapshot:** `autosave.v3`, game date **1850.9.1**, SHA-256 `734b3dc78c9a7a211f30623b7630ee089a03b31f3b8830906d3f62e5887be1ce`. Copied to `/private/tmp/sb_hamu_autosave_2026_10_29.v3` before inspection because DP was actively advancing the game.

| Save observation | Meaning |
|---|---|
| No `template=SB_ZUL_hamu`; no `sb_court_hamu_created_var` | The authored prince has not been introduced. The save predates 1865. |
| ID `33555032`, Hamu KaMdlela, born 1815, recruitable admiral | Generated namesake; no historical template. |
| ID `16781625`, Hamu KaMdlela, born 1809, recruitable general | Another generated namesake; no historical template. |

The current creator installs Hamu as a politician with **Ngenetsheni following 6**, neutral constitutional alignment and uncommitted personal endorsement. Neutral alignment can also keep him outside the royal candidate list. No new story or forced allegiance was added for him in this pass.

## Verification and remaining limits

- `tests.test_zulu_names`: **4/4 passed**. The tests compare every non-name culture field with current Vanilla, reject generated patronymics/duplicate pool entries, verify localisation coverage and retain historical template identities.
- The compatibility inventory check **passed** with 123 keyed overrides. It records the new keyed culture override and the changed Dingane/Mpande template hashes.
- Parent integration owns the first-adulthood Charismatic award and the brothers' allegiance/event behaviour. Child templates retain empty personality packages.
- DP still needs to verify new-game naming, the adult trait tooltip, coalition effects and Hamu's post-1865 introduction. No game was launched or save edited here.
- An independent birth-date audit remains separate: several popular genealogies disagree, including on Solomon. This name-only pass does not silently replace established scenario dates.

## Sources and retrieval

Searches combined the existing cast briefs, exact royal names, scholarly Zulu naming studies, James Stuart Archive testimony and installed game definitions. Primary oral testimony/editorial annotations were preferred for Hamu; scholarly interpretation for political context; institutional records for names. Search-result snippets were not used to invent unseen details. Links below were checked on 29 October 2026. No exhaustive claim is made for the finite name pool.

[1] South African History Online, “King Cetshwayo,” updated Aug. 23, 2019. [Biography](https://sahistory.org.za/people/king-cetshwayo). Synthesis; chronology cross-checked rather than treated as a script-ready timeline.

[2] M. Z. Shamase, “The royal women of the Zulu monarchy through the keyhole of oral history: Queens Nandi (c. 1764–c.1827) and Monase (c. 1797–1880),” *Inkanyiso*, vol. 6, no. 1, pp. 1–14, 2014, doi: [10.4102/ink.v6i1.240](https://doi.org/10.4102/ink.v6i1.240). [Publisher PDF](https://inkanyisojournal.org/index.php/ink/article/download/240/346). Full relevant pages inspected; retrospective oral traditions require attribution.

[3] R. L. Cope, “Written in Characters of Blood? The Reign of King Cetshwayo ka Mpande 1872–9,” *The Journal of African History*, vol. 36, no. 2, pp. 247–269, 1995, doi: [10.1017/S0021853700034137](https://doi.org/10.1017/S0021853700034137). Publisher metadata and abstract inspected, not the paywalled full article.

[4] S. Ngubane and N. Thabethe, “Shifts and continuities in Zulu personal naming practices,” *Literator*, vol. 34, no. 1, art. 431, 2013, doi: [10.4102/lit.v34i1.431](https://doi.org/10.4102/lit.v34i1.431). [Full text](https://literator.org.za/index.php/literator/article/view/431/1286).

[5] South African History Online, “Zulu Family History,” Sept. 4, 2012. [Genealogy](https://sahistory.org.za/article/zulu-family-history). Used narrowly for patronymic links; internal date problems noted above.

[6] A. Koopman, “UMahlekehlathini, uMehlomane, and uMbokodo: Zulu Names for Whites in Colonial Natal,” *Natalia*, no. 44, pp. 48–69, 2014. [Natal Society Foundation issue](https://natalia.org.za/Files/44/Natalia%20No%2044.pdf). The indexed p. 48 extract explicitly supplies the naming distinction; direct PDF retrieval timed out. No broader argument is inferred from the extract.

[7] The Presidency, “President Ramaphosa extends deepest condolences to the Zulu nation on the passing of Princess Alice,” Feb. 20, 2023. [Official statement](https://www.thepresidency.gov.za/president-ramaphosa-extends-deepest-condolences-zulu-nation-passing-princess-alice). Indexed statement used only for Solomon kaDinuzulu's identification; direct retrieval timed out.

[8] National Archives and Records Service of South Africa, catalogue entry for N. L. G. Cope's 1985 thesis, *The Zulu Royal Family under the South African Government, 1910–1933: Solomon kaDinuzulu, Inkatha and Zulu Nationalism*. [Catalogue](https://www.nationalarchives.gov.za/node/4544443); [university repository metadata](https://researchspace.ukzn.ac.za/items/87137e7b-35ce-4af1-8827-2bea189b6f4e/full). Metadata checked; archive direct fetch timed out.

[9] J. Guy, “The political structure of the Zulu kingdom during the reign of Cetshwayo kaMpande,” 1981, pp. 49–73 in the scanned pagination. [eMandulo archival copy](https://emandulo.apc.uct.ac.za/collection/Jeff_Guy/K/Guy_1981_Political_Cetshwayo.pdf). Relevant text, figures and names inspected; no DOI asserted.

[10] C. de B. Webb and J. B. Wright, eds., *The James Stuart Archive*, vol. 4, evidence of Ndabazezwe kaMfuleni recorded June 22, 1921, pp. 183–197, 1986. [Edited testimony and notes](https://emandulo.apc.uct.ac.za/collection/KCAL/4_VOL4/KCAL_JSAVol4_1986_edited_notes_Ndabazezwe_ka_Mfuleni_116_p183_p197.pdf).

[11] I. Knight, “A House Divided: The Zulu Princes Who Fought for the British in 1879,” Anglo-Zulu War Historical Society, undated. [Specialist article](https://www.anglozuluwar.com/wp-content/uploads/2020/11/AZWHS-The-Zulu-Princes-Who-Fought-For-The-British.pdf). Secondary reconstruction; read alongside [10].
