# Cross-Tag Event Travel-Time Audit

Date: 2026-07-22

Status: research baseline with the implemented normalisation matrix recorded below.

## Executive summary

SB currently uses many `1 day` and `3 day` handoffs between countries. Those values are plausible only in one of three circumstances:

1. The second event is part of the same administrative or military action rather than a new message.
2. The capitals are very close, normally less than about 200-300 km apart.
3. The event occurs after the relevant capitals have a working telegraph connection.

Before the interior telegraph network, a good lower bound for a fast frontier courier is about `100 km/day`. On established Cape post roads after the middle of the century, an aggressive lower bound is about `160 km/day`. These are deliberately optimistic values: they model the fastest plausible transmission of news, not ordinary travel. Actual routes were longer than the crow-flight distances used here and could be delayed by terrain, rivers, horse sickness, weather, security, and the availability of remounts.

The clearest current mismatches are:

- The Klip River chain, where every international handoff is currently one day.
- The Kimberley chain, where Cape Town, Bloemfontein, Kimberley, and sometimes Pretoria exchange decisions every three days.
- The Zoutpansberg compact appeal, where every Boer republic receives the appeal after the same three days regardless of distance.
- British colonial decisions before the 1879 international cable, where London sometimes receives or answers South African events in 1-21 days.
- Compact-renewal offers, which currently reach every Boer republic in one day even in the 1830s-1850s.

The later Bechuanaland and Anglo-Zulu content is much less problematic. By the late 1870s and 1880s, telegraphy makes a one-day political message credible on connected routes, although a physical commissioner, army, or governor would still take much longer.

## Implementation matrix

The normalisation uses fixed route delays for regional correspondence and dated script values for documented telegraph transitions. These delays apply only to newly scheduled events; events already queued in a save retain their original due dates.

### Reusable values

| Script value | Implemented timing |
|---|---|
| `sb_travel_london_southern_africa_message_days` | `50` before 1851; `42` during 1851-1871; `30` during 1872-1879; `3` from 1880. |
| `sb_travel_cape_eastern_message_days` | `6` before 1864; `3` from 1864. |
| `sb_travel_cape_kimberley_message_days` | `6` before 1876; `3` from 1876. |
| `sb_boer_compact_offer_message_days` | ORA-TRN `5`, ORA-ZPB `8`, ORA-LYD `7`, ORA-NAL `5`, TRN-ZPB `5`, TRN-LYD `4`, TRN-NAL `5`, ZPB-LYD `3`, ZPB-NAL `8`, LYD-NAL `5`. |
| `sb_natalia_boer_appeal_message_days` | ORA `5`, TRN `5`, ZPB `8`, LYD `5`, other Boer player countries `8`. |

The 1880 threshold represents the December 1879 international cable. The three-day value deliberately includes transmission, relay, decoding, and cabinet handling rather than modelling electrical transmission alone.

### Regional correspondence

| Chain | Implemented route |
|---|---|
| Klip River County | NAL-ZUL `2`; ZUL-ORA `6`; ORA-KLR/NAL `4`; same-country conflict preparation `1`. |
| Kimberley discovery | WBL-ORA `2`; WBL-TRN `5`; WBL-CAP uses the dated Cape-Kimberley value. |
| Kimberley claimant exchange | ORA-CAP `6`; TRN-CAP proxy route `10`; claimant-WBL is ORA `2` or TRN `5`; WBL-CAP uses the dated Cape-Kimberley value. |
| Zoutpansberg convention | TRN-ZPB `5`; ZPB appeal to ORA `8`, LYD `3`, NAL `8`; replies to TRN are ORA `5`, LYD `4`, NAL `5`, ZPB `5`. |
| Boer compact renewals | Uses the ten-pair matrix above, evaluated from proposer and recipient. |
| Marthinus coercive claim | TRN-ORA `5`; ORA-LYD `7`; ORA-ZPB `8`; ORA-NAL `5`; the `21-day` reply aggregation window remains unchanged. |
| Other Boer notices | NAL-TRN voluntary union `5`; CAP-TRN Grey proposal `10`; ZPB creation notices to ORA/TRN/NAL `8/5/8`; TRN-SWZ border correspondence `5` each way. |

### Imperial correspondence

Every actual dispatch between Britain and Southern Africa uses `sb_travel_london_southern_africa_message_days`: TRN formation, Albany's appeal and answer, Albany abolition instructions, BST and SWZ protection petitions, the BST claimant notice, the Port Natal raid report, Cape colonial-law pressure, the Transvaal confederation exchange, and the Imperial Confederation demand concerning Delagoa. CAP-ABY notices use the dated Cape eastern-network value.

The Natalia ultimatum now follows this order:

```text
GBR sends ultimatum
└─ London-Southern Africa message delay
   └─ NAL receives the ultimatum
      ├─ route-timed appeals reach Boer players
      └─ 9-day consultation
         └─ NAL answers
            ├─ AI Boer appeals use 5/5/8/5 days
            └─ refusal reaches Britain after the London message delay
```

