# Localisation Review Queue

This is the pending review register for new or changed non-event/JE localisation prose.

- Add one row for each exact localisation key. Do not use prefixes, ranges, or group-only entries.
- Use the repository-relative localisation file path.
- Keep each listed key under the plain `# TO REVIEW (non-event/JE keys)` comment in its localisation file.
- The plain comment and this register are tracking only. They do not classify or authorize an event or journal-entry namespace.
- Event and journal-entry prose instead uses its namespace-bound `# ### TO REVIEW ###` or `# ### REVIEWED ###` marker under `AGENTS.md`.
- Remove a row only after DP reviews or supplies the final text.

## Pending keys

| File | Keys | Context |
| --- | --- | --- |
| `localization/english/sb_l_english.yml` | `amendment_sb_imperial_administration` | Crown appointments in the Cape and British Natal. |
| `localization/english/sb_l_english.yml` | `amendment_sb_imperial_administration_desc` | Appointments, their expiry and military staffing. |
| `localization/english/sb_l_english.yml` | `sb_crown_appointments_reform_lock_tt` | Bureaucracy reform and amendment repeal restriction. |
| `localization/english/sb_interest_groups_l_english.yml` | `ideology_sb_anglo_colonialism` | Cape and British Natal garrison ideology. |
| `localization/english/sb_interest_groups_l_english.yml` | `ideology_sb_anglo_colonialism_desc` | The garrisons’ colonial policy. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_zulu_take_power_type_name` | Zulu civil-war demand. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_zulu_take_power_type_desc` | Zulu civil-war demand. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_zulu_take_power` | Zulu civil-war demand. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_zulu_take_power_desc` | Zulu civil-war demand. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_zulu_take_power_sway_desc` | Zulu civil-war demand. |
| `localization/english/sb_cultures_l_english.yml` | `sb_raid_transfer` | Temporary identity during the raid transfer. |
| `localization/english/sb_bst_l_english.yml` | `sb_bst_raid_ora_tt` | Frontier raid payment, captive eligibility and slavery law. |
| `localization/english/sb_zulu_glossary_l_english.yml` | `glossary_sb_amabutho` | Zulu glossary pilot title; pending DP prose/render review. |
| `localization/english/sb_zulu_glossary_l_english.yml` | `glossary_sb_amabutho_desc` | Zulu glossary pilot: age regiments, military/labour service and women's participation; pending DP prose/render review. |
| `localization/english/sb_zulu_glossary_l_english.yml` | `glossary_sb_amakhosi` | Zulu glossary pilot title; pending DP prose/render review. |
| `localization/english/sb_zulu_glossary_l_english.yml` | `glossary_sb_amakhosi_desc` | Zulu glossary pilot: chiefs/rulers and the singular inkosi; pending DP prose/render review. |
| `localization/english/sb_zulu_glossary_l_english.yml` | `glossary_sb_usuthu` | Zulu glossary pilot title; pending DP prose/render review. |
| `localization/english/sb_zulu_glossary_l_english.yml` | `glossary_sb_usuthu_desc` | Zulu glossary pilot: Cetshwayo's following and its continuation under Dinuzulu; pending DP prose/render review. |
| `localization/english/sb_zulu_glossary_l_english.yml` | `glossary_sb_umkhosi` | Zulu glossary pilot title; pending DP prose/render review. |
| `localization/english/sb_zulu_glossary_l_english.yml` | `glossary_sb_umkhosi_desc` | Zulu glossary pilot: nineteenth-century royal first-fruits festival; pending DP prose/render review. |
| `localization/english/sb_1_15_journal_conclusions_l_english.yml` | `sb_bechuanaland_british_conclusion` | 1.15 outcome conclusion; awaiting DP prose/render review. |
| `localization/english/sb_1_15_journal_conclusions_l_english.yml` | `sb_bechuanaland_boer_swa_conclusion` | 1.15 outcome conclusion; awaiting DP prose/render review. |
| `localization/english/sb_1_15_journal_conclusions_l_english.yml` | `sb_bst_oranje_conclusion` | 1.15 outcome conclusion; awaiting DP prose/render review. |
| `localization/english/sb_1_15_journal_conclusions_l_english.yml` | `sb_bst_basotho_conclusion` | 1.15 outcome conclusion; awaiting DP prose/render review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_coalition_recruitment` | 30 October: attraction-only modifier for the one-state recruitment test build; native effects show its current strength. |
| `localization/english/sb_court_dunn_l_english.yml` | `sb_court_victors_avenged` | 31 October: +10 ruler Popularity for five years after executing Dunn; native effect preview. |
| `localization/english/sb_court_dunn_l_english.yml` | `sb_court_dunn_armed_following` | 31 October: five-year +10 Prominence for a named ally receiving Dunn's shipment; refreshes without stacking. |
| `localization/english/sb_court_dunn_l_english.yml` | `sb_court_dunn_outgunned` | 31 October: five-year −10 Prominence for a named member of the opposing camp. |

Dunn's `sb_court_dunn.002` remains **TO REVIEW** after adding the authorised
faction allocation: named ally/opponent, separate Prominence and 1% death-risk
tooltips, and an unchanged two-week Firearms alternative. The event skill and
installed `shogunate.2` informed the coalition tradeoff; Dunn retains his existing
single portrait. [Shipment design and implementation](zulu_dunn_shipments_design_2026_10_30.md).

Dunn's `sb_court_dunn.003` remains **TO REVIEW** after the 31 October rewrite:
resentment of an enemy's intermediary, distinct execution/retention/banishment
tradeoffs and conditional Mthonga introduction. Used the event skill and installed
`shogunate.2`; retained paired portraits. New-reign Prerogative previews in
`sb_court_succession.001`/`.004` also remain under their existing **TO REVIEW**
markers. [Writing and implementation record](zulu_dunn_succession_followup_2026_10_31.md).

