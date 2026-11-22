# Refuge cohort workforce feasibility: installed 1.14.5

Read-only native investigation; no save changes or engine launch. The subsequently authored implementation is described below. `manifest.json` contains exact executable hash, symbols and disassembly argv. No generated effect-doc dump was found locally.

## Conserved move

`CMovePartialPopEffect::ReadMember` (0x101b489a4) accepts exactly `state`, `population`, `population_ratio`; unexpected members call ReportUnexpected. Its execution computes one moved total from workforce+dependants, sets a single count in SModifyPopContext and invokes CState::ModifyPop. There is no separate workforce/dependant selector or ratio override.

`CPop::MergePopsCalcMove` total-count branch (0x101101ecc onward) calls the donor's actual CalcWorkingAdultRatio and computes moved workforce from moved total times that ratio; dependants are the remainder (0x101102050..2060). Small integer/fixed-point rounding is possible. Thus changing the total moved amount does not impose a new household ratio. Selecting different source Pops could improve the mixture only within the existing donors' actual ratios and available sizes. A weighted combination of donors below 50% workforce cannot reach 50% workforce.

## Runtime create_pop is different and does support an initial ratio

Installed history documentation `common/history/pops/100_pops_example.txt` documents `working_adult_ratio`, and runtime CCreatePopEffect also supports the behavior. Its ReadMember routes token0x5365 to a fixed-point member at offset0x110. ExecuteDerived reads that value at0x101b5a724; when unset it substitutes PopType's base working ratio plus country modifier; otherwise the explicit value is used, clamped0..1. It initializes workforce=floor(size*ratio) and dependants=size-workforce using CPop::InitializeSize at0x101b5a8b0.

Therefore `create_pop = { size = 5000 working_adult_ratio = 0.5 ... }` creates a new approximately 2,500-worker/2,500-dependant Pop. It is not a way to change the ratio of a conserved move. CreatePop also resets IG support and initializes literacy from PopType (0x101b5a8b8..8e4), rather than cloning the donor's complete state. Removing donors and creating replacements would need a separate design to preserve population totals and relevant attributes; it lies outside the earlier review question, which specifically asked about a non-recreation route. That was a research scope, not a user prohibition.

## State modifier is not cohort-local

`CalcIdealWorkingAdultRatio` reads PopType's base plus StateWorkingAdultRatioAdd from the STATE aggregate modifier node (0x1010f62a8..6368; sum returned0x1010f64a4). The consumer does not read an individual-Pop timed modifier. A state/country grant changes the target for residents broadly, rather than only the new arrivals.

Direct native callers of this ideal-ratio function are initialization, actual-ratio fallback, CalculateGrowth, small-Pop consolidation and debug stats; see `ideal_ratio_callers.json`. CalculateGrowth compares actual and ideal ratios and applies demographic skew, capped by WORKING_ADULT_RATIO_SKEW_MAXIMUM (installed value2.0). This is not an immediate cohort ratio setter. Exact convergence time and whether a separate direct dependant-to-worker conversion occurs were not established; do not promise either from this excerpt.

No supported isolated in-place workforce-ratio setter was found. The broad native effect-class symbol scan found no Workforce/Dependent/WorkingAdult-specific effect class, but absence of a matching symbol is not a complete proof that no undocumented alternative exists.

## Gameplay caveats

Even 50% workforce is a demographic quantity, not guaranteed employment, wages or farmer qualification. Peasants remain subject to the existing Serfdom hiring floor; freeing demographic workforce alone does not grant permission to leave protected subsistence jobs. A moved Pop may merge with existing residents, and move_partial_pop exposes no new destination-Pop scope, making post-move whole-Pop changes unsafe as a cohort-only operation. No demographic rule protects the initial 50:50 ratio from later growth, casualties, migration or consolidation.


## Current implementation: grouped replacement with isolated metadata restoration

The user subsequently approved a 5,000-person replacement trial. The earlier non-recreation question was a research boundary, not a user prohibition.

`kill_population` is country-scoped (supported scope5); `kill_population_in_state` is state-scoped (76). Neither is a Pop-scoped operation. CPopEffect's constructed filter supports culture, religion, profession and strata; no exact individual-Pop selector or arbitrary trigger filter is read by ConstructFilter. This matters if the same identity occupies several source buildings.