Immediately before Britain opens the play, NAL is checked again for survival, independence, peace, and freedom from another committed play. An invalid target cancels the launch and clears the pending support markers.

### Mechanical exceptions

Short delays remain for hidden war setup, mandatory backers and war goals, result finalisers, country creation and tag changes, player-switch prompts, simultaneous IS notifications, expedition timers, Great Trek migration, Blood River/Retief narrative pacing, and same-country administrative follow-ups. These are one mechanical action rather than a second dispatch.

## What is being timed

The audit treats an event delay as the earliest plausible time for the information, demand, or reply represented by the next event to reach the receiving capital.

It does **not** automatically impose travel time on:

- hidden war-start setup;
- a diplomatic play and its mandatory war goals created by one decision;
- a country-creation event and its immediate setup package;
- a same-country summary or confirmation event;
- a player-switch prompt;
- simultaneous notifications of an already completed result.

Those are one logical action and can remain at `0-1 day` for engine reliability. When an event explicitly describes commissioners, an embassy, or a personal mission, the physical-travel figure is more appropriate than the faster message figure.

## Method

### Distance

Distances are great-circle distances between the assumed capitals, calculated with the haversine formula and rounded to the nearest 10 km:

```text
d = 2R * asin(sqrt(sin^2((lat2-lat1)/2)
    + cos(lat1) * cos(lat2) * sin^2((lon2-lon1)/2)))
```

This is the user's requested crow-flight minimum. It is not a route distance. It therefore produces a lower bound, especially across mountains, deserts, rivers, and sea routes.

### Inland calculation

For an untelegraphed political message:

```text
frontier minimum days = ceil(crow distance / 100 km per day)
Cape post-road minimum days = ceil(crow distance / 160 km per day)
```

The `100 km/day` frontier value follows evidence that long Cape horseback journeys could cover about 60 miles, or 97 km, per day. The `160 km/day` post-road value uses the exceptional 1857 report of 103 miles in 13 hours as an optimistic hard floor and assumes remounts or a very urgent courier. Ordinary wagons were closer to 40 miles, or 64 km, per day.

### Sea, rail, telegraph, motor, and air calculation

For long sea routes and scheduled rail or air routes, observed service times are more useful than dividing distance by a vehicle's instantaneous maximum speed. For example, a ship capable of 17 knots could not sustain that speed around Africa through contrary weather, coaling, port calls, and routing.

For telegraph-connected capitals, the report uses `1 day`. The electrical transmission itself was much faster, but a calendar day allows for filing, relaying, decoding, ministerial handling, and the game clock.

## Transport eras, 1836-1936

| Period | Fastest relevant system | Maximum or sustained benchmark | Audit rule |
|---|---|---|---|
| 1836-1850 | Horse, wagon, sail, early coastal steam | Long horseback travel about `97 km/day`; an exceptional 1857 ride covered `166 km` in 13 hours; wagon travel about `64 km/day`. A fast sailing ship could exceed `17 knots` in ideal winds, but `8-10 knots` is a safer planning ceiling. | Use `100 km/day` on the frontier. Use `160 km/day` only on an established Cape post road. Use an observed packet/voyage time for overseas routes. |
| 1851-1859 | Improved post roads and contract steam packets | The 1857 Southampton-Cape mail contract required a passage no longer than `42 days`. Cape post carts moved at about `7-10 mph` while running and changed horses regularly. | Inland as above; London-Cape political mail cannot plausibly be faster than about `42 days`, plus inland delivery. |
| 1860-1875 | Telegraph trunk lines, local rail, faster steam packets | Cape Town-Simon's Town telegraph opened in 1860 and Cape Town-Grahamstown in 1864. The 1863 mail contract allowed `38 days`; the 1872 proposal offered `30 days`. | Connected telegraph message: `1 day`. Otherwise retain horse/post or steam-packet floor. |
| 1876-1885 | Interior telegraph, international cable, expanding mainline rail | Kimberley joined the Cape telegraph network in 1876. South Africa obtained a cable link to Europe through Durban in December 1879. An 1882 Cape special train averaged `34 mph` (`55 km/h`) over 339 miles excluding stops. | Connected political messages: `1 day`. A physical rail traveller still needs at least `1-3 days` on regional routes. |
| 1886-1899 | Regional rail and telegraph, mature steam mail | In 1889 Cape Town-Kimberley took `42 hours` by rail over roughly 600-700 miles. Rail still ended at Kimberley for much of the northern interior. | Major connected capitals: `1 day` by telegram. Physical Cape-Kimberley trip: `2 days`; add frontier courier time beyond the railhead. |
| 1900-1918 | Rail, telegraph, early motor cars | A 1900 Cape motor demonstration reached `32 mph` (`51.5 km/h`), but early long-distance motor travel was far slower and road-limited. Rail remained the dependable long-distance mode. | Telegraph: `1 day`. Physical road travel: use about `20-30 km/h` sustained on a usable route, not the demonstration maximum. |
| 1919-1931 | Mature rail and motor transport, experimental aviation | Good-road motor travel could outperform horses locally, while the rail network carried long-distance passengers and mail. No regular London-Cape air service yet existed. | Political message: `1 day`. Physical regional trip: usually `1-3 days` by rail or motor if connected. |
| 1932-1936 | Telegraph, rail, motor, scheduled civil aviation | Imperial Airways aircraft cruised around `95-100 mph` (`153-161 km/h`). The early London-Cape route involved about 72 airborne hours, around 30 stops, aircraft changes, and 2,000 km of rail; the scheduled passenger journey took about `10 days`. | Telegram remains the one-day political floor. Air reduces long personal journeys, but does not make London-Cape same-day travel plausible. |

