# Character trait icon art brief — 19 October 2026

Status: DP approved the [eight refined cards](../output/imagegen/character_traits_foregrounds_2026_10_19/README.md), and all eight are integrated into the mod. They use the [revision 3 prompts](character_trait_icon_generation_prompts_2026_10_19_r3.md) and [deterministic gradient-map bases](../output/imagegen/character_card_templates_gradient_2026_10_19/README.md). The original frame, alpha and uncovered background pixels are preserved. All earlier artwork, transparent foregrounds and native PNG/DDS exports remain intact. DP's in-game rendering check remains pending.

Latest revision: at DP's request, **Mountain King now uses Vanilla's special gold frame and four corner stars**. The approved mountain foreground retains its original size and position. The [gold revision](../output/imagegen/mountain_king_special_2026_10_19/README.md) records its native sources and reproducible assembly; the earlier copper card remains available. The seven court cards are unchanged.

Foreground style references must be **exclusively Vanilla character cards**. DP explicitly selected Morgenröte's blank `0_base_icon_grey.dds` for the background templates. Those fixed bases supply placement context, not foreground rendering style. Generate transparent subjects and composite them onto the saved base; do not regenerate the card for each trait. The [original prompts](character_trait_icon_generation_prompts_2026_10_19.md) and [revision 2](character_trait_icon_generation_prompts_2026_10_19_r2.md) remain historical records. The seven court designs use Zulu/Nguni forms; Mountain King uses a specifically Basotho landscape.

## Inventory and meaning

SB now defines seven court-display traits and Mountain King, each using its approved custom card. The additional **Claimant** distinction displays an existing self-claim; it adds no political commitment or gameplay bonus.

The court has two independent axes:

- **Constitutional alignment:** royal, chiefly or unaligned.
- **Personal allegiance:** incumbent, a particular rival claimant or uncommitted.

A uSuthu supporter can oppose the current king. An amaKhosi supporter can co-operate with that king. Constitutional neutrality and personal non-commitment must therefore have distinct icons. Supporting the incumbent must also work when the incumbent is a head chief.

Being an active claimant is different from backing one. A character with rival endorsement whose recorded claimant is themselves now receives Claimant. Backing another character retains Supports a Rival Claimant. The existing allegiance refresh replaces these cards when the endorsement changes. Eligibility to be recognised as heir is not, by itself, an active rival claim.

## Recommended artwork list

These are symbolic compositions rather than documented faction insignia. The expanded prompt pack grounds the staff, shield and mountain forms in museum and historical sources, and distinguishes that evidence from the invented arrangement used to communicate a game state.

| Card | Current status | Broad composition | Colour family |
|---|---|---|---|
| **uSuthu loyalist** | Existing: `sb_court_alignment_royal_trait`; displayed as uSuthu Supporter | An empty royal seat with a Zulu prestige staff. Represent the royal institution without depicting a particular ruler. | Jade |
| **amaKhosi partisan** | Existing: `sb_court_alignment_chiefly_trait`; displayed as amaKhosi Supporter | Retain three equal chiefly knobkerries in a broad fan. Extend their shafts beneath the lower inner frame rather than cutting them off in empty space. | Jade |
| **Constitutionally unaligned** | Existing: `sb_court_alignment_neutral_trait` | Proposed replacement: one composed figure with two equally open, empty hands, weighing alternatives without choosing either. No shield or faction badge. | Jade |
| **Supports the incumbent** | Existing: `sb_court_endorsement_incumbent_trait` | One supporter kneels before the seated incumbent. Use a plain seat and no crown so it also represents a head chief. | Aubergine |
| **Supports a rival claimant** | Existing: `sb_court_endorsement_claimant_trait` | A supporter and claimant shake hands in the foreground; a smaller, subdued seated incumbent remains separate in the background. | Aubergine |
| **Personally uncommitted** | Existing: `sb_court_endorsement_uncommitted_trait` | One open, empty hand. No clasp and no staff: allegiance has not been pledged. | Aubergine |
| **Claimant** | Added: `sb_court_claimant_trait`; displays an existing self-claim | Retain one hand firmly grasping and raising the staff of office. A tall, assertive composition contrasts with the rival-supporter's handshake scene. | Copper |
| **Mountain King** | Existing: `sb_moshoeshoe_lifeline` | A broad, flat-topped mountain with a small upright staff in the foreground. The rock mass dominates, conveying an enduring ruler and mountain stronghold. | Vanilla special gold, including corner stars |

