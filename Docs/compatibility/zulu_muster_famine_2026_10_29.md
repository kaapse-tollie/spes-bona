# Klip River famine during the claimant war

29 October 2026. DP reports improved force balance but famine on the Klip River side. Five retained saves, September 1839–January 1840, confirm the famine. DP selected temporary wartime provisioning. That scoped relief is now implemented; the corrective engine replay remains pending. No saves were edited.

## Confirmed observations

The January save has two separate markets. Mpande holds Zululand as country 481; Dingane holds the Zulu-owned Natal portion as country 16777264. Both carry the new multi-state muster receipt.

| January 1840 | Zululand | Klip River |
|---|---:|---:|
| Population | 244,375 | 36,263 |
| Starving population | Under 0.01% | **100%** |
| Regular barracks | 3 | 2 |
| Temporary muster | 6 | 4 |
| Recorded grain output | 8.07910 | **1.43091** |
| Recorded meat output | 1.63383 | **0** |
| Recorded fruit output | 34.15272 | **0** |

Klip River's famine began **30 May 1839**, one week after the temporary muster was established on **23 May**. Its famine record lists 1,094 deaths by January. The state falls from 37,633 people in September to 36,263 in January, although births, war losses and population movement also affect that decline: it is not all attributable to famine.

The Klip River treasury has £4,088 and a positive weekly balance of about £309. Its six subsistence levels have capacity for 30,000 peasants but employ only 3,669. This is not evidence of bankruptcy or exhausted farmland. Commercial food production—the two ranch levels and a banana plantation—remains on the mainland. Klip River has only its small subsistence grain surplus. The main Zulu peasant Pop there has Food Security 0 and severe starvation; the total recorded starving share is 100% in all five saves.

## Cause and limits

The scripted allocation provides recruitment capacity and workers without providing a corresponding food-producing economy. Once the native war separates their markets, Klip River loses access to the mainland's food production. The retained saves support this economic explanation; they do not preserve complete current market buy-order/price caches or the exact initial population transfer.

More military recruitment or military wages alone does not supply missing food. Moving additional peasants without commercial production is not a demonstrated solution either: subsistence farms provide only a small marketable surplus. Do not equate military workforce capacity with a sustainable civilian economy.

The installed native Food Security description identifies food shortage and relative food expenditure as the two principal factors. The native Emergency Relief decree gives only +0.05 Food Security; that small effect must not be claimed to cure a zero-security market automatically. Any temporary relief tuning needs its own engine check and must be disclosed as an abstraction rather than a demonstrated increase in grain supply.

## Selected remedy and boundaries

DP selected the first of these two remedies:

1. Temporary wartime provision restricted to the scripted multi-state participants and removed at tracked resolution/cancellation. This keeps the current geographical economy intact but introduces a relief abstraction whose magnitude must be verified in-game.
2. Allocate existing food-producing buildings and their workers alongside the army. This provides actual food but extends the split into civilian economic redistribution, including ownership and lasting post-war consequences.

Do not change native one-state splits, arable-land history, unrelated markets, or global famine rules. Preserve the existing force balance while testing the selected remedy. Test both factions, both winners and the end of relief; avoiding famine for the first week is insufficient.

`sb_court_wartime_provisions` now gives **+1.5 Food Security** (+150 percentage points) to each actual faction when its scripted multi-state muster begins. The same tracked cleanup removes it on victory or cancellation, including native-war disappearance. It has no independent timer, repeated scan, treasury subsidy or goods output. It does not redistribute farms, alter force quotas or repair existing saves. One-state-origin wars never receive it.

The magnitude is deliberately a strong testing abstraction. Installed native arithmetic is `clamp(1 + modifier − basic-food cost share − shortage severity, 0, 1)`: a displayed zero may conceal a negative raw score, so +0.4 is insufficient. The most food-heavy installed buy package is wealth 1, with 90/151 of its base expenditure on basic food. At the native maximum price of 175% and full shortage, +1.5 leaves approximately **45.7% Food Security**, above the 40% starvation threshold. The focused test checks all installed wealth packages over base/minimum/maximum prices and shortage levels. This bound does not model every external modifier or establish engine relief delivery.

The [native excerpts](evidence/zulu_food_security_1_14_5_arm64.txt) preserve the pre-clamp calculation and cost-share inspection. Vanilla's Emergency Relief decree supplies the supported modifier and icon precedent; SB deliberately uses a much stronger value for this narrow trial. Food prices and the underlying economic shortfall remain. No claim is made that this creates grain or guarantees a sustainable independent post-war economy.

**Validation:** 87 focused claimant/muster tests pass, including both player choices, both winners, native-war disappearance, repeated cleanup, foreign-root isolation and the one-state bypass. Replay from before answering the claimant challenge; the new effect is not retroactively added to an already-created muster. Verify recovery after the first native food update and removal after reunification. No game was launched.

[Preserved evidence](evidence/zulu_muster_famine_2026_10_29.json) records save hashes, dates, populations, employment, output and budget observations. Full temporary snapshots are held in `/private/tmp/sb-muster-famine-2026-10-29/`. No game was launched and no corrective engine result is claimed.
