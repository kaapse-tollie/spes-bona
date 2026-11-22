# Victoria 3 1.15.1 / CMF 1.67.3 runtime checks

The [19 November CMF 1.67.9 update](cmf_1_67_9_update_2026_11_19.md) adds replay checks for the shared outliner and expanded journals on this game build. The observations below are dated to the original hotfix.

Date: 11 November 2026. Target: build `26591675`, public branch, all DLC,
CMF `1.67.3 + sb-1.15.1-r1`, SB `0.20.3`. **No row is fully accepted yet.**

DP's [11 November launch log](1_15_1_launch_review_2026_11_11.md) contains no
new compatibility-patch parser/scope errors. This supplies the log-inspection
part of `RT151-01`; journal/outliner rendering remains pending, as do all other
rows. Panama's anchor mismatch is present in native 1.15.1 source data; it is
recorded separately without claiming successful port operation.

DP launches the game. Use a cold launch and fresh campaign with CMF before SB.
Record the load order, country, date, observed result and relevant log excerpt.
Earlier 1.15.0 observations remain historical; no save migration is included.

| ID | Scenario | Acceptance |
| --- | --- | --- |
| RT151-01 | Fresh all-DLC launch; open active/concluded journals and outliner | Normal rendering and no new related parser/scope errors. |
| RT151-02 | International situation and organisation outliner entries, including goals/actions | CMF's upstream goal bars and possible actions display and update correctly. |
| RT151-03 | Bechuanaland and Imperial Confederation progress widgets; Zulu Prerogative marker | Dynamic bars update with their tooltips; the bespoke Prerogative marker remains correct. |
| RT151-04 | Employed upper-strata military-industry owners; unemployed/lower-strata controls | Native ownership attraction contributes twice owned military-industry assets, capped at 150, only for eligible pops; existing SB aristocrat attraction and tooltip remain. |
| RT151-05 | Colonial claims against recognised, unrecognised and decentralised owners; existing claimant claims | Native claim-independent infamy and decentralised discount apply; SB's Boer-region exclusion still blocks the same targets. |
| RT151-06 | Check resource capacities and Griqua startup | Namaqualand/Zambia/Katanga copper is 9/21/35 without duplicated parent capacity. PHL/WBL retain SB tier 6 plus the three selected technologies and their laws/institutions. |
| RT151-07 | Cultural/religious/national/slave secession during a revolution; ideological controls | The six native opt-ins work; ideological defaults and Chiefdoms/Cape restrictions remain. Include NAL's marked Zulu movement disband/recreation handoff. |

Use disposable debug scenarios for states unavailable immediately at campaign
start. Static tests model the copied calculations and scope markers; they do not
establish native uprising scheduling, GUI rendering or engine load order.
Record unexplained diagnostics for attribution rather than treating every native
warning as an SB regression. Installed Tiger 1.19.0 is a diagnostic aid, not a
1.15.1 compatibility certificate.

The [existing 1.15.0 matrix](1_15_0_runtime_matrix.md) and
[Chiefdoms matrix](../zulu_thirteen_chiefs_runtime_matrix_2026_11_10.md) retain their
separate unresolved scenarios. This hotfix does not close those gates.
