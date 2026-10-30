# Klip River and Zululand: population evidence for SB

Research date: 29 October 2026. Scope: the 1836 starting distribution, with checks against the 1840s and the period of Mpande’s proposed 1856 retirement. Research only; no population, map or gameplay definitions changed.

## Finding and recommendation

**No defensible numerical reconstruction of the population inside SB’s Klip River province in 1836 was located.** The existing 2,000 is an authored baseline, not a verified historical census figure. The strongest local demographic benchmark found is **about 10,200 Africans and 1,400 Europeans in the historical Klip River County in 1855**, reported by Beverley Ellis from the Natal Blue Book. Different geography, dates and migration prevent treating that figure as a replacement for SB’s 1836 value. [1, p. 165]

For the present civil-war repair, restore the **campaign’s pre-war distribution**, rather than impose a new historical ratio. Preserve losses and demographic change: restoration should undo the exceptional wartime redistribution, not resurrect the original headcount. That is a gameplay recommendation, not a claim that the original SB distribution is historically accurate.

## What SB currently represents

The inspected working tree gives ZUL the following starting population. These are script values, not numbers extracted from a live save. [2]

| Authored territory | Population | Share of ZUL’s starting population |
|---|---:|---:|
| ZUL-owned part of `STATE_NATAL`, province `xBBCA32` | 2,000 Zulu | 0.741% |
| `STATE_ZULULAND`, nine provinces | 266,000 Zulu + 2,000 Tsonga slaves | 99.259% |
| Total | 270,000 | 100% |

The ratio is therefore **1:134**, Klip River to the remaining ZUL population. The rest of `STATE_NATAL` is separately authored: NGI has 84,945 people and CAP 55. Adding those to the Klip population would confuse a state region with ZUL’s actual holding. [2]

The mod’s travel-time reference associates KLR with Ladysmith. This helps identify the intended historical setting, but neither that label nor the single province proves that its polygon reproduces a nineteenth-century county boundary. No georeferenced overlay of the two boundaries was completed in this research. [3]

## Historical geography and demographic change

The 1847 dispute concerned territory between the Thukela, Buffalo/Mzinyathi and Drakensberg. Leśniewski’s reconstruction also stresses the weakness and retrospective nature of many records before British attention turned to the dispute in 1847. This supports caution about using statements of territorial ownership as population measurements. [4, pp. 24–26]

The administrative county was created in October 1848, covering about 3,720 square miles. It was later divided into Ladysmith and Newcastle divisions in 1862. Ellis’s 1855 figures refer to that county, not an independently verified match to SB’s `xBBCA32`. Her discussion suggests uneven African settlement, including concentrations along the Mzinyathi and Thukela. Colonial descriptions of apparently unoccupied land are not household enumerations and should not be converted into zero population. [1, p. 165]

There were substantial movements of people during the interval. Michael Lobban records approximately 7,000 amaHlubi entering Natal in 1848: they initially settled at the Klip River, then were moved near Champagne Castle after about a year. He also records land being allocated to about 5,000 Putini people. These are migrating groups, not two numbers to add mechanically to the Klip district’s resident total. They demonstrate why smooth backward extrapolation from 1855 is unsafe. [5, ch. 3, “The Trial and Detention of Langalibalele”]

## What can be justified for each test date?

| Date | Evidence available | Use in SB |
|---|---|---|
| 1836 | No matched local enumeration found | Keep 2,000 explicitly provisional; this brief neither verifies nor disproves it. |
| 1840s | Disputed territorial control and substantial movements of population | Do not assume the starting ratio remains historically constant. Use the campaign’s actual population at the war’s start. |
| 1855–56 | Approximate 1855 county figure from the Blue Book through Ellis | A later regional benchmark for the population balance review, not a direct 1836 replacement or exact SB province count. |
| After Klip River is ceded | SB’s territorial ownership differs from its starting setup | Do not restore population into an unrelated owner’s state solely to recreate the starting ratio. A split wholly within Zululand is a different case. |

There is **insufficient evidence for a defensible 1836 confidence interval or Klip:Zululand historical ratio**. In particular, the 268,000 assigned to the rest of Zululand was not independently validated here. Dividing the 1855 county estimate by that authored denominator would mix dates, boundaries and evidentiary standards.

