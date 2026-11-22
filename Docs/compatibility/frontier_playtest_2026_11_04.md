# Frontier playtest, 4 November 2026

The five retained 1.14.5 autosaves are monthly checkpoints from 1 May to
1 September 1881. All five follow the partition. Zululand state 779 records
an ownership change on 21 November 1880. The recreated ZUL country (16777921)
is ruled by Mehlokazulu Nyawo (33555468). None of the five saves contains
Zibhebhu’s name or historical template. They cannot distinguish an original
chief lost at annexation from a chief who never entered the original court.

## 1. The late partition

The installed Zibhebhu template normally enters through selection of a Landowner
leader from 1877 to 1897. The partition now admits the unused canonical template
in that window. An available living Zibhebhu heads the first council from 1877.
An early partition, his death or retirement, and subsequent vacancies follow
the existing selection by Prominence. The game retains ordinary mortality.

For the authored British annexation, the goal type's `on_enforced` effect shelters
the original living non-royal chief before the native annexation removes his
country. It checks the holder, target and exact recorded diplomatic play.
`CWarGoal::Execute` calls the type hook at arm64 `0x101443088`; the global
enforcement on-action follows execution. The same person can consequently
remain in ZUL until enforcement and return when it is restored. The copied
definition follows installed patched CMF outside that hook, including its
territorial mirror and land-grab guard.

From a checkpoint before the annexation, record the chief’s ID in battle and
after the handoff. Test a late partition when he has never appeared, a recorded
death, an early Klip partition and a later vacancy. These engine checks are
pending. [Court matrix, scenario 164](../zulu_court_runtime_matrix_2026_10_19.md)

## 2. Diamond discoveries

By the May save, Transvaal had discovered all 20 regional levels without
Pumpjacks and Vrystaat all five without Dynamite. By September the eight
deposits held 47 discovered levels out of 95. The saves record cumulative
quantities and give no date for the first discovery.

In the installed executable the technology predicate returns success at the
first matching technology (arm64 `0x1013a2d10`). All three regional variants
listed Prospecting alongside the later technology. Native eligibility can also
come from another owner or an eligible foreign investor. The regional thresholds
are Dynamite for Vrystaat, Pumpjacks for Northern Cape, West Transvaal and
Namaqualand, and Pneumatic Tools for Northern Transvaal, Drakensberg, Botswana
and Zambezi. Kimberley has a separate event and a 20-level budget.

Removing Prospecting from the three later building definitions fixes the common
early route on future rolls. Existing discovered levels persist in the save.

### Owner-only surveys

DP subsequently excluded foreign investors from discovery. For new campaigns,
eight permanent state regions each hold their original hidden budget. Their
first qualifying territorial owner starts a rolling 365-day calendar. In a
split region a single qualifying fragment is selected each year. A successful
roll records a province there and reports after 0–364 days. The province's
current owner must still qualify. A cancelled find consumes that year's
opportunity without spending any reserve. Transfers and reloads retain the
anniversary. Once the deposit is exhausted, renewals stop.

The owner's resource-discovery modifier adjusts the daily reference rate of
0.02%. The four-term annual conversion gives 7.04% at baseline and 11.99%
at +75%, to two decimal places. A year can deliver one find. Find sizes follow
the installed minimum-plus-random-bonus draw and are capped at the remaining
levels. Native `change_resource_potential.amount` reads a literal integer
(1.14.5 arm64 `0x101b5f7f4`), so delivery repeats a one-level grant for the
sampled count and deducts the same count from the region's reserve.

The local owner receives a discovery toast. Capacity is shared geographically
under the game's normal split-state rules. Building or expanding a mine in a
survey region requires its territorial owner's technology. De Beers uses the
same mine in all nine regions, including Kimberley. The native resource entries
and three earlier mine types have been retired. The earlier saves above are
evidence for the bug and cannot be used to verify this new-campaign setup.
DP's [B145-27 replay](1_14_5_runtime_matrix.md) is pending. The 33 focused
diamond, resource, company and frontier checks pass. A deterministic source
replay of West Transvaal cancelled the find after an unqualified conquest.
In the qualified branch the same surveyed province survived a state merger,
delivered 14 levels to the new owner, sat through a missed year and delivered
the final six levels. The full survey build ran
1,052 tests with eight skips. Two pre-existing unit failures remain. The rebase
test expects 123 keyed overrides while the earlier Zululand annexation hook
brings the inventory to 124. The other failure reports the outstanding Swazi,
Klip and Natal localisation reviews. The override comparison itself passes.

## 3. Other playtest cases

| Case | Expected in-game observation |
|---|---|
| Natal names | British Natal displays Natal Colony. Independent NAL displays Natalia even with the Southern African colonial marker. On the Boer hub set the city reads Chaka’s Kraal. The Dutch period description explicitly identifies the site with Dukuza. [Frans Lion Cachet, chapter V](https://www.dbnl.org/tekst/cach001wors01_01/cach001wors01_01_0018.php) |
| Griqualand East | Decline the petition in `.220` and advance beyond another monthly check. The proposal stays closed. Acceptance establishes the march-state and previews its relationship with the Cape. |
| Xhosa wars | The AI adopts the scoped frontier strategy before plays seven, eight and nine begin. Its +1000 boldness follows the installed Taiping example. Check actual AI escalation and a separate diplomatic play as a control. |
| Basutoland | Taking the transfer decision opens `sb_bst_frontier.210` for the Cape after it becomes Basutoland’s direct overlord. Acknowledging the notice performs no second transfer. |
| Chiefdoms tooltips | Compare the government options, intervention costs and effects, skirmishes, defections, Boer appeal, bribe and result. Check individual rendered bullets and disabled requirements as Natal and Transvaal. |

These cases await DP replay from before the relevant decision or transition.

The focused run passed 94 tests, including a final name-priority check. In full discovery the existing localisation
review check failed and eight historical cases skipped (1,048 tests in total).
Of the 17 validator gates, the unit and localisation gates report the same
pre-existing Swazi `.098`, Klip `.060`/`.080` and Natal `.050` review discrepancies.
Map, naval, compatibility, dependency verification and runtime script checks passed.
Advisory Tiger's 1.13.5 schema also flags the two 1.14.5 fields copied from
patched CMF in Annex Country. DP's in-game checks remain pending.
