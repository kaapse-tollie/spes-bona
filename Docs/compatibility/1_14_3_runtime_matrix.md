# 1.14.3 fresh-game runtime matrix

Target: SB 0.20.1; game 1.14.3, build 25347710, core manifest
5228357714133991559; CMF 1.66.0 + sb-1.14.3-r1.

DP performs all game launches and engine checks. Use new campaigns; no old-save
migration or recovery. Klip River needs a checkpoint from this baseline before
the punitive play starts. Historical results do not certify this target.

| ID | Scenario and acceptance condition | Result |
|---|---|---|
| B143-01 | Fresh launch and new 1836 campaign; verify exact game/mod versions and audit error/warning logs | **Engine pending — DP** |
| B143-02 | Annex/Conquer/Return infamy tooltips use global GDP/population shares; compare consequential/inconsequential states and claimed/unclaimed land | **Engine pending — DP** |
| B143-03 | Territorial timers, recapture/reversal, and mirrored split-state reconstitution work; retaking land reverses conquest radicalization as intended by Vanilla | **Engine pending — DP** |
| B143-04 | ORA versus BST: hold BST Vrystaat but not Drakensberg; record both timers and resulting ownership | **Engine pending — DP; design ON HOLD**. Do not implement the two-stage workaround |
| B143-05 | Revoke Claim remains assent-only; diplomatic demands resolve correctly | **Engine pending — DP** |
| B143-06 | Klip: NAL Make Protectorate plus Return State against ZUL-owned Natal remain primary; Zulu backdown concedes both; British backing and separate Zulu counter-demand persist | **Engine pending — DP** |
| B143-07 | Klip negotiated peace, capitulation, and timers in either order: government event waits for both actual outcomes; partial peace/reversal grants nothing extra; no unrelated-war gate | **Engine pending — DP** |
| B143-08 | Klip government event once: direct annexation, chiefdom puppet/Zibhebhu/CAP exile, or Crown preserving actual king/heir and protectorate | **Engine pending — DP** |
| B143-09 | Cultural-majority revolution/secession state weights evaluate without old-API errors; CAP stays excluded; other CMF movement behavior retained | **Engine pending — DP** |
| B143-10 | Regional AI incorporation: NAL/Zululand, CAP/Bechuanaland and Griqualand West, ORA/Drakensberg; unrelated countries and human/wrong-owner controls unchanged | **Engine pending — DP** |
| B143-11 | AI demands, play backing, treaty selection, and state values reflect the new Vanilla balance | **Engine pending — DP** |
| B143-12 | ORA qualifying victory over MTB delivers Great Trek .002 once; Blood River targets opponents/Natal and delivers Natalia once, including guns-bargain route | **Engine pending — DP** |
| B143-13 | Other story-war victory/defeat/white-peace/backdown/reversal and exact subject restoration retain once-only settlements | **Engine pending — DP** |
| B143-14 | Building hiring, individual/bulk production-method controls, naval transport completion, merge tracking, and return-home controls remain usable | **Engine pending — DP** |

No engine run was performed for this rebase. Append dated DP observations and
retained log evidence to each scenario rather than replacing pending with static
test results. The existing five deferred release gates remain separately tracked.
