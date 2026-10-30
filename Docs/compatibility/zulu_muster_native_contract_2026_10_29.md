# Zulu wartime muster: installed native contract

Target: Victoria 3 **1.14.5**, Steam build **25629520**, CMF **1.66.0 + sb-1.14.3-r1**. Read-only source/disassembly inspection; no binary changes, dependency patch or game launch.

## Findings used by the implementation

- The installed `common/buildings/buildings.md` documents script-created non-buildable recruitment buildings through `recruits_combat_units = yes`. `bg_army` inherits government funding and military status. The existing [native allocation inspection](evidence/zulu_claimant_allocation_1_14_5_arm64.txt) shows the military-building collection used by civil-war army allocation. This supports a prototype; it does not prove that this new type will be staffed, mobilised and used correctly by the AI.
- Installed land combat-unit definitions use **1,000 maximum manpower**. Training methods define the serviceman/officer ratio separately. The temporary type reuses `pmg_training_conscription`, including SB's 99:1 customary method. Source tests compare the implemented job calculation with the installed ratios.
- `CState::CalcConscriptionCapacity` delegates to the maximum-building-capacity calculation. `IsBuildingAllowedInState` checks building-group/region availability, not the building's scripted `potential`. The conscription-specific capacity branch calls `NMobilization::CalcMaxConscriptionCenterLevel` directly. A proposed `potential` injection was therefore discarded; no such override is shipped.
- `CalcMaxConscriptionCenterLevel` constructs a `CValueCalculator`, then calls `CalcConscriptionRate`. The latter adds the base/extra rate and its multiplicative modifier. The constructor clears the flag permitting negative multiplicative factors; `GetValue` floors a total multiplier below −1 to a zero factor. It is therefore safe to suppress the rate multiplicatively without generating negative capacity.
- The scoped `−10` multiplier leaves a zero factor under ordinary native positive modifiers, including the tested +500% case. Native revolution/uprising bonuses are additive rates and cannot overcome a zero factor. This contract does not claim support for an external modifier package exceeding +900% multiplicative conscription.

[Reproducible arm64 excerpts](evidence/zulu_muster_1_14_5_arm64.txt) include the symbol names, binary hash and reproduction command. Full functions were inspected. Script interfaces and training definitions are pinned in [the claimant contracts](zulu_contested_crown_contracts_1_14_5.json); no existing historical contract was replaced.

## Verification limits

Native unit creation, AI control, capacity refresh timing, officer qualifications, hiring, mobilisation, native building merging and safe removal of temporary units remain **pending DP**. The source harness supplies actual split/winner callbacks as inputs; it does not simulate those engine operations. A zero-rate calculation does not alone prove that already-existing conscript units have been removed or that none reappear.

The implementation removes native centres once at the scripted multi-state rebuild, retains the suppression modifier until tracked cleanup, and removes only its distinct muster type on demobilisation. One-state origins receive none of these changes. [DP matrix](../zulu_civil_war_muster_runtime_matrix_2026_10_29.md).
