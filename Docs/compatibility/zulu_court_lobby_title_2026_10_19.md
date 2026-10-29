# Prerogative title: lobby and nested localisation — 19 October 2026

**Latest status:** DP verified the lobby title after the first correction, but the live title still failed. The top-scope implementation and test described below are historical and superseded by the second correction at the end of this report.

## Observed failure

DP reported that the Unique Journal Entries lobby row remained blank after a fresh launch, with further errors when opening the JE. The captured log has 4,389 lines. All but one belong to the title lookup:

| Message | Count |
|---|---:|
| `SelectLocalization(ROOT.GetCountry.IsValid, ...)` failed | 890 |
| Data error in `je_sb_zulu_kingdom` | 890 |
| ROOT promotion failed in the validity check | 889 |
| ROOT promotion failed in the nested country title | 573 |
| Nested country-title lookup failed | 573 |
| Data error in `sb_prerogative_country_title` | 573 |
| Existing `gfx/map/textures/` file-watcher message | 1 |

The late messages repeat the nested title failure. This capture contains no applied-modifier-description errors. That absence does not prove that every modifier tooltip was exercised.

Source: DP's `Victoria 3/logs/error.log`, copied unchanged to `/private/tmp/sb-court-lobby-error-2026-10-19.log`. SHA-256: `d9844141493d50dd93e74dbd46c130a86c554d3b2dc6b2131e95c227852a967f`. The file-watcher message also appears in the existing 18 October launch evidence; it is not a new title or missing-artwork error.

## Cause and native contracts

The previous fix tried to test `ROOT.GetCountry.IsValid`. If ROOT itself is absent, the engine cannot promote it to a scope, so it fails before testing validity or choosing the static fallback. Adding that guard did not make the lobby lookup safe. The nested localisation also attempted to promote ROOT, and the late log shows that failing separately.

Installed Vanilla evidence:

- `gui/multiplayer_lobby_types.gui`: the lobby's `Country.GetLobbyJournalEntries` model renders `JournalEntryType.GetName`.
- `gui/journal_entry.gui` and CMF's corresponding panel: a live panel renders `JournalEntry.GetName`.
- Read-only inspection of the installed arm64 functions confirms that `CDataJournalEntryType::GetName` localises the database key, while `CDataJournalEntry::GetName` calls `LocalizeWithTopScope` using the JE's stored scope. No game execution was involved.
- `gui/minimap.gui` and `gui/ingame_hud.gui` use the global `IsInGame` function; it does not need ROOT or a selected country.
- Vanilla's `je_the_hungry_forties` title in `localization/english/ip3_misc_01_l_english.yml` and `je_federation_of_india` in `ip2_misc_01_l_english.yml` use `SCOPE.GetRootScope.GetCountry.GetCustom(...)` for an active JE's country.

The error log establishes the failed promotions. The exact internal reason the nested ROOT override is unavailable is not needed to fix it; the live JE's top scope is the native alternative. Do not confuse the selected player with that owning country.

## Change

Only two runtime localisation expressions change:

1. `je_sb_zulu_kingdom` selects its static Royal Prerogative fallback using `IsInGame`, with no ROOT or country access in the condition.
2. The selected in-game key uses `SCOPE.GetRootScope.GetCountry.GetCustom('sb_prerogative_title')`. The existing constitution check chooses Royal or Chiefly Prerogative.

There is no GUI override, new JE, country variable, gameplay change, or rewrite of reviewed prose. The live title follows the JE's owning country, including NGN inheritance, rather than `GetPlayer`. Existing modifier-description code is unchanged because this log does not implicate it.

## Verification

- The new context regression failed against the original lobby expression.
- Fixing only that expression still failed at the nested ROOT lookup.
- After both corrections, all **60 focused institutional/court/law tests pass**.
- Title checks cover a lobby with no root or live JE, uninitialised country variables, Monarchy, Social Monarchy, Federated Chiefdoms, ZUL/NGN, and an unrelated caller with the opposite constitution. These are source-driven context checks, not engine rendering tests.
- Full discovery: **592 tests, 583 passed, one failure, eight skips**. The failure and the separate localisation gate still report existing reviewed-prose drift in Klip River `.060`/`.080` and Natal Crisis `.050`; those namespaces and their approval baseline are untouched.
- Full validator: **15/17 gates passed, warned or skipped**. CMF, override, map, naval and runtime-contract checks pass. Advisory Tiger reports 1,066 errors and 145 warnings across the existing tree; it targets 1.13.5 rather than the installed 1.14.5 and reports no diagnostic for the revised title expressions. Whitespace checks pass.
- The [evidence record](evidence/zulu_court_lobby_title_2026_10_19.json) contains the log summary, source hashes and validation counts. Raw validation: `/private/tmp/sb-court-lobby-2026-10-19-validation.txt`.

**Pending DP:** fresh-launch lobby row reads Royal Prerogative; open the JE and its tooltip without either title error; a chiefly constitution displays Chiefly Prerogative. No game launch was performed by Codex.

## Second correction: the selected localisation loses script context

DP's next report confirms that the lobby title now appears. The live JE instead logs `Promote 'SCOPE' returned nullptr` for `sb_prerogative_country_title`. Its captured error log has 2,775 lines: 925 instances each of failed SCOPE promotion, failed nested lookup and the resulting localisation error.

Read-only inspection of `NPdxDataUtilityFunctions::SelectLocalization` establishes the missing step: it selects a key, creates a fresh localisation data container and calls `PdxDataParseAndLocalize` with no key/value pairs forwarded from its caller. The temporary ROOT/SCOPE bindings added by `JournalEntry.GetName` therefore cannot be relied upon inside the selected key. The prior test wrongly passed its top-scope fixture straight through that call. A directly scoped native JE title was not an adequate precedent for the extra nested lookup.

The existing GUI binding is different. Vanilla's `JOURNAL_ENTRY_TOOLTIP` selects `JOURNAL_ENTRY_STATUS` through the same helper, and the selected text uses `[JournalEntry.GetStatusDesc]`. The live JE panel, journal rows and fancy tooltip bind a `JournalEntry` object; CMF retains that binding. The selected SB title now uses `[JournalEntry.GetCountry.GetCustom('sb_prerogative_title')]`. This retains the actual JE owner and does not use GetPlayer. The successful lobby gate remains unchanged and never evaluates the live key there.

The regression now drops script bindings at the nested call and keeps only the GUI JournalEntry. It fails against the SCOPE version and passes after the one-line localisation correction. Coverage still includes no-context lobby, uninitialised country variables, Royal/Chiefly selection, ZUL/NGN and an unrelated player or script root. These checks model the observed contract; they do not execute the engine renderer.

Focused checks: **60 passed**. Full discovery again ran **592 tests: 583 passed, one failure and eight skips**. The validator remains **15/17**, with the same reviewed-prose drift causing both failed gates. CMF, override, map, naval and runtime-contract checks pass. Advisory Tiger reports 1,066 errors and 141 warnings; the warning-message differences concern unchanged Bechuanaland scope analysis, with no diagnostic for the revised title expression. Full validation is recorded separately in [revision 2 evidence](evidence/zulu_court_lobby_title_2026_10_19_r2.json), with raw output at `/private/tmp/sb-court-lobby-2026-10-19-r2-validation.txt`. The earlier results above remain intact.

**Engine status:** lobby title verified by DP. Live panel, journal row and pinned JE tooltip titles remain pending DP, especially Chiefly Prerogative after a constitution change. No game launch performed by Codex.
