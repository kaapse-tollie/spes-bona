# Victoria 3 1.15.0 — conflict scan and rebase preparation

**5 November 2026. Preparation only; no rebase implemented.** SB's current
working tree, including uncommitted work, is the source of intended behaviour.
The supported SB baseline remains 1.14.5. This report proposes a fresh-campaign
rebase; it does not propose save migration or changes to SB's content design.

This needs a substantive compatibility port. The main blockers are JE outcomes,
CMF's journal UI and political definitions, and world/map data hidden by SB's
full-file overrides. Changing supported-version strings or refreshing hashes
would conceal those conflicts.

**Current design update:** DP's [pass-one decisions](1_15_0_rebase_design_2026_11_05.md)
select latest compatible CMF, currently verified **1.67.1**, the authored-map-delta
policy and native-copper-first staging. That record supersedes earlier open
recommendations here. The [1.67.0 staging review](1_15_0_cmf_1_67_0_followup_2026_11_05.md)
records most of the upstream port; 1.67.1 fixes its two remaining old-form trigger
calls and seven obsolete ideology references. Dependency observations below
retain the original installed-1.66 scope. SB itself has not been rebased.

The [modding-digest follow-up](1_15_0_modding_digest_review_2026_11_05.md) adds
localisation escaping, CMF group illustrations, a custom-DNA field and four CMF
movement-trigger calls to the worklist. It also records digest discrepancies
and [planning decisions D1–D8](1_15_0_modding_digest_review_2026_11_05.md#decisions-to-settle-when-building-the-plan).
Read it alongside the relevant workstream; the original evidence remains dated
to the first scan.

## Read by workstream

- [Target, scope and scan counts](#target-scope-and-scan-counts)
- [JE outcomes and presentation](#je-outcomes-and-presentation)
- [CMF upstream status and dependency work](#cmf-upstream-status-and-dependency-work)
- [World history, maps and resources](#world-history-maps-and-resources)
- [Other gameplay and localisation contracts](#other-gameplay-and-localisation-contracts)
- [Proposed implementation order](#proposed-implementation-order)
- [Verification and remaining limits](#verification-and-remaining-limits)
- [Digest findings and planning decisions](1_15_0_modding_digest_review_2026_11_05.md)

Read the relevant section and its linked evidence rather than loading every
inventory. Existing [repository boundaries](../../AGENTS.md), the
[override/rebase rules](../pitfalls/compatibility.md) and the complete
[localisation policy](../policies/localisation-review.md) remain authoritative.
SB requires all DLC, including State and Revolution; DP performs game launches.

## Target, scope and scan counts

| Component | Observed identity |
| --- | --- |
| Installed Victoria 3 | `1.15.0 (Ivan-Chai)`, Steam build `26453692`, branch `public` |
| Installed core depot | `529341`, manifest `7727600027425614094`, created 3 November 2026 at 17:10:02 UTC |
| SB | `0.20.3`; both version files still target `1.14.5` |
| Installed CMF | Official `1.66.0` plus SB patch `sb-1.14.3-r1`; complete tree matches the existing pin |
| Comparison baseline | Current [override inventory](override_inventory.json), principally pinned to 1.14.5, plus the [CMF patch contracts](../../patches/cmf/sb-1.14.3-r1/manifest.json) |

The old 1.14.5 core manifest is no longer in Steam's local depot cache. This is
**not a complete 1.14.5 → 1.15.0 depot diff**. It compares retained source hashes
and object hashes with installed 1.15.0, inventories current collisions, and
reviews high-risk source differences. An SB-versus-current-Vanilla diff contains
both intended SB changes and upstream changes; it is not an old/new Vanilla diff.

| Surface | Result |
| --- | --- |
| 39 registered exact-path SB overrides | 15 upstream files changed; 24 retained their pinned bytes |
| 124 registered keyed SB overrides | 62 upstream object hashes changed; 59 objects unchanged; three SB-owned objects have no Vanilla baseline |
| Unchanged keyed objects in changed containing files | 43: source-file drift alone does not establish a gameplay change |
| Two non-shadowed AI contracts | Both changed: `ai_strategy_default`, `state_transfer` |
| 16 CMF-to-Vanilla contracts | Eight object hashes changed; six more have containing-file drift only; two fully unchanged |
| Localisation | All 24 registered source rows changed at file level, across nine source files; this does not prove every collided line changed |
| Inventory coverage | No new/missing exact-path or explicit keyed SB overrides; registered mod file/object hashes match the working tree |
| SB JEs | All 27 definitions, in 17 files, still contain legacy outcome fields; none uses `outcome` |
| CMF JEs | All five bundled definitions contain legacy outcome fields |

The 62 object changes include **35 character templates**. Counts are raw hash
drift, including formatting and comments; they are review queues, not counts of
confirmed defects. [Complete contract results](evidence/1_15_0_pre_rebase_2026_11_05/conflict_scan.json)
retain both hashes and ownership intent.

## JE outcomes and presentation

**Required migration.** Installed
[1.15 JE documentation](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md>)
explicitly replaces completion, failure, invalidation and timeout effect blocks
with repeated `outcome` blocks. Current Vanilla has 449 JEs, no legacy outcome
fields, and 447 entries with outcomes. The two outcome-free definitions do not
make old fields valid.

Use the [per-JE migration inventory](evidence/1_15_0_pre_rebase_2026_11_05/je_migration_inventory.json)
to move each trigger, effect and tooltip together:

| Old contract | 1.15 destination / preservation requirement |
| --- | --- |
| `complete` + `on_complete`; `fail` + `on_fail` | Separate `outcome.trigger` and `outcome.effect` pairs; preserve conditions, scope, ordering and cleanup |
| `invalid` + `on_invalid` | Outcome with `hidden invalid_outcome`; retain its cleanup and distinguish it from ordinary failure |
| `on_timeout` | Outcome flagged `timeout`, without a trigger; retain the JE-level duration. At most one timeout outcome |
| Custom completion/failure headers | Outcome `header` and `effect_header`; keep existing approved wording |
| Completed/failed event-outcome descriptions | Corresponding outcome's `event_outcome_desc` / `event_outcome_effect_desc`; previews must not execute rewards |
| Contextless/shared JE settlement | Preserve shared versus per-participant effects; use `effect_all_involved` only where the actual former contract requires it |

Every outcome needs a `conclusion_desc`; non-hidden outcomes need headers. Reuse
appropriate existing standard keys where suitable. New flavour text must follow
the localisation policy; do not rewrite reviewed namespaces to accommodate a
mechanical migration without DP's approved replacement.

The [Bechuanaland Corridor](../../common/journal_entries/1-11_sb_bechuanaland_corridor.txt)
needs particular care: two political outcomes, custom headers, a shared container,
invalidation and linked event delivery. Persistent institutional JEs and the
deliberately disabled Vanilla Highveld JE also need a valid schema without
gaining new completion or activation behaviour. The installed
[abolition JE](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_abolish_monarchy.txt>)
and [Scramble JE](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_scramble_for_africa.txt>)
provide concrete outcome and timeout examples.

**Progress bars need a narrower port.** SB has 15 native scripted bars. Eleven
use `default`, `default_green` or `default_bad`, which the installed
[1.15 bar documentation](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/scripted_progress_bars.md>)
and GUI still support. Do not replace these merely because the pre-release
modding diary described the old presentation system as replaced.

Four [SB bars](../../common/scripted_progress_bars/sb_progress_bars.txt) use
`double_sided_bad`: Cape balance, Zulu dynastic stability, Bechuanaland influence
and Chiefdom balance. No current Vanilla bar uses that field. Port their visuals
to the documented texture/colour/marker interface while preserving ranges,
direction, arithmetic and CMF indices. The new
[Great Game bar](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/00_great_game_progress_bars.txt>)
is an example, not a replacement design. CMF styling, widgets, concluded-entry
display and the new Advance/Retreat lists still require separate UI checks.
The dependency port also needs illustrations for seven CMF journal groups;
SB's existing Vanilla groups already supply them. See the
[group audit](1_15_0_modding_digest_review_2026_11_05.md#cmf-journal-group-illustrations).

## CMF upstream status and dependency work

**At the initial check, CMF had upstream edits but no released 1.15 port was found.** This
distinguishes release, default branch, development branch and open proposals.
The checked identities, changed-file lists and PR files are retained in
[CMF upstream evidence](evidence/1_15_0_pre_rebase_2026_11_05/cmf_upstream_status.json).

| Upstream surface | Observed state on 5 November |
| --- | --- |
| Latest GitHub release | [1.66.0](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/releases/tag/1.66.0), published 2 September; release asset SHA-256 remains `79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b` |
| `main` | `5eaa4c0212895ab2b0924358ccb99850a8ecb78d`; three commits after 1.66.0: second Manaflow placeholder, localisation changes including yes/no macro keys, and a credit correction. These are the same three noted by the previous rebase |
| `1.14` branch | `31e0ab91233c611dd5b7da4f799fb75e3c6afc2e`; six commits after 1.66.0. Additional work updates war goals, changes interaction replacement directives, removes old struct maintenance, then [removes the three territorial war-goal overrides](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/commit/31e0ab91233c611dd5b7da4f799fb75e3c6afc2e) on 18 October |
| Open PR 153 | [Anonymise progress-bar containers](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/pull/153): changes container identity, effects, triggers, buttons and demo JE; unmerged, not a 1.15 outcome/UI port |
| Open PR 152 | [Simplified Chinese localisation](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/pull/152); unmerged |
| Workshop | Current payload not verified: public changelog request returned HTTP 429 and no cached local Workshop metadata was found |

Do not switch SB to `main` or `1.14` as a compatibility fix. Neither comparison
provides the necessary new journal interface. The installed patched tree is
intact; that proves dependency integrity, not 1.15 compatibility.

The dependency review must be wider than the old 16 pins:

- **Journal GUI:** CMF replaces `journal_panel` and `journal_entry_panel` types
  from differently named files. Its panel still calls
  `JournalEntry.GetCompletionTooltip` and old double-sided bar APIs; current
  [Vanilla's panel](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/gui/journal_entry.gui>)
  renders `JournalEntry.GetOutcomes` and concluded entries. Migrating SB's JE
  scripts alone does not port the effective UI. The digest's generated GUI
  snapshots are insufficient to prove removal or continued support of individual
  methods; see the [source caveats](1_15_0_modding_digest_review_2026_11_05.md#corrections-and-evidence-caveats).
- **Political content:** the installed CMF has 40 non-comment references to
  `ideology_social_democrat`, which has no definition in current Vanilla or CMF.
  Its character checks also use `ideology_communist`; that identifier still
  exists for interest groups, while the new character ideology is
  `ideology_communist_leader`. Do not globally rename the IG ideology. The new
  progressive category uses `ideology_state_socialist`.
- **Parties and movements:** CMF retains `social_democrat_party`, while native
  1.15 supplies `socialist_party` and `revolutionary_party`. Review the full
  politics integration rather than patching two category triggers alone. Seven
  SB movement replacements add another effective layer over CMF. The digest
  follow-up also identifies [four old-form population-share trigger calls](1_15_0_modding_digest_review_2026_11_05.md#cmf-movement-trigger-parameters)
  in three CMF movements that SB does not replace.
- **War goals:** the installed patch still supplies annex/conquest/return-state
  definitions. SB additionally replaces conquest for the Swazi restriction and
  annexation for the British–Zulu character handoff. Upstream branch deletion
  does not remove SB's own copies. Decide whether to retire the old CMF land-grab
  hook or carry it deliberately; preserve SB's authored restrictions/handoff.
- **Other UI and hooks:** the current surface scan finds 16 runtime exact-path
  overlaps, 29 shared GUI type names and 76 common-object overlap/explicit
  replacement rows. These include expected additive on-actions and intentional
  extensions, not 121 proven new conflicts. They identify what a dependency
  rebase must review beyond the historical patch manifest.

See the [dependency surface inventory](evidence/1_15_0_pre_rebase_2026_11_05/semantic_scan.json).
Prefer a verified compatible upstream release if one appears before execution.
Otherwise prepare a new, reproducible SB compatibility patch against an exact
immutable base. Do not edit the installed sibling dependency by hand. The
[current patch loader](../../tools/cmf_patch.py) only permits `common/` payloads
and overwrites existing files; GUI/localisation changes or deletions need explicit support
and appropriate integrity/rollback tests before such a patch can be installed.

## World history, maps and resources

**Required full-shadow rebases.** The changed exact paths are listed in the
[contract scan](evidence/1_15_0_pre_rebase_2026_11_05/conflict_scan.json).

| Surface | Concrete conflict and preparation |
| --- | --- |
| Global state history | SB's `00_states.txt` omits new `STATE_KOSTROMA`, `STATE_LITHUANIA`, `STATE_SARATOV`, `STATE_TULA` and `STATE_VOLOGDA` blocks. Scripts still contain 11 `s:` links to removed `STATE_KAUNAS`, `STATE_GALICH`, `STATE_TARTARIA` and `STATE_CHUKOTKA`. Start from 1.15 world history and reapply SB's regional partition/ownership changes |
| European formations | Current bodies differ for Russia and Portugal. Russia has new state references, formation composition and supply hubs; retain SB's deliberate Portuguese formations while adopting the current Russian baseline |
| Starting movements | Native Russia now creates a Cossack movement and Bukhara has a land-reform movement. Carry these alongside SB's deliberate exclusion of generic Absolutists from its institutional countries |
| Regional pops | Review the changed Sub-Saharan file, including Kazembe, Mozambique and Angola outside or on the edge of SB's authored scope; preserve SB's own demographic changes |
| Historical treaties | The Nagasaki goods transfer now uses copper instead of lead. Preserve SB's treaty policy and absent day-one TRN, rather than restoring Vanilla's three TRN treaties |
| Highveld events and buttons | Source changed. Review together with the disabled JE and SB's replacement story; avoid re-enabling a duplicate Vanilla chain |
| Global map assets | Province raster, province terrains, all five locator files and spline binary changed upstream. The old global shadows also hide changes outside Southern Africa. Reapply proven SB edits to a 1.15 baseline; do not merely repin old binaries |
| Regional state definitions | Eight previously untouched blocks now differ: Amhara, Gonder, Oromia, Katanga, Zambia, Mozambique, South Madagascar and South Cameroon. Changes include cold fields, copper and a blockade locator |

Evidence: [history block comparison](evidence/1_15_0_pre_rebase_2026_11_05/history_comparison.json),
[undefined state links](evidence/1_15_0_pre_rebase_2026_11_05/missing_state_links.json),
and [regional differences](evidence/1_15_0_pre_rebase_2026_11_05/semantic_scan.json).

Native 1.15 adds copper capacity in **Katanga (30), Zambia (18) and Namaqualand
(6)**; Katanga and Zambia also gain the African Copper Belt trait. SB's full
regional file suppresses these additions. Retain native additions outside SB's
authored resource scope; reconcile Namaqualand with SB's resource policy rather
than silently replacing its researched totals. Check copper demand and inherited
production methods without folding a general economic rebalance into the port.

**Naval verification needs redesign before repinning.** The new network parses
as 11,010 nodes and 11,091 connections. Applying the old checker reports no
matching node for 29 of SB's 33 state ports. Crucially, the same checker fails
for **all 31 unmodified Vanilla Sub-Saharan ports**. This negative control prevents
calling the 29 results SB-specific disconnections. Re-establish the 1.15 port,
locator, spline and travel-network relationship, then validate against Vanilla
and a deliberately broken case. Map acceptance and actual deployments remain
engine checks. [Raw results and control](evidence/1_15_0_pre_rebase_2026_11_05/je_and_naval_scan.json)
are paired with [the control detail](evidence/1_15_0_pre_rebase_2026_11_05/semantic_scan.json).

The known local spline backups are from 1.13.8 or earlier SB work, not a verified
1.14.5 Vanilla baseline. Obtain exact old source bytes where a three-way merge
requires them, or reconstruct and verify the authored delta from retained
evidence. Do not label a two-way comparison a complete historical merge.

## Other gameplay and localisation contracts

- **Territorial infamy:** current conquest saves `infamy_ignores_claim` before
  evaluating `state_infamy_value`; current annexation adds the Russian-unification
  infamy factor. Port the complete native bodies before reapplying CMF/SB deltas.
  Review return-state too. Timer enforcement and final settlement remain separate
  callbacks; do not revive beta-only expiry assumptions just to satisfy old tests.
- **Laws and politics:** Frontier Colonisation gains a Russia/internal-colonisation
  enactment guard; Legacy Slavery has changed progressiveness; Junker ideology has
  opinions on new laws. Social Mobility gains a Tsar-upgrade eligibility guard and
  substantial AI content. Preserve SB's narrow gates while restoring untouched
  global branches. Mass Conscription also has raw object drift, including formatting;
  it needs review rather than an assumed mechanical change.
- **Characters:** retirement adds native politician conversion and content-specific
  branches. Review the 35 template changes, PHL's regnal numbering and SAF's dynamic
  name with SB's rosters/identity policy. New favourite/notable roles are not an
  instruction to redesign SB's court system. The digest adds a schema migration
  for [Fodo's custom DNA](1_15_0_modding_digest_review_2026_11_05.md#sb-custom-dna).
- **AI:** re-evaluate the default strategy, state-transfer scoring and the three
  incorporation triggers together. Their raw changes include reordered predicates;
  preserve SB's owner checks and four regional priorities unless a semantic change
  requires adaptation.
- **Localisation:** inspect collided keys within the nine changed source files;
  file hashes alone do not justify rewriting text. Preserve approved namespaces,
  British English, SB names and intentional dominion policy. New conclusion text
  follows the exact [localisation policy](../policies/localisation-review.md).
  Separately from collided Vanilla keys, the [escaping audit](1_15_0_modding_digest_review_2026_11_05.md#localisation-function-arguments)
  identifies 88 unescaped references across 58 SB lines and 494 candidates in
  CMF's bundled languages. Apply the exact review policy before editing them.

A targeted scan found no active SB references to the listed removed war-exhaustion,
old strait-importance or ship-interest-gain symbols from the patch notes. This is
only a search for those specific symbols, not an API compatibility certificate.
The existing narrow CMF title/container and Vanilla on-action presence checks
still pass; they do not cover the changed interfaces above.

## Proposed implementation order

1. **Freeze the source inputs.** Preserve this working-tree baseline and capture
   the exact 1.15 files/manifests needed for the port before another Steam update.
   Resolve missing old bytes only where necessary. Keep unrelated work intact.
   **Gate:** reproducible input hashes and a complete affected-surface list.
2. **Choose and prepare CMF's compatible baseline.** Recheck release/main/branch/PR
   status at execution time. Port journal UI, outcomes and politics, and decide
   territorial-hook ownership. Extend patch packaging only as required.
   **Gate:** immutable base, explicit patch delta, verified staging tree and safe
   repeated installation/rollback; SB's dependent replacements reviewed separately.
3. **Restore current world and map data.** Rebase global state history/formations,
   regional history/resources, raster, terrain, locators and splines. Rebuild the
   naval validation contract using the Vanilla control. **Gate:** no removed state
   links; native regions outside SB's intended delta retained; coherent map assets.
4. **Migrate all JE contracts.** Use the 27-row inventory, including hidden and
   persistent entries; port four custom bar styles and preserve CMF wiring.
   Add the missing CMF group illustrations without changing group visibility.
   **Gate:** equivalent triggers/effects/cleanup and valid new outcome presentation;
   no duplicate application for shared outcomes or delayed acknowledgements.
5. **Port remaining gameplay overlays.** Work through the keyed review queue and
   AI callers, custom DNA and the digest's CMF trigger parameter differences,
   then scoped localisation requirements, including quote escaping. Recheck recent Zulu succession,
   recruitment, handoff and Basotho relief work against 1.15 native behaviour.
   **Gate:** explicit dispositions for every drift, preserving authored policy.
6. **Update validation and release bookkeeping last.** Add the actual target/build/
   manifest, dependency identity, reviewed hashes and new schema expectations to
   the checker/tests. Keep historical reports historical; replace stale current
   assertions rather than weakening them. Align README, supported-version fields
   and override manifest. Apply the repository's version policy before a commit.
   **Gate:** appropriate static suite, dependency integrity and target-specific
   evidence, with known tool/schema limits recorded.
7. **DP performs fresh-start verification.** Use the matrix below before claiming
   compatibility. An upstream release or hotfix arriving mid-port requires another
   targeted comparison rather than silently moving the target.

## Verification and remaining limits

Completed here:

- Verified installed launcher/Steam identity and decoded the current core manifest.
- Verified **146 explicitly listed audited core files** against manifest sizes and
  SHA-1s; [payload evidence](evidence/1_15_0_pre_rebase_2026_11_05/current_payload_verification.json)
  also records SHA-256s. This is not a full 20 GB installation/DLC verification.
- Compared every registered exact-path/keyed override, both AI contracts and all
  16 historical CMF contracts; checked additional plain-key/GUI/dependency surfaces.
- Confirmed the installed CMF tree still matches `sb-1.14.3-r1` and checked public
  upstream release, main, branches and open PRs without installing anything.
- Ran the [existing override checker](evidence/1_15_0_pre_rebase_2026_11_05/existing_override_checker.txt).
  It correctly fails against the new build with 223 diagnostic lines, including
  old target pins and repeated containing-file drift. That is not 223 independent
  gameplay defects. No pins were refreshed to silence it.
- Parsed the new naval graph and ran the unmodified-Vanilla negative control.

The full validator and Tiger scan were not run. The available Tiger binary reports
`1.19.0`; its 1.15 schema coverage has not been established. Existing launch logs
identify **1.14.5**, so they are not evidence for this target. Earlier native binary
investigations, source tests and playtests retain their original version limits.

| DP engine scenario after implementation | Required observation | Status |
| --- | --- | --- |
| Fresh campaign with all DLC and exact CMF/SB installation | Startup, new world states/Poland, SB countries and population setup; clean relevant logs | Pending |
| Journal panel and representative persistent/completing JEs | Activation, buttons, headers, bars, timeout, invalidation, concluded page and long text | Pending |
| Bechuanaland shared JE, both political outcomes | Participant perspectives, correct winner, single settlement, late replies and cleanup | Pending |
| Cape/Trek/Natal/Chiefdom chains | Gates, pulses and event delivery preserved through migrated outcomes | Pending |
| Conquest, annexation and recovery | Swazi restriction, British–Zulu pre-annex handoff, timer enforcement, reversal and peace receipts | Pending |
| Zulu succession and constitutional conflicts; Basotho relief | Current court actors, recruitment/territory promises, both winners, economic viability and cleanup | Pending |
| Land/sea deployment through Cape, Natal, Lourenço Marques and split regions | Accepted map/splines, reachable ports, actual movement, trade/market access | Pending |
| Non-SB control countries and later politics | Native Russia content, parties, socialist/communist character rules, laws and decree branches retained | Pending |
| Copper and diamond economies | Intended capacities, discoveries, inherited production methods and market behaviour | Pending |

The initial scan added this report and its evidence directory; its
[audit scope and input identities](evidence/1_15_0_pre_rebase_2026_11_05/audit_scope.json)
remain historical. The [digest follow-up](1_15_0_modding_digest_review_2026_11_05.md#verification-and-handoff)
adds the pinned reference, further notes and a digest-reading route. Game scripts,
localisation, versions, live inventories and the CMF installation remain
unchanged. Neither investigation claims engine success.
