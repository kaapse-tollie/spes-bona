# Resource Migration Note

## Purpose

This note explains the `Variant H` resource migration used in the SB resource workbook at [resource_rework_vanilla_comparators.xlsx](../References/resource_rework_vanilla_comparators.xlsx).

`Variant H` is not a balance-first bracket. It is the migration-target bracket:

- `Arable` and `Arable Resource` rows follow the evidence-led line.
- Mining and special-resource rows follow an extreme-investment upper-bound.
- The split SB Transvaal states are then reweighted so that **regional differences are evidence-based**, instead of inheriting the same unsplit vanilla ceiling three times.

The practical consequence is:

- overall Transvaal coal potential stays at the adjusted vanilla ceiling, but shifts decisively eastward;
- iron potential concentrates almost entirely in northern Transvaal;
- `Gold Fields (discovered)` is treated as a **start-date semantic**, not a geology flag.

For live implementation, non-gold special resources keep their existing `undiscovered` semantics unless there is separate evidence for a genuine 1836 start resource. That means the southern Mozambique and Zambezi rubber rows inherit the `Variant H` cap reduction, but stay `undiscovered` in the state files rather than being turned into start-date rubber.

## Rule: what `Gold Fields (discovered)` means

For this migration, `Gold Fields (discovered)` means:

- the field was already known and in active use at the 1836 game start; and
- the field should therefore not be hidden behind later discovery logic.

That rule forces a semantic cleanup. Most southern African rush fields were **not** discovered by 1836:

