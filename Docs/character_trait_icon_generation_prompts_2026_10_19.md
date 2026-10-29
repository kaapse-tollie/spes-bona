# Character trait icons — generation prompts, 19 October 2026

Status: DP approved generation. All eight cards have been generated with the built-in image_gen tool and saved in the [artwork folder](../output/imagegen/character_traits_2026_10_19/README.md). No runtime changes.

Historical prompt record: these are the exact first-pass prompts. DP subsequently requested greyscale, simpler imagery and several composition changes. Use the separate [revision 2 prompt pack](character_trait_icon_generation_prompts_2026_10_19_r2.md) for the next pass; the fenced prompts below remain unchanged.

Latest workflow: [revision 3](character_trait_icon_generation_prompts_2026_10_19_r3.md) uses fixed blank templates and generates only transparent foregrounds. It supersedes revision 2's full-card edit workflow.

## Reference policy

Only the unmodified **Vanilla character cards** listed below may supply the rendering style. Morgenröte and other example mods informed the earlier design discussion only. Do not attach the earlier mixed reference sheets, mod artwork, or automatically selected previous conversation images to generation.

These exports preserve the original 240 × 320 RGBA image content and alpha. Select the individual files named for each prompt:

- [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png)
- [imperious.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)
- [stalwart_defender.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/stalwart_defender.png)
- [pious.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)
- [mountain_commander.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/mountain_commander.png)

[Vanilla-only preview sheet](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/vanilla-style-reference-sheet.png) · [Original game paths](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/sources.json)

Museum and historical sources below inform the **written subject descriptions**, not the artistic style. No museum photographs are included in the generation input pack. Each prompt is complete and can be used independently with its specified Vanilla references.

## Cultural grounding and symbolic limits

The court set uses **Zulu/Nguni** staff and shield forms. Mountain King has its own **Basotho** subject. “Bantu” is not being used as an instruction to mix unrelated regional costumes or insignia.

