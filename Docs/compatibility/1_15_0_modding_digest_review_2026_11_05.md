# Victoria 3 1.15.0 — digest reconciliation and planning decisions

**5 November 2026. Investigation only; no rebase implemented.** This supplements
the [conflict scan](1_15_0_pre_rebase_scan_2026_11_05.md). The digest adds work on
localisation escaping, CMF journal-group illustrations, SB's custom DNA and CMF
movement-trigger parameters. It confirms the JE migration and the narrower
four-bar styling port. It also contains summaries and generated records that
must not be applied mechanically.

**Implementation update:** DP authorised the [implementation plan](1_15_0_implementation_plan.md), including selective native once-only adoption in this rebase. Earlier pass-one deferral of that feature is superseded. See the [implementation report](1_15_0_implementation.md) for results.

**Pass-one decisions:** DP selected the latest CMF, now **1.67.1**, and
settled the rebase boundaries below. The [pass-one design](1_15_0_rebase_design_2026_11_05.md)
records the release check, map/copper policy, feature destinations and delegated
verification method. The [earlier 1.67.0 inspection](1_15_0_cmf_1_67_0_followup_2026_11_05.md)
remains evidence for the dependency port; its two trigger-call and seven ideology
findings are fixed in 1.67.1. The original findings below describe installed
1.66.0 plus its SB patch. No dependency installation or rebase has occurred.

## Read by question

