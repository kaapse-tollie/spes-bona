# BST/Lesotho subsistence protection audit — 1 November 2026

Read-only native inspection of the executable and save excerpts supplied by the parent investigator. No engine launch or gameplay edit. Executable path, SHA-256 and exact reproducible symbol commands are in manifest.json.

## Confirmed native path

1. Installed law_serfdom (game/common/laws/01_land_reform.txt:50–57) supplies building_minimum_incorporated_subsistence_employment_add = 0.5. Vanilla modifiers_l_english.yml:765–766 describes this as the employment level below which other buildings cannot hire from subsistence.
2. CBuilding::CalcProtectedEmploymentPercentage checks that the building is subsistence and state incorporation is >=1, then reads that modifier from the building's modifier object. See protected_employment.txt.
3. CBuilding::CalcEmploymentPercentage divides cached current employees (+0x38) by cached maximum employees (+0x48). The six saved Lesotho subsistence levels use the 5,000-peasant-per-level basic PM: 3,256/30,000 is about 10.85%, below 50%. See employment_percentage.txt and the installed PM.
4. CEmploymentHelper::Collect marks each such source employee with flag 0x20 when current percentage <= protected percentage. See collect_sets_protected_flag.txt.
5. CollectTransfers rejects a flagged employee when the destination workplace ID differs from the source Pop's existing workplace. See transfer_rejects_protected_other_workplace.txt. This supplies a concrete reason why the saved 91 employable farmer qualifications do not prove that the maize farm can recruit those peasants. It does not prove that no other wage/qualification constraint exists.

## State scope

CBuilding::CalcModifier resolves its current State, updates/imports that state's modifier node with full category mask and registers the state as an explicit dependency (0x100106168–0x1001061bc). See building_modifier_inheritance.txt. A state-scoped building modifier therefore reaches this native consumer. Existing SB also applies the exact same modifier in state scope through sb_zululand_chiefdom_reserves; that unrelated feature was not changed.

## Narrow proposal and limits

A temporary -0.50 protected-subsistence-employment modifier confined to BST-owned Drakensberg can offset the existing +0.50 from Serfdom without changing the national law or creating population. Add bounded food-security relief while recruitment and recovery occur; this does not create grain sell orders or establish future farm hiring. Remove BST-specific relief on ownership loss; verify the native next employment ticks, farmer/labourer recruitment, wages, grain output, food security, growth and expiry in DP's replay.

A 20% transfer of mixed existing Sotho farmers/labourers is a separate demographic choice. It can bring existing qualified workers but also adds consumers and changes the donor economy. More arable capacity does not release the current protected workers, and can increase protected subsistence capacity.