These are generic role cards. Dingane, Mpande, Cetshwayo and later claimants do not each need a separate allegiance icon: the character card and court text identify the person. An additional sovereign, recognised-heir, exile, coup leader or renounced-claim card is outside this batch unless a distinct visible trait is subsequently wanted.

## Art direction

**Agreed direction: transparent greyscale symbols and schematic figures matching Vanilla alone, composited onto fixed coloured frames.** Use broad shaded planes, restrained depth and very little surface texture. Desaturating realistic skin, wood or rock is insufficient. Each design should remain recognisable from its silhouette, with one principal object or gesture and limited supporting detail. The two allegiance scenes require particular checks at small size.

The inspected Vanilla set mostly uses blue for personality, grey for expertise, pink/red for adverse conditions, and gold for unique character traits. Morgenröte helped establish the usefulness of grouping traits by colour and silhouette. Its rendering, borders, palettes and artwork are not generation references.

Retained SB palettes:

| Family | Main field | Border/shadow | Pale highlight | Purpose |
|---|---|---|---|---|
| Jade | `#79A397` | `#355B50` | `#D7E8DE` | Constitutional alignment |
| Aubergine | `#A48AAE` | `#55405E` | `#E9DEED` | Personal allegiance |
| Copper | `#BD8964` | `#704A32` | `#EEDCC5` | Distinctive character roles |

Colours identify the kind of information, not whether a faction is good or bad. Keep the two neutral cards within their respective families. All figures, objects, clothing, beads and landscape use neutral charcoal-to-grey shading. Colour is confined to the card frame and field; do not tint the subjects with natural material colours or coloured reflected light.

Two alternatives considered:

| Direction | Strength | Limitation | Assessment |
|---|---|---|---|
| Detailed portraits or court-scene miniatures | Strong character and historical atmosphere | Faces may imply a specific person; realistic scene detail becomes unclear at trait size. More difficult to reuse through successions. | Avoid. The revised allegiance cards use abstract figures and simple gestures, as in Vanilla Compliant and Elder. |
| Flat heraldic faction badges | Very clear silhouettes; easy to distinguish | A uniform emblem set would depart from the shaded trait-card language and could appear to be authentic faction heraldry. | Useful silhouette discipline, but not the final rendering style. |
| Greyscale objects, gestures and schematic figures | Matches Vanilla; reusable across named characters; clear two-axis grouping | Allegiance still needs its written label, particularly claimant versus claimant supporter. | Selected direction; Vanilla alone supplies the rendering style. |

## Reference inspection and production constraints

Inspected local references:

- Installed Vanilla `game/gfx/interface/icons/character_trait_icons/`: 126 DDS files; 125 at 240 × 320 RGBA and one at 60 × 82.
- Morgenröte `gfx/interface/icons/character_trait_icons/`, including its source/background examples and existing older assets: 175 DDS files; 174 at 240 × 320 RGBA and one at 208 × 208.
- Gates of the Bosphorus: six inspected DDS trait cards, all 240 × 320 RGBA.
- Hail Columbia: five inspected DDS trait cards, all 240 × 320 RGBA.

Use **240 × 320, portrait 3:4** as the intended final card canvas, with transparency around the frame. Preserve a common border, inset and lighting direction across the finished set. No lettering, stars denoting skill ranks, or elaborate scene backgrounds are needed for these allegiance states. Check the designs together at their small in-game display size before converting and integrating any final assets.

**Current generation reference pack — exclusively Vanilla:**

- [Vanilla-only preview sheet](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/vanilla-style-reference-sheet.png)
- [Exact source paths and unmodified PNG exports](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/sources.json)
- [Additional Vanilla figure references for revision 2](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/inspection-sheet.png) and [source manifest](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/sources.json).

Use the individual PNG exports listed in that manifest for generation. The preview sheet is for human review. Historical sources inform the written object descriptions; museum photography is not a rendering-style input.

**Earlier mixed reference sheets — exploration history only; do not supply these to image generation:**

- [Compact reference strip](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/reference-strip.png)
- [Expanded reference sheet](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/existing-reference-sheet.png)
- [Exact reference paths and image metadata](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/existing-reference-sources.json)

Implementation inventory sources:

- `common/character_traits/sb_court_allegiance_traits.txt`
- `common/character_traits/sb_character_traits.txt`
- `localization/english/sb_court_politics_l_english.yml`
- `common/scripted_effects/sb_court_politics_effects.txt`
- `common/scripted_triggers/sb_court_politics_triggers.txt`