- Kimberley’s diamond rush begins after a chance find in **1867**, with dry diggings in **1870** and a large rush by **1871**. See [Britannica, South Africa: Diamonds, gold, and imperialist intervention](https://www.britannica.com/place/South-Africa/Diamonds-gold-and-imperialist-intervention-1870-1902) and [Britannica, Kimberley](https://www.britannica.com/place/Kimberley-South-Africa).
- The Witwatersrand’s main reef was discovered in **1886** after earlier minor finds in **1884**. See [South African History Online, Discovery of the Gold in 1884](https://sahistory.org.za/article/discovery-gold-1884) and [Britannica, South Africa: Diamonds, gold, and imperialist intervention](https://www.britannica.com/place/South-Africa/Diamonds-gold-and-imperialist-intervention-1870-1902).
- Pilgrim’s Rest was declared a gold field in **1873**, and Barberton’s rush dates to **1884**. See [Mpumalanga Museums, Pilgrim’s Rest](https://museums.mpg.gov.za/pilgrims-rest/) and [South African History Online, Barberton](https://sahistory.org.za/place/barberton-mpumalanga).

Accordingly, `Variant H` zeroes `Gold Fields (discovered)` in the SB scope unless there is clear evidence of a start-date field already in use.

This is a semantic correction, not a geology nerf. In most cases the same endowment is retained as `Gold Fields (undiscovered)`.

## Variant H decisions

### 1. Northern Cape special-field cleanup

#### `STATE_NORTHERN_CAPE`

- `Gold Fields (discovered)`: `7 -> 0`
- `Gold Fields (undiscovered)`: `20 -> 20`

Why:

- Kimberley is central to the state’s later mineral history, so the state should keep a strong late special-field row.
- But Kimberley is a **post-1836** discovery sequence, not a start-date field.

Evidence:

- [Britannica, South Africa: Diamonds, gold, and imperialist intervention](https://www.britannica.com/place/South-Africa/Diamonds-gold-and-imperialist-intervention-1870-1902): the diamond rush begins with a chance find in **1867**, richer dry diggings in **1870**, and by **1871** nearly 50,000 people were at the later Kimberley camp.
- [Britannica, Kimberley](https://www.britannica.com/place/Kimberley-South-Africa): Kimberley was founded after diamond discoveries on nearby farms in **1869–71**.

Migration rationale:

- SB keeps the large late field, but it belongs in `undiscovered`, not `discovered`.

### 2. Split Transvaal coal

#### `STATE_TRANSVAAL`

- `Coal Mine`: `29 -> 5`

Why:

- Western Transvaal/Gauteng is not the main coal basin. The inherited G value was an artefact of spreading an unsplit Transvaal ceiling too evenly across the three SB states.

Evidence:

- [Coaltech 2020, Northern Witbank-Highveld Coalfield](https://coaltech.co.za/wp-content/uploads/2019/10/Task-1.8.1-Characterisation-quantification-and-location-of-the-remaining-resources-including-previously-partially-mined-areas-2001.pdf): the quantified reserve study is explicitly for the **Northern Witbank-Highveld Coalfield**, i.e. the eastern coal province rather than western Transvaal.
- [South African Government, Waterberg-Bojanala Priority Area speech](https://www.gov.za/news/speeches/deputy-minister-rejoice-mabudafhasi-addresses-launch-waterberg-bojanala-priority-area): the Witbank/Middelburg coalfields had been the source of **more than 80% of South Africa’s total coal output for many years**.

Migration rationale:

- `STATE_TRANSVAAL` keeps only a small residual coal cap. The western state should not inherit the main eastern coalfield.

#### `STATE_EAST_TRANSVAAL`

- `Coal Mine`: `30 -> 63`

Why:

- Eastern Transvaal is the coal heartland of the split cluster.

Evidence:

- [Coaltech 2020, Northern Witbank-Highveld Coalfield](https://coaltech.co.za/wp-content/uploads/2019/10/Task-1.8.1-Characterisation-quantification-and-location-of-the-remaining-resources-including-previously-partially-mined-areas-2001.pdf): the Northern Witbank-Highveld coalfield alone had about **14.4 billion tonnes** of remaining resources and **2.82 billion tonnes** of saleable reserves in the 2001 CSIR/Coaltech review.
- [Eskom heritage, Witbank Power Station](https://www.eskom.co.za/heritage/history-in-decades/escom-1923-1932/witbank-power-station/): by the mid-1920s Witbank was already being integrated into the Rand power economy, which is exactly the kind of infrastructure signal that supports an extreme 1936 upper-bound.

Migration rationale:

- `STATE_EAST_TRANSVAAL` becomes the dominant coal state inside the Transvaal cluster.

#### `STATE_NORTHERN_TRANSVAAL`

- `Coal Mine`: `34 -> 36`

Why:

- Waterberg is geologically huge, but it is late.

Evidence:

- [SAIMM, Characterization of the coal resources of South Africa](https://www.saimm.co.za/Journal/v105n02p095.pdf): Waterberg held about **28%** of South Africa’s recoverable coal reserves in the Bredell reserve comparison, larger than any single named coalfield, and was identified as the likely replacement for Witbank.
- [Exxaro, Grootegeluk coal mine history](https://exxaro-reports.co.za/reports/ar-2017/mineral-reserves-resources/grootegeluk-coal-mine.php): the Waterberg coalfield was discovered in **March 1920** as a scientific curiosity; intensive exploration on the main Grootegeluk farms started only in **1973**, and the mine was commissioned in **1980**.

Migration rationale:

- Northern Transvaal keeps a high geological ceiling, but it still sits below eastern Transvaal in a 1936 upper-bound because the coalfield was late-discovered, late-proven, and late-infrastructured.

#### Cluster rule

The total Transvaal coal ceiling in `Variant H` is kept at the adjusted vanilla total:

- `TRN Coal Mine`: vanilla-adjusted `104`, Variant H `104`

The migration changes **distribution**, not overall Transvaal coal mass:

- `STATE_TRANSVAAL`: `5`
- `STATE_NORTHERN_TRANSVAAL`: `36`
- `STATE_EAST_TRANSVAAL`: `63`

That preserves gameplay-scale continuity with vanilla while correcting the internal geography.

### 3. Split Transvaal iron

#### `STATE_NORTHERN_TRANSVAAL`

- `Iron Mine`: `20 -> 55`

Why:

- The only clear pre-1936 commercial iron row in the split Transvaal cluster is Thabazimbi.

Evidence:

- [Britannica, Thabazimbi](https://www.britannica.com/place/Thabazimbi): superior-grade hematite there was discovered in **1919** and mined in **1931**.
- [Kumba Iron Ore annual report 2010](https://www.kumba.co.za/~/media/Files/A/Anglo-American-Group/Kumba/report-library/2010/comm-full.pdf): Thabazimbi “started producing in **1931**” and had already been in continuous operation for almost 80 years by 2010.

Migration rationale:

- Northern Transvaal gets almost the entire iron ceiling because it is the only split Transvaal state with direct pre-1936 commercial iron evidence.

#### `STATE_TRANSVAAL`

- `Iron Mine`: `18 -> 0`

#### `STATE_EAST_TRANSVAAL`

- `Iron Mine`: `17 -> 0`

Why:

- No comparable pre-1936 commercial iron province was identified in the western or eastern split states.
- The prior G values were balance artefacts carried over from the unsplit vanilla Transvaal row.

Evidence:

- [Britannica, Thabazimbi](https://www.britannica.com/place/Thabazimbi) identifies the northern ore body, not a Gauteng or eastern analogue.
- [Kumba Iron Ore annual report 2010](https://www.kumba.co.za/~/media/Files/A/Anglo-American-Group/Kumba/report-library/2010/comm-full.pdf) treats Thabazimbi as the relevant historical Transvaal iron operation; there is no equivalent pre-1936 commercial iron story for the other two split rows in the same evidence pass.

Migration rationale:

- `Variant H` intentionally concentrates the commercial iron cap where the evidence is strongest.

### 4. Split Transvaal gold-field semantics

#### `STATE_TRANSVAAL`

- `Gold Fields (discovered)`: `11 -> 0`
- `Gold Fields (undiscovered)`: `31 -> 34`

Why:

- The Witwatersrand is the dominant goldfield in the cluster, but it was discovered after the game start.

Evidence:

- [South African History Online, Discovery of the Gold in 1884](https://sahistory.org.za/article/discovery-gold-1884): minor discoveries were made in **1884**, but the main reef is attributed to George Harrison’s **1886** find at Langlaagte.
- [SAIMM, Mining Heritage](https://www.saimm.co.za/events/0305apcom/downloads/465-474%20smith.pdf): the 1886 discovery set off the gold rush and the Witwatersrand Basin is described as the **richest goldfield ever discovered**.

Migration rationale:

- `STATE_TRANSVAAL` keeps the dominant late special-field row, but it must be `undiscovered`, not `discovered`.

#### `STATE_EAST_TRANSVAAL`

- `Gold Fields (discovered)`: `4 -> 0`
- `Gold Fields (undiscovered)`: `3 -> 10`

Why:

- Eastern Transvaal has real goldfield history, but it is the earlier eastern rush sequence, not a start-date field.

Evidence:

- [Mpumalanga Museums, Pilgrim’s Rest](https://museums.mpg.gov.za/pilgrims-rest/): payable gold was discovered in **1873**, and Pilgrim’s Rest was declared a gold field in September of that year.
- [South African History Online, Barberton](https://sahistory.org.za/place/barberton-mpumalanga): Barberton’s rush dates to **1884**, with the town named after the Barber discovery and the goldfields flourishing thereafter.

Migration rationale:

- Eastern Transvaal gets a meaningful secondary `undiscovered` goldfield row, well below the Rand but far above the near-zero G allocation.

#### `STATE_NORTHERN_TRANSVAAL`

- `Gold Fields (discovered)`: `5 -> 0`
- `Gold Fields (undiscovered)`: `2 -> 4`

Why:

- Northern Transvaal did have goldfield activity, but it was minor relative to the Rand and eastern escarpment.

Evidence:

- [University of Illinois, Map of the Zoutpansberg Goldfields](https://digital.library.illinois.edu/items/419cc4c0-e946-0133-1d3d-0050569601ca-4): by **1893** the Zoutpansberg goldfields were established enough to warrant a dedicated map in the *Geographical Journal*.
- [American Geosciences Institute, Antimony/Gold Mineralisation of the Murchison Greenstone Belt](https://information.americangeosciences.org/open-collections/igc/3756/): Consolidated Murchison was historically an antimony producer with **gold as a co-product**, and cumulative historical production to 2015 included **44.7 tonnes of gold**.

Migration rationale:

- Northern Transvaal keeps a small later goldfield row, but it is intentionally tertiary.

### 5. Why `Gold Fields (discovered)` goes to zero so often

This is the largest visual change in the workbook, and it is deliberate.

The previous rows mixed together two different meanings:

- geology exists somewhere in the state; and
- the field was already discovered and active in 1836.

Those are not the same thing. `Variant H` uses:

- `Gold Fields (discovered)` for start-date fields;
- `Gold Fields (undiscovered)` for later rushes or later formal exploitation.

That is why:

- `CAP Gold Fields (discovered)` falls from `8` to `0`;
- `TRN Gold Fields (discovered)` falls from `12` to `0`;
- `ORA Gold Fields (discovered)` falls from `16` to `0`;
- `SAF Gold Fields (discovered)` falls from adjusted-vanilla `36` to `0`;
- but `Gold Fields (undiscovered)` rises instead.

This is a semantic migration, not a claim that the minerals do not exist.

## Aggregate balance effects

These numbers come directly from the workbook’s `Balance Summary` sheet.

### CAP totals

| Resource | SB baseline | Vanilla prior (adj.) | Variant H |
|---|---:|---:|---:|
| Arable Land | 132 | 150 | 145 |
| Coal Mine | 36 | 56 | 51 |
| Iron Mine | 0 | 33 | 30 |
| Gold Fields (discovered) | 8 | 8 | 0 |
| Gold Fields (undiscovered) | 8 | 8 | 20 |

### TRN totals

| Resource | SB baseline | Vanilla prior (adj.) | Variant H |
|---|---:|---:|---:|
| Arable Land | 58 | 50 | 82 |
| Coal Mine | 88 | 104 | 104 |
| Iron Mine | 42 | 60 | 55 |
| Gold Fields (discovered) | 20 | 12 | 0 |
| Gold Fields (undiscovered) | 20 | 12 | 48 |

### ORA totals

| Resource | SB baseline | Vanilla prior (adj.) | Variant H |
|---|---:|---:|---:|
| Arable Land | 42 | 40 | 60 |
| Coal Mine | 32 | 60 | 52 |
| Iron Mine | 16 | 30 | 25 |
| Gold Fields (discovered) | 16 | 16 | 0 |
| Gold Fields (undiscovered) | 16 | 16 | 14 |

### SAF totals

| Resource | SB baseline | Vanilla prior (adj.) | Variant H |
|---|---:|---:|---:|
| Arable Land | 232 | 240 | 287 |
| Coal Mine | 156 | 220 | 207 |
| Iron Mine | 58 | 123 | 110 |
| Gold Fields (discovered) | 44 | 36 | 0 |
| Gold Fields (undiscovered) | 44 | 36 | 82 |

### Full SB scope totals

| Resource | SB baseline | Vanilla prior (adj.) | Variant H |
|---|---:|---:|---:|
| Arable Land | 439 | 540 | 482 |
| Coal Mine | 246 | 484 | 436 |
| Iron Mine | 58 | 153 | 136 |
| Lead Mine | 60 | 0 | 30 |
| Gold Fields (discovered) | 44 | 52 | 0 |
| Gold Fields (undiscovered) | 44 | 52 | 96 |

## Interpretation

The important balance result is:

- `Variant H` does **not** blow out aggregate coal and iron far beyond vanilla.
- The biggest numerical movement is in special gold fields, and that movement is mainly a **discovered -> undiscovered** semantic correction plus split-state separation.

In other words:

- the migration mostly redistributes where the game finds later mineral booms;
- it does not simply inflate every mining row upward.

That is the intended result.