### Vehicle-speed reference

| Mode | Fastest defensible benchmark used here | Why it is not applied mechanically to the whole journey |
|---|---:|---|
| Long-range horse rider | About `97 km/day` on extended journeys | The animal needs rest and forage, and frontier routes did not provide continuous remount stations. |
| Exceptional rider / relay post | `166 km` in 13 hours in the cited 1857 example; post carts ran at about `11-16 km/h` while moving | This is an optimistic ceiling on a prepared route, not an ordinary daily average everywhere in Southern Africa. The 1857 example is used as a mid-century ceiling, not evidence that every 1836 route could sustain it. |
| Horse or ox wagon | About `64 km/day` | Wagons moved people and supplies but were not the fastest way to carry an urgent political message. |
| Fast sailing ship | Greater than `17 knots`, or about `31.5 km/h`, in ideal wind | This is a peak sailing speed. Wind, routing, calms, and port handling make it unsuitable as a direct event-delay divisor. |
| Contract steam packet | Southampton-Cape schedules of `42 days` in 1857, `38 days` under the 1863 contract, and a proposed `30 days` in 1872 | The observed end-to-end mail schedule already includes the operational limits that a nominal ship speed omits. |
| Steam railway | `34 mph`, or `55 km/h`, on an 1882 special train excluding stops | Normal timetables, stops, gradients, incomplete lines, and a courier beyond the railhead substantially reduce end-to-end speed. |
| Early motor car | `32 mph`, or `51.5 km/h`, at a 1900 Cape demonstration; roughly `20-30 km/h` is a safer usable-road planning rate | The demonstration maximum did not describe a long journey over frontier roads. |
| Early scheduled aircraft | `95-100 mph`, or `153-161 km/h`, airborne | Frequent stops, daylight operations, transfers, weather, and rail segments made the 1932 London-Cape passenger schedule about ten days. |

## Capital assumptions

| Tag | Audit capital | Notes |
|---|---|---|
| GBR | London | Strictly follows the user's capital-to-capital rule, even where a local governor or High Commissioner could historically act faster. |
| POR | Lisbon | Portuguese imperial decisions. |
| GER / SWA overlord | Berlin in the canonical German route | A different overlord requires recalculation. |
| CAP / most SAF routes | Cape Town | SAF can inherit another institutional base; that is a dynamic exception. |
| ABY | Grahamstown / Makhanda | Approximation for the Albany administration. |
| XHO | Qonce / King William's Town area | Approximation for a mobile Xhosa court and frontier government. |
| ORA | Bloemfontein | Used throughout. |
| TRN | Potchefstroom before 1860; Pretoria thereafter | Both distances are shown when the distinction matters. |
| NAL | Pietermaritzburg | Applies to Boer Natalia and British Natal unless the capital moves. |
| KLR | Ladysmith | Klip River County. |
| ZUL | Mgungundlovu/Ulundi area | Ulundi is used as a stable map approximation. |
| SWZ | Lobamba | Used throughout. |
| BST | Thaba Bosiu | Used throughout. |
| PHL | Philippolis | Used throughout. |
| WBL | Kimberley | The game capital/hub is used; early historical Griquatown would add or subtract distance depending on the route. |
| ZPB | Schoemansdal | Used throughout. |
| LYD | Lydenburg | Used throughout. |
| GLE | Kokstad | Used throughout. |
| GZA / MZQ | Lourenco Marques / Maputo | Used for the relevant southern Mozambique events. |
| SWA | Windhoek | Used for colonial-administration travel. |
| SGO | Vryburg | Used for Stellaland-Goshen. |

## Cross-tag event audit

The `minimum lag` column is the earliest defensible delay for the event as written. Where a set can fire across several decades, both pre-telegraph and telegraph values are given.

### Great Trek, Natalia, and the early frontier

