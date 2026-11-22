# Resource Update: Contributor and Maintainer Guide

**1.15 port update:** native copper and the removal of Northern Cape's lead
proxy supersede the dated pre-port allocation below. See the
[current resource record](resource_gameplay_overrides.md#1151-compatibility-update--11-november-2026)
and RES115-01 for the separate copper audit.

**Implemented:** 25 August 2026

**Status:** live in the mod; a fresh campaign is required

**Scope:** 17 Southern African state regions, including Lourenço Marques

This is the entry point for anyone reviewing or changing Spes Bona's resource
allocation. It separates the live game design from the research estimates and from
superseded work.

## Which source is authoritative?

Use the first applicable row. A historical estimate never overrides the implemented
gameplay layer by implication.

| Question | Authoritative source |
|---|---|
| What does a new campaign receive? | The [state-region file](../map_data/state_regions/04_subsaharan_africa.txt), [technology-gate effect](../common/scripted_effects/sb_resource_technology_gates_effects.txt), Kimberley effects, and their executable test. |
| Why does the live design depart from the research center? | [Resource Gameplay Override Record](resource_gameplay_overrides.md). |
| What are the evidence ranges, categories, comparators, and uncertainties? | [Full resource-audit guide](../../References/Resource%20rework/sb_full_resource_audit_2026-08-24/README.md) and its IEEE-cited Markdown/PDF report. |
| What did SB or an earlier proposal contain? | The [dated legacy archive](../../References/Resource%20rework/archive/README.md). Archived figures are provenance only. |

The short [Resource Balance Executive Summary](resource_balance_summary.md) is a
release-facing synopsis, not an independent source of numbers.

## What the update does

The research audit estimates plausible resource bands using matched Vanilla
comparators and Southern African evidence. Agriculture includes commercial crops,
subsistence cultivation, managed pasture, productive natural range, and discounted
arid range. Crop and pasture evidence is converted into wheat-equivalent output using
nutritional-energy, constant-value, and geometric-blend methods across lower, median,
and upper category profiles. Commercial production has weight 1.00; other categories
receive disclosed discounts. Wood distinguishes commercial or managed forestry,
current natural woodland, protected woodland, historically cleared or degraded cover,
open woodland, and shrub. Natural and protected woods therefore count rather than
being treated as zero. The same categories and scenario rules are applied to SB states
and comparator states so neither side receives a denominator advantage.

The maintainer then selected a live value inside those bands in most cases and made a
small number of explicit balance exceptions. Those selections are labelled as design
choices in the override record; they are not presented as revised historical facts.

The affected state identifiers are:

| In-game name | Script identifier | In-game name | Script identifier |
|---|---|---|---|
| Western Cape | `STATE_CAPE_COLONY` | Northern Cape | `STATE_NORTHERN_CAPE` |
| Griqualand West | `STATE_GRIQUALAND_WEST` | Bechuanaland | `STATE_BECHUANALAND` |
| Eastern Cape | `STATE_EASTERN_CAPE` | West Transvaal | `STATE_TRANSVAAL` |
| East Transvaal | `STATE_EAST_TRANSVAAL` | Northern Transvaal | `STATE_NORTHERN_TRANSVAAL` |
| Transorangia | `STATE_VRYSTAAT` | Natal | `STATE_NATAL` |
| Zululand | `STATE_ZULULAND` | Drakensberg | `STATE_DRAKENSBERG` |
| Botswana | `STATE_BOTSWANA` | Lourenço Marques | `STATE_LOURENCO_MARQUES` |
| Zambezi | `STATE_ZAMBEZI` | Hereroland | `STATE_HEREROLAND` |
| Namaqualand | `STATE_NAMAQUALAND` |  |  |

## How to read the totals

The **configured horizon** includes static capacity, native reserves, diamond survey
budgets and one-time technology stages. It is a ceiling used for design
comparison, not a claim that every level is available in 1836.

- Static arable, wood, fishing, whaling, ordinary mines, crop slots, rubber, and
  initial discoverable resources are defined in the state-region file.
- Eight regions start with **95 hidden diamond levels** in total. An owner who has
  researched the regional technology can discover capacity for Diamond Mines.
- Technology-gated iron and coal stages remain immediately usable with custom toasts.
- The legacy gold/oil callbacks retain their existing capacity effects. Native
  inspection on 18 October found that these do not add undiscovered reserves; the
  earlier documentation claimed otherwise. This separate issue awaits a scoped fix.
- Kimberley uses its pre-existing event path: one initial diamond mine plus nineteen
  additional levels.
- “Unique-parent Vanilla” counts each unsplit Vanilla parent once. Summing the same
  Vanilla parent once for every SB child would inflate the comparator.
- “Old SB” includes scripted additions, not just values visible in the state file.

The implemented configured horizon is **383 arable, 65 wood, 149 coal, 33 fishing,
46 iron, 20 lead, 1 sulfur, 17 whaling, 92 gold potential, 115 diamonds, 32 rubber,
and 6 oil potential**. State-by-state selections and comparison totals are in the
override record. Drakensberg 8 and Namaqualand 5 are explicitly provisional
playtesting values; their fresh-campaign pass/fail checks are recorded there.

## Technology-gate architecture

The first qualifying territorial owner starts a 365-day survey window for the
region. Each year one qualifying state supplies its owner's discovery modifier.
The base annual chance is 7.04%. A successful survey reports on day 0–364, after
checking the technology of whoever then owns the surveyed province. An ineligible
owner cancels that find and leaves the reserve intact. The next window opens on
the original anniversary. Foreign investment rights confer no survey eligibility.

All finds expand buildable capacity for the same Diamond Mines building. In a
split region each owner needs the regional technology to build or expand its own
mines. Existing mines continue operating after conquest. See the [survey
lifecycle and playtest cases](compatibility/frontier_playtest_2026_11_04.md#owner-only-surveys).

The remaining scripted stages call the same idempotent effect when:

1. a country completes a relevant technology;
2. a campaign starts with that technology already researched; or
3. ownership of an affected state changes to an eligible country.

Each of those stages has one global completion flag. Diamond reserves are recorded
once per geographic region at campaign start.

The table lists unchanged resource budgets and eligibility thresholds. Diamond
entries require a successful survey. The other entries retain their
existing scripted effects.

| Technology | Configured additions |
|---|---|
| Nitroglycerin | Bechuanaland +2 gold potential; Northern Transvaal +1 gold potential; Griqualand West +4 iron. |
| Dynamite | West Transvaal +25 gold potential; East Transvaal +4 gold potential; Transorangia +5 diamonds; Griqualand West +5 iron. |
| Pumpjacks | West Transvaal +50 gold potential and +20 diamonds; Zambezi +4 gold potential; Lourenço Marques +6 oil potential; Northern Cape +4 diamonds; Namaqualand +14 diamonds. |
| Pneumatic Tools | Transorangia +4 gold potential and +3 coal; Griqualand West +10 iron; Northern Transvaal +6 diamonds; Drakensberg +6 diamonds; Botswana +9 coal and +30 diamonds; Zambezi +8 iron, +5 coal, and +10 diamonds. |

The gate router is in
[`sb_mineral_discoveries_on_actions.txt`](../common/on_actions/sb_mineral_discoveries_on_actions.txt).
Direct-capacity message types and English text are in
[`sb_resource_gate_messages.txt`](../common/messages/sb_resource_gate_messages.txt)
and
[`sb_resource_gates_l_english.yml`](../localization/english/sb_resource_gates_l_english.yml).

## Crop-slot decisions

Victoria 3 permits one grain building per state in this design. Griqualand West and
Bechuanaland use maize. The existing Natal coffee, Zululand cotton, and Lourenço
Marques cotton abstractions remain deliberate gameplay choices. They were not silently
replaced by the audit's literal crop recommendation.

## Safe change workflow

For a balance-only change within the existing evidence range:

1. update the state file, survey register or technology stage;
2. add the decision and rationale to the override record;
3. update the expected state and regional totals in
   [`test_resource_rework_implementation.py`](../tests/test_resource_rework_implementation.py);
4. update the executive summary if the regional total changes; and
5. run the focused test and full validator.

For a new historical claim, category method, comparator panel, or uncertainty range,
create a new dated audit iteration. Do not rewrite the 24 August audit snapshot or
promote a file from the legacy archive into the live design without revalidation.

From the mod repository root:

```sh
python3 -m unittest tests.test_resource_rework_implementation
python3 tools/validate.py --skip-cmf-sync
```

For a release check with proprietary game files available, use the full validation
command in the repository [README](../README.md#validation). Static state-region
changes must be tested in a fresh campaign; filewatcher reload and old saves are not
valid balance tests.

## Archive policy

Superseded pre-audit material is retained under a dated archive with a relocation
manifest. It must remain readable for provenance but must not be linked as the current
recommendation. Generated Python caches and Finder metadata are not research artefacts
and are not retained.