- [Source identity and comparison limits](#source-identity-and-comparison-limits)
- [Additional required work](#additional-required-work)
- [Confirmed, already covered or inapplicable items](#confirmed-already-covered-or-inapplicable-items)
- [Corrections and evidence caveats](#corrections-and-evidence-caveats)
- [D1–D8 decisions and remaining gates](#decisions-to-settle-when-building-the-plan)
- [Pass-one detail and feature routing](1_15_0_rebase_design_2026_11_05.md)
- [Verification and handoff](#verification-and-handoff)

The [local reference index](../../../References/modding_digests.md) routes to
individual digest topics. The [audit inventory](evidence/1_15_0_modding_digest_2026_11_05/digest_audit.json)
contains file/key/line matches; search the named section instead of loading it
whole. Follow the [repository boundaries](../../AGENTS.md) and complete
[localisation policy](../policies/localisation-review.md), including DP's
pass-one clarification of syntax-only fixes and `TO REVIEW` prose.

## Source identity and comparison limits

A complete local snapshot is available under
[References/Modding-Digests](../../../References/Modding-Digests/), pinned to
[upstream commit `b4e1e105`](https://github.com/Victoria-3-Modding-Co-op/Modding-Digests/commit/b4e1e105a8003e4b9c11488b938931d6e89d4985).
All 687 exported files were checked against that commit's tree, then assigned
SHA-256s in the [snapshot manifest](../../../References/modding_digests_snapshot.json).
The local export is unmodified; corrections belong in these notes.

The [1.15 digest overview](../../../References/Modding-Digests/1.15.0/discord.md)
explicitly compares **1.13.11 → 1.15.0**, including 1.14 changes. Matching records
from its `1.14.5-openbeta` and `1.15.0` directories provide an additional
documentation comparison, not a complete old/new game-source comparison. The
missing old Steam manifest and source bytes remain missing. The
[file-change list](../../../References/Modding-Digests/1.15.0/changes_files.md)
excludes PNG, DDS and spline files, so it does not resolve the map rebase.

All **25 substantive type-documentation files** in `1.15.0/types/` match their
installed 1.15 counterparts byte-for-byte; the two `changes_*` indexes in that
directory were excluded. The generated GUI records require a separate caveat
below. The installed target remains build `26453692`, core manifest
`7727600027425614094`, as recorded by the original scan.

## Additional required work

### Localisation function arguments

The [escaping rule](../../../References/Modding-Digests/1.15.0/changes_breaking.md#required-quote-escaping)
requires `|q` on a `$key$` reference inside a quoted localisation-function
argument, for example `Concept('concept_pop', '$concept_pops|q$')`. This does
not mean escaping every localisation substitution indiscriminately.

The targeted scan found:

| Layer | Unescaped occurrences | Distinct lines | Files |
| --- | --- | --- | --- |
| SB English | 88 | 58 | 14 |
| Installed CMF, all bundled languages | 494 | 459 | 22 |
| CMF English subset | 41 | 38 | 2 |

Examples include SB's [contested-crown tooltip](../../localization/english/sb_contested_crown_l_english.yml)
and [dominion replacements](../../localization/english/replace/sb_dominion_l_english.yml).
The JSON's `quote_escaping` section preserves every matched expression and key.
These are direct syntactic candidates, not 582 independently observed engine
errors. The search excludes comment-only text and already escaped references;
it does not expand indirect macros or parse the full localisation language.

Plan a narrowly scoped SB escaping pass; upstream CMF supplies the inspected
dependency corrections. Classify each SB key under the exact review policy
before editing. DP's pass-one clarification permits minor necessary syntax-only
fixes in reviewed namespaces while preserving substantive wording, meaning, tone
and intended presentation. Preserve markers. New conclusion text is a separate
wording decision: `TO REVIEW` text may be revised within scope, while substantive
changes to reviewed text still need DP's replacement or approval.

### CMF journal-group illustrations

All **seven** definitions in
[CMF's journal-group file](../../../Community%20Mod%20Framework/common/journal_entry_groups/0_com_journal_entry_groups.txt)
lack `illustration`. The [digest](../../../References/Modding-Digests/1.15.0/changes_breaking.md#journal-entry-group-illustration)
and [installed group definitions](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/journal_entry_groups/00_journal_entries.txt>)
establish the new presentation contract. `themed` remains optional; do not
automatically promote hidden/helper groups into visible themed content.

SB defines no custom groups and its 27 JEs reference existing Vanilla groups.
The missing illustrations therefore belong in the dependency port. Existing
native artwork is a possible minimal solution; bespoke artwork is a scope
decision. Preserve each group's country/contextless identity.

### SB custom DNA

The single definition in [SB's DNA file](../../common/dna_data/sb_ngi_leaders.txt),
`dna_fodo_kanombewu`, lacks `gene_asian_east`. It is used by the
[Nguni character templates](../../common/character_templates/sb_nguni_chiefdoms_characters.txt).
The [digest's required gene](../../../References/Modding-Digests/1.15.0/changes_breaking.md#new-east-asian-gene)
and installed [gene definition](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/genes/01_genes_morph.txt>)
add a small schema migration to the character workstream. Preserve the authored
portrait, using the documented neutral values unless a deliberate visual change
is separately chosen. Loading and appearance still require DP's check.

### CMF movement-trigger parameters

The versioned `pop_type_percent_country` documentation changes its fields from
`pop_type`/`percent` to `target`/`value`. Installed
[ideological movements](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/political_movements/00_ideological_movements.txt>)
and [slave-revolt movements](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/political_movements/05_slave_revolt_movements.txt>)
use the new form, including typed targets such as `pop_type:slaves`.

CMF retains **four old-form calls**: one each in `movement_anti_slavery` and
`movement_land_reform`, and two in `movement_slave_revolt`, across
[ideological movements](../../../Community%20Mod%20Framework/common/political_movements/ycom_00_ideological_movements.txt)
and [slave-revolt movements](../../../Community%20Mod%20Framework/common/political_movements/ycom_05_slave_revolt_movements.txt).
None of those three definitions is replaced again by SB. No direct SB calls
were found. Add these to the CMF politics port, preserving comparisons and
thresholds. Source mismatch is established; whether the engine still tolerates
old aliases was not tested.

## Confirmed, already covered or inapplicable items

| Digest item | Disposition for this rebase |
| --- | --- |
| JE outcomes | Confirms migration of all 27 SB and five CMF definitions. Preserve the original per-JE inventory and shared-effect/cleanup requirements. |
| Bar styles | Confirms that `default`, `default_green` and `default_bad` survive. Keep the 11 corresponding SB bars; port the four `double_sided_bad` presentations. |
| Subject restoration | All eight SB subject definitions already contain `re_establish_war_goal`. Do not redo the 1.14 port merely because the digest lists it. |
| Ship AI, objective illustrations, mobilisation-group backgrounds | Neither SB nor installed CMF defines these types. No direct edits identified; do not create overrides solely to satisfy the checklist. |
| State renames, cold fields and new map content | Confirms the world/map workstream; does not establish an SB-authored delta or replace the failed naval check's Vanilla control. |
| Removed APIs and concepts | No non-comment matches for the digest's 26 removed symbols in the scanned SB/CMF runtime text. This includes the old JE completion/failure callbacks. A separate 1.14.5-doc comparison found removed `has_war_goal_at_risk_of_being_dropped`, also with no hits. These are bounded negative searches. |
| `create_ship`, `exile_character`, preferred-law iterators | Documentation adds optional ship graphics, optional regional-exile arguments and additional supported iterator scopes. Existing inspected uses do not require adopting those features. |
| `on_country_formed` | Generated expected scope changes from `none` to `country`; native source explicitly documents a country root. SB's Bechuanaland hook already uses country scope. Keep its formation/lifecycle replay; an annotation change alone does not prove an engine regression. |

The new [concluded-JE callback](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt>)
has a journal-entry root in native source despite a `none` scope in the generated
on-action summary. If used, trace native scopes and call sites; do not copy the
summary's scope into a test fixture. No existing SB/CMF old-callback migration
was identified by the symbol search.

## Corrections and evidence caveats

1. **Mirrors are not mandatory on every war goal.** The digest's brief statement
   is too broad. The matching installed [war-goal contract](../../../References/Modding-Digests/1.15.0/types/war_goal_types.md)
   makes `mirrored_wargoal` opt into timer enforcement and documents the
   negotiated/capitulation route without it. SB has nine mirrored goals and six
   deliberately unmirrored `assent_required` story/claim goals. Do not add mirrors
   or timer land transfers to those six. The three installed CMF goals already
   have mirrors; their upstream removal remains a separate ownership decision.
2. **The Chukotka summary disagrees with this target.** The digest lists
   `STATE_CHUKOTKA` as added. No definition exists in the installed region files,
   and the original scan found one remaining SB state link to it. Retain the
   unresolved link in the world-history workstream; determine the correct
   province/state mapping from the actual target instead of creating a state
   from the summary.
3. **Generated GUI data are insufficient for this port.** All **five**
   `data_types_*.txt` files are byte-identical between the repository's 1.14.5
   and 1.15 directories. They still list `JournalEntry.GetCompletionTooltip`
   but omit `JournalEntry.GetOutcomes`, which the installed
   [journal GUI](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/gui/journal_entry.gui>)
   actually calls. Therefore their zero-difference result cannot certify CMF's
   old panels or establish which old methods the engine removed. The effective
   UI still lacks the new outcomes/concluded-entry presentation and needs review.
4. **Generated descriptions need checking.** Many changed API rows only add a
   `Value Type` annotation. The `any_state_region_in_africa` records contain
   unrelated scripted-trigger text; no iterator regression is inferred from
   them. Duplicate event-target headings were excluded from the automated
   comparison and recorded, not silently collapsed into a compatibility claim.

These caveats still limit what the digest establishes. The separately verified
[CMF 1.67.1 release](1_15_0_rebase_design_2026_11_05.md#dependency-baseline)
supplies much of the dependency migration; the digest itself is not a complete
compatibility certificate. Recheck upstream before freezing the implementation
baseline.

## Decisions to settle when building the plan

**Pass one recorded on 5 November.** These are design decisions for the coming
plan, not an implemented rebase. Engineering evidence gaps remain explicit;
DP need not choose arbitrary answers to them. The [design detail](1_15_0_rebase_design_2026_11_05.md)
and [open work register](../audit_issues_open.md#victoria-3-115--rebase-and-secondary-extensions)
hold the supporting tradeoffs and follow-ups.

| ID | Status | Decision and remaining limits |
| --- | --- | --- |
| D1 — Dependency baseline | Agreed | Latest compatible CMF; currently verified 1.67.1. Pin the selected release for execution and derive the residual SB compatibility delta. Re-audit old contracts; never install the old patch wholesale. |
| D2 — Territorial hooks | Agreed through D1 | Retire superseded territorial overrides/no-op calls; preserve SB's Swazi restriction and British–Zulu handoff in the current native definitions. Full contract review remains necessary. |
| D3 — Map reconstruction | Policy agreed; evidence gate open | Start with 1.15 and carry only SB-authored changes relative to 1.14. Keep untouched native edits inside and outside SB's region. Recover/reconstruct the old delta; validate province/parent mapping and replace the unreliable naval check. |
| D4 — Copper allocation | Two-stage policy agreed | Use native copper and remove proven copper-as-lead proxies now; copper-focused resource audit afterwards (`RES115-01`). Northern Cape's eight proxy lead levels are confirmed; do not remove genuine lead or invent equivalent copper capacity. Namaqualand's ambiguous lead allowance remains provisional. |
| D5 — Journal presentation | Agreed | Make existing content work: outcomes, equivalent bars, CMF presentation and suitable conclusions. Register optional JE mechanics for the first post-rebase extension. |
| D6 — Reviewed localisation | Agreed | `TO REVIEW` prose may be revised within scope. Reviewed prose permits spelling/grammar and minor necessary syntax-only compatibility fixes preserving substance and intended presentation. Exact marker/namespace rules remain; substantive reviewed replacements still require DP. |
| D7 — New feature adoption | Destinations agreed; once-only amended into core port | Record every requested capability in the [feature routing](1_15_0_rebase_design_2026_11_05.md#feature-routing). Cold fields and selective once-only adoption belong in the core port; all other selected features retain secondary-extension or later thematic/release destinations. Preserve shared lifecycle state; no blanket flag removal. |
| D8 — Verification gate | Agreed by delegation | Use the [staged verification approach](1_15_0_rebase_design_2026_11_05.md#verification-decision): target-aware source checks and controlled map validation, then DP's fresh-campaign GUI/gameplay matrix. Retain missing historical inputs, stale GUI docs, unverified validator coverage and all unrun engine scenarios as explicit limits. |

Optional capabilities and their limits are described in the
[feature digest](../../../References/Modding-Digests/1.15.0/changes_features.md),
[button contract](../../../References/Modding-Digests/1.15.0/types/scripted_buttons.md)
and versioned [effects documentation](../../../References/Modding-Digests/1.15.0/docs/effects.log).
They are not prerequisites merely because they are newly available.

## Verification and handoff

The audit searched non-comment runtime text in `common`, `events`, `gui`,
`localization`, `map_data` and `gfx`, limited to `.txt`, `.gui`, `.yml`, `.asset`
and `.gfx`. Top-level definition checks and direct token matches establish the
listed source findings; they do not execute scopes, expand all macros, resolve
every load-order interaction or test native acceptance of old aliases. The
original scan's missing-baseline, Tiger-schema and runtime limits still apply.

Add these observations to DP's existing engine matrix after implementation:

- Affected SB and CMF localisation renders with correct concept links, apostrophes
  and nested quotations; no related format errors.
- CMF group headers and representative concluded/shared JEs display correctly;
  hidden helper groups stay hidden.
- Fodo's custom portrait loads and preserves its intended appearance.
- Anti-slavery, land-reform and slave-revolt eligibility/attraction retain their
  intended thresholds under the corrected dependency contracts.

The original digest follow-up added the upstream reference snapshot and
documentation/evidence, updated the conflict report and added the `UPSTREAM-05`
recording route. Its [verification record](evidence/1_15_0_modding_digest_2026_11_05/verification.json)
remains historical. The later [pass-one verification](evidence/1_15_0_design_pass1_2026_11_05/verification.json)
covers these decisions, the register and DP's narrow localisation-policy
clarification. No game launch, gameplay test, rebase implementation, dependency
installation or commit was performed in either documentation pass.
