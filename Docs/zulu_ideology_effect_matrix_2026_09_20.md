# ZUL ideology effect matrix — proposed revision, 20 September 2026

Companion to [the current outcome design](zulu_chiefdoms_outcome_design_2026_09_20.md). Design only. No runtime ideology or law changes.

Every row below is provisional unless separately accepted by DP. Old columns were extracted from installed Vanilla 1.14.3 and current SB; proposed columns are the design. These are package stances, not guaranteed final IG opinions after leader ideologies, later political events, or law variants.

`++` strongly approve; `+` approve; `0` explicitly neutral; `-` disapprove; `--` strongly disapprove; `—` no position from these packages. `parent X` reports the parent law’s source stance for comparison, not a claim that an unimplemented variant already exists. Proposed new-law IDs are working names.

## Package ownership

| Actor | Proposed ideologies | Changes to initialization |
|---|---|---|
| LO / Royal Establishment | Royal Prerogative + Homestead Order + native Patriarchal | Replace Paternalistic and Hierarchic; keep Patriarchal |
| PB / Chiefly Notables | Chiefly Authority + Homestead Order + native Patriarchal | Replace Reactionary, Meritocratic, Patriotic; account for native Mercantile addition |
| uSuthu movement | One focused constitutional/military core | Narrow current `ideology_sb_usuthu`; preserve the native movement object |
| AF | Existing package | No identity, ideology, or attraction-definition rework |

Royal Prerogative and Chiefly Authority own governance, power, bureaucracy and army positions. Homestead Order owns economy, taxation, policing and citizenship. Patriarchal owns women’s rights and speech. Thus none of the proposed IG packages has conflicting overlapping law blocks. uSuthu is separate; the IG packages are not added to its core ideology.

## Full stance comparison

The table includes all laws named by any old or proposed package, plus explicit unchanged absence on slavery and church/state. Other law groups have no added positions. Old PB includes Mercantile because ZUL starts with Traditionalism and Vanilla global history adds it under that law.

### Governance Principles

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_monarchy` | ++ | ++ | + | + | ++ | ++ |
| `law_theocracy` | + | - | + | 0 | - | - |
| `law_presidential_republic` | 0 | - | 0 | 0 | - | - |
| `law_parliamentary_republic` | 0 | - | 0 | 0 | - | - |
| `law_corporate_state` | 0 | 0 | 0 | 0 | 0 | 0 |
| `law_social_monarchy` | + | + | + | + | + | + |
| `law_council_republic` | -- | -- | - | - | -- | -- |
| `law_chiefdom` | — | -- | — | ++ | -- | -- |
| `law_sb_federated_chiefdoms` | — | -- | — | ++ | parent -- | -- |

### Distribution Of Power

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_single_party_state` | 0 | 0 | 0 | - | 0 | 0 |
| `law_landed_voting` | ++ | 0 | - | + | + | 0 |
| `law_autocracy` | ++ | ++ | - | - | ++ | ++ |
| `law_oligarchy` | + | 0 | - | + | + | 0 |
| `law_wealth_voting` | 0 | 0 | 0 | 0 | 0 | 0 |
| `law_census_voting` | - | - | + | 0 | - | - |
| `law_universal_suffrage` | -- | -- | - | - | -- | -- |
| `law_anarchy` | -- | -- | -- | -- | -- | -- |
| `law_technocracy` | -- | -- | - | - | -- | -- |
| `law_elder_council` | — | -- | — | ++ | -- | -- |
| `law_sb_council_of_chiefs` | — | -- | — | ++ | parent -- | -- |

### Bureaucracy

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_hereditary_bureaucrats` | + | + | - | + | + | — |
| `law_appointed_bureaucrats` | 0 | + | 0 | 0 | + | — |
| `law_elected_bureaucrats` | - | - | + | - | - | — |

### Policing

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_local_police` | + | + | 0 | + | — | — |
| `law_dedicated_police` | 0 | 0 | + | 0 | — | — |
| `law_militarized_police` | 0 | 0 | ++ | 0 | — | — |
| `law_no_police` | - | - | - | - | — | — |

### Economic System

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_traditionalism` | ++ | + | -- | + | + | — |
| `law_agrarianism` | + | + | - | + | 0 | — |
| `law_interventionism` | 0 | 0 | + | 0 | 0 | — |
| `law_industry_banned` | - | 0 | -- | 0 | -- | — |
| `law_laissez_faire` | - | 0 | 0 | 0 | - | — |
| `law_cooperative_ownership` | -- | 0 | -- | 0 | -- | — |
| `law_command_economy` | -- | 0 | 0 | 0 | - | — |
| `law_extraction_economy` | - | 0 | -- | 0 | -- | — |

### Trade Policy

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_isolationism` | + | — | - | — | — | — |
| `law_mercantilism` | + | — | + | — | — | — |
| `law_protectionism` | 0 | — | + | — | — | — |
| `law_free_trade` | - | — | 0 | — | — | — |

