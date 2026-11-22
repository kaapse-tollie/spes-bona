# Victoria 3 1.15.0 journal-entry implementation

Recorded 5 November 2026 against the selected 1.15.0 installation and CMF 1.67.1.
This report covers the journal-entry part of the
[approved rebase design](1_15_0_rebase_design_2026_11_05.md). It records source
verification, not engine certification.

## Result

All 27 SB journal definitions now use 54 native `outcome` blocks. The migration
preserves the authored completion, failure, invalidation and timeout triggers,
effects and event previews. Outcome order is completion, failure, invalidation,
then timeout where present; confirming the engine's treatment of competing
conditions remains a runtime gate. Existing activation, monthly and weekly
effects, buttons, progress-bar indices and time limits are unchanged in the 25
authored definitions checked against the captured pre-port source.

- The contextless Bechuanaland corridor keeps its settlement in `effect`, not
  `effect_all_involved`, so the shared operation is not deliberately repeated
  for every participant. Its existing guards and cleanup remain intact.
- Zulu institutions and the other persistent entries retain only their existing
  invalidation exits; no completion condition was invented. Disabled Highveld
  retains its false activation/completion and empty terminal effects.
- Native invalidation uses `hidden invalid_outcome`; timeout uses `timeout` and
  no ordinary trigger. Existing custom outcome headers and event reward
  previews are attached to the corresponding outcome.
- Standard native conclusion text is reused except for the two alternative
  political victories in Bechuanaland and the two frontier results. Their four
  new general keys describe the winner without labelling a participant's
  victory a failed journal entry. They are marked `TO REVIEW`; no existing
  reviewed prose was substantively rewritten.

The two complete native replacements were rebased separately:

- [Scramble for Africa](../../common/journal_entries/zz_sb_scramble_for_africa_override.txt)
  retains the full 1.15 definition, including its new activation description and
  native cleanup. The SB growth modifier is granted and repaired as before and
  removed on completion, failure and timeout.
- [Abolish the Monarchy](../../common/journal_entries/zz_sb_abolish_monarchy_override.txt)
  retains the full 1.15 definition and invalidation cleanup, adding only SB's
  existing Boer activation exclusion and invalidation condition.

## Progress bars and CMF presentation

The four obsolete `double_sided_bad` declarations in
[SB progress bars](../../common/scripted_progress_bars/sb_progress_bars.txt) now
use native progress/background/glow textures and markers: Cape balance, Zulu
dynastic stability, Bechuanaland influence and Chiefdom balance. All 15 bars'
arithmetic, ranges, direction and nonvisual declarations are checked against the
pre-port contracts. The other eleven styles remain supported and unchanged.

The [Chiefdom GUI](../../gui/sb_zululand_chiefdoms_progress_bars.gui) uses native
`scripted_progressbar_dynamic` and `ScriptedProgressBar.IsDynamic`; its separate
Boer commitment branch is retained. The bespoke Prerogative layout is retained.

Pristine CMF 1.67.1 did not render dynamic native bars in its two fallback
containers. The narrowly scoped
[CMF compatibility payload](../../patches/cmf/sb-1.15.0-r1/files/gui/com_gui_progressbars.gui)
adds the native dynamic renderer to the journal and outliner fallbacks. It
preserves the CMF-owned branches, indices, drift and target handling. This
payload is part of the dependency agent's verified `sb-1.15.0-r1` installation.
The native source contracts are the `scripted_progressbar_dynamic` type in
`game/gui/shared/progressbars.gui`, its journal use in
`game/gui/journal_entry.gui`, and its outliner use in `game/gui/journal.gui`.
Correct appearance and interaction still require the running game.

The additional [CMF source audit](evidence/1_15_0_journal_implementation/cmf_source_audit.json)
checks its five migrated test JEs, illustration assets and eleven interface
contracts. Its four organisation/situation examples preserve their former
terminal trigger/effect bodies; the styling demonstration now uses a permanently
false hidden invalidation outcome. Group illustration assets resolve through
CMF or native files. Active/potential/concluded lists, concluded descriptions
and outcome rendering use the new native APIs.

One upstream defect remains recorded: the international-situation test JE has a
combined, undefined timeout conclusion key. Its only scripted creation is the
orphan `com_debug.2` test event, explicitly marked not to call; SB has no caller.
The audit records it without extending the live compatibility patch. This is
not a claim that every CMF debug demonstration is engine-certified.

## Evidence and checks

The final targeted suite passed **153 tests**. It includes the new migration
contracts, existing JE reward-preview and source-executed regression fixtures,
shared-corridor integration, Zulu institution/frontier/court checks, Natal,
frontier handoffs, Rhodesian invalidation and current-native Scramble parity.

- [Executable migration tests](../../tests/test_1_15_journal_entries.py) compare
  25 authored JEs against captured source contracts, check native outcome shape,
  check all 15 bar calculations and compare the monarchy replacement to native.
- [Captured contracts](evidence/1_15_0_journal_implementation/contracts.json)
  retain pre-port file hashes and parsed nonterminal/trigger/effect/preview
  hashes. [Migration mapping](evidence/1_15_0_journal_implementation/migration.json)
  records the field conversion. Its initial body hashes for the two native
  replacements are explicitly superseded by current-native parity checks.
- [Verification result](evidence/1_15_0_journal_implementation/verification.json)
  records the exact command, result and limits. The test output is retained in
  `generated/rebase_1_15_0/je_tests.log`.
- The new [conclusion localisation](../../localization/english/sb_1_15_journal_conclusions_l_english.yml)
  uses the required UTF-8 BOM, English header and general-key review marker.
  Existing review-marker classification rules are unchanged.

## DP runtime gates

Use a fresh all-DLC campaign with the selected game and installed CMF patch.

1. Open active and concluded journals and the outliner. Check standard and
   custom group illustrations, translated headings, result text and event
   previews, including both political outcomes of Bechuanaland and the frontier.
2. Exercise completion, failure, invalidation and applicable timeout paths.
   Check event delivery and cleanup, including competing terminal conditions.
   Confirm shared Bechuanaland settlement occurs once across participants and
   produces the same ownership/resource outcomes as before.
3. Confirm persistent institutions remain present through ordinary play,
   invalidate only on their existing conditions, and leave Highveld disabled.
   Check Scramble modifier cleanup and monarchy invalidation cleanup.
4. Inspect the four migrated bars in their actual interfaces: fill direction,
   colours, values, endpoints, marker, tooltips and hover behaviour. Check CMF's
   native fallback in both journal and outliner and retain the separate
   Prerogative neutral-centre/threshold presentation.

These tests do not establish native outcome evaluation timing, native event
dispatch/once-only consumption, save/load semantics or actual GUI rendering.
Those engine checks remain pending; no performance improvement is claimed.
