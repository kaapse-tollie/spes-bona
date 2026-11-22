# Zulu glossary pilot — main review and Vanilla comparison

7 November 2026. Research and presentation review, recorded before implementation.

DP subsequently authorised the accepted pilot. See the
[implementation record](../compatibility/1_15_0_zulu_glossary_pilot_2026_11_07.md)
for the source changes, static checks and pending engine inspection. The review
below preserves the evidence and limits at the research checkpoint.

## Review disposition

**Main-agent review complete: the four revised definitions are accepted as
source-grounded proposals for a bounded pilot.** The agent's
[research brief](zulu_glossary_pilot_2026_11_07.md) contains period limits,
drafts, exact keys and nine references. This accepts research quality and the
proposed source context; it does not mark the prose REVIEWED or certify rendering.

| Entry | Preferred first link | Main-review boundary |
| --- | --- | --- |
| Amabutho | `sb_institutional_reach_breakdown`, existing **Amabutho**, in [institution prose](../../localization/english/sb_institutions_l_english.yml) | Explain the historical institution without replacing the army law's game rules; preserve its broader social scope. |
| amaKhosi | First **amaKhosi** in `sb_court_movements_breakdown`, [institution prose](../../localization/english/sb_institutions_l_english.yml) | Link the word's meaning while retaining the surrounding explanation of SB's particular movement. Do not make “Great Chiefs” the literal glossary translation. |
| uSuthu | Existing **uSuthu** in `sb_court_succession.007.d.usuthu`, [succession prose](../../localization/english/sb_court_succession_l_english.yml) | Named Cetshwayo–Mbuyazi context is appropriate. No link from the timeless generic movement caption; its universal period/context application remains unvalidated. Do not change the existing date gate here. |
| Umkhosi | Existing **first fruits** in `sb_zulu_court.200.d`, [court prose](../../localization/english/sb_zulu_court_l_english.yml) | Define the royal first-fruits sense; preserve the separately selected chiefly branch and dynamic title. |

**Corrections requested and incorporated:** acknowledge uSuthu's broader later
royal-house/adherent sense without projecting it automatically into every 1836
royalist context; retain Cetshwayo's continuing cause in the draft, as well as
Dinuzulu's; describe capitalisation as a choice to preserve SB display; remove
wording that could imply DP approval; and separate source checks before an
implementation from rendering checks afterwards. The revised draft and all four
placement classifications were reread. No gameplay or localisation was changed.

A historical glossary entry can be available in the encyclopaedia before its
subject appears in a campaign. The limitation concerns what a particular live
actor or event link denotes, not a new date lock on dictionary access. Whether to
rename the general royal movement is a separate design decision. The current
“Great Chiefs” label can remain a game label without becoming the word's literal
translation. Neither naming issue requires silently expanding this pilot.

## Vanilla comparison

Installed Vanilla 1.15.0 defines **20 glossary entries** in
[00_glossary.txt](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/glossary/00_glossary.txt>).
None is an entry for these four terms. No glossary directory was found in the
installed CMF tree; its two game-concept files also contain none of the four.
SB's existing Thirteen Chiefdoms game concept serves a different purpose.

| Native example | Observed approach | Application to the pilot |
| --- | --- | --- |
| [Zemstvo](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/glossary_l_english.yml:31>) | Defines an institution directly, then explains its composition and functions. | Explain what an institution is before its significance; keep SB's laws and numerical effects in their existing game descriptions. |
| [Uchikowashi](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/glossary_l_english.yml:16>) | Definition followed by a short paragraph distinguishing related behaviour. | A concise distinction can prevent a misleading translation, such as equating every ibutho with a permanent male army. |
| [Decembrist Revolt](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/glossary_l_english.yml:28>) | Names the actors and dates the historical referent. | Give uSuthu its particular historical actors and context; do not define a generic loyalist ideology under that name. |
| [Zaibatsu](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/glossary_l_english.yml:19>) | Definition, origins and examples occupy separate paragraphs. | Include only the context needed to interpret the term; a compact pilot need not become a general history survey. |
| [Gongen](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/glossary_l_english.yml:22>) | One short defining sentence suffices. | There is no required paragraph count or minimum length. |

The five sampled descriptions range from about **19 to 76 words** after formatting
removal. This is a sample, not a rule for every native glossary. They use factual
reference prose and highlight the defined term; they do not imitate event-window
dialogue. Preserve British English in SB even where native spelling differs.

**Prose alignment applied, 7 November, at DP's request.** The four drafts in the
brief now follow those native structures more closely:

| Draft | Native model | Applied change |
| --- | --- | --- |
| Amabutho | Zaibatsu / Zemstvo | Define the term and singular form first; give the nineteenth-century organisation and service context in a separate paragraph. Retain women's participation. |
| amaKhosi | Gongen | Give the meaning directly in one short paragraph; retain the singular without adding a constitutional programme. |
| uSuthu | Decembrist Revolt | Identify the historical following and named actors first, then its succession and continuing royal context. Add no unsupported onset date. |
| Umkhosi | Uchikowashi / Gongen | Lead with the ceremony's meaning and explicit historical setting, followed by its purpose. Retain past tense and the period limit. |