### Army Model

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_peasant_levies` | + | 0 | — | 0 | — | 0 |
| `law_professional_army` | 0 | + | — | 0 | — | 0 |
| `law_national_militia` | 0 | - | — | + | — | 0 |
| `law_mass_conscription` | - | 0 | — | 0 | — | 0 |
| `law_sb_amabutho_system` | parent + | ++ | — | - | — | ++ |
| `law_sb_chiefly_militias` | parent 0 | -- | — | ++ | — | -- |

### Land Reform

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_serfdom` | ++ | — | — | — | 0 | — |
| `law_tenant_farmers` | + | — | — | — | 0 | — |
| `law_commercialized_agriculture` | 0 | — | — | — | 0 | — |
| `law_peasant_proprietorship` | -- | — | — | — | - | — |
| `law_collectivized_agriculture` | -- | — | — | — | -- | — |

### Taxation

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_consumption_based_taxation` | + | 0 | 0 | 0 | — | — |
| `law_land_based_taxation` | + | + | - | + | — | — |
| `law_per_capita_based_taxation` | 0 | 0 | + | 0 | — | — |
| `law_proportional_taxation` | - | 0 | + | 0 | — | — |
| `law_graduated_taxation` | -- | 0 | - | 0 | — | — |

### Welfare

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_no_social_security` | + | — | — | — | — | — |
| `law_poor_laws` | 0 | — | — | — | — | — |
| `law_wage_subsidies` | - | — | — | — | — | — |
| `law_old_age_pension` | - | — | — | — | — | — |

### Citizenship

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_ethnostate` | 0 | 0 | + | 0 | 0 | — |
| `law_subjecthood` | + | + | 0 | + | + | — |
| `law_national_supremacy` | 0 | 0 | ++ | 0 | 0 | — |
| `law_racial_segregation` | 0 | 0 | + | 0 | 0 | — |
| `law_cultural_exclusion` | 0 | 0 | 0 | 0 | 0 | — |
| `law_multicultural` | - | 0 | - | 0 | - | — |

### Caste Hegemony

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_hindu_caste_enforced` | ++ | — | - | — | — | — |
| `law_hindu_caste_codified` | + | — | - | — | — | — |
| `law_hindu_caste_not_enforced` | - | — | 0 | — | — | — |
| `law_affirmative_action` | -- | — | 0 | — | — | — |

### Edo Social System

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_strict_edo_system` | ++ | — | -- | — | — | — |
| `law_intermediate_edo_system` | + | — | - | — | — | — |
| `law_lax_edo_system` | - | — | + | — | — | — |

### Rights Of Women

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_no_womens_rights` | + | + | — | + | — | — |
| `law_women_own_property` | - | - | — | - | — | — |
| `law_women_in_the_workplace` | - | - | — | - | — | — |
| `law_womens_suffrage` | -- | -- | — | -- | — | — |

### Free Speech

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_outlawed_dissent` | + | + | + | + | — | — |
| `law_censorship` | + | + | + | + | — | — |
| `law_right_of_assembly` | 0 | 0 | 0 | 0 | — | — |
| `law_protected_speech` | - | - | - | - | — | — |

### Labour Associations

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_combination_acts` | — | — | + | — | — | — |
| `law_guild_system` | — | — | + | — | — | — |
| `law_anti_strike_laws` | — | — | 0 | — | — | — |
| `law_corporatized_unions` | — | — | 0 | — | — | — |
| `law_right_to_associate` | — | — | - | — | — | — |
| `law_factory_councils` | — | — | -- | — | — | — |

### Migration

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_closed_borders` | — | — | + | — | — | — |
| `law_migration_controls` | — | — | ++ | — | — | — |
| `law_no_migration_controls` | — | — | - | — | — | — |

### Internal Security

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_secret_police` | — | — | + | — | — | — |
| `law_national_guard` | — | — | + | — | — | — |
| `law_no_home_affairs` | — | — | - | — | — | — |
| `law_guaranteed_liberties` | — | — | -- | — | — | — |

