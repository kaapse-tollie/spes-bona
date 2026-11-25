# Krakatoa on the Southern African coast

24 November 2026 · Decision brief for Spes Bona

## Executive summary

**Keep the historical wave in the Cape narrative. Remove Southern Africa from the blanket destructive tsunami effect if SB uses vanilla's single damage level.** Tide gauges recorded the 27 August 1883 tsunami at Port Elizabeth, Port Alfred and Cape Town [1, p. 63, Table 1, and Fig. 7]. The captain of the *Hawarden Castle* reported having to drop a second anchor in Algoa Bay [2, pt. III, p. 133]. These observations support harbour disturbance. I found no regional harvest failure or population loss attributable to this wave in the records examined [1, sec. 3, South African records], [2, pt. III, pp. 130–134]. Vanilla's Southern African effect adds 10 devastation and a harvest condition with mortality, subsistence and agricultural penalties [3, `krakatoa_tsunami_effect` and `tsunami_effect`], [4, medium devastation and `tsunami`].

## Scope and method

The decision concerns the physical tsunami of August 1883, the 17-state Southern Africa footprint, and SB's neighbouring Mozambican coast [2, pt. III], [5, `geographic_region_southern_africa_old` and tsunami list]. I compared the Royal Society committee's gauge analysis and eyewitness correspondence with a later digitisation of the records, searched for Natal, Durban, Delagoa Bay and Mozambique by name, and inspected the installed 1.15.2 effect and SB's geographic override. This was a targeted English-language review. The two quantitative accounts use much of the same underlying gauge material [1, sec. 3], [2, pt. III].

## What reached the coast

| Observation and SB geography | Evidence |
|---|---|
| Port Elizabeth / Algoa Bay, Eastern Cape | Maximum positive excursion **0.81 m**, negative excursion **0.77 m**, total range **1.58 m** [1, p. 63, Table 1]. A mail steamer swung against its anchor in the evening and rode on two cables [2, pt. III, pp. 132–133]. |
| Port Alfred, Eastern Cape | **0.52 m** positive, **0.42 m** negative, **0.94 m** total range [1, p. 63, Table 1]. |
| Cape Town / Table Bay, Cape Colony | **0.32 m** positive and negative, **0.64 m** total range [1, p. 63, Table 1]. The gauge was inside the breakwater, and the committee cautioned that harbour geometry affected the comparison [2, pt. III, pp. 133–134]. |
| Natal and Zululand | The three measured South African stations in the reanalysis are all farther south [1, p. 63, Table 1, and Fig. 7]. The committee separately recorded pumice arriving on the Natal coast in September **1884**, a year after the eruption [2, pt. I, p. 47]. The extent of any inundation at Durban or on the Zululand coast remains unresolved. |
| Lourenço Marques, Moçambique and Zambezia | The sources examined provide no local gauge height, documented crop loss or attributable deaths for these states. The ocean-basin travel-time model makes an arriving disturbance plausible, with local effects unresolved [1, Fig. 3 and Table 1]. |
| Atlantic coast north of the Cape | Table Bay establishes that the wave entered the Atlantic [1, p. 69]. That observation alone cannot determine damage in Northern Cape, Namaqualand or Hereroland. |

The gauge ranges measure peak-to-trough variation. They cannot be read as the depth of water over farms or the height reached on shore [1, p. 63, Table 1]. Harbour currents can threaten a moored vessel without a corresponding regional crop loss, as the Algoa Bay account illustrates [2, pt. III, p. 133].

## What Victoria 3 applies

SB adds its coastal Natal split to vanilla's list alongside Zululand. The list also names inland regions including Botswana, Vrystaat and Transvaal [5, tsunami zone, Southern Africa]. Vanilla first checks whether an **owned state is coastal** and belongs to the zone. It then applies the condition and devastation at **state-region scope** [3, `tsunami_effect`]. Removing the names of entirely inland regions alone would accomplish little. A coastal split state, on the other hand, can admit a larger region into the effect [3, `tsunami_effect`].

The Southern and East African strategic regions get the medium setting of **10 devastation**. The harvest condition also modifies infrastructure, market access price impact, agriculture, plantations, ranching, extraction, peasant consumption and mortality. The script rolls intensity from 1–3 here [3, `krakatoa_tsunami_effect`], [4, `tsunami`, modifier and intensity]. These effects are appreciably broader than the evidence for the Cape harbours [1, Table 1], [2, pt. III, p. 133].

## Limits and recommendation

1. **With existing mechanics, remove the Southern African coastal states from destructive coverage.** In SB's core this means Natal, Zululand, Eastern Cape, Cape Colony, Northern Cape, Namaqualand, Hereroland and Lourenço Marques. Review Moçambique and Zambezia alongside them before changing neighbouring vanilla territory [5, tsunami zone], [6, coastal port entries]. Preserve the eruption itself and global atmospheric content. This is a design recommendation.
2. **If a local acknowledgement is wanted, use the existing eruption news or one short, cosmetic Cape harbour notice.** The steamer putting down a second anchor is a documented detail [2, pt. III, p. 133]. I would choose that over a bespoke harvest condition or a regional mortality modifier.
3. Reconsider a locality if contemporary port, district or agricultural records document significant damage there. Confidence is high in the three measured arrivals and lower in how strongly unsampled coastlines were affected [1, Table 1], [2, pt. III, pp. 130–134]. The sources do not establish an absence of waves at other ports.

## References

[1] E. Pelinovsky, B. H. Choi, A. Stromkov, I. Didenkulova and H. S. Kim, “Analysis of Tide-Gauge Records of the 1883 Krakatau Tsunami,” *Advances in Natural and Technological Hazards Research*, vol. 23, pp. 57–77, 2005. [DOI](https://doi.org/10.1007/1-4020-3331-1_4).

[2] G. J. Symons, ed., *The Eruption of Krakatoa, and Subsequent Phenomena: Report of the Krakatoa Committee of the Royal Society*. London, Harrison and Sons, 1888. See W. J. L. Wharton, part III, “On the Seismic Sea Waves,” especially the letter of Capt. M. P. Webster on p. 133. [ETH-Bibliothek digitised edition](https://doi.org/10.3931/e-rara-16337).

[3] Paradox Development Studio, *Victoria 3*, v1.15.2, “Krakatoa list” and “Reusable Tsunami.” [Installed effects](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_krakatoa_effects.txt>).

[4] Paradox Development Studio, *Victoria 3*, v1.15.2, Krakatoa script values and tsunami harvest condition. [Devastation values](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/script_values/krakatoa_values.txt>) · [Harvest condition](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/harvest_condition_types/00_harvest_condition_types.txt>).

[5] Spes Bona, “Geographic regions,” 1.15.2 working tree, 24 Nov. 2026. [Regional membership](../../common/geographic_regions/sb_geographic_regions.txt).

[6] Spes Bona, “Sub-Saharan Africa state regions,” 1.15.2 working map, 24 Nov. 2026. [Port provinces](../../map_data/state_regions/04_subsaharan_africa.txt).
