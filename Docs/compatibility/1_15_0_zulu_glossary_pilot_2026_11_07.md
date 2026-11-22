# Zulu glossary pilot — implementation

**7 November 2026 · EXT115-02 · Implemented at DP's request; engine inspection pending**

Four historical glossary entries now explain Amabutho, amaKhosi, uSuthu and
Umkhosi at the accepted body-text locations. The same scope agent implemented
the definitions after the [sourced brief](../research/zulu_glossary_pilot_2026_11_07.md),
[main review and Vanilla prose comparison](../research/zulu_glossary_review_2026_11_07.md)
and DP's “Okay implement” instruction. The core rebase remains closed;
broader glossary coverage remains open under `EXT115-02`.

## Source changes

[Four empty glossary definitions](../../common/glossary/sb_zulu_glossary.txt)
use the native title/description convention and default presentation.
[Eight localisation keys](../../localization/english/sb_zulu_glossary_l_english.yml)
implement the accepted drafts with native bold italic term emphasis, italic
singular forms, bold named actors and paragraph breaks. No custom icons, URLs,
widgets or dictionary date gates are added.

| Entry | Linked source | Preserved context |
| --- | --- | --- |
| Amabutho | `sb_institutional_reach_breakdown` in [institutions](../../localization/english/sb_institutions_l_english.yml) | Existing institutional reform explanation and displayed word. |
| amaKhosi | First occurrence in `sb_court_movements_breakdown` in [institutions](../../localization/english/sb_institutions_l_english.yml) | Existing chiefly-movement explanation and formatting; later numeric readouts remain unlinked. |
| uSuthu | `sb_court_succession.007.d.usuthu` in [succession](../../localization/english/sb_court_succession_l_english.yml) | Cetshwayo–Mbuyazi branch and existing emphasis; no generic movement-caption link. |
| Umkhosi | Existing “first fruits” in `sb_zulu_court.200.d` in [court events](../../localization/english/sb_zulu_court_l_english.yml) | Royal gathering body; chiefly branch and dynamic title remain unchanged. |

The four links use literal `Glossary` arguments, following native custom-label
examples. Existing body text, movement labels and gameplay scripts are preserved.
All eight new keys use plain non-event/JE tracking and have exact rows in the
[review queue](../localisation_review_queue.md). Existing namespace markers and
review baselines retain their authority; implementation does not promote any
text to REVIEWED. The brief's historical limits and separate movement-naming
questions still apply.

## Verification

| Check | Result and limit |
| --- | --- |
| Definitions and prose | **PASS:** four unique empty native definitions, eight matching localisation keys, UTF-8 BOM and exact conversion of the accepted Markdown drafts. No matching key collision in Vanilla or CMF. |
| Four link edits | **PASS:** reversing only the four glossary wrappers restores all three existing localisation files byte for byte. Existing displayed words, emphasis, other branches and review classifications are unchanged. |
| Localisation gate | **PASS:** all eight new general keys tracked and queued once; event/JE coverage remains **107 reviewed, 195 to review**. Review baselines are unchanged. |
| Full validation | **15 PASS, 2 WARN, 0 FAIL**, with explicit installed Vanilla/CMF roots and `--tiger`. Includes unit tests, dependency integrity, inventories, map/naval and script contracts. |
| Local documentation links | **PASS:** 112 local links across the six touched documents, including file, line and anchor targets. The research record retains external-source evidence; those URLs were not fetched again in this implementation. |
| Scope audit | **PASS:** only the five implementation files and six documentation files differ from the captured working tree. All other captured files remain unchanged. |

The two existing full-suite warnings remain: deferred release gates `BC-20`,
`BC-22`, `CP-07`, `QUAL-09`, `SUP-05`; and Tiger 1.19.0's incomplete 1.15 schema.
Tiger was therefore not run as a target validator. The checks used Victoria 3
1.15.0 (build `26453692`, core manifest `7727600027425614094`) and the installed
CMF 1.67.2 + `sb-1.15.0-r2`; dependency pins and SB's release version are unchanged.

Before-file copies, hashes, the task-only patch and check output are retained in
`generated/zulu_glossary_implementation_2026_11_07/`. Key evidence files are
`source_verification.json`, `documentation_links.json`, `localisation.txt` and
`full_validation.txt`.

## DP in-game inspection

| Surface | Check |
| --- | --- |
| Institutional Reach explanation | Hover **Amabutho** and check its two paragraphs, emphasis and singular form. |
| Court movement breakdown | Hover the first **amaKhosi**; confirm the surrounding movement explanation and later readouts remain readable. |
| The Other Brother, `.007.d.usuthu` branch | Hover **uSuthu** in the actual Cetshwayo–Mbuyazi context; check named actors and existing bold text. |
| Royal gathering, `.200.d` branch | Hover **first fruits** and confirm it opens **Umkhosi**; inspect wrapping and the separate chiefly branch. |
| Encyclopaedia | Find all four entries, check titles and descriptions, and inspect nested tooltip access from the live surfaces above. |

Static checks cannot establish tooltip hit areas, wrapping, nested hover behaviour
or live context rendering. DP performs those checks; Victoria 3 was not launched
by the agents. No commit, release-version bump or performance claim is included.