Bold italic marks the defined term, as in native entries; the uSuthu draft also
highlights its named actors. The Markdown previews convey that emphasis without
installing localisation markup. Lexical meanings use the present tense;
historically bounded accounts retain the past. These are prose revisions only:
the source bases, period caveats, preferred links, review classifications and
implementation limits remain unchanged.

Native examples demonstrate both direct `[glossary_key]` references and custom
display labels. The [zemstvo reform button description](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/ip5_02_l_english.yml:151>)
uses the plural `zemstvos`; the [Decembrist JE reference](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/ip5_02_l_english.yml:181>)
uses an adjectival label. The [uchikowashi event tooltip](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/ep2_02_l_english.yml:67>)
links a lowercase term within explanatory prose. Apply that pattern to a few
useful body-text occurrences, preserving their displayed wording. These examples
do not establish that nested glossary markup is safe in every movement caption,
modifier name or dynamically assembled event title.

The [native glossary schema](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/glossary/glossary.md>)
requires a `glossary_` key and its title/description localisation; icons are
optional. Plain definitions fit this non-biographical pilot. No CMF widget or
custom interface is indicated. The schema describes Learn More URLs as registered
in code; a custom source URL on that button is not a demonstrated script feature.
Historical sources belong in the research record unless a supported in-game
route is separately established.

## SB scope and placement checks

- Current [institutional eligibility](../../common/scripted_triggers/sb_institutions_triggers.txt)
  is Zulu-lineage/profile gated. The [dynasty trigger](../../common/scripted_triggers/sb_firearms_triggers.txt)
  covers ZUL and qualifying NGN inheritance; explicit inherited Zulu profiles
  also cover countries carrying that persisted profile. Generic filenames are not evidence that
  unrelated cultures currently receive this prose. Recheck any later expansion.
- The [military modifier](../../common/scripted_effects/sb_institutions_effects.txt)
  additionally requires the Amabutho law. Prefer an explanatory body occurrence,
  such as `sb_institutional_reach_breakdown`, over hyperlinking the modifier name
  without a rendering check.
- [Succession event .007](../../events/sb_court_succession_events.txt) selects
  `.d.usuthu` for a Mbuyazi heir from 1852; its saved opposing brother is
  Cetshwayo. That gives a relevant named-actor context. The script's 1852 threshold
  is not historical proof of the term's first use and has not been changed.
- [Court event .200](../../events/sb_zulu_court_events.txt) uses its first-fruits
  description for the royal branch, with a separate chiefly description.
  Linking the existing phrase `first fruits` is a better initial experiment than
  adding markup to the dynamically selected `Umkhosi` title. Preserve the chiefly
  branch and event logic.

The validator classifies the general institution, movement and gathering keys as
non-event/JE prose, already in the [general review queue](../localisation_review_queue.md).
Event `.200` and succession `.007` remain **TO REVIEW**. A general key rendered
inside an event does not inherit that event's marker. New glossary title and
description keys would also need plain non-event/JE review tracking and queue
rows. No review markers or baselines were changed here.

## Main-agent evidence checks

The main agent independently inspected all four DSAE entries online and the
agent's lawfully downloaded full-text sources: the archaeological manuscript's
pp.2–5; Mgidhlana's recorded testimony on printed pp.105–106; the edited
Mgqibelo/Nguna note on p.121n9; Snedegar's S32–S34; and Rautenbach's p.64n4 and
p.75n84. These support qualified historical meanings, not unlimited temporal
or political labels. The UCT Press metadata was checked separately, including
its book DOI and distinction between print, PDF and repository dates.

The main browser's direct PDF retrieval returned an access error or timeout for
those sources; locally retained lawful copies supplied the inspected text.
No paywall or access control was bypassed. Page locators distinguish the accepted
archaeological manuscript's pages from journal pagination. Snedegar explicitly
labels part of his account a Zulu/Swazi composite; its ritual details must not all
be assigned to Zulu practice. The modern legal chapter is used for its explicit
interruption/revival caveat, not as a timeless description of the nineteenth century.

## Verification limits

This pass verifies sources, metadata where accessible, current source routing,
review classifications and local documentation links. It does not verify
rendered hover behaviour, line wrapping, nested title/caption markup or every
alternate-history context. Native examples establish an implementation pattern,
not observation of SB's future implementation. DP performs the relevant engine
inspection after an implementation exists. No gameplay, GUI, glossary
definitions, localisation text, markers, review baselines or version metadata
have changed in this research task. The source comparison, original-file hashes
and documentation checks are retained under
`generated/zulu_glossary_research_2026_11_07/`.