- **Prestige staffs:** carved shafts and refined geometrical finials have a documented Zulu/Nguni context. The Met's example combines wood and metal-wire detail; its broad dating does not make it an exact 1836 model. The prompts simplify these material features rather than reproduce that particular object. [The Met, prestige staff](https://www.metmuseum.org/art/collection/search/314578).
- **Kings, chiefs and beadwork:** Sandra Klopper discusses long staffs carried by Zulu dignitaries and an 1836 depiction of Dingane with beadwork and a prestige staff. This supports the general vocabulary; the proposed wrist bands and the precise staff arrangements are artistic constructions. [Klopper, Staffs Associated with Kings and Chiefs](https://southafrica.co.za/staffs-associated-with-kings-chiefs.html).
- **Shield construction:** the British Museum's Zulu shield from circa 1879 has an oval ox-hide body, rows of slits and a wooden support. These are the physical features used here; its historical owner or regiment is not being assigned to a faction. The catalogue description was accessible through search, although direct page retrieval returned 403. [British Museum, Af,+.1431](https://www.britishmuseum.org/collection/object/E_Af-1431).
- **Mountain King:** Thaba Bosiu's flat sandstone plateau was Moshoeshoe's residence and stronghold. The foreground staff is a game-art metaphor for the ruler, not an authenticated personal possession. [South African History Online, Thaba Bosiu](https://sahistory.org.za/place/thaba-bosiu-lesotho).

The cards do not claim that a single staff historically meant uSuthu, a fan of three meant amaKhosi, or particular bead colours encoded allegiance. Those arrangements communicate SB's states. A prestige staff was not exclusive to a monarch; a head-ring is not being treated as a royal crown. Avoid using “tribal” or “African” as substitutes for the specific material descriptions.

## Shared visual decisions

- The Vanilla **frame, shading, depth and restraint** are the artistic target. All cards remain portrait 3:4 and use the same frame geometry.
- Constitutional cards use jade; personal allegiance uses aubergine; claimant and Mountain King use reddish copper. Colour indicates information type, not moral judgement or historical faction colour.
- Objects are dark, sculptural and simplified. Natural materials remain secondary to silhouette and legibility.
- Neutral states are intact, readable cards, with the same contrast as committed states.
- The staff is deployed differently across the set: one central upright; an equal three-part fan; a shallow diagonal offered on a palm; and an upright shaft held in a closed grip.
- One prompt produces one card. The subject names below identify files; no names or labels are rendered into the images.
- Generation is complete. The [selected-set review sheet](../output/imagegen/character_traits_2026_10_19/review_sheet_selected.png) compares 240 × 320 and 60 × 80 px previews; the original 1086 × 1448 RGBA files are retained unchanged. Fingers, the two neutral cards, and claimant versus claimant-supporter were inspected. DP's visual approval and in-game review remain pending.

## 1. uSuthu loyalist

Existing court trait: sb_court_alignment_royal_trait. Current display name: uSuthu Supporter.

Intended reading: One centre of royal authority; supporting the royal constitution does not identify a particular king.

Reference files: [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png), [imperious.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png).

```text
Create one Victoria 3 character-trait card, portrait 3:4, composed for a final 240 × 320 px game asset. Use ONLY the supplied unmodified Vanilla character cards as artistic-style references. Match their softly bevelled rectangular frame, double inset border with stepped corners, gently graded field, faint background ornament and dark, softly shaded sculptural symbol. Use restrained upper-left illumination, readable mid-tones and a compact shadow. The result should resemble a Vanilla icon with a new subject and palette, rather than a photograph, painted event scene or flat vector logo. Replace the reference subjects completely.

Input images: Image 1: direct.png — Vanilla style reference only; Image 2: imperious.png — Vanilla style reference only.

Subject and composition: One long, elegant nineteenth-century Zulu prestige staff stands upright in front of an elongated oval cowhide shield. Give the staff a slender, polished dark-hardwood shaft, a modest rounded geometric finial and two short, understated bands suggesting fine brass-wire binding. It is a dignitary's carved staff, not a European sceptre. The narrow shaft projects clearly above the shield and is the composition's strongest vertical line. The shield has a natural ivory-and-charcoal hide surface, two close vertical rows of short rawhide-lacing marks and a simple central support. Show a slight three-quarter turn so its curved hide construction reads. The staff rises to about four-fifths of the inner card height; the shield occupies the middle and lower field, leaving the finial isolated against pale negative space. Keep the hide pattern restrained and use no painted faction device. Convey one coherent centre of authority through the arrangement, not through a crown or invented royal insignia.

Palette: Muted jade field #79A397, deep green-grey frame #355B50, pale grey-green upper highlight #D7E8DE. The main symbol remains dark, with subdued natural-material hints; do not paint the symbol solid green.

Finish and constraints: Keep the motif within the inset frame, with clear negative space and a silhouette readable at roughly 60 × 80 px. Simplify fine carving, beads and hide texture rather than adding microscopic detail. The framed card is opaque; only the exterior beyond its rounded corners is transparent. No text, letters, numerals, rank stars, crowns, coats of arms, modern flags or additional objects. Do not copy the original references' objects or background colours. Do not use artwork or style from any mod.
```

## 2. amaKhosi partisan

Existing court trait: sb_court_alignment_chiefly_trait. Current display name: amaKhosi Supporter.

Intended reading: Several chiefs of comparable standing; a broad composition rather than one dominant royal vertical.

Reference files: [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png), [imperious.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png).

```text
Create one Victoria 3 character-trait card, portrait 3:4, composed for a final 240 × 320 px game asset. Use ONLY the supplied unmodified Vanilla character cards as artistic-style references. Match their softly bevelled rectangular frame, double inset border with stepped corners, gently graded field, faint background ornament and dark, softly shaded sculptural symbol. Use restrained upper-left illumination, readable mid-tones and a compact shadow. The result should resemble a Vanilla icon with a new subject and palette, rather than a photograph, painted event scene or flat vector logo. Replace the reference subjects completely.

Input images: Image 1: direct.png — Vanilla style reference only; Image 2: imperious.png — Vanilla style reference only.

Subject and composition: Three nineteenth-century Zulu chiefly prestige staffs form a compact, open fan. Their upper ends are equally prominent and reach the same visual level; none is taller, brighter or larger than the others. Separate the shafts clearly. Use polished dark hardwood and modest geometric finials: one rounded knob, one shallow faceted oval and one slightly flattened rounded head. Include only a small suggestion of incised collars or fine wire binding. These are related variations within a local carving tradition, not three fantasy weapons. The shafts converge loosely near the bottom without being tied into a bundle. The fan fills roughly two-thirds of the inner card width and three-quarters of its height. Keep the three finials distinct at thumbnail size, with pale gaps between them. There is no throne, crown, military spearhead or fourth central object. The equal, distributed arrangement is the symbolic indication of chiefly government.

Palette: Muted jade field #79A397, deep green-grey frame #355B50, pale grey-green upper highlight #D7E8DE. The main symbol remains dark, with subdued natural-material hints; do not paint the symbol solid green.

Finish and constraints: Keep the motif within the inset frame, with clear negative space and a silhouette readable at roughly 60 × 80 px. Simplify fine carving, beads and hide texture rather than adding microscopic detail. The framed card is opaque; only the exterior beyond its rounded corners is transparent. No text, letters, numerals, rank stars, crowns, coats of arms, modern flags or additional objects. Do not copy the original references' objects or background colours. Do not use artwork or style from any mod.
```

## 3. Constitutionally unaligned

Existing court trait: sb_court_alignment_neutral_trait.

Intended reading: A complete local political identity without either faction's staff arrangement; not a disabled or broken asset.

Reference files: [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png), [stalwart_defender.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/stalwart_defender.png).

```text
Create one Victoria 3 character-trait card, portrait 3:4, composed for a final 240 × 320 px game asset. Use ONLY the supplied unmodified Vanilla character cards as artistic-style references. Match their softly bevelled rectangular frame, double inset border with stepped corners, gently graded field, faint background ornament and dark, softly shaded sculptural symbol. Use restrained upper-left illumination, readable mid-tones and a compact shadow. The result should resemble a Vanilla icon with a new subject and palette, rather than a photograph, painted event scene or flat vector logo. Replace the reference subjects completely.

Input images: Image 1: direct.png — Vanilla style reference only; Image 2: stalwart_defender.png — Vanilla style reference only.

Subject and composition: A single, undecorated nineteenth-century Zulu cowhide shield is the entire central motif. Use a tall, gently tapered oval outline with rounded ends, a slightly convex hide surface, two close vertical rows of small rawhide-lacing marks and a straight wooden stiffener just visible beyond the top and bottom. Turn it very slightly to show thickness and construction while keeping the silhouette clear. Its face has a quiet, natural charcoal-and-pale-hide variation; it carries no painted emblem, heraldic division, geometric faction marking or extra staff. The shield fills about two-thirds of the inner card width and three-quarters of its height. Keep it intact and well lit, with a confident dark outline and visible volume. Neutrality must read as an intentional, legible state rather than a faded, damaged or greyed-out card. Retain the Zulu hide-shield form; do not copy the European shield shape from the Vanilla rendering reference.

Palette: Muted jade field #79A397, deep green-grey frame #355B50, pale grey-green upper highlight #D7E8DE. The main symbol remains dark, with subdued natural-material hints; do not paint the symbol solid green.

Finish and constraints: Keep the motif within the inset frame, with clear negative space and a silhouette readable at roughly 60 × 80 px. Simplify fine carving, beads and hide texture rather than adding microscopic detail. The framed card is opaque; only the exterior beyond its rounded corners is transparent. No text, letters, numerals, rank stars, crowns, coats of arms, modern flags or additional objects. Do not copy the original references' objects or background colours. Do not use artwork or style from any mod.
```

## 4. Supports the incumbent

Existing court trait: sb_court_endorsement_incumbent_trait.

Intended reading: A personal pledge of co-operation that works for a monarch or a head chief.

Reference files: [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png), [pious.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png).

```text
Create one Victoria 3 character-trait card, portrait 3:4, composed for a final 240 × 320 px game asset. Use ONLY the supplied unmodified Vanilla character cards as artistic-style references. Match their softly bevelled rectangular frame, double inset border with stepped corners, gently graded field, faint background ornament and dark, softly shaded sculptural symbol. Use restrained upper-left illumination, readable mid-tones and a compact shadow. The result should resemble a Vanilla icon with a new subject and palette, rather than a photograph, painted event scene or flat vector logo. Replace the reference subjects completely.

Input images: Image 1: direct.png — Vanilla style reference only; Image 2: pious.png — Vanilla style reference only.

Subject and composition: Two adult hands with dark-brown skin meet in a firm, calm clasp at the centre of the card, with short bare forearms entering from the lower left and lower right. Render the hands with the simplified dark sculptural modelling of Vanilla's hand icons, with enough soft highlight to separate fingers and palms. On one wrist show a narrow band of small, plain cream and charcoal glass beads; the other wrist is bare. Treat this restrained detail as local nineteenth-century Zulu material context, not a colour-coded political message. Let the joined hands form one broad, stable horizontal silhouette in the middle and lower field. Keep the gesture dignified and balanced; neither participant dominates or kneels. There are exactly two hands, anatomically coherent, with no sleeves, gloves, cuffs, throne or regalia. Do not add the praying figure from the reference. This is a pact between people, usable under either royal or chiefly rule.

Palette: Muted aubergine field #A48AAE, deep plum-grey frame #55405E, pale lilac-grey upper highlight #E9DEED. Hands and objects remain dark charcoal and muted natural browns; do not paint them purple.

Finish and constraints: Keep the motif within the inset frame, with clear negative space and a silhouette readable at roughly 60 × 80 px. Simplify fine carving, beads and hide texture rather than adding microscopic detail. The framed card is opaque; only the exterior beyond its rounded corners is transparent. No text, letters, numerals, rank stars, crowns, coats of arms, modern flags or additional objects. Do not copy the original references' objects or background colours. Do not use artwork or style from any mod.
```

## 5. Supports a rival claimant

Existing court trait: sb_court_endorsement_claimant_trait.

Intended reading: Offering assistance to another person's claim; open supporting hand rather than a self-assertive grip.

Reference files: [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png), [imperious.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png).

```text
Create one Victoria 3 character-trait card, portrait 3:4, composed for a final 240 × 320 px game asset. Use ONLY the supplied unmodified Vanilla character cards as artistic-style references. Match their softly bevelled rectangular frame, double inset border with stepped corners, gently graded field, faint background ornament and dark, softly shaded sculptural symbol. Use restrained upper-left illumination, readable mid-tones and a compact shadow. The result should resemble a Vanilla icon with a new subject and palette, rather than a photograph, painted event scene or flat vector logo. Replace the reference subjects completely.

Input images: Image 1: direct.png — Vanilla style reference only; Image 2: imperious.png — Vanilla style reference only.

Subject and composition: An adult dark-brown hand and short bare forearm enter from the lower left, palm upwards, presenting a slender Zulu prestige staff towards the upper right. Rest the shaft across the open palm and lightly supporting fingers; do not show a closed fist claiming it. The staff forms a clear shallow diagonal across the inner card, with its rounded geometric finial fully visible in the upper-right area. Use polished dark hardwood with a restrained incised collar and one short band suggesting fine brass-wire binding. A narrow band of cream and charcoal glass beads encircles the visible wrist. Keep the hand and staff as the only objects and leave clear space around the finial. The gesture is an offer made to someone outside the composition; do not add a receiving hand or a second person. Its shallow diagonal and open palm must remain distinguishable from the vertical, firmly grasped staff on the Claimant card.

Palette: Muted aubergine field #A48AAE, deep plum-grey frame #55405E, pale lilac-grey upper highlight #E9DEED. Hands and objects remain dark charcoal and muted natural browns; do not paint them purple.

Finish and constraints: Keep the motif within the inset frame, with clear negative space and a silhouette readable at roughly 60 × 80 px. Simplify fine carving, beads and hide texture rather than adding microscopic detail. The framed card is opaque; only the exterior beyond its rounded corners is transparent. No text, letters, numerals, rank stars, crowns, coats of arms, modern flags or additional objects. Do not copy the original references' objects or background colours. Do not use artwork or style from any mod.
```

## 6. Personally uncommitted

Existing court trait: sb_court_endorsement_uncommitted_trait.

Intended reading: An allegiance not yet pledged; visually related to the offering hand but empty.

Reference files: [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png).

```text
Create one Victoria 3 character-trait card, portrait 3:4, composed for a final 240 × 320 px game asset. Use ONLY the supplied unmodified Vanilla character cards as artistic-style references. Match their softly bevelled rectangular frame, double inset border with stepped corners, gently graded field, faint background ornament and dark, softly shaded sculptural symbol. Use restrained upper-left illumination, readable mid-tones and a compact shadow. The result should resemble a Vanilla icon with a new subject and palette, rather than a photograph, painted event scene or flat vector logo. Replace the reference subjects completely.

Input images: Image 1: direct.png — Vanilla style reference only.

Subject and composition: One adult dark-brown hand is held open and empty at a gentle three-quarter angle, palm upwards and slightly towards the viewer. The short bare forearm rises from the lower centre of the card. Fingers are naturally relaxed with small, readable separations, not spread into a stop sign or raised for an oath. Add only a narrow wrist band of small cream and charcoal glass beads, matching the restrained material detail used on the other personal-allegiance cards. Model the hand in dark, softly highlighted Vanilla-style relief, preserving clear palm volume and an unbroken wrist. Centre the empty palm where the pledged or offered object would otherwise appear; the absence of a staff is intentional and should be immediately visible. Use one hand only, with no shield, weapon, coin, broken chain, injury, tattoo, sleeve or additional symbol. The pose conveys available but unpledged co-operation rather than fear or surrender.

Palette: Muted aubergine field #A48AAE, deep plum-grey frame #55405E, pale lilac-grey upper highlight #E9DEED. Hands and objects remain dark charcoal and muted natural browns; do not paint them purple.

Finish and constraints: Keep the motif within the inset frame, with clear negative space and a silhouette readable at roughly 60 × 80 px. Simplify fine carving, beads and hide texture rather than adding microscopic detail. The framed card is opaque; only the exterior beyond its rounded corners is transparent. No text, letters, numerals, rank stars, crowns, coats of arms, modern flags or additional objects. Do not copy the original references' objects or background colours. Do not use artwork or style from any mod.
```

## 7. Claimant

Proposed distinct card; no separate active-claimant trait currently exists. Artwork preparation does not implement it.

Intended reading: The person pressing the claim, distinct from someone offering support to them.

Reference files: [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png), [imperious.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png).

```text
Create one Victoria 3 character-trait card, portrait 3:4, composed for a final 240 × 320 px game asset. Use ONLY the supplied unmodified Vanilla character cards as artistic-style references. Match their softly bevelled rectangular frame, double inset border with stepped corners, gently graded field, faint background ornament and dark, softly shaded sculptural symbol. Use restrained upper-left illumination, readable mid-tones and a compact shadow. The result should resemble a Vanilla icon with a new subject and palette, rather than a photograph, painted event scene or flat vector logo. Replace the reference subjects completely.

Input images: Image 1: direct.png — Vanilla style reference only; Image 2: imperious.png — Vanilla style reference only.

Subject and composition: One adult dark-brown hand firmly grips the lower-middle shaft of a tall Zulu prestige staff, holding it upright with quiet confidence. The short bare forearm enters from the bottom edge. Show fingers wrapping coherently around the shaft and a visible thumb, with a narrow cream-and-charcoal glass-bead wrist band. Use a long polished dark-hardwood staff with an understated rounded geometric finial, a carved collar and small indications of fine brass-wire binding. Its shaft is nearly vertical, leaning only slightly, and the finial stands isolated high in the inner field. The hand sits in the lower third, allowing the uninterrupted rising shaft to dominate the composition. This is a personal claim to leadership: the hand possesses the staff rather than offering it on an open palm. Keep the gesture contained, without a threatening swing, clenched fist raised independently of the staff, crown, throne, second hand or named character portrait.

Palette: Reddish copper field #BD8964, dark burnt-umber frame #704A32, pale warm upper highlight #EEDCC5. Keep this visibly more terracotta than Vanilla's golden unique-character cards. The central subject remains dark and desaturated.

Finish and constraints: Keep the motif within the inset frame, with clear negative space and a silhouette readable at roughly 60 × 80 px. Simplify fine carving, beads and hide texture rather than adding microscopic detail. The framed card is opaque; only the exterior beyond its rounded corners is transparent. No text, letters, numerals, rank stars, crowns, coats of arms, modern flags or additional objects. Do not copy the original references' objects or background colours. Do not use artwork or style from any mod.
```

## 8. Mountain King

Existing SB trait: sb_moshoeshoe_lifeline. Basotho rather than Zulu subject.

Intended reading: Moshoeshoe's enduring mountain stronghold, conveyed through a specifically Basotho place.

Reference files: [direct.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png), [mountain_commander.png](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/mountain_commander.png).

```text
Create one Victoria 3 character-trait card, portrait 3:4, composed for a final 240 × 320 px game asset. Use ONLY the supplied unmodified Vanilla character cards as artistic-style references. Match their softly bevelled rectangular frame, double inset border with stepped corners, gently graded field, faint background ornament and dark, softly shaded sculptural symbol. Use restrained upper-left illumination, readable mid-tones and a compact shadow. The result should resemble a Vanilla icon with a new subject and palette, rather than a photograph, painted event scene or flat vector logo. Replace the reference subjects completely.

Input images: Image 1: direct.png — Vanilla style reference only; Image 2: mountain_commander.png — Vanilla style reference only.

Subject and composition: An isolated miniature relief of Thaba Bosiu, Moshoeshoe's Basotho stronghold, dominates the card. Give it a broad, almost level sandstone summit, a steep dark cliff band and lower sloping shoulders. Its silhouette is wide, grounded and compact, with a few large readable rock planes rather than detailed landscape painting. Add one modest, plain dark-wood walking staff standing in the near foreground, slightly off centre, much smaller than the plateau and without the elaborate Zulu finial used on the court cards. It is an artistic cue to enduring leadership, not a purported surviving personal relic of Moshoeshoe. Use charcoal and muted sandstone tones with restrained highlights on the plateau edge. The mountain fills most of the lower two-thirds of the frame; keep the upper field quiet. Preserve Thaba Bosiu's flat-topped character, without an alpine peak, snow, castle, crown, modern hat or copied commander-rank star. No sky, horizon, buildings, people or scenic background.

Palette: Reddish copper field #BD8964, dark burnt-umber frame #704A32, pale warm upper highlight #EEDCC5. Keep this visibly more terracotta than Vanilla's golden unique-character cards. The central subject remains dark and desaturated.

Finish and constraints: Keep the motif within the inset frame, with clear negative space and a silhouette readable at roughly 60 × 80 px. Simplify fine carving, beads and hide texture rather than adding microscopic detail. The framed card is opaque; only the exterior beyond its rounded corners is transparent. No text, letters, numerals, rank stars, crowns, coats of arms, modern flags or additional objects. Do not copy the original references' objects or background colours. Do not use artwork or style from any mod.
```

## Handoff

DP approved these prompts and requested generation. Eight initial built-in calls used the individual Vanilla PNGs listed above. A single amaKhosi refinement brought the centre staff down to the outer heads' level; the generated card was the edit target and unmodified Vanilla Direct remained the sole artistic-style reference. The [generation manifest](../output/imagegen/character_traits_2026_10_19/generation_manifest.json) preserves the exact prompts, inputs, selected filenames and source paths, including the refinement.

The selected artwork is ready for DP's visual review. DDS export and game integration have not been performed. The proposed Claimant card remains an artwork/design distinction until its runtime handling is separately implemented.

