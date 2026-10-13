# 1.14.2 fresh-game runtime matrix

Target: SB 0.20.1; game build 25207758, core depot manifest 2887980275526736263;
CMF 1.66.0 + sb-1.14.2-r1. Only new campaigns are supported. Old-save tests are excluded.

| ID | Scenario and acceptance condition | Result |
|---|---|---|
| B142-01 | Cold launch: exact game version and both intended mods loaded | **Main menu verified**; checksum f575; launch errors remain, see report/evidence |
| B142-02 | New 1836 campaign; startup history, journals and map initialise | **Engine pending** — New Game UI action fails with noWindowsAvailable |
| B142-03 | Conquer/Return/Annex: timer advances under control, reverses on recapture; territorial mirrors reconstitute split states | **Engine pending** |
| B142-04 | Revoke Claim does not auto-enforce; diplomatic demands can resolve | **Engine pending**; assent policy statically verified |
| B142-05 | ORA returns BST Vrystaat and adds Drakensberg conquest. Hold only Vrystaat; record each timer and ownership before/after enforcement | **Engine pending; design ON HOLD**. Never substitute a two-stage workaround in this test |
| B142-06 | ORA defeats MTB through the authored route; Great Trek .002 appears exactly once | **Engine pending** |
| B142-07 | Blood River: ORA and ZUL goals target opponents and Natal; peace/capitulation decides the result and ORA victory delivers Natalia once, including rejected guns-bargain variant | **Peace-based behavior restored; engine retest pending DP.** Decisive-timer experiment failed DP's test (goal executed at 100%, war stayed active) and was reverted; evidence in `blood_river_timer_design_2026_09_12.md` |
| B142-08 | Other story wars: victory, defeat, white peace, backdown, timer reversal; terminal settlement exactly once | **Engine pending** — carry forward the applicable scenario definitions from the historical OB1 matrix, with new runs |
| B142-09 | Independence/restoration/revolutions preserve each exact subject relation and participation policy | **Engine pending** |
| B142-10 | AI NAL/Zululand, CAP/Bechuanaland and Griqualand West, ORA/Drakensberg; human/wrong-owner/wrong-state controls unchanged | **Engine pending** |
| B142-11 | Eligible buildings hire; individual and bulk production-method controls remain usable | **Engine pending** |
| B142-12 | Naval transport completes, army tracking/merging works, return-home control is usable | **Engine pending** |
| B142-13 | Vanilla-only and CMF-only cold-launch controls distinguish harbour and blocker errors | **Engine pending** |

Static tests do not certify these engine scenarios. Use the retained launch evidence
and `1_14_2_rebase.md` for the completed observations. The game was left at its main
menu; no existing campaign was loaded or modified.