The implementation in `common/scripted_effects/sb_bst_refugee_effects.txt`, called by frontier event `.020`, removes 5,000 from the selected donor's same-culture/religion/profession group in its source state, rather than demanding removal from that one Pop object. `kill_population_in_state = { value = 5000 culture = ... religion = ... pop_type = ... }` first allocates a common removal percentage and then applies an absolute remainder pass (0x101b45f80..5fe4). Provided the filtered source pool contains at least5,000, the total removed is exactly5,000. The original selection of a donor with total_size>=5,000 establishes that lower bound.

Native CPop::Kill clamps an individual removal to current total, removes workforce=floor(n*actual working-adult ratio) and dependants=n-workforce, and updates literacy, qualifications, employment/size data and political support proportionally. It explicitly calls AdjustLoyalistsAndRadicalsAfterDeath (0x101101968..978). No explicit genocide/diplomatic-penalty callback appears in the inspected kill effect or CPop::Kill; downstream death/statistic bookkeeping was not exhaustively audited. This is a death-cleanup operation, not a verified nonfatal deletion or migration record. No supported exact nonfatal local deletion effect was found.

Creation ends through CState::ModifyPop, whose destination scan calls CanPopsMerge over residents (0x101310774..808). A new-ID diff therefore cannot guarantee an isolated destination Pop. The implementation instead chooses a staging culture absent from all destination Pops (promethean, then ainu, then maori), revalidates that absence before debit, and creates the5,000 arrivals under that identity at working_adult_ratio=.5. It restores the selected donor's frozen wealth and literacy while the arrivals remain isolated; changing culture to Sotho is last and may then merge them into residents. No metadata setter runs after that merge. A merged Pop need not itself show50% workforce; the newly added increment is2,500 workers and2,500 dependants. If all staging identities are occupied, the transaction performs no debit and consumes no receipt.

CreatePop's culture/religion/profession are static-definition parser fields, not runtime event-target fields. The implementation uses literal dispatch over the15 installed professions and17 religions. Native creation defaults are overridden only for donor wealth/literacy, before culture restoration; qualifications, political support and other unhandled metadata are not completely cloned. Copying the selected largest donor's wealth/literacy is also not a weighted reconstruction of every same-identity source Pop debited. Native merge weighting does not justify describing all existing residents as retaining exactly unchanged displayed averages.


## Native destination profession and metadata-restoration corrections

`GetFinalPopTypeForMovePop` is not a universal identity-preserving move. It returns the default profession if the source type cannot be unemployed; it also returns that default for a slave type if the destination country has no slavery. Otherwise it keeps the original profession. `CPopTypeDatabase::Init` reads DEFAULT_POP_TYPE into offset0xf68 and explicitly diagnoses a broken assumption if its bit0 ('can be unemployed') is false; see poptype_database_core_init.txt at0x10195f824 and0x10195f9d0. Installed 00_defines.txt1463 sets DEFAULT_POP_TYPE="laborers". Of the15 installed professions, peasants alone have unemployment=no; slaves alone have is_slave=yes. Thus native mapping is peasants→laborers; slaves→laborers where slavery is absent; every other installed profession unchanged. A replacement preserving native destination behavior must debit the ORIGINAL profession and create the MAPPED profession, rather than changing the source filter.

A staged wealth-restoration setter should include `update_loyalties = no`, as Vanilla's starting-wealth setters do. Native CSetPopWealth constructor defaults the flag true (set_wealth_construct.txt0x101b3f900..904); execution translates it into the SetWealth loyalty enum (set_wealth_execute.txt0x101b3fb04..10). CPop::SetWealth with the default enum0 explicitly calls UpdatePopLoyaltiesFromStandardOfLivingChanges (pop_set_wealth.txt0x1010eaec8..ed8); enum1 instead refreshes the displayed SoL baseline without that reaction. Restoring a cloned wealth value should not manufacture a fresh SoL-change loyalty award.


## Final source review status

The current helper separates SOURCE_POP_TYPE and ARRIVAL_POP_TYPE, applies the native peasants/slavery mapping above, and sets `update_loyalties = no` during isolated wealth restoration. It validates BST ownership and the eligible source pool and places its country-scoped once receipt before debit. The unchanged Mountain Refuge trial retains only the active +30% in-kind income effect for10years; the user's +50% throughput line remains commented. No hiring-floor exemption or direct Food Security effect was added. Native employment, later demographic evolution and economic recovery still require DP's replay; source-executed tests cannot prove those outcomes.
