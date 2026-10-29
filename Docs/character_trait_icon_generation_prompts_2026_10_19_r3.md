# Character trait cards — transparent foreground prompts, revision 3

Status: all eight transparent foregrounds have been generated with the built-in image_gen tool and composited onto the [deterministic bases](../output/imagegen/character_card_templates_gradient_2026_10_19/README.md). The [finished PNG/DDS cards, original foregrounds and review sheet](../output/imagegen/character_traits_foregrounds_2026_10_19/README.md) are saved separately. Earlier artwork remains intact. This replaces revision 2's full-card editing workflow while preserving its subject designs; runtime integration remains pending.

## Fixed templates and assembly

| Family | Fixed PNG | Fixed DDS | Subjects |
|---|---|---|---|
| Jade | [0_base_icon_jade.png](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_jade.png) | [0_base_icon_jade.dds](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_jade.dds) | uSuthu, amaKhosi, constitutionally unaligned |
| Aubergine | [0_base_icon_aubergine.png](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_aubergine.png) | [0_base_icon_aubergine.dds](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_aubergine.dds) | Incumbent, rival claimant, personally uncommitted |
| Copper | [0_base_icon_copper.png](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_copper.png) | [0_base_icon_copper.dds](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_copper.dds) | Claimant, Mountain King |

These bases apply a deterministic luminance-to-colour gradient to the requested Morgenröte `0_base_icon_grey.dds`. They preserve its native 240 × 320 coordinates and complete alpha channel without resampling. The [template manifest](../output/imagegen/character_card_templates_gradient_2026_10_19/manifest.json) records the source hash, gradient stops and verification. The [earlier generated bases](../output/imagegen/character_card_templates_2026_10_19/README.md) remain available for comparison. Only the reference bases changed; the eight foreground designs and generation prompts are unchanged.

Generate **one foreground per call**, using the built-in tool with `transparent_background: true`. Attach each prompt's three local PNGs in the listed order; inspect local images before using them. Image 1 is placement context only. Images 2 and 3 are the exclusive artistic-style references. Do not attach the old full-colour trait art, mixed mod reference sheets or museum photographs.

The output must contain only greyscale subject pixels and any compact, partially transparent shadow. It must not contain a card, coloured field, ornamental linework or simulated checkerboard transparency. Compose on the same portrait 3:4 canvas, intended for 240 × 320, with subjects positioned inside Image 1's inner field. Using the template as a reference helps placement; it does not itself guarantee background identity.

**Assembly supplies that guarantee:** alpha-composite the subject onto the saved native PNG, preserving the base wherever foreground alpha is zero. Clip subject pixels to the interior where needed, so the original frame remains above the lower ends of staffs and forearms. Retain the base's exterior transparency. Compare assembled background/frame pixels against the saved base before DDS export. No NN generation is used for final assembly.

