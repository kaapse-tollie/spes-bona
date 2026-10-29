# Cape independence and primary culture changes

Recorded 29 October 2026. Victoria 3 1.14.5, with Community Mod Framework and Spes Bona loaded. Open follow-up: **`PT-20261029-01`** in the [audit register](../audit_issues_open.md).

CAP's surviving revolutionary government became independent and subsequently acquired **Cape Malay, Cape Creole and Nama** as primary cultures. Vanilla's **The Severed Limb** event, `colonial_administration_events.2`, explains the culture replacement through its majority-rule option `.b`. CAP's starting `southern_africa_subject_var` admits this generic colonial-collapse event after independence.

## Campaign evidence

Eight checkpoints share playthrough ID `2639442d-1c1a-45e9-b459-5522bb255b8c`. Their [preserved hashes and extracted records](evidence/cape_colonial_collapse_2026_10_29.json) cover the latest autosave, its four rotations and three earlier copies of the same campaign. Save sizes and modification times were stable during each read.

| Checkpoint or recorded date | Observation |
|---|---|
| 1 December 1842, 1 January 1849 and 1 January 1852 | Original CAP country **732** is a British colony, with **Anglo-African** as its sole primary culture. Its British colony pact dates to 1 January 1836. |
| 18 July 1853 | Initial law records on successor CAP **16777796** share this activation date, consistent with creation of the revolutionary country. No Colonial Affairs replaces Frontier Colonisation; Wealth Voting replaces Oligarchy. The retained Parliamentary Republic record also dates to this day. |
| 21 March 1854 | Successor CAP records `last_civil_war_date=1854.3.21`. A British `catalyst_revolution_successful` targets that same country on the same date. |
| 6 April 1854 | Presidential Republic replaces Parliamentary Republic in the successor's law history. This is consistent with the government-choice event reached from colonial collapse, but the law record alone does not identify its caller. |
| 1 January through 1 May 1857 | All five autosaves contain CAP **16777796**, recognised and independent of Britain, with `cultures={ 332 317 328 }`: Cape Malay, Cape Creole and Nama. Each retains `colonial_collapse_var`; `southern_africa_subject_var` is absent. |

The latest checkpoint is `save games/autosave.v3`, dated **1 May 1857**. Its capital is state **424**, `STATE_CAPE_COLONY` (Western Cape). The primary-culture IDs resolve from the save's culture database:

| Culture | Save ID | Relevant homeland |
|---|---|---|
| Cape Malay | 332 | Western Cape |
| Cape Creole | 317 | Western Cape, Eastern Cape and Northern Cape |
| Nama | 328 | Western Cape, Eastern Cape, Northern Cape and Namaqualand |
| Anglo-African | 320 | Western Cape, Eastern Cape and Northern Cape |

## Vanilla event route

CAP's country history sets `southern_africa_subject_var`. Vanilla's `on_monthly_pulse_country` includes `colonial_administration_events.2`. That event becomes eligible when the country is independent, has one of the generic African colonial markers and lacks `colonial_collapse_var`. Its immediate effect sets the collapse marker.

The majority-rule option `.b` requires Nationalism and one further condition, including No Colonial Affairs. The latest CAP has both Nationalism and No Colonial Affairs; the latter's activation dates to 18 July 1853. The checkpoints do not retain the Nationalism research date.

The option then:

1. Adds primary cultures present in the capital that have a homeland there.
2. Removes every primary culture in `heritage_group_european`, which includes Anglo-African through `heritage_british`.
3. Removes the generic colonial markers, retires eligible European characters and schedules `independence.2` for a new government choice.

In the latest capital, Boer, Cape Malay, Cape Creole and Nama are present and have homelands there. Removing European primary cultures leaves exactly the three saved cultures. SB's ordinary liberal victory in `sb_cape.100` only adds Cape Creole and cannot by itself account for this replacement.

## Cleanup and evidence limits

SB's `sb_refresh_cap_aby_subject_state` already removes `southern_africa_subject_var` from independent CAP. Its caller runs on becoming independent and on the yearly country pulse. The campaign nevertheless retains the colonial-collapse outcome. The checkpoints do not establish whether a revolutionary successor missed the relevant cleanup, inherited the marker later, or completed an already-open event after cleanup. The Vanilla event has no cancellation trigger to recheck its eligibility while open.

The collapse marker establishes that the event opened; the exact culture replacement and cleared colonial marker support its majority-rule branch. No selected-option receipt or exact choice date survives. The initiating political movement is also no longer retained, so the settler-victory marker must not be treated as proof of which movement started the revolution.

## Open follow-up

**`PT-20261029-01` remains open for design review.** Decide whether an independent CAP reached through revolution should retain this Vanilla majority-rule route, receive an authored Cape settlement, or be excluded from generic colonial collapse. Trace marker inheritance, the actual successor country, cleanup callbacks and pending-event delivery before selecting an implementation.

Completion requires the intended behaviour to be documented, any agreed change to have source checks, and DP to verify British colony continuity, revolutionary victory and defeat, peaceful independence, and a pending colonial-collapse popup across cleanup and save/reload. Keep the culture outcome distinct from the separate question of how independence was won. This documentation does not select or implement a gameplay change.

## Source references

Paths beginning with `game/` refer to the installed Vanilla game. Source hashes are retained in the evidence file.

- SB `common/history/countries/cap - cape colony.txt:63–66`: starting colonial marker.
- Vanilla `game/common/on_actions/00_code_on_actions.txt:475–485`: monthly event dispatch.
- Vanilla `game/events/colonial_administration_events.txt:319–474`: collapse eligibility, marker, majority-rule culture replacement and government follow-up.
- Vanilla `game/events/iberia_events/independence.txt`: government choices in `independence.2`.
- SB `common/cultures/sb_southern_african_cultures.txt:92–96` and Vanilla `game/common/discrimination_traits/00_cultural_heritages.txt:98–100`: Anglo-African's European heritage group.
- SB `common/scripted_effects/sb_subject_autonomy_effects.txt:237–243` and `common/on_actions/sb_cap_subject_cleanup_on_actions.txt`: existing cleanup and its callers.
- SB `events/sb_cape_events.txt:61–139`: ordinary liberal victory's Cape Creole grant.
