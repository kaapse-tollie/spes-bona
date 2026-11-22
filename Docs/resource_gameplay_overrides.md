# Resource Gameplay Override Record

**Decision date:** 2026-08-25

**Status:** implemented; fresh campaign required

**Playtest status:** Drakensberg and Walvis Bay checks pending

**Evidence baseline:** [full resource audit, 24 August 2026](../../References/Resource%20rework/sb_full_resource_audit_2026-08-24/README.md)
**Implementation guide:** [Resource Update: Contributor and Maintainer Guide](resource_update_guide.md)

## 1.15.1 compatibility update — 11 November 2026

The port follows native copper: Namaqualand **9**, Zambia **21** and Katanga
**35**, for **65** across the regional file. The researched SB allocation contains
Namaqualand's 9; Zambia and Katanga remain unchanged native state blocks.
Northern Cape's eight lead proxy levels remain removed. Hereroland 10 and
Namaqualand 2 lead remain, giving the SB allocation **12 lead** and **9 copper**.
The historical tables below retain their dated research/comparison baselines.
See the [hotfix report](compatibility/cmf_1_67_3_and_1_15_1_patch_2026_11_11.md).
The copper-focused follow-up remains RES115-01 in the
[open register](audit_issues_open.md#victoria-3-115--remaining-verification-and-secondary-extensions).

## Decision rule

The full resource audit remains the evidence record, including every lower, central,
and upper estimate. The live mod now uses that research proposal as its base and then
applies the maintainer's explicit gameplay layer below. These entries are balance and
state-specialisation choices; they must not be cited later as revised historical
estimates.

"Configured horizon" includes static capacity, native reserves, diamond survey
budgets and the one-time scripted stages. Each of the eight diamond deposits
opens to annual surveys when a territorial owner researches the regional
technology. A successful survey reveals capacity for the same Diamond Mines
building used by Kimberley's event-driven 1 + 19 route.
Iron and coal stages still add usable capacity with an owner-visible notification.

The eight legacy gold/oil callbacks are unchanged. Inspection of the installed native
capacity effect found that it changes capped capacity rather than undiscovered
reserves; the earlier description of those callbacks was incorrect. Their separate
follow-up and verification limits are recorded in the open audit register and the
[diamond discovery implementation](compatibility/diamond_discovery_2026_10_18.md).

## Approved overrides

| State | Resource | Research proposal | Live design | Design choice |
|---|---|---:|---:|---|
| Bechuanaland | Gold potential | 1 [1–2] | **2** | Use the evidential upper bound because the state otherwise has very little economic differentiation; remains gated by nitroglycerin and engine discovery. |
| Eastern Cape | Arable | 24 [16–28] | **28** | Use the upper bound to support a state that may be divided among Cape, Xhosa, and Griqualand East owners. |
| Eastern Cape | Wood | 5 [4–9] | **6** | Small forestry uplift within the historical reconstruction range. |
| Eastern Cape | Coal | 1 [1–2] | **2** | Use the upper bound for modest extractive depth. |
| West Transvaal | Arable | 38 [26–61] | **26** | Use the lower bound to curb stacking in the gold-and-diamond core. |
| West Transvaal | Iron | 1 [0–2] | **2** | Use the upper bound while remaining minor beside its precious-mineral economy. |
| Eastern Transvaal | Wood | 3 [1–6] | **6** | Restore part of the former forestry capacity at the upper evidence bound. |
| Northern Transvaal | Arable | 29 [23–32] | **24** | Near-lower allocation chosen to reduce the three-state Transvaal arable surplus. |
| Northern Transvaal | Iron | 4 [3–6] | **6** | Adopt the upper bound here rather than in Eastern Transvaal because this state has fewer competing resource strengths. |
| Transorangia | Arable | 57 [38–94] | **56** | Balance rounding; materially the evidence centre. |
| Transorangia | Wood | 7 [5–18] | **8** | Small within-range forestry uplift. |
| Transorangia | Iron | 0 [0–1] | **1** | Retain a one-level abstraction/gameplay token at the upper bound. |
| Natal | Arable | 20 [20–28] | **24** | Restore the pre-audit playable allocation while remaining within range. |
| Natal | Coal | 1 [1–2] | **2** | Use the upper bound. |
| Natal | Iron | 1 [1–2] | **2** | Use the upper bound as a small abstraction. |
| Zululand | Arable | 10 [9–13] | **12** | Raise the split-state allocation without returning to the full upper bound. |
| Zululand | Wood | 3 [1–5] | **4** | Within-range uplift for the separate state economy. |
| Drakensberg | Arable | 4 [2–6] | **8** | Conservative playtesting exception above the evidence band: add two levels after the six-level trial produced immediate starvation and poor growth. |
| Drakensberg | Coal | 0 [0–1] | **1** | Retain the prior one-level gameplay token. |
| Drakensberg | Diamonds | 5 [5–12] | **6** | Explicit balance exception above the previously approved lower-bound rule; remains gated by pneumatic tools. |
| Lourenço Marques | Arable | 24 [16–33] | **32** | Near-upper allocation for the broad south-of-Pungwe footprint. |
| Lourenço Marques | Wood | 9 [7–14] | **10** | Small within-range forestry uplift. |
| Zambezi | Arable | 62 [42–86] | **60** | Minor balance rounding. |
| Zambezi | Rubber | 17 [14–20] | **16** | Match the Vanilla state allowance while retaining plausible plantation potential. |
| Hereroland | Arable | 17 [9–25] | **18** | Small within-range playability uplift. |
| Hereroland | Wood | 1 [0–2] | **2** | Use the historical upper bound. |
| Hereroland | Fishing | 7 [5–8] | **6** | Match the Vanilla allowance. |
| Hereroland | Lead | 9 [7–12] | **10** | Small within-range increase for the Tsumeb mining identity. |
| Namaqualand | Arable | 4 [raw evidence 1] | **5** | Conservative one-level playtesting increase. This is a split-state allocation diagnostic, not a claim that Walvis Bay is already guaranteed an arable level. |
| Namaqualand | Fishing | 5 [4–7] | **7** | Use the upper bound and match Vanilla. |
| Namaqualand | Lead | 1 [0–2] | **2** | Use the upper bound as a small base-metal abstraction. |

Botswana receives no gameplay override and therefore keeps the complete research
proposal. Cape Colony, Northern Cape, and Griqualand West likewise retain their
research-proposal values.

## Explicitly resolved alternatives

- Eastern Transvaal iron remains **6**, not the optional upper value of 8. Its existing
  104 coal and 4 gated gold potential already create a dense extractive portfolio.
- Northern Transvaal iron **does** rise to 6. This is the selected location for the
  extra Transvaal iron capacity.
- The crop abstractions previously protected by the maintainer remain: Natal coffee,
  Zululand cotton, and Lourenço Marques cotton.
- The two approved grain corrections are implemented: Griqualand West uses maize
  instead of wheat, and Bechuanaland uses maize instead of millet. Every state still
  exposes only one grain building.

## Active playtesting checks

- **Drakensberg `8`:** start a fresh campaign as Basutoland and confirm that
  starvation does not begin immediately and that the population can sustain positive
  growth. If it still fails, record local grain and meat prices, standard of living,
  market access, and subsistence-farm staffing before raising the cap again; the
  failure may be an income or market problem rather than exhausted land.
- **Namaqualand `5`:** start a fresh campaign and inspect the Cape-owned Walvis Bay
  fragment directly. Success requires at least one effective arable level there. The
  previous four-level cap apportioned `0 / 3 / 1` to Cape / Nama / San, and the current
  province-weight reconstruction predicts that five may still apportion `0 / 3 / 2`.
  Treat a zero at Walvis as a failed check, even though `x8031D0` is marked prime land.

## Configured-horizon totals

Vanilla counts each unsplit parent state once. Old SB includes its scripted additions.

| Resource | Old SB | Unique-parent Vanilla | Research proposal | Live design | Δ vs old SB | Δ vs Vanilla |
|---|---:|---:|---:|---:|---:|---:|
| Arable | 383 | 540 | 379 | **383** | 0 | −157 |
| Wood | 51 | 73 | 57 | **65** | +14 | −8 |
| Coal | 128 | 496 | 146 | **149** | +21 | −347 |
| Fishing | 32 | 44 | 32 | **33** | +1 | −11 |
| Iron | 35 | 123 | 41 | **46** | +11 | −77 |
| Lead | 12 | 0 | 18 | **20** | +8 | +20 |
| Sulfur | 1 | 0 | 1 | **1** | 0 | +1 |
| Whaling | 17 | 4 | 17 | **17** | 0 | +13 |
| Gold potential | 104 | 37 | 91 | **92** | −12 | +55 |
| Diamonds | 20 | 0 | 114 | **115** | +95 | +115 |
| Rubber | 33 | 32 | 33 | **32** | −1 | 0 |
| Oil potential | 0 | 0 | 6 | **6** | +6 | +6 |

## Implementation contract

- Static caps and crop slots live in
  [`map_data/state_regions/04_subsaharan_africa.txt`](../map_data/state_regions/04_subsaharan_africa.txt).
- The [regional survey register](../common/scripted_effects/sb_diamond_surveys.txt)
  defines each diamond budget and technology. There is one active survey calendar
  per region. The [mine](../common/buildings/sb_diamond_mines.txt) applies its
  construction requirement to the local owner in split states.
- The remaining scripted technology stages live in
  [`common/scripted_effects/sb_resource_technology_gates_effects.txt`](../common/scripted_effects/sb_resource_technology_gates_effects.txt).
- Technology acquisition, starting-technology catch-up, and later ownership changes
  all call the same idempotent gate effect through
  [`common/on_actions/sb_mineral_discoveries_on_actions.txt`](../common/on_actions/sb_mineral_discoveries_on_actions.txt).
- Seven gold stages and the Lourenço Marques oil stage retain their existing effects;
  they do not populate the native undiscovered-reserve field. No gold/oil mechanic
  changes are included in the diamond revision.
- Seven direct iron/coal stages use one-time custom notifications naming
  the state, resource, capacity increase, and technology.
- Kimberley retains its existing event-led 1 + 19 diamond design.
- Static-map changes require a fresh campaign; filewatcher reload and existing saves
  are not valid balance tests for this revision.

The executable contract is locked by
[`tests/test_resource_rework_implementation.py`](../tests/test_resource_rework_implementation.py),
which reconstructs every configured state value and the regional totals from the live
state file, survey register, gate stages and Kimberley event. `tests/test_diamond_discovery.py`
checks annual odds, territorial eligibility, delayed finds, remaining reserves,
Kimberley's separate route and De Beers support. DP's fresh-game checks are pending.