## Decision record

| Status | Decision |
|---|---|
| Agreed | Plan the icon set before using image generation. |
| Agreed | Use colours different from the existing Vanilla trait families. |
| Agreed | Use exclusively Vanilla cards as foreground artistic-style references. DP later explicitly selected Morgenröte's blank base for the frame/background templates. |
| Agreed | Give court icons recognisably Zulu/Nguni objects and materials; treat Mountain King separately as Basotho. |
| Initial source inspection | Six court traits and Mountain King existed; there was no separate active-claimant trait. |
| Provisional recommendation | Seven court designs, including an active-claimant distinction, plus Mountain King: eight designs total. |
| Provisional recommendation | Shaded symbol cards with jade, aubergine and copper families; compositions as listed above. |
| Developed | Eight complete generation prompts, with specified compositions, palettes, cultural details and Vanilla-only reference selections. |
| Completed | Eight cards generated with the built-in image_gen tool; copied unchanged into the workspace and inspected at full and preview sizes. One amaKhosi refinement equalised the staff-head height. |
| DP feedback | Keep the generated frames and palettes. Central imagery is too realistic and colourful: use simplified greyscale Vanilla treatment throughout. |
| DP feedback | Replace the ambiguous neutral shield; make uSuthu more recognisably royal; use kneeling and rival-handshake scenes; finish the chiefly shafts at the border or with a fade. |
| Proposed refinement | Royal seat plus staff; balanced empty-handed neutral figure; shafts extending beneath the border. Eight standalone revision 2 edit prompts preserve the first-pass artwork and exact original prompts. |
| DP direction | Save three blank coloured templates from `0_base_icon_grey.dds`. Generate subjects on transparent backgrounds and composite them with fixed bases to prevent background variation between traits. |
| Completed | Three blank bases generated and saved at 240 × 320 in PNG and lossless RGBA DDS, with hashes and original generated masters. Eight revision 3 prompts link their base and request transparent foregrounds only. |
| Verification boundary | PNG and DDS pixels match for each base. The generated bases are not pixel-exact recolourings of the source DDS; using the same saved base during composition preserves background identity within each family. |
| DP follow-up | Use a pixel-based gradient transformation of the original DDS; preserve all generated versions for comparison. |
| Completed | Three deterministic gradient-map bases preserve all 240 × 320 pixel coordinates and the complete original alpha channel. PNG/DDS pixels match, gradient stops are recorded, and the build is reproducible. A native-size comparison confirms outline differences in the earlier AI bases, which remain untouched. Foreground prompts now link the deterministic bases. |
| Completed | Eight revised transparent subjects generated with Vanilla-only foreground style references. Mechanical compositing onto the fixed bases preserves frame, exterior alpha and uncovered pixels exactly. Separate raw foregrounds, positioned layers, finished PNG/DDS cards, generation records and a review sheet are saved. |
| DP approval | "Looks really good, thanks integrate it into the the mod." The refined eight-card set is approved for installation. |
| Completed | Eight native DDS files copied byte-for-byte into `gfx/interface/icons/character_trait_icons/` and linked from the trait definitions. The Claimant display uses the existing rival endorsement and self-reference, without changing commitments, ideologies or bonuses. |
| Verified | All eight installed DDS files match their recorded source hashes and decode to the approved 240 × 320 RGBA PNGs. The 29 court tests pass, including self-claim/supporter/heir distinctions, exile, repeat refresh and changes of allegiance. |
| Validation limitation | Full validation reached 15/17 gates passed, warned or skipped. Both failed gates report existing reviewed-prose drift in Klip River `.060`/`.080` and Natal Crisis `.050`; those namespaces were not edited here. Unit discovery: 588 tests, one failure, eight skips. Tiger is advisory against the newer game version. |
| Pending DP | In-game rendering of all cards, trait tooltips and the Claimant/supporter distinction. No game launch was performed. |
| DP direction, implemented | Replace only Mountain King's copper base with Vanilla's special gold frame, including its distinct outline and corner stars. Preserve the approved foreground and all earlier versions. |
| Verified | Gold revision uses pixels from the installed special-card set, unchanged foreground size/position, native alpha and identical decoded PNG/DDS pixels. Runtime DDS matches the new manifest; rendering remains pending DP. |

The two new Claimant localisation keys are listed for DP prose review. Generation prompts remain historical records of the art stage; their earlier runtime-pending notes are superseded by this integration record.
