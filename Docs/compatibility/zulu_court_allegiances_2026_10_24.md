# Zulu court: current allegiances, neutral weight and opening balance

24 October 2026. Implements DP's separate current-allegiance/succession views and trial λ = 0.25. Investigates the opening alliances without changing traits or authored allegiances. Baseline remains SB 0.20.2, Victoria 3 1.14.5 build 25629520, and CMF 1.66.0 + `sb-1.14.3-r1`. No dependency patch, save migration or game launch.

## Source changes

**Current Allegiances** includes the king's own house, loyal supporters and each rival's present adherents. **Next Succession** retains the distinct future pledges. A chief can co-operate with Dingane now and support Mpande's eventual accession. Each view counts a house once, through its leader; the leader carries the eligible members' combined prominence.

Present uncommitted prominence is discounted only for H:

```text
H = 100 × (incumbent backing − rival backing)
    / (current pledged prominence + 0.25 × personally uncommitted prominence)
C = clamp(H + ruler popularity / 2, −100, 100)
T = clamp(0.75 × C + 0.25 × movement balance, −100, 100)
```

H is zero when its denominator is zero. The existing monthly approach, cap, Institutional Reach and effects remain unchanged. The discount strengthens the larger committed side, including opposition when rivals predominate. It does not discount succession shares, purchase prices, attraction contributions or the 25% major-challenger denominator.

The projection resets before each calculation. CAP exile preserves home backing. If a constitutional split places a living patron in another court while a follower remains at home, that follower's opposition still counts, displayed separately; the helper does not overwrite the other country's projection. Character navigation retains the single native action and existing bounded scrollbox.

General localisation changes are queued for DP. No reviewed event/JE prose or approval baseline changed. No Vanilla/CMF override hash changed.

## Retained checkpoint

Source: `save games/autosave.v3`, copied before analysis to `/tmp/sb-court-allegiances-2026-10-24/autosave.v3`. Header date **1 February 1836**, game 1.14.5, ZUL country ID **481**. Size **113,050,026 bytes**; SHA-256 `557a80737ae65b83fb70d039cf7cd4b33e549b3949a679cbe8a96c3d46074624`.

Country and character databases were parsed separately. Saved numeric variable identities were decoded as signed 64-bit fixed-point values divided by 100,000, including omitted zero identities. The table reflects the saved court calculation, not a claim that every engine-generated character had already joined the registry.

| Coalition | Present backing | Share of present pledges | Next-succession backing | Share of succession pledges |
|---|---:|---:|---:|---:|
| Dingane | 206 | 73.31% | 0 | 0% |
| Mpande | 25 | 8.90% | 25 | 33.33% |
| Gqugqu | 50 | 17.79% | 50 | 66.67% |

Total represented prominence is **705**. Current pledged backing is **281**, with **424** personally uncommitted. Future succession pledges total only **75**, leaving **630** without a future pledge. Dingane's 206 consists of his own 100, Ndlela's 86 and Dambuza's 20. This was already included in Prerogative before this change; the old succession-only display obscured it.

The updated source was executed against reconstructed checkpoint inputs with native prominence held at its saved values and the existing SB +5/−10 modifiers accounted for once. It reproduces all totals above and the new court backing below. This is a source replay, not an engine run or save migration.

## Why Gqugqu starts ahead

Both princes are politicians, marked historical, with the same +5 claimant modifier. Neither has another house pledged to him in this checkpoint. Both currently oppose Dingane through self-named claimant commitments.

| Direct prominence source | Mpande | Gqugqu |
|---|---:|---:|
| Historical character | +10 | +10 |
| Politician role | +10 | +10 |
| Claimant modifier | +5 | +5 |
| Basic Political Operator | +5 | +5 |
| Compliant | −5 | N/A |
| Ambitious | N/A | +10 |
| Imperious | N/A | +10 |
| **Total observed in save** | **25** | **50** |

Mpande's other traits are Honorable, Tactful and Reserved; none adds direct prominence. Their personality packages therefore explain the entire observed **25-point difference**. The native prominence/popularity relationship must still be respected in later tuning; this table is the verified checkpoint decomposition, not a claim that prominence never responds to popularity.

The [18 October research brief](../zulu_chiefly_coalitions_research_2026_10_18.md) explicitly leaves Gqugqu's personality package unvalidated. The [19 October cast research](../zulu_oral_history_cast_research_2026_10_19.md) records later Mawa–Gqugqu and Nongalaza/Sotobe–Mpande associations, while warning against projecting them wholesale into 1836. The current authored opening keeps those figures personally uncommitted. Generated councillors also begin uncommitted. No unsupported opening alliance has been added to compensate for traits.

**Recommended next balance decision:** review Gqugqu's inherited Ambitious/Imperious package against evidence first; develop the named later commitments through court events. Do not equate a lack of opening allies with historical parity or manufacture Mpande loyalists solely to cancel a numerical trait advantage. Current total shares remain approximately 3.55% for Mpande and 7.09% for Gqugqu, below the existing 25% major-challenger threshold; λ does not change that threshold.

## Effect on the opening court

Saved H was `100 × (206 − 75) / 705 = 18.58156`. With λ = 0.25, the denominator becomes `281 + 0.25 × 424 = 387`, giving **H = 33.85013**.

Dingane's checkpoint popularity is **−75**: Hedonist −15, Imperious −35, Ruthless −15 and the existing Dynastic Crisis modifier −10, present since 4 January. Q/2 contributes −37.5. The source replay changes **C from −18.91844 to −3.64987** and, with the checkpoint's zero movement balance, **T from −14.18883 to approximately −2.73740**. Prerogative approaches that target through its existing monthly drift; it is not assigned the new target immediately.

The king's popularity therefore still matters even after counting his coalition clearly and reducing neutral dilution. At this popularity the existing annual voluntary-acknowledgement chance is zero. These are balance findings, not additional changes in this patch.

## Validation and handoff

- Focused court checks: **73 passed**, including seven new cases for present/future commitments, λ, single counting, house succession, death/exile, empty/all-neutral courts, split countries and GUI eligibility.
- Full discovery: **636 tests; 627 passed, 8 historical-input skips, 1 pre-existing failure, no errors**. The failure is the reviewed-localisation aggregate for `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`. Their file is unchanged from the pre-edit snapshot; approvals were not regenerated.
- Full validator: **15/17 gates passed, warned or skipped**. Unit validation and localisation fail on that same prior prose mismatch. Installed CMF, override inventory/comparison, maps, naval connectivity and runtime contracts pass. Live CMF release sync was explicitly skipped; existing deferred gates remain BC-20, BC-22, CP-07, QUAL-09 and SUP-05.
- Advisory Tiger: **0 fatal, 1,066 errors, 146 warnings, 1 untidy, 1 tip**, unchanged from the preceding batch. No diagnostic identifies a changed court statement; the existing `GetTimedModifier` warnings still point to the unchanged effects readout in the institutions localisation file. Tiger's 1.13.5 schema remains advisory against installed 1.14.5.

The pre-edit snapshot, save extracts, replay result and full validation output are under `/tmp/sb-court-allegiances-2026-10-24/`. Durable input/output hashes and source inventory are in [the evidence record](evidence/zulu_court_allegiances_2026_10_24.json).

**Pending DP:** fresh domestic/foreign court rendering; clear king/current versus future-pledge shares; λ tuning under loyalist and rival dominance; death, exile and constitutional split reconciliation in the engine. See the updated [runtime matrix](../zulu_court_runtime_matrix_2026_10_19.md). The existing same-constitution war prototype remains unverified and test-only. The parallel-review requirement remains suspended by DP; no reviewer agent was spawned.