| Event set | Expected date | Capital leg and crow distance | Relevant transport | Current scripted handoff | Minimum lag |
|---|---:|---|---|---:|---:|
| `struggle_for_the_highveld.1 -> .2`, Battle of Vegkop / In Mzilikazi's Wake | 1836-1838 | ZUL Ulundi to TRN Potchefstroom, about `460 km` | Frontier rider | `0 days` | `5 days` if this is news sent to the TRN capital. If it is one battlefield-resolution action, `0-1 day` is acceptable. |
| `struggle_for_the_highveld.3 -> .4`, Natal Cession / Boers Demand the Thukela | 1837-1838 | ORA Bloemfontein to ZUL Ulundi, about `520 km` | Embassy or mounted courier | `7 days` | `6 days` for a courier; `8-10 days` is better if Retief's physical delegation is intended. Current value is defensible. |
| `sb_natal_crisis.010-.051`, Retief mission and Blood River diplomatic branches | 1837-1840 | Bloemfontein-Ulundi `520 km`; later Ulundi-Pietermaritzburg `170 km` | Physical delegation, then frontier courier | Mostly `7-30 days` | `6-10 days` for ORA-ZUL; `2 days` for ZUL-NAL. Existing narrative delays are not too short. |
| `sb_swazi_frontier.094-.097`, ZUL-SWZ war question and result | 1839-1845 | Ulundi-Lobamba about `210 km` | Frontier courier | Opening `21 days`; follow-up `5 days` | `3 days`. Existing values are conservative. |
| `sb_natal_crisis.100-.119`, British ultimatum to Natalia and Boer appeals | 1842-1845 | London-Pietermaritzburg `9,500 km`; NAL-ORA `410 km`; NAL-TRN `450-480 km`; NAL-ZPB `730 km`; NAL-LYD `500 km` | Sailing/early steam mail, then mounted couriers | GBR-NAL `21 days`, NAL reply `1 day`, Boer appeals `7/10/12/14 days` | London-NAL `45-60 days`; NAL-ORA `5`; NAL-TRN `5`; NAL-ZPB `8`; NAL-LYD `5`. The staggered Boer appeals are plausible, but the imperial leg is too fast under a strict London-capital reading. |
| `sb_klip_river_county.010-.060`, commissioners, Zulu answer, ORA appeal, and conflict launch | 1843-1846 | NAL-ZUL `170 km`; ZUL-ORA `520 km`; ORA-KLR `360 km`; KLR-NAL `130 km` | Mounted courier or physical commissioners | Every international handoff is `1 day` | NAL-ZUL `2 days`; ZUL-ORA `6`; ORA-KLR `4`; KLR-NAL `2`. This is the strongest early-chain candidate for retiming. |
| `sb_boer_republics.007`, British notice of TRN formation | 1838-1852 | Potchefstroom-London about `9,100 km` crow-flight | Sailing/steam packet plus overland post | `14 days` | About `45-60 days` before the contract packet era; about `47-52 days` in the 1850s. |
| `sb_boer_republics.120-.131`, ZPB and LYD creation notices | 1840s-1850s | ZPB-ORA `760 km`; ZPB-TRN `330-480 km`; ZPB-NAL `730 km`; LYD-TRN `230-380 km` | Frontier courier | ZPB notices `7 days`; LYD fork `60 days` | ZPB-ORA `8`; ZPB-TRN `4-5`; ZPB-NAL `8`; LYD-TRN `3-4`. The seven-day common value is close, while the constitutional fork is intentionally much longer than transport requires. |
| `sb_frontier_ai_wars.010-.040`, ORA-PHL, ORA-BST, BST-TRN/ZPB, and ZUL-GZA scripted plays | 1840-1856 | ORA-PHL `160 km`; ORA-BST `150 km`; BST-TRN about `300-420 km`; ZUL-Maputo `290 km` | Local frontier warning and mobilization | Hidden events normally wait `7-14 days` after a qualifying pulse | No cross-country event reply is represented. Keep as a mechanical exception; `2-5 days` would be the courier floor if an ultimatum event is later added. |
| `sb_cape.001` and `sb_frontier_ai_wars.100-.120`, Cape-Xhosa opening and scripted wars | 1836; then after 1845, 1850, and 1870 | Cape Town-Qonce about `840 km` | Cape post road, later telegraph | Opening after `7 days`; hidden war scheduling varies | About `6 days` by urgent post before 1864; `1 day` after the 1864 Cape-Grahamstown telegraph, plus a short frontier relay where needed. War creation itself is a mechanical exception. |

### Conventions, Boer unions, and Cape constitutional content