If the pre-release balance pass needs alternative starting scenarios, label them as gameplay sensitivity tests. A higher Klip allocation must be tested against food supply and the wider Natal setup as well as military recruitment. The later county estimate can help flag implausible orders of magnitude only after the map boundaries are compared; it is not a warrant to assign 10,200 people to the current province.

## Evidence appraisal and outstanding work

- **High confidence:** the inspected SB population arithmetic and ownership boundaries.
- **Moderate confidence:** the quoted 1855 administrative estimate as transmitted by Ellis. Her thesis supplies an exact primary-source locator, but the original Blue Book table has not been inspected independently.
- **High confidence in relevance, limited demographic precision:** the documented migration and changing geography make a fixed backward extrapolation inappropriate.
- **Low confidence:** any exact 1836 Klip population or historical ratio to the entire Zulu kingdom.

Before changing starting population, compare an historical county map with the SB province polygon; inspect **Natal Blue Book 1855, p. 244** and neighbouring years; and trace available 1840s magistrates’ or location returns to named settlements. Record what each return counts—people, households, taxpayers or warriors—rather than silently converting between them. A separate appraisal of Zululand’s total is needed before claiming a historically grounded ratio.

## Method and access limits

This was a targeted research brief, not a systematic review. Searches combined Klip River/Mnambithi, Natal/Zululand, population, African settlement and the dates 1836/1840s/1855/1856. Local SB population and ownership scripts were inspected independently of historical searches. External routes included UKZN’s institutional repository, Cambridge University Press and the journal *Werkwinkel*, followed through citations to archival and administrative material.

The Ellis repository metadata and indexed text of printed p. 165 were inspected; the large PDF could not be retrieved for a complete examination in this environment. The Blue Book is therefore an **indirectly consulted primary source**. Lobban’s open-access chapter and Leśniewski’s publisher-hosted article were consulted directly. No numerical claim relies on an unsourced web summary, a military-strength estimate converted into total population, or a purportedly empty-land narrative. The failure to locate an 1836 enumeration is a search result, not proof that none survives.

## References

[1] B. Ellis, *The impact of the white settlers on the natural environment of Natal, 1845–1870*, M.A. thesis, University of Natal, Pietermaritzburg, 1998, p. 165, especially n. 7 citing *Blue Book*, 1855, p. 244. [UKZN repository record](https://researchspace.ukzn.ac.za/items/da761974-dc5a-4e25-aeba-bd591c05769b), persistent identifier [hdl:10413/5835](http://hdl.handle.net/10413/5835); [repository PDF](https://researchspace.ukzn.ac.za/server/api/core/bitstreams/626dda00-1a43-47f1-b282-b1888a168758/content). Repository metadata and the relevant indexed page consulted 29 October 2026.

[2] Spes Bona working tree, inspected 29 October 2026: [population history](../common/history/pops/04_subsaharan_africa.txt), `STATE_ZULULAND` and `STATE_NATAL`, lines 2961–3002; [state ownership](../common/history/states/00_states.txt), lines 6065–6103; [state-region province definitions](../map_data/state_regions/04_subsaharan_africa.txt), lines 1214–1254. These establish the implementation, not historical accuracy.

[3] Spes Bona, [Cross-tag event travel times](cross_tag_event_travel_times.md), KLR capital entry, inspected 29 October 2026.

[4] M. Leśniewski, “Chronology of the Klip River Affair of 1847,” *Werkwinkel*, vol. 9, no. 1, pp. 23–41, 2014. DOI: [10.2478/werk-2014-0002](https://doi.org/10.2478/werk-2014-0002). [Publisher record](https://pressto.amu.edu.pl/index.php/werk/article/view/werk-2014-0002); [publisher PDF](https://pressto.amu.edu.pl/index.php/werk/article/download/werk-2014-0002/28366). Consulted 29 October 2026.

[5] M. Lobban, “Zulu Political Prisoners, 1872–1897,” in *Imperial Incarceration: Detention without Trial in the Making of British Colonial Africa*. Cambridge: Cambridge University Press, 2021, pp. 80–123, section “The Trial and Detention of Langalibalele.” DOI: [10.1017/9781009004848.003](https://doi.org/10.1017/9781009004848.003). Print ISBN 978-1-316-51912-7. [Open-access chapter](https://www.cambridge.org/core/books/imperial-incarceration/zulu-political-prisoners-18721897/21354AD11338C07AD5C1BF6288893297). Consulted 29 October 2026.