### Navy Model

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_merchant_navy` | — | — | -- | — | — | — |
| `law_jeune_ecole` | — | — | 0 | — | — | — |
| `law_professional_navy` | — | — | ++ | — | — | — |
| `law_diplomatic_navy` | — | — | + | — | — | — |

### Slavery

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_slavery_banned` | — | — | — | — | — | — |
| `law_debt_slavery` | — | — | — | — | — | — |
| `law_slave_trade` | — | — | — | — | — | — |
| `law_legacy_slavery` | — | — | — | — | — | — |

### Church And State

| Law key | Old LO | New LO | Old PB | New PB | Current uSuthu | New uSuthu |
|---|---|---|---|---|---|---|
| `law_state_religion` | — | — | — | — | — | — |
| `law_freedom_of_conscience` | — | — | — | — | — | — |
| `law_total_separation` | — | — | — | — | — | — |
| `law_state_atheism` | — | — | — | — | — | — |

## Meaning and tradeoffs

- **Different authority, shared social setting.** Chiefly Notables can approve a monarchy while preferring chiefly institutions. They do not represent every historical chief or automatically oppose every royal claimant. Royalists favour centralized military authority; chiefs favour local command. These are proposed game abstractions.
- **Homestead Order is deliberately narrow.** Both groups favour Traditionalism/Agrarianism, land-based tribute, local policing and Subjecthood. Broader native positions on modern trade, welfare, racial hierarchy, caste, Edo hierarchy, migration and labour organization are removed. This does make the groups less uniformly obstructive to later reforms. Leaders and other movements can still oppose them. Keeping every generic conservative position would be a larger political programme than the evidence currently supports.
- **Land law remains neutral in this package.** Do not equate customary access and chiefly allocation automatically with European Serfdom, private freehold or modern collectivization. This neutrality is a deliberate modelling limit, not a claim that land did not matter. No starting land or slavery law changes follow from the matrix.
- **Patriarchal is retained for LO and added to PB.** PB speech positions remain numerically identical to former Patriotic positions; its women’s-rights positions are newly explicit. Native Patriarchal is a broad abstraction and does not describe every right historically exercised by Zulu women.
- **Movement satisfaction is narrower.** Inherited Traditionalism, Subjecthood and bureaucracy no longer calm the movement through its core ideology. Chiefdom, Council and Chiefly Militias all conflict with it. A retained Professional Army neither helps nor hurts through this core. Monarchy and Autocracy satisfy its constitutional aims after restoration.
- **Existing law variants need explicit audit.** The new laws need their own rows; ordinary parent laws also remain covered. Other native/SB variants use their documented parent contract unless an explicit row is designed. This table does not redesign non-ZUL IGs, leader pools, IG traits or every unrelated custom law.

## Historical basis and its limits

Kuper’s publisher extract emphasizes continuities between homesteads, chiefly structures and royal political organization. It supports a shared social foundation rather than assigning one camp a wholly alien social system; the individual game-law ratings are our design inference. Only the publisher extract, not the full article, was inspected. [Kuper, 1993](https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/house-and-zulu-political-structure-in-the-nineteenth-century1/3845DBD388FD72AEA89A9D169FEB113B).

Cetshwayo’s strengthening of amabutho against the diffusion of power to territorial chiefs supports distinguishing royal military authority from chiefly command. It does not supply positions on Victoria 3’s twentieth-century policy options. [SAHO, King Cetshwayo](https://sahistory.org.za/people/king-cetshwayo).

Royalist chief Ndabankulu Ntombela illustrates why IG membership and uSuthu membership must not be exclusive camps. [Nxumalo, 2026](https://www.cambridge.org/core/journals/journal-of-african-history/article/british-political-hegemony-and-imperialism-crushing-of-the-usuthu-and-the-onkweni-sections-of-the-zulu-royal-family-1880s1913/07EC250864BDC9DDC04451959454E07B).

## Source and precedent check

- Vanilla: `common/ideologies/00_ig_ideologies.txt`, `00_ig_ideologies_flavored.txt` (Mercantile), `common/history/global/00_global.txt`, and PB/LO definitions.
- SB: `common/ideologies/sb_usuthu_ideology.txt`, ZUL country history, Chiefdom/Elder Council overrides and Amabutho.
- Hail Columbia: `ideology_usfp_tribal_government` separates constitutional views from `ideology_usfp_native_american_agrarian` economic views. Its specific Indigenous American stances are not transplanted to ZUL.
- Gates of the Bosphorus: Tanzimat journal uses `set_core_ideology` on an existing political movement. It is a scripting precedent for changing an agenda without creating another movement, not historical evidence for this design.
- Native political definitions distinguish core ideology, character-ideology pool, attraction, support and actual activism. No source inspection here substitutes for DP’s engine testing.