| Event set | Expected date | Capital leg and crow distance | Relevant transport | Current scripted handoff | Minimum lag |
|---|---:|---|---|---:|---:|
| `sb_boer_conventions.140/.161`, Sand River Convention | Around 1852, but dynamically later | London-Potchefstroom `9,100 km` or London-Pretoria `9,030 km` | Contract steam mail plus frontier post; telegraph only after 1879 | Initial event randomly delayed `60-240 days` | About `50 days` in the 1850s; `30-40 days` in the 1870s before the cable; `1 day` after December 1879. Current opening delay safely covers transmission. |
| `sb_boer_conventions.141`, Bloemfontein Convention | Around 1854, but dynamically later | London-Bloemfontein `9,320 km` | Steam packet plus Cape post | Random `1-6 years` after the gate | About `48 days` in the 1850s; `1 day` after the international telegraph connection. The present delay is political pacing, not travel time. |
| `sb_boer_conventions.142/.160`, British anti-slavery response and Albany imposition | 1850s-1870s | London to TRN/ORA/ABY, roughly `9,100-9,780 km` | Steam mail, later cable | Often `7-90 days`, with longer retry timers | `45-55 days` before 1879; `1 day` after 1879. A DP created by the British response needs no additional second delay. |
| `sb_boer_conventions.143-.151`, ZPB invokes the Boer compact | 1850s-1860s | ZPB-TRN `330-480 km`; ZPB-LYD `240 km`; ZPB-ORA `760 km`; ZPB-NAL `730 km` | Frontier courier | All appeals and the TRN summary use `3 days` | TRN `4-5`; LYD `3`; ORA `8`; NAL `8`. The equal three-day fan-out is implausible for ORA and NAL. |
| `sb_boer_compacts.010`, compact-renewal offers | Any date | Dynamic pair: ORA-TRN `280-420 km`; ORA-ZPB `760`; ORA-LYD `610`; ORA-NAL `410`; TRN-ZPB `330-480`; TRN-LYD `230-380`; TRN-NAL `450-480`; ZPB-LYD `240`; ZPB-NAL `730`; LYD-NAL `500` | Frontier courier, later telegraph | Every recipient gets the offer after `1 day` | Before telegraph: respectively `3-5`, `8`, `7`, `5`, `4-5`, `3-4`, `5`, `3`, `8`, and `5 days`. Use `1 day` only once the relevant pair has telegraph access. |
| `sb_martinus_confederation.002 -> .001`, Grey's Cape/Orange proposal | 1854-1861 | Cape Town-Bloemfontein about `910 km` | Cape post route | `7 days` | `6 days`. Current value is sound. |
| `sb_martinus_confederation.010-.048`, coercive Pretorius claim | 1854-1860s | TRN-ORA `280 km` from Potchefstroom or `420 km` from Pretoria; ORA-LYD `610`; ORA-ZPB `760`; ORA-NAL `410` | Frontier courier | TRN-ORA `7`; ORA backer events `7`; aggregate TRN response `21` | TRN-ORA `3-5`; ORA-LYD `7`; ORA-ZPB `8`; ORA-NAL `5`. The 21-day aggregation safely allows every reply. |
| `sb_martinus_confederation.080-.082`, election and shared presidency | 1850s onward | Same ORA political process | Same-country administration | `1 day` | `0-1 day`; exempt. |
| `sb_martinus_confederation.120-.121`, Natalia voluntarily joins the union | 1850s onward | Pietermaritzburg-Potchefstroom/Pretoria about `450-480 km` | Frontier courier | `3 days` | `5 days` before telegraph; `1 day` once connected. |
| `sb_martinus_confederation.131 -> .130`, Grey's Transvaal proposal | Late 1850s-1860s | Cape Town-Potchefstroom/Pretoria about `1,270-1,310 km` | Cape post plus frontier courier | `7 days` | About `9-12 days` before a through telegraph route. |
| `sb_swazi_border.1-.4`, TRN-SWZ border claim | 1850s-1860s | Potchefstroom-Lobamba about `410 km`, or Pretoria-Lobamba `310 km` | Frontier courier | `7 days` each way | `4-5 days`. Current value is conservative. |
| `sb_cape.103/.200-.205`, Albany secession and London response | 1850s-1870s | Cape Town-London `9,670 km`; Cape Town-Grahamstown `750 km` | Steam mail and Cape post; Cape-Grahamstown telegraph after 1864 | CAP-GBR can be immediate; GBR-CAP `7/21 days`; CAP-ABY `14 days` | CAP-London `42-50 days` in the 1850s, `30 days` in the 1870s before 1879, then `1 day`; Cape-ABY `5 days` before 1864 or `1 day` after. The pre-cable imperial replies are too fast. |
| `sb_cape.020/.030/.031`, Responsible Government | 1850s-1872 normally, but dynamic | Cape Town-London `9,670 km` | Steam mail, later cable | Several `1-7 day` follow-ups | `30-50 days` before 1879; `1 day` after 1879. Same-CAP cleanup events remain exempt. |
| `sb_cape.111/.120-.122/.130`, Convict Crisis and rival law petitions | 1849-1870s | Primarily Cape internal politics; the Convict Crisis also invokes London | Cape political process; steam mail if London answers | Mostly `7-21 days` | Internal CAP steps need no travel floor. Any explicit London answer should use `42-50 days` before 1879. |
| `sb_frontier_ai_wars.130`, Xhosa Cattle-Killing Movement | 1856 onward at first peace | Cape Town-Qonce about `840 km` | Urgent post | Monthly pulse, so `1-30 days` | About `6 days`. The monthly pulse already exceeds the physical minimum on average. |
| `sb_griqualand_east.220-.221`, creation and integration of GLE | 1860s-1870s | Cape Town-Kokstad about `1,100 km` | Cape post; telegraph through the eastern network later | Creation `14 days`; integration `1 day` | About `7 days` before a through telegraph route; `1 day` after connection. The integration is also defensible as one administrative act rather than a reply. |
| `sb_bst_frontier.100 -> .110`, British protection of BST and notice to the Boer claimant | 1850s-1870s | London-Thaba Bosiu `9,390 km`; London-Bloemfontein `9,320 km` | Steam mail, later cable | Boer claimant notified after `1 day` | `45-55 days` before 1879; `1 day` after 1879. If the event is rewritten as the Cape High Commissioner's act, Cape Town-Bloemfontein is about `6 days` by urgent post. |