The brothers' coming-of-age events `sb_court_succession.006` (The Two Brothers)
and `.007` (The Other Brother) in `localization/english/sb_court_succession_l_english.yml`
are **TO REVIEW**, added 29 October. The installed `shogunate.2` provides the
succession-dispute writing model; `commander_events.4` provides the native paired
portraits. Both brothers remain the named subjects. Authored scenes distinguish
the public designation from the younger or passed-over brother gathering support;
they are not historical quotations. Trait effects use native previews; each named
house's future pledge has its own tooltip. Portraits, long names, wrapping and
delivery await DP. Ordinary recognition prose is reused without alteration.

The later 29 October revision reverses the AI preference to Mbuyazi and separates
Cetshwayo's larger rival backing from Mbuyazi's smaller court circle. `.007` has
early wording and a dated uSuthu/iziGqoza variant; the latter is not backdated to
the brothers' 1844 coming of age. John Dunn's new `sb_court_dunn.001` namespace in
`localization/english/sb_court_dunn_l_english.yml` is **TO REVIEW**. Its paired
portraits show Dunn and Mbuyazi; the acknowledgement previews the actual future
pledge. See [Dunn's source and writing record](zulu_dunn_mbuyazi_event_2026_10_29.md).

Claimant victory `sb_court_succession.005` remains `TO REVIEW`. The 27 October
revision describes the agreed deaths of the losing coalition and the surviving
houses; the choice's stakes tooltip states the same consequence before war.
On 28 October `.005.a.tt` adds the button-only +10 Prerogative reward (cap 100); its prose remains under the event’s existing `TO REVIEW` marker.
On 29 October it also explains the 18-month protection from further low-Prerogative claimant challenges, beginning at victory rather than acknowledgement. The +10 reward is unchanged.
The installed `regency.2` public-description/private-scene model informed the
short outcome rewrite. Both portraits, wrapping and outcome names await DP.

Blood River outcomes `.080` and the new Zulu defeat event `.082` remain `TO REVIEW`.
On 26 October DP confirmed that their firearms and court consequences belong in
the Zulu outcome event, including after backdown. The portrait layout follows
installed `regency.2`; the prose names the territorial and court consequences
without assuming a battle occurred. Opening the popup applies its consequences;
the acknowledgement reports them and finishes the handoff. Rendering is pending DP.

The six recurring court scenes `sb_zulu_court.210`–`.215` were rewritten on
26 October. All remain `TO REVIEW`. Named pledges, the Council's future or immediate
law change, and separate personal/movement consequences replace ambiguous
“displayed character” descriptions. The native writing/portrait references and
per-event review are recorded in `Docs/zulu_court_event_prose_review_2026_10_26.md`.


Retief’s petition (`sb_natal_crisis.020`) remains `TO REVIEW`. Its revised scene
uses concrete actors, the returned cattle and the three choices over the land
bargain, following the installed `shogunate.2` structure/style review. DP requested
the ruler and Retief together: native `commander_events.4` supplies the paired
portrait layout. New allegiance tooltips join the house, Prominence and patron in
one dependent outcome; independent payment rows remain separate. The paired
portraits and final tooltip wrapping still require DP’s engine review.


The revised `sb_natal_interwar.030.a.tt`, `.b.tt` and `.c.tt` use available game
concepts. Pop Attraction uses Vanilla's modifier-description hover; Crown replaces
ZUL's loyalists with +15 relations toward NAL and GBR while retaining NAL's
loyalists. These remain under the event namespace's existing `TO REVIEW` marker.
Modifier preservation now keeps the old Initial Enthusiasm name and gives the
fresh twenty-year boost its own Annexation of Zululand label. No event or option
text explains the internal preservation; the only new key is the modifier name.

| Localisation file | Exact key | Review note |
|---|---|---|
| `localization/english/sb_court_politics_l_english.yml` | `Langazana` | Historical Devout leader; 28 October leadership package. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_no_surname` | Intentionally blank surname for Langazana; no verified patronymic. |
| `localization/english/sb_court_politics_l_english.yml` | `kaZokufa` | Historical amaCube chief, distinct from fictional Sigananda Zulu. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_esiklebheni` | Langazana's separately represented establishment. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_cube` | Sigananda's separately represented following. |
| `localization/english/sb_diamond_mines_l_english.yml` | `notification_sb_diamond_survey_discovery_name` | Owner’s regional diamond survey notification. |
| `localization/english/sb_diamond_mines_l_english.yml` | `notification_sb_diamond_survey_discovery_desc` | Owner’s regional diamond survey notification. |
| `localization/english/sb_diamond_mines_l_english.yml` | `notification_sb_diamond_survey_discovery_tooltip` | Owner’s regional diamond survey notification. |
| `localization/english/sb_natal_interwar_l_english.yml` | `sb_zululand_annexation_movement_attraction` | Name of the fresh annexation bonus, separate from preserved Initial Enthusiasm; no bookkeeping prose. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_responsible_colony_type_name` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_responsible_colony_type_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_responsible_colony` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_responsible_colony_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_responsible_colony_monarchy_type_name` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_responsible_colony_monarchy_type_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_responsible_colony_monarchy` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_responsible_colony_monarchy_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_dominion_type_name` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_dominion_type_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_dominion` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_dominion_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_boer_presidential_union_type_name` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_boer_presidential_union_type_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_boer_presidential_union` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_boer_presidential_union_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_boer_confederal_partner_type_name` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_boer_confederal_partner_type_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_boer_confederal_partner` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_boer_confederal_partner_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_cape_confederal_dependency_type_name` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_cape_confederal_dependency_type_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_cape_confederal_dependency` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_cape_confederal_dependency_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_zulu_chiefdoms_type_name` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_zulu_chiefdoms_type_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_zulu_chiefdoms` | Technical subject-restoration UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_zulu_chiefdoms_desc` | Technical subject-restoration UI text. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `dp_sb_bechuanaland_proxy_namaqualand_locked` | Technical 1.14 Namaqualand proxy-play UI text. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `dp_sb_bechuanaland_proxy_namaqualand_locked_desc` | Technical 1.14 Namaqualand proxy-play UI text. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `dp_sb_bechuanaland_proxy_namaqualand_locked_tooltip` | Technical 1.14 Namaqualand proxy-play UI text. |
| `localization/english/sb_griqualand_west_l_english.yml` | `dp_sb_griqualand_oranje_independent_return_wbl_proxy_locked` | Technical 1.14 independent-WBL proxy-play UI text. |
| `localization/english/sb_griqualand_west_l_english.yml` | `dp_sb_griqualand_oranje_independent_return_wbl_proxy_locked_desc` | Technical 1.14 independent-WBL proxy-play UI text. |
| `localization/english/sb_griqualand_west_l_english.yml` | `dp_sb_griqualand_oranje_independent_return_wbl_proxy_locked_tooltip` | Technical 1.14 independent-WBL proxy-play UI text. |
| `localization/english/sb_griqualand_west_l_english.yml` | `sb_griqualand_west_251_independent_tt` | Technical 1.14 sequential-refusal tooltip text. |
| `localization/english/sb_griqualand_west_l_english.yml` | `sb_griqualand_west_254_boer_aggressor_tt` | Technical 1.14 sequential-refusal tooltip text. |
| `localization/english/sb_griqualand_west_l_english.yml` | `sb_griqualand_west_254_cap_aggressor_tt` | Technical 1.14 sequential-refusal tooltip text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_griqualand_story_revoke_claim` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_griqualand_story_revoke_claim_desc` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_griqualand_story_revoke_claim_sway_desc` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_griqualand_story_revoke_claim_type_desc` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_griqualand_story_revoke_claim_type_name` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_story_humiliation` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_story_humiliation_desc` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_story_humiliation_sway_desc` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_story_humiliation_type_desc` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_story_humiliation_type_name` | Technical 1.14 story-war goal UI text. |
| `localization/english/sb_zulu_dynasty_extra_l_english.yml` | `Sigananda` | Preserve the character template's supplied first name instead of random-name fallback. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_defend_type_name` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_defend_type_desc` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_defend` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_defend_desc` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_defend_sway_desc` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_control_type_name` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_control_type_desc` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_control` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_control_desc` | Blood River Natal control objective. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_natal_control_sway_desc` | Blood River Natal control objective. |
| `localization/english/sb_l_english.yml` | `dp_sb_natal_crisis_desc` | Replace humiliation with the Blood River Natal control objective. |
| `localization/english/sb_l_english.yml` | `dp_sb_natal_crisis_tooltip` | Replace humiliation with the Blood River Natal control objective. |
| `localization/english/sb_l_english.yml` | `sb_natalia_port_natal_before_ultimatum_tt` | Disable Seize Port Natal once Britain dispatches its ultimatum. |

## Natal-owned Zululand settlement — 13 September 2026

| File | Key | Reason |
|---|---|---|
| `localization/english/sb_natal_crisis_l_english.yml` | `sb_klip_river_county_060_tt` | Two Vanilla demands replace punitive annexation; event prose remains DP-reviewed. |
| `localization/english/sb_natal_crisis_l_english.yml` | `dp_sb_klip_river_punitive_expedition_desc` | 17 October refusal-path consistency audit: describe Return State and Make Protectorate, replacing obsolete annexation wording. |
| `localization/english/sb_natal_crisis_l_english.yml` | `dp_sb_klip_river_punitive_expedition_tooltip` | 17 October refusal-path consistency audit: name both demands and retain British backing. |
| `localization/english/sb_natal_crisis_l_english.yml` | `sb_klip_river_county_020_c_tt` | 17 October refusal-path consistency audit: align ZUL's refusal tooltip with NAL's existing two-demand tooltip. |

| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_boer_commitment_bar_tooltip` | Boer Commitment sources, threshold, and conditional settlement explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_chiefdom_balance_bar_tooltip` | Authority in Zululand live monthly drift breakdown. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_drift_sponsorship` | Authority in Zululand live monthly drift breakdown. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_drift_volunteers` | Authority in Zululand live monthly drift breakdown. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_chiefdom_balance_bar` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_chiefdom_balance_bar_usuthu` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_chiefdom_balance_bar_zibhebhu` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_increase_policing_button_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_unload_refugees_effect_tt` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_return_claimant_effect_tt` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_sponsor_usuthu_button_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_sanction_volunteers_button_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_zibhebhu_incorporation_legacy` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_zibhebhu_incorporation_legacy_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_policing_cost_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_support_chiefs_button` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_support_chiefs_button_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_end_chief_support_button` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_end_chief_support_button_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `ideology_sb_usuthu` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `ideology_sb_usuthu_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_usuthu_sponsorship` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_usuthu_volunteers` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_usuthu_policing` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_chief_patronage_cost` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `concept_sb_zulu_chiefdoms` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `concept_sb_zulu_chiefdoms_desc` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_usuthu_live_readout` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_usuthu_influence_tooltip` | Chiefdoms movement contest implementation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_end_policing_button` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_end_policing_button_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_end_usuthu_sponsorship_button` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_end_usuthu_sponsorship_button_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_end_volunteers_button` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_end_volunteers_button_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_increase_policing_possible_tt` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_return_claimant_button` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_return_claimant_button_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_return_claimant_possible_tt` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_sanction_volunteers_button` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_sponsor_usuthu_button` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_unload_refugees_button` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_unload_refugees_button_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_unload_refugees_possible_tt` | Requires Zulu peasant households in Natal, the Shepstone System and an eligible destination in Zululand. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_boer_commitment_bar` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_boer_commitment_bar_high` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_boer_commitment_bar_low` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_boer_volunteer_mortality` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_boer_volunteer_mortality_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_chiefdom_reserves` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_chiefdom_reserves_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_crown_incorporation_legacy` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_crown_incorporation_legacy_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_policing_cost` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_usuthu_sponsorship_cost` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_usuthu_sponsorship_cost_desc` | Chiefdoms movement contest implementation; preserved labels or revised explanation. |

| `localization/english/sb_court_politics_l_english.yml` | `Mdlalose` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `Ngenetsheni` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `Ntuli` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `kaNgqengelele` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_accommodation_button` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_accommodation_button_desc` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_following_recruitment` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_politics_004_offer_tt` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_recognize_successor_button` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_recognize_successor_button_desc` | Recognition grants roughly half of supporting Prominence as future pledges, preserving existing promises; pending DP review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_recognize_successor_tt` | Recognition grants roughly half of supporting Prominence as future pledges, preserving existing promises; pending DP review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_breakdown` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_live_readout` | 7 November: owner-specific Royal/Chiefly title now appears in the live readout; values unchanged. Pending DP prose/layout review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_military` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_political` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_natal_crisis_l_english.yml` | `sb_klip_river_county_020_a_dynasty_tt` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_natal_crisis_l_english.yml` | `sb_klip_river_county_020_b_dynasty_tt` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_natal_crisis_l_english.yml` | `sb_klip_river_county_020_c_dynasty_tt` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `RULER_TITLE_SB_HEAD_CHIEF` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `gov_sb_federated_chiefdoms` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `gov_sb_federated_chiefdoms_desc` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `ideology_sb_zulu_chiefly` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `ideology_sb_zulu_chiefly_desc` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `ideology_sb_chiefist` | 27 October: character ideology assigned by constitutional alignment; DP approved the display name Chiefly Federalist. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `ideology_sb_chiefist_desc` | 27 October: chiefly government and Council preferences; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `ideology_sb_zulu_traditionalist` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `ideology_sb_zulu_traditionalist_desc` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `law_sb_chiefly_council` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `law_sb_chiefly_council_desc` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `law_sb_federated_chiefdoms` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `law_sb_federated_chiefdoms_desc` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `movement_sb_zulu_chiefly` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `movement_sb_zulu_chiefly_name` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `movement_sb_zulu_royal` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `movement_sb_zulu_royal_name` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `movement_sb_zulu_traditionalist` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `movement_sb_zulu_traditionalist_name` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zulu_institutions_laws_l_english.yml` | `sb_firearms_army_reform_locked_tt` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_bribe_chief_button` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `je_sb_zululand_bribe_chief_button_desc` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_chiefly_patronage` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_incident_mobilization` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_zululand_refugee_recruitment` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_chiefly` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_neutral` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_royal` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_incumbent` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_rival` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_uncommitted` | Zulu institutional/court implementation; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_institutions_active_tt` | Readable institutional/court requirement; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_no_constitutional_war_tt` | Readable institutional/court requirement; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_no_pending_negotiation_tt` | Readable institutional/court requirement; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_prerogative_25_tt` | Readable institutional/court requirement; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_prerogative_50_tt` | Readable institutional/court requirement; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_royal_candidate_available_tt` | 28 October: recognition also permits a living minor; no adult following is granted. Pending DP. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_adult_member_available_tt` | Readable institutional/court requirement; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_institutions_social_mobility_available_tt` | Readable institutional/court requirement; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_institutions_reach_positive_tt` | Readable Institutional Reach condition; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_country_title` | 7 November: used only by the live readout, where JournalEntry exists. Type-only JE names are context-free. Pending DP rendering review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_base_legitimacy` | 27 October: renamed Courtly Politics at DP's request; −25 Legitimacy at IR 50. Pending DP rendering review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_effects_active` | Shows the IR-scaled base Legitimacy deduction alongside applied Prerogative modifiers; pending DP rendering review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_effects_none` | Prerogative tooltip when neither modifier is present; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_royal_title` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_chiefly_title` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_royal_flavour` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_prerogative_chiefly_flavour` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_institutional_reach_readout` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_institutional_reach_breakdown` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_court_movements_readout` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_institutions_l_english.yml` | `sb_court_movements_breakdown` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_l_english.yml` | `sb_zulu_dynastic_stability_bar_low` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_l_english.yml` | `sb_zulu_dynastic_stability_bar_high` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_roster_heading` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_roster_explanation` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_roster_commitments` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_roster_backs_incumbent` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_roster_backs_claimant` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_royal_trait` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_royal_trait_desc` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_chiefly_trait` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_chiefly_trait_desc` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_neutral_trait` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_alignment_neutral_trait_desc` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_incumbent_trait` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_incumbent_trait_desc` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_claimant_trait` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_claimant_trait_desc` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_uncommitted_trait` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_endorsement_uncommitted_trait_desc` | Court presentation and allegiance traits; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_claimant_trait` | Approved character-card integration; new Claimant display label, pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_claimant_trait_desc` | 29 October: a claim can coexist with support for the reigning sovereign; pending DP prose review. |

## Court rework — 19 October 2026

| File | Key | Review note |
|---|---|---|
| `localization/english/sb_court_politics_l_english.yml` | `Dambuza` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `Maphitha` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `Masiphula` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `Mawa` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `Nongalaza` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `Sotobe` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `kaMamba` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `kaMpangalala` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `kaNondela` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `kaNzibe` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `kaSobadli` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `kaSojiyisa` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `movement_sb_dynastic_test` | 28 October: remove the test label from the live claimant movement; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `movement_sb_dynastic_test_name` | 28 October: remove the test label from the live claimant movement; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_dynastic_ai_supply` | 28 October: AI supply reduction during the tracked dynastic war; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_broken_undertaking` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_candidate_summary` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_candidates_heading` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_current_heading` | 24 October: current allegiance separate from next succession; pending DP. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_current_pool_summary` | 24 October: ruler's coalition and quarter-weight uncommitted backing; pending DP. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_current_coalition_summary` | 24 October: coalition prominence and share of present pledges; pending DP. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_external_opposition_summary` | 24 October: present opposition whose patron belongs to a different court; pending DP. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_chiefly_privileges` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_commander_summary` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_commanders_heading` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_confront_rival` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_confront_rival_desc` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_confrontation_available_tt` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_confrontation_tt` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_council_bargain_tt` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_firearms_reward_tt` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_followings_heading` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_future_pledge_named` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_future_pledge_none` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_heir_named` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_heir_none` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_introduce_heir_button` | 28 October: Present a Son; generalise the Dingane action to undocumented royal lines. Pending DP. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_introduce_heir_button_desc` | 28 October: once-per-reign newborn, recognition, 50-P charge and existing supporting-house transfer. Pending DP. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_introduce_heir_tt` | 28 October: remove Uthumbu-specific wording; retain the cost and coalition consequences. Pending DP. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_member_summary` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_no_accession_tt` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_pledge_representative_tt` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_public_credit` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_public_credit_tt` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_public_discredit` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_public_discredit_tt` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_purge_tt` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_regency_named` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_release_commitments_tt` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_secure_pledge` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_secure_pledge_desc` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_service_recognised` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_supporter_row` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_unpledged_summary` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_window_incumbent` | New or updated court UI; TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_window_levers` | New or updated court UI; TO REVIEW. |

## Court runtime follow-up — 19 October 2026

| `localization/english/sb_court_politics_l_english.yml` | `sb_court_current_roles` | Court prominence/role presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_role_ig_leader` | Court prominence/role presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_role_general` | Court prominence/role presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_role_admiral` | Court prominence/role presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_role_agitator` | Court prominence/role presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_role_magnate` | Court prominence/role presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_role_executive` | Court prominence/role presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_role_politician` | Court prominence/role presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_junior_status` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_councillors_heading` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_individual_prominence` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_member_summary` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_personal` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_royal` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_qulusi` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_ntuli` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_ncwana` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_buthelezi` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_ngenetsheni` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_dunn` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_mdlalose` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_mandlakazi` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_ntonteleni` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_nyandu` | House/coalition presentation (20 October); TO REVIEW. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_house_emgazini` | House/coalition presentation (20 October); TO REVIEW. |

## 25 October: annual allegiance and event deck

New/replaced event namespaces `sb_zulu_court.200`, `.201`, `.210`–`.215` are TO REVIEW. These are original scenes based on the style of installed Japan DLC events; their gameplay implements DP’s approved package.

| File | Key | Status |
|---|---|---|
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_undertaking_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_service_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_discredit_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_current_council_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_redirect_privileges_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_redirect_council_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_privileges_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_exchange_patrons_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_dispute_a_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_dispute_b_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_dispute_pay_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_guns_chiefs_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_guns_central_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_service_discredited` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_petulant_discredit` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_chiefly_gun_contacts` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_chiefly_retief_contacts` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_annual_current_change_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_annual_current_joined_tt` | TO REVIEW: direct character names for current allegiance joins; no nested localisation scope (27 October). |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_annual_current_withdrew_tt` | TO REVIEW: direct character names for current allegiance withdrawals; no nested localisation scope (27 October). |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_annual_future_change_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_annual_future_joined_tt` | TO REVIEW: direct character names for future allegiance joins; no nested localisation scope (27 October). |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_annual_future_withdrew_tt` | TO REVIEW: direct character names for future allegiance withdrawals; no nested localisation scope (27 October). |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_gathering_royal` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_gathering_chiefs` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_blood_river_victory` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_blood_river_defeat` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_swazi_victory` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_swazi_defeat` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_broker` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_support_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_opposition_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_klip_cession_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_klip_broker_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_neutral_named_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_rival_named_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_ally_named_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_broker_named_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_successor_named_tt` | TO REVIEW: approved mechanics, new explanatory wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_campaign_ruler_tt` | TO REVIEW: new court outcome/report wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_campaign_supporter_tt` | TO REVIEW: new court outcome/report wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_campaign_firearms_tt` | TO REVIEW: collected guns grant up to 10 percentage points of firearms adoption when the outcome option is selected; 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_campaign_defeated_ruler_tt` | TO REVIEW: permanent −25 Popularity loss on clicking the Blood River/Swazi defeat option; preview uses present tense (27 October). |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_campaign_defeat_prerogative_tt` | TO REVIEW: −25 Prerogative loss on acknowledging the Blood River defeat; updated option preview, 29 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_campaign_opposition_tt` | TO REVIEW: named house and rival coalition in the defeat report. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_campaign_defector_tt` | TO REVIEW: each of the two least prominent eligible incumbent-supporting houses defects to the same named rival as the largest uncommitted house; Ndlela is excluded. Blood River/Swazi defeat, 27 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_gathering_royal_flavour` | TO REVIEW: new court outcome/report wording. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_gathering_chiefs_flavour` | TO REVIEW: new court outcome/report wording. |

## Court coercion follow-up, 25 October 2026

| File | Key | Review scope |
|---|---|---|
| `localization/english/sb_court_politics_l_english.yml` | `notification_sb_court_rival_submitted_desc` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `notification_sb_court_rival_fled_desc` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_renunciation_cooldown_tt` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_purge_unused_tt` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_purge_war_available_tt` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_purge_flight_tt` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_purge_war_tt` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_committed_authority` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_claim_defended` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `notification_sb_court_renunciation_refused_name` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `notification_sb_court_renunciation_refused_desc` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_court_politics_l_english.yml` | `notification_sb_court_renunciation_refused_tooltip` | Revised claim renunciation/purge costs, exact quoted odds and independent cooldowns; DP review pending. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_episode_cost_tt` | TO REVIEW: frozen payment / named allegiance presentation, 25 October follow-up. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_allegiance_tt` | TO REVIEW: frozen payment / named allegiance presentation, 25 October follow-up. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_frontier_support_named_tt` | TO REVIEW: frozen payment / named allegiance presentation, 25 October follow-up. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_retief_refusal_tt` | DP-supplied war warning; ORA's name uses the event's existing `boer_republic` scope, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_retief_guns_amaKhosi_tt` | TO REVIEW: existing chiefly-concession explanation retained. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_patronage_cost_tt` | TO REVIEW: pledge price and prominence preview. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_patronage_backing_tt` | TO REVIEW: pledge price and prominence preview. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_chiefly_privileges_tt` | Court event rewrite: named parties and distinct costs/consequences; pending DP review, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_future_council_tt` | Court event rewrite: named parties and distinct costs/consequences; pending DP review, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_council_repeal_tt` | Court event rewrite: named parties and distinct costs/consequences; pending DP review, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_discredit_ruler_tt` | Court event rewrite: named parties and distinct costs/consequences; pending DP review, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_discredit_withdrawal_tt` | Court event rewrite: named parties and distinct costs/consequences; pending DP review, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_exchange_withdrawal_tt` | Court event rewrite: named parties and distinct costs/consequences; pending DP review, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_dispute_a_opposition_tt` | Court event rewrite: named parties and distinct costs/consequences; pending DP review, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_dispute_b_opposition_tt` | Court event rewrite: named parties and distinct costs/consequences; pending DP review, 26 October. |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_block_successor_pledge_tt` | Succession pledge refusal: named pledge prevented at a cost of 10 Prerogative; pending DP review, 26 October. |

## 26 October: Natal, firearms and Swazi follow-up

Zulu-facing event namespaces `sb_natal_crisis.020`, `.026`, `.080`, `.081` and `sb_swazi_frontier.094`, `.097` remain **TO REVIEW**. Rewritten against installed DLC bargain and outcome structures; no reviewed Boer prose changed. Firearms JE explanations, on-demand Uthumbu and campaign result rows are updated in their existing queue entries.

| File | Key | Review note |
| --- | --- | --- |
| `localization/english/sb_nguni_l_english.yml` | `sb_nguni_no_diplomatic_play_tt` | TO REVIEW: readable requirements; predicates unchanged. |
| `localization/english/sb_nguni_l_english.yml` | `sb_nguni_settlements_resolved_tt` | TO REVIEW: readable requirements; predicates unchanged. |
| `localization/english/sb_nguni_l_english.yml` | `sb_nguni_formation_lands_tt` | TO REVIEW: readable requirements; predicates unchanged. |

## 26 October: sons' adulthood and weekly firearms

- `sb_court_succession.003` in `localization/english/sb_court_succession_l_english.yml`: **TO REVIEW**. Once-only father/son declaration; paired native portrait window. Installed `regency.2` informed the named public declaration and concrete private scene. New prose is authored fiction, not a historical quotation.
- `je_sb_adopt_firearms` in `localization/english/sb_firearms_l_english.yml`: **TO REVIEW**. Reason, status and completion explain one market-supply gate; the 29 October follow-up increases completion to 260 qualifying weeks, wraps the internal completion check, and shows the native Effects preview. `je_sb_adopt_firearms_remove_penalties_tt` previews removal of the remaining weapons penalties. The obsolete `event_effects_sb_firearms.001_tt` is retired; the completion event keeps Innovative and native New Tactics effects without a dynasty/Prerogative reward. Obsolete separate treaty/industry statuses remain retired.
- Existing queued `sb_court_introduce_heir_button_desc` and `sb_court_introduce_heir_tt` now say newborn and 50 P. Other court choices are unchanged.

26 October, honour-path cleanup: DP requested retirement of `sb_natal_crisis.021` and its unreviewed localisation. Its existing hidden handoff now runs in `.020.a`; `.020` and reviewed `.030` prose are unchanged. Earlier prose-review evidence remains historical.

## 26 October: Blood River guns on the outcome options

- `sb_natal_crisis.080`, `.081` and `.082` in `localization/english/sb_natal_crisis_l_english.yml` remain **TO REVIEW**. Revised `.d`, `.f` and `.a` describe a few guns collected along the frontier and an instruction to use them. The scenes also fit backdown and negotiated outcomes; they do not require a fought battle or invent a gun-cession term.
- Native references: installed `regency.2` for a concrete scene behind the public outcome and `regency.3` for an acknowledgement whose option performs the change. Existing sovereign portraits and the neutral diplomatic scene are retained. New narrative is authored flavour, with no attributed quotation.

## 26 October: mild court-refusal penalties

| File | Key | Review note |
| --- | --- | --- |
| `localization/english/sb_zulu_court_l_english.yml` | `sb_court_refusal_prerogative_tt` | TO REVIEW: 5-P cost for valid refusals in `.212`, `.213` and `.215`; no charge for a stale scene. |

## 26 October: explicit chiefdom annexation preview

| File | Key | Review note |
| --- | --- | --- |
| `localization/english/sb_natal_crisis_l_english.yml` | `sb_natalia_chiefdoms_absorbed_tt` | TO REVIEW: name Zulu as the annexing country, bold the annexation action and highlight the Nguni Chiefdoms. `.026` has ZUL as ROOT; no event flavour changed. |

## 27 October: army-name apostrophe

| File | Key | Review note |
| --- | --- | --- |
| `localization/english/sb_firearms_l_english.yml` | `dingane_amabutho` | TO REVIEW: typographic apostrophe in “Dingane’s Amabutho” avoids terminating Vanilla's single-quoted front-tooltip argument. Name and meaning unchanged. |
| `localization/english/sb_contested_crown_l_english.yml` | `law_sb_contested_crown` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `law_sb_contested_crown_desc` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `law_sb_contested_social_crown` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `law_sb_contested_social_crown_desc` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `ideology_sb_contested_crown` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `ideology_sb_contested_crown_desc` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `ideology_sb_contested_social_crown` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `ideology_sb_contested_social_crown_desc` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_claimant_mobilisation` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_claimant_armed_forces` | 28 October: Divided over the Crown; broaden the existing −20 Approval package to every IG until the conflict ends; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_dynastic_sponsor_tt` | 28 October: both choices disclose −20 Approval for all IGs until resolution or cancellation; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `gov_sb_contested_crown` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `gov_sb_contested_crown_desc` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `gov_sb_contested_regency` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `gov_sb_contested_regency_desc` | Contested Crown claimant war; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_dynastic_coalitions_tt` | 28 October: one existing barracks level is reserved for the weaker side, remaining levels follow frozen shares, conscription retains its ratio; stronger side receives Zululand (ties favour the incumbent); pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_dynastic_force_split_tt` | 28 October: both choices disclose immediate recruitment redistribution, military household relocation by actual barracks shares, later rebuilding, lost manpower/experience/unit composition, recruitment/training and the continuing conscription limit; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_dynastic_back_incumbent_tt` | 27 October: selected contender stays in the player's original country; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_dynastic_back_claimant_tt` | 27 October: prince takes the original throne, sovereign leads rebels, no player switch; pending DP prose review. |
| `localization/english/sb_contested_crown_l_english.yml` | `sb_court_dynastic_stakes_tt` | 27 October: defeat kills the entire frozen coalition; third-party and uncommitted characters survive. Pending DP prose review. |
| `localization/english/sb_l_english.yml` | `sb_fecund` | Fecund special trait for Mpande; DP requested name, 27 October. |
| `localization/english/sb_l_english.yml` | `sb_fecund_desc` | TO REVIEW: fruitful and abundant household, following DP's requested description, 27 October. |

## Civil-war muster — 29 October 2026

| File | Key | Reason |
| --- | --- | --- |
| `localization/english/sb_court_muster_l_english.yml` | `building_sb_court_muster` | Temporary levy recruitment building for multi-state claimant wars. |
| `localization/english/sb_court_muster_l_english.yml` | `sb_court_muster_conscription_suspended` | Native conscription restriction while the replacement muster is active. |
| `localization/english/sb_court_muster_l_english.yml` | `sb_court_wartime_provisions` | Temporary 75% Food Security relief for both actual claimant-war factions, including native one-state splits; removed when the tracked conflict ends. |

| `localization/english/sb_zulu_names_l_english.yml` | `Bathonyile` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Biyela` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Buthelezi` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Chube` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Dilikana` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Godlumkhonto` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Gwala` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Hlabisa` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Hloyisile` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Langeni` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mabhoko` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Magwaza` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Matshana` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mbatha` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mbopha` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mchunu` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mdletshe` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mehlokazulu` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mfanawendlela` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mfuzi` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mkabi` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mlandela` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mmama` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mnqandi` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Monase` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Mpungose` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Msushwana` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Ndabankulu` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Nomantshali` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Ntombela` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Nyamakayishi` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Nyawo` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Senzangakhona` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Sibisi` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Sitshaluza` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Sokwetshatha` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Somfula` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Tshani` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Vumandaba` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `Zungu` | 29 October: documented clan/given name or royal patronymic; pending DP review. |
| `localization/english/sb_zulu_names_l_english.yml` | `kaCetshwayo` | 29 October: documented clan/given name or royal patronymic; pending DP review. |

## Later-court implementation — 30 October 2026

`sb_court_dunn.001`–`.003` and `sb_hamu_bargain.001`–`.003`, `.010` are TO REVIEW.
Admission and judgement use paired portraits; deliveries and the foreign offer use
the named trader/prince. Installed `shogunate.2` supplied the coalition-bargain model.
No reviewed namespace was rewritten. Rendering remains pending DP.

| File | Key | Reason |
|---|---|---|
| `localization/english/sb_court_dunn_l_english.yml` | `sb_court_trader` | Later-court trait or funding interface. |
| `localization/english/sb_court_dunn_l_english.yml` | `sb_court_trader_desc` | Later-court trait or funding interface. |
| `localization/english/sb_court_dunn_l_english.yml` | `Mthonga` | Later-court trait or funding interface. |
| `localization/english/sb_hamu_bargain_l_english.yml` | `sb_hamu_fund` | Later-court trait or funding interface. |
| `localization/english/sb_hamu_bargain_l_english.yml` | `sb_hamu_fund_desc` | Later-court trait or funding interface. |
| `localization/english/sb_hamu_bargain_l_english.yml` | `sb_hamu_end_funding` | Later-court trait or funding interface. |
| `localization/english/sb_hamu_bargain_l_english.yml` | `sb_hamu_end_funding_desc` | Later-court trait or funding interface. |
| `localization/english/sb_hamu_bargain_l_english.yml` | `sb_hamu_funding_valid_tt` | Later-court trait or funding interface. |
| `localization/english/sb_hamu_bargain_l_english.yml` | `sb_hamu_subsidy_cost` | Later-court trait or funding interface. |
| `localization/english/sb_hamu_bargain_l_english.yml` | `sb_hamu_boer_patronage` | Later-court trait or funding interface. |

| `localization/english/sb_court_politics_l_english.yml` | `sb_court_coercion_not_supporting_ruler_tt` | New requirement: a prince supporting the incumbent cannot be confronted or purged. |

| `localization/english/sb_institutions_l_english.yml` | `sb_ir_governance_adjustment` | Active law contribution to Institutional Reach; DP presentation review pending. |
| `localization/english/sb_institutions_l_english.yml` | `sb_ir_economy_adjustment` | Active law contribution to Institutional Reach; DP presentation review pending. |
| `localization/english/sb_institutions_l_english.yml` | `sb_ir_police_adjustment` | Active law contribution to Institutional Reach; DP presentation review pending. |
| `localization/english/sb_institutions_l_english.yml` | `sb_ir_distribution_adjustment` | Active law contribution to Institutional Reach; DP presentation review pending. |
| `localization/english/sb_institutions_l_english.yml` | `sb_ir_bureaucracy_adjustment` | Active law contribution to Institutional Reach; DP presentation review pending. |
| `localization/english/sb_institutions_l_english.yml` | `sb_ir_army_adjustment` | Active law contribution to Institutional Reach; DP presentation review pending. |
| `localization/english/sb_institutions_l_english.yml` | `sb_ir_local_police_adjustment` | Active law contribution to Institutional Reach; DP presentation review pending. |
| `localization/english/sb_firearms_l_english.yml` | `sb_firearms_current_penalties` | Live current penalty heading in the Firearms JE. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_challenge_threshold_label` | 30 October: separate challenge/succession sections and thresholds; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_challenge_summary_royal` | 30 October: separate challenge/succession sections and thresholds; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_challenge_rule_royal` | 30 October: separate challenge/succession sections and thresholds; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_challenge_unavailable` | 30 October: separate challenge/succession sections and thresholds; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_succession_summary_royal` | 30 October: separate challenge/succession sections and thresholds; pending DP prose review. |
| `localization/english/sb_court_politics_l_english.yml` | `sb_court_succession_unavailable` | 30 October: separate challenge/succession sections and thresholds; pending DP prose review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_intervention_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_servicemen_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_bribe_available_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_open_bribe_tt` | Price is shown before the bribe is paid. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_police_cost_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_police_pressure_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_police_refund_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_police_end_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_sponsor_cost_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_sponsor_pull_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_sponsor_commit_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_sponsor_refund_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_sponsor_end_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_sponsor_commit_end_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_volunteer_cost_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_volunteer_pressure_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_volunteer_commit_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_volunteer_relief_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_volunteer_end_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_volunteer_commit_end_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_patronage_cost_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_patronage_pull_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_patronage_refund_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_patronage_end_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_zulu_loyalists_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_repeal_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_repeal_relations_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_fervour_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_repeal_attraction_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_garrison_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_refugee_attraction_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_bribe_funds_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_bribe_target_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_contest_open_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_chiefs_contest_closed_tt` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_natal_crisis_l_english.yml` | `ai_strategy_sb_xhosa_frontier_defence` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_natal_crisis_l_english.yml` | `ai_strategy_sb_xhosa_frontier_defence_desc` | 4 November playtest follow-up for DP review. |
| `localization/english/replace/dynamic_state_and_hub_names_l_english.yml` | `HUB_NAME_STATE_NATAL_city_boer` | 4 November playtest follow-up for DP review. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `sb_natalia_swazi_defender_blocked_tt` | 7 November: reason Natalia cannot join the Swazi defending side in the marked frontier dispute. Pending DP prose review. |

## Chiefdoms refinement — 10 November 2026

New/changed general text awaiting DP review (existing reviewed namespaces preserved):

| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_contest_status` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_status_review` | 14 November follow-up: whole-day countdown to the existing JE-age deadline; removes raw hour suffix. DP rendering review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_status_waiting` | 14 November: chiefly settlement condition after ten years; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_status_organising` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_status_war` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_status_reunion` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_chiefly_panel` | 14 November: aggregate house Prominence added beside native movement values; DP rendering review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_royal_panel` | 14 November: aggregate house Prominence added beside native movement values; DP rendering review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_claimant_named` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_claimant_vacant` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_chief_named` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_chief_vacant` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_support_explanation` | 15 November: full political backing, signed 0.1-point prominence pressure, ±30-point cap and current target adjustment; DP rendering/prose review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_prominence_pressure` | 15 November: native modifier name for the balance of chiefly backing; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_escalation_event` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_escalation_native` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_active_interventions` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefs_foreign_armies_excluded_tt` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefdoms_native_test` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_chiefdoms_native_test_desc` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_court_house_members_heading` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_court_house_dingane` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_court_house_mpande` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_court_house_gqugqu` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_court_house_cetshwayo` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_chiefdoms_refinement_l_english.yml` | `sb_court_house_mbuyazi` | Chiefdoms refinement; DP review pending. |
| `localization/english/sb_boer_republics_l_english.yml` | `sb_youth` | Youth trait name. Awaiting DP review. |
| `localization/english/sb_boer_republics_l_english.yml` | `sb_youth_desc` | Youth expiry conditions. Awaiting DP review. |
| `localization/english/sb_boer_republics_l_english.yml` | `sb_marthinus_groot_boere_mandate` | Appointment popularity modifier. Awaiting DP review. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `subject_type_sb_nrp_protectorate` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `subject_type_sb_nrp_protectorate_no_icon` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_name` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_propose_name` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_break_name` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_ask_to_break_name` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_desc` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_pact_desc` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_notification_name` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_notification_desc` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_notification_break_name` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_notification_break_desc` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_notification_third_party_break_name` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_zululand_settlement_l_english.yml` | `sb_nrp_protectorate_action_notification_third_party_break_desc` | Vryheid protectorate, vanilla diplomatic label. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_nrp_protectorate_type_name` | Vryheid protectorate restoration. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_nrp_protectorate_type_desc` | Vryheid protectorate restoration. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_nrp_protectorate` | Vryheid protectorate restoration. |
| `localization/english/sb_war_goal_contracts_l_english.yml` | `war_goal_sb_reestablish_nrp_protectorate_desc` | Vryheid protectorate restoration. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_017_completion_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_017_missions_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_017_company_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_017_settler_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_017_ruthless_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_017_swa_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `company_sb_south_west_africa_company` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `company_sb_south_west_africa_company_desc` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `dyn_c_sb_south_west_africa_company` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `dyn_c_sb_south_west_africa_company_adj` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_policy_missions` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_policy_settler` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_policy_ruthless` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_policy_ruthless_sol` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_administrative_capacity` | Warren and South West Africa policy rework. |
| `localization/english/sb_namibia_l_english.yml` | `sb_nam_company_slot` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `sb_warren_cape_yield_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `sb_warren_ask_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `sb_warren_offer_direct_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `sb_warren_offer_proxy_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `sb_warren_offer_neutral_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `sb_warren_kimberley_yield_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `sb_warren_stand_firm_tt` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `dp_sb_bechuanaland_warren_kimberley_locked` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `dp_sb_bechuanaland_warren_kimberley_locked_desc` | Warren and South West Africa policy rework. |
| `localization/english/sb_bechuanaland_corridor_l_english.yml` | `dp_sb_bechuanaland_warren_kimberley_locked_tooltip` | Warren and South West Africa policy rework. |