The earlier [cultural grounding](character_trait_icon_generation_prompts_2026_10_19_r2.md#cultural-and-compositional-choices) remains applicable: these are symbolic arrangements, not faction heraldry or reconstructed ceremonies. All materials and human figures are rendered in neutral greyscale regardless of their real-world colours.

## 1. uSuthu loyalist

Runtime trait: `sb_court_alignment_royal_trait`.

Inputs:

1. [Jade base — placement only](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_jade.png)
2. [Vanilla Imperious — style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)
3. [Vanilla Pious — style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)

```text
Create ONLY a greyscale foreground illustration on a genuinely transparent RGBA background, on a portrait 3:4 canvas intended for a 240 × 320 px Victoria 3 trait card. Image 1 is the fixed blank card for placement and scale only: do not reproduce or edit its frame, coloured field or ornament. Images 2 and 3, unmodified Vanilla cards, are the exclusive artistic-style references. The output will be composited onto Image 1 separately.

Subject: an EMPTY royal seat with a long Zulu prestige staff resting against one side. The dominant shape is a simple, broad nineteenth-century armchair with upright back, short arms and sturdy legs, viewed slightly from the front. Suggest a folded hide across the seat with one broad edge, without fur or animal pattern. The slender staff has a small rounded carved finial and rises just above the seat. Keep the objects together as one compact silhouette. No seated person: the symbol represents the royal institution rather than a particular sovereign. Do not reproduce Imperious's Gothic throne or crown-like finial. No shield, European crown, gilding or invented heraldry.

Render the seat, hide and staff entirely in neutral charcoal, mid-grey and pale-grey highlights. Match Vanilla's broad, softly shaded icon volumes, restrained depth and minimal surface detail. No brown wood, beige hide, gold metal, green reflected light, wood grain or photographic texture.

Place the motif within the inner field shown by Image 1, leaving clear surrounding space and a silhouette readable at 60 × 80 px. Any compact shadow must have transparent surroundings. Everything outside the subject and shadow must be alpha zero: no background rectangle, white matte, coloured glow, border, decorative linework, text or rank stars.
```

## 2. amaKhosi partisan

Runtime trait: `sb_court_alignment_chiefly_trait`.

Inputs:

1. [Jade base — placement only](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_jade.png)
2. [Vanilla Direct — style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png)
3. [Vanilla Imperious — style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)

```text
Create ONLY a greyscale foreground illustration on a genuinely transparent RGBA background, on a portrait 3:4 canvas intended for a 240 × 320 px Victoria 3 trait card. Image 1 is the fixed blank card for placement and scale only: do not reproduce or edit its frame, coloured field or ornament. Images 2 and 3, unmodified Vanilla cards, are the exclusive artistic-style references. The output will be composited onto Image 1 separately.

Subject: three Zulu chiefly knobkerries in a compact open fan. Give them related but slightly different rounded or simply faceted heads. All three heads are equal in prominence and reach the same upper visual level; the central staff must not be taller. Keep clear gaps between their heads and upper shafts, with understated collars and minimal carving.

Let the shafts converge loosely towards the bottom and continue down beyond the position of Image 1's lower inner border. Their lower ends will be hidden beneath the fixed frame during compositing. Do not terminate the three shafts abruptly together in the empty field. Do not draw the frame itself. No binding, fourth staff, spearhead or dominant royal object.

Render all three staffs entirely in greyscale: charcoal, mid-grey and pale-grey highlights, with broad smooth shading like Vanilla. No brown wood, gold bindings, green tint, wood grain, scratches or glossy realistic finish. Simplify their volumes rather than drawing a desaturated product photograph.

Keep the fan within the inner field's width and its three heads distinct at 60 × 80 px. Everything outside the staffs and their compact soft shadow must be alpha zero: no background rectangle, white matte, card, border, ornament, text or rank stars.
```

## 3. Constitutionally unaligned

Runtime trait: `sb_court_alignment_neutral_trait`.

Inputs:

1. [Jade base — placement only](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_jade.png)
2. [Vanilla Inexperienced — figure simplification only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/inexperienced.png)
3. [Vanilla Pious — figure modelling only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)

```text
Create ONLY a greyscale foreground illustration on a genuinely transparent RGBA background, on a portrait 3:4 canvas intended for a 240 × 320 px Victoria 3 trait card. Image 1 is the fixed blank card for placement and scale only: do not reproduce or edit its frame, coloured field or ornament. Images 2 and 3, unmodified Vanilla cards, are the exclusive artistic-style references. The output will be composited onto Image 1 separately.

Subject: one anonymous adult figure seen from the waist up, facing forwards with a level head and calm posture. Both forearms open gently outwards at the same height, elbows low and both empty palms upwards: a balanced weighing of two possibilities, choosing neither. Keep the shoulders relaxed, without a helpless shrug. Separate both hands clearly from the torso. Show a bare upper torso, a simple wrap at the waist and one understated bead band at the neck. Keep the figure schematic and dignified, without detailed features or a named historical identity. No staff, shield, throne, crown, faction badge, scales, question marks, book or tool.

Use neutral greyscale throughout, with smooth charcoal masses and a few broad grey highlights. No natural skin colour, pores, hair strands, individual bead colours or realistic fabric. Do not copy Inexperienced's European clothing or question marks, or Pious's praying pose.

Position the figure inside Image 1's inner field. Let the lower torso fade gradually to transparency, never to a painted background colour. Retain strong contrast so neutrality does not look like a disabled card. The balanced two-handed silhouette must read at 60 × 80 px. All surrounding pixels must be alpha zero: no coloured field, white matte, frame, ornament, text or additional objects.
```

## 4. Supports the incumbent

Runtime trait: `sb_court_endorsement_incumbent_trait`.

Inputs:

1. [Aubergine base — placement only](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_aubergine.png)
2. [Vanilla Compliant — figure hierarchy and simplification](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/compliant.png)
3. [Vanilla Pious — figure modelling](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)

```text
Create ONLY a greyscale foreground illustration on a genuinely transparent RGBA background, on a portrait 3:4 canvas intended for a 240 × 320 px Victoria 3 trait card. Image 1 is the fixed blank card for placement and scale only: do not reproduce or edit its frame, coloured field or ornament. Images 2 and 3, unmodified Vanilla cards, are the exclusive artistic-style references. The output will be composited onto Image 1 separately.

Subject: a compact symbolic scene of EXACTLY TWO anonymous adults. A supporter kneels on one knee in the foreground, turned towards the incumbent, head gently bowed and one hand against the chest. The incumbent sits upright on a simple broad seat behind and beside the supporter, holding a slender Zulu prestige staff vertically. Separate the silhouettes so the kneeling posture and seated figure remain distinct. The supporter is respectful, not crawling or prostrate. The incumbent looks towards the supporter without threatening or pointing down at them.

Use schematic nineteenth-century Zulu dress: simple wraps, bare forearms and minimal beadwork, without detailed faces. The plain seat has no crown, so the pledge can represent service to either king or head chief. No European regalia, weapons, chains, additional attendants or landscape.

Render all people, clothing, beads, seat and staff entirely in neutral greyscale. Match Vanilla's abstract silhouettes and broad soft modelling. No brown skin or wood, purple reflections, coloured clothing, detailed anatomy, fabric texture or theatrical lighting. This is an emblematic vignette, not a realistic historical scene.

Fit the scene inside Image 1's inner field with clear negative space and readability at 60 × 80 px. Everything outside the people, seat, staff and compact soft shadow must be alpha zero. No card, coloured background, white matte, floor rectangle, border, ornament, text or rank stars.
```

## 5. Supports a rival claimant

Runtime trait: `sb_court_endorsement_claimant_trait`.

Inputs:

1. [Aubergine base — placement only](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_aubergine.png)
2. [Vanilla Elder — figure separation](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/elder.png)
3. [Vanilla Compliant — simplified interaction](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/compliant.png)

```text
Create ONLY a greyscale foreground illustration on a genuinely transparent RGBA background, on a portrait 3:4 canvas intended for a 240 × 320 px Victoria 3 trait card. Image 1 is the fixed blank card for placement and scale only: do not reproduce or edit its frame, coloured field or ornament. Images 2 and 3, unmodified Vanilla cards, are the exclusive artistic-style references. The output will be composited onto Image 1 separately.

Subject: two anonymous adults in the foreground, seen approximately from the thighs upwards, facing one another and shaking hands. Their joined hands make a clear bridge between their separate torsos. One is the supporter; the other is the rival claimant, distinguished by a slender Zulu prestige staff held upright in the free hand. Keep the staff secondary to the handshake.

Behind them in the upper part of the composition, add a smaller, subdued silhouette of the CURRENT incumbent on a plain seat. Keep that incumbent clearly separate from the foreground pair. The image must read as an alliance with someone other than the existing ruler. Exactly two active foreground figures and one small background incumbent; no crowd or court surroundings. The background incumbent is still part of the transparent subject layer, not a painted background.

Use schematic Zulu wraps and restrained beadwork, no crowns or European regalia. All people, garments, staff and seat are neutral greyscale. Use charcoal foreground figures with broad grey highlights and a softer mid-grey incumbent. Match Vanilla's abstract modelling: no detailed faces, natural skin colour, fabric texture, modern suits, masks or weapon exchange.

Position the entire group inside Image 1's inner field. The foreground heads and joined arms must read at 60 × 80 px; the seated figure is secondary. All pixels outside these silhouettes and compact soft shadow must be alpha zero. No background panel, coloured field, white matte, card frame, ornament, text or rank stars.
```

## 6. Personally uncommitted

Runtime trait: `sb_court_endorsement_uncommitted_trait`.

Inputs:

1. [Aubergine base — placement only](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_aubergine.png)
2. [Vanilla Direct — hand modelling](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png)
3. [Vanilla Pious — smooth volumes](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)

```text
Create ONLY a greyscale foreground illustration on a genuinely transparent RGBA background, on a portrait 3:4 canvas intended for a 240 × 320 px Victoria 3 trait card. Image 1 is the fixed blank card for placement and scale only: do not reproduce or edit its frame, coloured field or ornament. Images 2 and 3, unmodified Vanilla cards, are the exclusive artistic-style references. The output will be composited onto Image 1 separately.

Subject: one large open, empty hand with palm facing upwards, relaxed fingers and a short forearm entering from below. Include a narrow, understated wrist band suggesting a few plain beads. The hand holds no staff, clasps no other hand and makes no pledge. Show a coherent thumb and four fingers, separated through simple volumes rather than detailed joints. Keep the broad open-hand silhouette dominant and centred in the inner field.

Render the hand and beads entirely in neutral greyscale: charcoal shadows, mid-grey body and a few soft pale-grey highlights. Use Vanilla's simplified sculptural modelling. No natural skin colour, cream beads, purple reflections, pores, veins, nail detail or fine creases. Avoid photographic anatomy even though the result is monochrome.

Fade the lower forearm softly to transparency, not to a coloured or white patch. Keep this single-hand design distinct from the two-handed neutral figure. It must remain readable at 60 × 80 px. All pixels outside the hand and its compact soft shadow must be alpha zero. No card, coloured field, white matte, border, ornament, text, rank stars or extra objects.
```

## 7. Claimant

Proposed artwork distinction only; no separate runtime trait is added by this prompt.

Inputs:

1. [Copper base — placement only](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_copper.png)
2. [Vanilla Direct — hand modelling](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png)
3. [Vanilla Imperious — symbolic volumes](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)

```text
Create ONLY a greyscale foreground illustration on a genuinely transparent RGBA background, on a portrait 3:4 canvas intended for a 240 × 320 px Victoria 3 trait card. Image 1 is the fixed blank card for placement and scale only: do not reproduce or edit its frame, coloured field or ornament. Images 2 and 3, unmodified Vanilla cards, are the exclusive artistic-style references. The output will be composited onto Image 1 separately.

Subject: one firm hand grasping and raising a long Zulu prestige staff in a tall, assertive composition. Place the hand in the lower half, the shaft rising nearly upright, with a rounded geometric finial clear against transparent space above. The fingers wrap coherently around the shaft and the thumb visibly closes the grip. Include only a restrained bead wrist band and simple collar details on the staff. This is a personal claim, not an offering gesture or handshake.

Let the forearm extend down to the position of Image 1's lower inner border. The fixed frame will hide its end during compositing; do not draw a border or end the arm abruptly in the middle of the field.

Render the hand, beads and staff entirely in neutral greyscale, with charcoal silhouettes, broad mid-grey planes and restrained pale-grey highlights. No brown skin or wood, cream beads, gold bands, copper reflections, wood grain, skin creases or photographic detail. Bindings, if visible, are simple grey bands.

Fit the motif within the inner field and preserve legibility at 60 × 80 px. Everything outside the subject and compact soft shadow must be alpha zero. No coloured background, white matte, card, frame, crown, ornament, text, rank stars or additional objects.
```

## 8. Mountain King

Runtime trait: `sb_moshoeshoe_lifeline`. Basotho subject.

Inputs:

1. [Copper base — placement only](../output/imagegen/character_card_templates_gradient_2026_10_19/0_base_icon_copper.png)
2. [Vanilla Mountain Commander — landscape simplification only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/mountain_commander.png)
3. [Vanilla Imperious — symbolic volumes](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)

```text
Create ONLY a greyscale foreground illustration on a genuinely transparent RGBA background, on a portrait 3:4 canvas intended for a 240 × 320 px Victoria 3 trait card. Image 1 is the fixed blank card for placement and scale only: do not reproduce or edit its frame, coloured field or ornament. Images 2 and 3, unmodified Vanilla cards, are the exclusive artistic-style references. The output will be composited onto Image 1 separately.

Subject: the broad, flat-topped Thaba Bosiu plateau, with steep sides and a small upright staff in the foreground. The wide summit and substantial rock mass dominate. Do not substitute Mountain Commander's pointed Alpine peaks. Keep the staff a small secondary indication of the ruler and mountain stronghold; it is not a spear, flagpole or monument.

Model the plateau as a few large, softly shaded charcoal and grey planes, with pale-grey upper ledges and dark recesses. Use the restrained symbolic depth of the Vanilla mountain icon. Remove natural sandstone colour, tiny erosion detail, granular texture, scree, grass and scenic atmospheric rendering. The entire mountain and staff must be neutral greyscale, without tan, brown, gold or copper light. No sky, clouds, sun, snow, castle, crown or rank star.

Position the isolated mountain relief within Image 1's inner field, with a broad silhouette readable at 60 × 80 px. The lower rocky edge can fade gently to transparency, never into a painted field. All pixels outside the mountain, staff and compact shadow must be alpha zero. No opaque landscape rectangle, coloured background, white matte, card border, ornament, text or extra objects.
```

## Acceptance checks

- Each output is a foreground with real alpha, not a full card or a subject on an opaque matte.
- All subject pixels are neutral greyscale; template colours do not tint the artwork.
- Vanilla's simpler volumes replace realistic material detail.
- Constitutional and personal neutrality remain distinct; royal seat, kneeling pledge and rival handshake read at thumbnail size.
- Chiefly staff heads are equally prominent. Shafts and forearms meet the lower inner frame naturally after compositing.
- The chosen base is reused unchanged. Frame, exterior alpha and background outside the foreground/shadow match its saved pixels exactly.
- Keep generated foregrounds and composited cards as separate assets, and preserve all earlier artwork and prompts. Runtime integration remains outside this generation step.