### Diamonds, ports, imperial confederation, and late colonial crises

| Event set | Expected date | Capital leg and crow distance | Relevant transport | Current scripted handoff | Minimum lag |
|---|---:|---|---|---:|---:|
| `sb_griqualand_west.021/.022`, discovery reaches the claimant | 1867-1872 | Kimberley-Bloemfontein `140 km`; Kimberley-Potchefstroom `320 km`; Kimberley-Pretoria `480 km`; Kimberley-Cape Town `830 km` | Mounted courier and Cape post | Every branch uses `3 days` | ORA `2 days`; TRN `4-5`; CAP `6 days`. Three days is reasonable only for the ORA route. |
| `sb_griqualand_west.022 -> .023`, claimant presses CAP | 1867-1872 | Bloemfontein-Cape Town `910 km`, or TRN-Cape Town `1,270-1,310 km` | Cape post plus frontier courier | `3 days` | ORA-CAP `6`; TRN-CAP about `9-12`. |
| `sb_griqualand_west.023 -> .241/.242/.243`, CAP answers claimant | 1867-1872 | Same routes in reverse | Cape post plus frontier courier | `3 days` | ORA `6`; TRN `9-12`. |
| `sb_griqualand_west.241/.242 -> .251`, claimant asks WBL to choose | 1867-1872 | Bloemfontein-Kimberley `140 km`, or TRN-Kimberley `320-480 km` | Frontier courier | `3 days` | ORA-WBL `2`; TRN-WBL `4-5`. |
| `sb_griqualand_west.251 -> .252/.253/.254`, Waterboer's choice reaches CAP | 1867-1872 | Kimberley-Cape Town `830 km` | Cape post | `3 days` | `6 days` before the 1876 telegraph link; `1 day` after 1876. |
| `sb_griqualand_west.025/.260`, authority and Diamond Rush outcomes | 1870s onward | Dynamic winner, WBL, and CAP | Post or telegraph | Usually `7-14 days` or same-event effects | `1 day` after Kimberley's 1876 telegraph connection; before then use the appropriate `2-6 day` route above. Immediate mine/subject effects are mechanical exceptions. |
| `sb_delagoa.010-.021`, Delagoa Route to the Sea | Usually 1860s-1890s | TRN-Maputo about `230-440 km`; Lisbon-Maputo `8,400 km` | Frontier courier and ocean mail; international cable after 1879 | Completion events fire after `1 day` | TRN-Maputo `3-5 days` before telegraph; Lisbon-Maputo roughly `30-45 days` before 1879; `1 day` after 1879. The completion can remain one day if it is merely a simultaneous IS result notification. |
| `sb_imperial_confederation.030 -> .031`, London demands Delagoa | Usually 1870s-1890s | London-TRN about `9,000-9,100 km` | Steam mail before 1879, international telegraph afterward | `7 days` | `30-50 days` before 1879; `1 day` after 1879. |
| `sb_imperial_confederation.001/.050/.051`, scheme opening and result | Usually 1870s-1890s | GBR and a dynamic participant set | Steam mail or telegraph | Generally same-event or short notification | Before 1879, a London-led visible response needs `30-50 days`; after 1879, `1 day`. The contextless JE opening and final mechanical rewards are exempt. |
| AI GBR opens the standard Anglo-Zulu annexation play | Confederation-era transit route, or 1879 onward | London-Ulundi about `9,400 km` | Steam mail before late 1879; international cable thereafter | Diplomatic play opens immediately once its gates pass | The ordinary diplomatic-play escalation period supplies the warning and political preparation. No extra scripted message delay is needed; the Zulu victory result remains a short `3-day` mechanical notification. |
| `sb_bst_frontier.220`, Basotho Gun War | 1879-1881 normally | Cape Town-Thaba Bosiu `1,010 km` | Interior telegraph by this period | Event or DP created immediately once gates pass | `1 day` for a political message. The play and its goals are one action and need no extra delay. |
| `sb_nam.010-.151`, Namibia mission, SWA formation, and overlord administration | 1870s-1890s | Berlin-Windhoek `8,360 km` in the German route | Ocean mail, then cable/telegraph; physical governor still travels by sea | SWA setup and play-as prompt use `1 day` | Political telegram `1-3 days` once a coastal connection exists; physical official or expedition `20-30 days`. Country creation and the player-switch prompt are mechanical exceptions and may remain at one day. |
| `sb_bechuanaland_corridor.001/.010`, crisis opening and Warren demand | Around 1884-1885 | Cape Town-Vryburg `980 km`; Kimberley-Vryburg `200 km` beyond the northern rail/telegraph axis | Telegraph to Kimberley plus courier beyond it | Crisis intro `1 day`; Warren demand `3 days` | About `3 days` in 1884: one day to the rail/telegraph head and two days by urgent courier. Current Warren delay is well chosen. |
| `sb_bechuanaland_corridor.020/.021`, SWA-overlord intervention response | Around 1884-1885 | Dynamic European GP capital to London; Berlin-London about `930 km` | European telegraph | `3 days` | `1 day`. Three days is conservative but credible for cabinet handling. |
| `sb_bechuanaland_corridor.030 -> .031`, Caprivi memorandum and British answer | Around 1884-1885 | Berlin-London `930 km` in the German route | European telegraph | `3 days` each way | `1 day` each way. Again, three days can represent deliberation rather than transport. |
| `sb_gaza.040`, Guns on the Caravan Road and relations with POR | 1836-1860s | Maputo-Lisbon `8,400 km`, but POR receives no reply event | Local raid/policy decision | Single GZA-facing event | No inter-event lag to change. If Portugal is later given a response event, use `30-50 days` before 1879 or `1 day` afterward. |
| `sb_griqualand_east.221` and late CAP subject integrations | 1870s onward | Cape Town-Kokstad `1,100 km` | Eastern Cape/Natal telegraph by the late 1870s | `1 day` | `1 day` after telegraph connection; otherwise about `7 days`. |

