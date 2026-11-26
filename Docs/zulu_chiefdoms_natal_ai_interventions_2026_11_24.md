# Thirteen Chiefs interventions by British Natal and Transvaal

24 November 2026 · Victoria 3 1.15.2 · Confirmed design and implementation register

## British Natal

| Action | Dynamic Historical | Strict Historical |
|---|---|---|
| Policing | Commit 100 free Authority at **70% or higher** actual uSuthu Activism. Stand down at **40% or below** or when remaining Authority is negative. Zero remaining Authority can sustain the order. | Stand down throughout the JE, including an order inherited from a player. |
| Chiefly patronage | Start at **£500/week** with positive weekly income, positive cash and zero principal. Maintain course while living off savings, servicing debt from a surplus, or breaking even. Stop in default or when a deficit coincides with debt or empty reserves. | Stand down throughout. |
| Chiefly bribe | Above **50%** actual uSuthu Activism, approach the most prominent eligible neutral representative. Pay the whole price from cash if a positive weekly surplus remains after patronage and Natal is debt-free and outside default. | Decline throughout. |

At **20% or more** Zulu radicals in Natal, Dynamic Natal can permit the claimant to return. Once the claimant is physically home, the AI sends **20% of Natal’s Zulu peasant households** to Zululand if the Shepstone and territorial requirements are met. It checks before granting loyalists for the claimant’s return, then retries on the monthly review if still eligible. Strict can take both actions once the JE reaches **1,095 days**. [Return rules](../common/script_values/sb_zululand_drift_values.txt#L95) · [Refugee and claimant effects](../common/scripted_effects/sb_zululand_settlement_effects.txt#L927)

## Transvaal and the ZAR

TRN/ZAR can participate while backing Hamu. Natal’s monthly review adds an eligible Transvaal to an existing JE, including saves where it was absent when the JE opened. The September 1879 checkpoint has the Hamu subsidy and a Chiefs entry opened on 24 August with GBR, NAL and ZUL involved. [Participant check](../common/scripted_triggers/sb_zululand_settlement_triggers.txt#L121) · [Monthly membership update](../common/scripted_effects/sb_zululand_settlement_effects.txt#L808)

Both historical modes sanction volunteers whenever the participant has a Servicemen pop. This adds 20 points to the royal Activism target and earns **3 commitment per month**. The separate appeal sends **500 people** from one Boer Servicemen pop to the royal side’s land in Zululand and grants **20 commitment once**. Transvaal receives an announcement after they move. An undersized donor leaves the appeal pending. A held announcement or reload cannot move another 500. Off retains its equal AI odds of sending or declining. [Volunteer dispatch](../common/scripted_effects/sb_zululand_settlement_effects.txt#L1039) · [Transvaal announcement](../events/sb_zululand_settlement_events.txt#L130)

| Weekly finances | Start £250/week sponsorship | Existing sponsorship |
|---|---|---|
| Surplus and debt-free | Start, even with zero cash or a surplus smaller than £250 | Continue |
| Surplus and debt above zero but below 50% of maximum credit | Start if the weekly balance before the order is **greater than £250** | Continue |
| Surplus and debt at or above 50% | Stay off | Continue |
| Deficit and debt below 10%, including a draw on savings | Stay off | Continue |
| Deficit and debt at or above 10% | Stay off | Stop |
| Break-even | Stay off | Continue |

Default suspends paid interventions. An active subsidy is already included in the reported weekly balance. At 40% debt, +£251/week qualifies an inactive Transvaal for sponsorship and leaves £1/week. At +£250 it stays off. Sponsorship attracts supporters to the uSuthu and earns **2 commitment per month**. [Monthly orders](../common/scripted_effects/sb_zululand_settlement_effects.txt#L1236)

**Royal bribes depend entirely on finances and an eligible neutral chief.** With a positive weekly balance after sponsorship, choose the most prominent neutral representative whose full quote leaves debt at or below **10% of maximum credit**. This works at zero royal Activism. With £100,000 of credit, £8,000 principal and zero cash, a £2,000 purchase fits and £2,001 exceeds the limit. A debt-free payer with zero credit can spend available cash. [AI affordability](../common/scripted_triggers/sb_zululand_settlement_triggers.txt#L401)

## Delivery and replay

- The Natal monthly review checks both governments in their own country scopes, applies recurring orders, awards commitment, evaluates the settlement, then considers one bribe per eligible AI payer. The weekly JE review stands down unaffordable orders and reconciles modifiers on the actual royal and chiefly movements, including a civil-war split. Human governments retain their manual buttons. Off uses the original Transvaal sponsorship policy and appeal odds.
- The price remains **20%, 50% or 80% of the payer’s reserve capacity** at 10, 50 or 100 personal Prominence. A pending offer retains its payer, chief and price across reloads. AI rechecks the live budget, eligibility and neutrality at payment. If the other government has secured the house, the stale offer closes without a charge. [Price curve](../common/script_values/sb_court_politics_values.txt#L52) · [Payment event](../events/sb_zululand_settlement_events.txt#L548)
- The land grant requires **a royal victory, a valid promise and 100 earned commitment**. From zero, uninterrupted commandos can earn 100 in **34 monthly awards**, or **20** with sponsorship. A timely accepted appeal reduces those counts to **27** and **16**. [Commitment receipt](../common/scripted_effects/sb_usuthu_politics_effects.txt#L19)
- DP’s **1 June 1882** Anglo-Zulu War save uses Dynamic Historical and precedes the partition. It can replay the opening of the JE and the first monthly review. [Pre-JE checkpoint](<../../../save games/anglo-zulu-war-local_1882_06_01.v3>)
- On **1 June 1883** the JE is open. Natal has **63,084 radicals among 236,581 Zulu residents**. The largest Transvaal Servicemen pop is Tswana (8,873), followed by a Boer pop of 5,928. The old dispatch selected by size alone. Replay here to observe both the refugee return and the Boer departure. [Active JE](<../../../save games/13-chiefs-local_1883_06_01.v3>)
- On **17 February 1886** the old dispatch has a receipt, but neither NRP nor residual Zululand has a Boer pop. The new republic is governed by **Rudolf Petrus Cloete**, a generated Boer. The founding check now commissions Lucas Meyer explicitly and verifies the first government after the country is created. A new grant settles up to 500 surviving Boer residents in NRP, counting those already on its side of the split. An accepted boundary preserves the surviving community in **E1E455 and E882CE**. [Founding checkpoint](<../../../save games/NRP-formed-local_1886_02_17.v3>)

The source-executed regression covers both modes, financial and Activism boundaries, priority between a subsidy and a bribe, affordable target selection, competing and held offers, the appeal and the commitment clock. In-game budget timing, popup delivery and the eventual settlement are the remaining replay checks. [Intervention regression](../tests/test_chiefs_ai_interventions.py)