## Cross-tag sets that should remain immediate

The following involve more than one tag in script, but do not represent a message travelling from one capital to another:

- The force, modifier, and war-goal setup inside `sb_frontier_ai_wars.*`.
- Country creation and setup in `sb_boer_republics.*`, `sb_griqualand_east.220`, `sb_nam.140-.151`, and `sb_klip_river_county.050/.060` once the political decision has already arrived.
- Result finalizers in the Kimberley, Basotho, Natalia, Anglo-Zulu, and Bechuanaland chains.
- Simultaneous IS opening/closing notices in Delagoa and Imperial Confederation.
- The SWA player-switch offer.
- Relationship changes toward POR in `sb_gaza.040`, because Portugal does not receive a second event.

Artificially delaying these would not make the story more historical. It would only create a window in which scopes, ownership, wars, or subject relationships could change between two halves of what is logically one effect.

## Recommended reusable timing bands

These are convenient script-facing bands for a future implementation pass. They are rounded upward from the calculated minima so they remain believable despite the crow-flight underestimate.

| Circumstance | Suggested delay |
|---|---:|
| Same country or same administrative act | `0-1 day` |
| Adjacent capitals under 200 km, before telegraph | `2 days` |
| 200-400 km frontier route | `3-5 days` |
| 400-700 km frontier route | `5-8 days` |
| 700-1,100 km frontier/Cape route | `8-12 days` |
| London-Southern Africa before 1851 | `50-60 days` |
| London-Southern Africa, 1851-1871 | `42-55 days` including inland delivery |
| London-Southern Africa, 1872-1878 | `30-40 days` including inland delivery |
| Connected domestic telegraph, from the relevant local connection date | `1 day` |
| London-Southern Africa after December 1879 | `1 day` for a telegram; `18-25 days` for a person or physical document by sea |
| Physical regional rail journey, late 1880s onward | `1-3 days` on a connected route |
| Scheduled London-Cape air journey, 1932-1936 | about `10 days` |

## Namespace coverage check

| Event namespace/file | Treatment in this report |
|---|---|
| `struggle_for_the_highveld` | Great Trek/Natal rows. |
| `sb_anglo_zulu` | Anglo-Zulu row. |
| `sb_bechuanaland_corridor` | Warren, intervention, and Caprivi rows. |
| `sb_boer_compacts` | Dynamic compact-renewal row. |
| `sb_boer_conventions` | Sand River, Bloemfontein, anti-slavery, and ZPB compact rows. |
| `sb_boer_republics` | Republic-formation notification rows. |
| `sb_bst_frontier` | British protection, transfer, and Gun War rows. |
| `sb_cape` | Cape-Xhosa, Albany/London, Responsible Government, Convict Crisis, and petition rows. |
| `sb_delagoa` | Delagoa IS row. |
| `sb_firearms` | Excluded: the completion event is single-country. |
| `sb_frontier_ai_wars` | Frontier-war and Xhosa rows; war setup marked as a mechanical exception. |
| `sb_gaza` | POR relationship row. |
| `sb_great_trek` | Great Trek/Highveld rows. |
| `sb_griqualand_east` | GLE creation/integration rows. |
| `sb_griqualand_west` | Kimberley rows. |
| `sb_imperial_confederation` | Scheme, Delagoa response, and Natal acceleration rows. |
| `sb_klip_river_county` | Klip River row. |
| `sb_martinus_confederation` | Grey, coercive claim, election, and NAL union rows. |
| `sb_namibia` | Mission/SWA administration row. |
| `sb_natal_crisis` | Retief/Blood River and British ultimatum rows. |
| `sb_swazi_border` | TRN-SWZ row. |
| `sb_swazi_frontier` | ZUL-SWZ row. |
| `sb_zulu_court` | Excluded: all events are internal to ZUL. |
| `sb_zulu_dynasty` | Excluded: succession events are internal to ZUL; cross-border war results are covered under their originating chains. |

## Important caveats

1. A capital-to-capital rule intentionally overstates London involvement in some colonial decisions. Historically, a governor, High Commissioner, resident, or military commander in Southern Africa could act without waiting for a new dispatch from London. If an event's text explicitly identifies that local authority, Cape Town, Pietermaritzburg, or the field headquarters should replace London.
2. Crow-flight distance systematically understates real land travel. The calculated values are floors, not typical journey times.
3. Telegraph availability was route-specific, not a universal technology switch. Cape Town-Grahamstown is valid from 1864, Kimberley from 1876, Natal's link into the Cape network from 1878, and international communication from late 1879. Remote frontier endpoints still needed a courier from the nearest office.
4. A telegram can carry a decision but not a commissioner, army, refugee population, or signed physical instrument. Events describing physical movement should retain rail, road, or sea travel time even after telegraphy.
5. Dynamic capitals, conquest, civil wars, and alternate SWA overlords can invalidate a fixed distance. The values here audit the expected historical route and should not be turned into country-specific hard gates without fallback logic.

## Sources

- Chris Andreas, "Species Extinction, Infrastructure Development and Epidemics: The Changing Ecology of African Horsesickness in the Cape Colony, c.1653-1900," for roughly 60-mile riding days, the exceptional 103-mile 1857 ride, 40-mile wagon days, and post-cart speeds: <https://www.tandfonline.com/doi/full/10.1080/03057070.2024.2508570>
- UK Parliament, 1873 Cape mail-contract debate, for 38-day and proposed 30-day Southampton-Cape mail schedules: <https://hansard.parliament.uk/Commons/1873-06-09/debates/09188250-7fd4-4b02-ada8-f46c38ffd802/CommonsChamber>
- TPO & Seapost Society, for the 1857 mail contract's 42-day maximum voyage: <https://www.tpo-seapost.org.uk/tpo2/spcapepacket.html>
- Royal Museums Greenwich, for the meaning of a knot and Cutty Sark's greater-than-17-knot peak under favorable wind: <https://www.rmg.co.uk/stories/maritime-history/knots-measuring-speed-sea>
- Franco Frescura Archive, Cape telegraph diary, for the 1864 Cape Town-Grahamstown link, Kimberley in 1876, and the 1879 European connection: <https://francofrescura.sahistory.org.za/postal-history/postal-history-telegraphy-diary/>
- South African History Online, for the first South Africa-Europe cable in 1879: <https://sahistory.org.za/dated-event/first-cable-connection-between-sa-and-europe-launched>
- The Heritage Portal, for the 42-hour Cape Town-Kimberley rail journey in 1889: <https://www.theheritageportal.co.za/review/here-fascinating-account-what-south-africa-was-1889>
- Cape Government Railways 1st Class 4-4-0 service history, for the 1882 34 mph special-train benchmark: <https://en.wikipedia.org/wiki/CGR_1st_Class_4-4-0>
- Franschhoek Motor Museum, for the 32 mph maximum recorded at the 1900 Cape motor event: <https://www.fmm.co.za/anniversary-celebration-south-africas-first-motorrace/>
- Gordon Pirie, "Incidental tourism: British Imperial air travel in the 1930s," for the early London-Cape route's 72 airborne hours, roughly 30 stops, aircraft changes, and rail segments: <https://www.tandfonline.com/doi/full/10.1080/17551820902742772>
- Imperial Airways route history, for the 1932 London-Cape mail and passenger service and the roughly ten-day passenger schedule: <https://en.wikipedia.org/wiki/Imperial_Airways>
