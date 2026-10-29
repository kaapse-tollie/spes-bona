# Character trait cards — refined prompts, revision 2

Status: prompt refinement following DP's review of the first generated set. **No images generated for this revision.** The selected first-pass files remain unchanged. The new compositions below are proposals for the next generation pass, not additional trait definitions.

Superseded workflow: DP subsequently requested fixed blank bases and transparent foregrounds. Use [revision 3](character_trait_icon_generation_prompts_2026_10_19_r3.md), which preserves these subject designs and links the saved templates. The full-card edit prompts below remain as history.

## What changes

Keep the approved card frames, coloured fields, proportions and family palettes. Rework the central artwork as **simplified greyscale symbols and figures**, taking the rendering language exclusively from Vanilla cards. Removing colour alone is insufficient: remove the realistic skin, wood, hide and rock textures too.

| Card | Revised central subject |
|---|---|
| uSuthu loyalist | An empty royal seat with a Zulu prestige staff resting against it. The institution is represented without identifying a particular king. |
| amaKhosi partisan | Retain the three equal knobkerries. Extend their shafts beneath the lower inner border; no floating, abruptly cut ends. |
| Constitutionally unaligned | One composed figure weighing two possibilities with equally open, empty hands. No shield or faction insignia. |
| Supports the incumbent | A supporter kneeling before the seated incumbent. |
| Supports a rival claimant | A foreground supporter and claimant shaking hands; a subdued seated incumbent behind them. |
| Personally uncommitted | Retain the single open, empty hand. |
| Claimant | Retain the hand firmly grasping the upright prestige staff. |
| Mountain King | Retain the broad Thaba Bosiu plateau and foreground staff, simplified into a greyscale relief. |

The neutral figure's balanced gesture is a visual metaphor for withholding a constitutional preference, not confusion or inability to decide. The single open hand remains the separate personal-allegiance symbol. Labels still carry the precise political meaning.

## Reference and edit policy

Each prompt is standalone. Attach its images in the listed order, **one card per generation call**:

1. The selected first-pass SB image is the **edit target only**. It supplies the approved frame, background and palette to preserve. Its realistic central artwork is explicitly rejected as a rendering reference.
2. All subsequent images are **unaltered Vanilla character cards**, supplying the sole artistic-style references. No example-mod artwork or museum photographs enter the generation inputs.

The existing card is a preservation target, not an exception to the Vanilla-only style rule. Do not substitute a review sheet or pull arbitrary recent conversation images into a call. Inspect each local edit target before editing.

The additional Vanilla references were exported from installed DDS files without changing their pixels. [Inspection sheet](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/inspection-sheet.png) · [Source paths and hashes](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/sources.json).

The families remain jade for constitutional alignment, aubergine for personal allegiance, and reddish copper for distinctive roles. Preserve the actual target colours; do not recolour the frame or desaturate the whole card.

## Cultural and compositional choices

Use the royal seat as the main uSuthu symbol: it reads more directly at trait size than an entire royal homestead. This is a stylised seat of office, not a claim that there was one standard historical “Zulu throne”. Dingane received an upholstered chair in 1836, and long prestige staffs were used by kings and chiefs. Those precedents support a restrained nineteenth-century seat-and-staff vocabulary without a European crown or invented pan-African regalia. [Sandra Klopper, Staffs Associated with Kings and Chiefs](https://southafrica.co.za/staffs-associated-with-kings-chiefs.html).

The new human figures use schematic local dress and poses, not portraits. The kneeling and handshake arrangements communicate SB's allegiance states; they are not reconstructions of documented ceremonies. Keep the seated incumbent uncrowned so the allegiance cards also work for a head chief. The constitutional card represents a royal institution through its title and seat; personal allegiance depicts a relationship between people.

Retain the earlier [subject-source notes](character_trait_icon_generation_prompts_2026_10_19.md#cultural-grounding-and-symbolic-limits) for Zulu/Nguni staffs and Basotho Thaba Bosiu. Historical objects inform silhouettes, not photographic surface detail.

## 1. uSuthu loyalist

Runtime trait: `sb_court_alignment_royal_trait`. The display name remains a separate localisation matter.

Inputs:

1. [Selected card — edit target](../output/imagegen/character_traits_2026_10_19/usuthu_loyalist_v1.png)
2. [Vanilla Imperious — style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)
3. [Vanilla Pious — style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)

```text
Edit Image 1 into one refined Victoria 3 character-trait card. Preserve its jade frame, inset border, coloured field, faint background ornament, framing and 3:4 proportions. Keep the card opaque and its exterior transparent. Image 1 is the edit target only; use Images 2 and 3, the unmodified Vanilla cards, as the exclusive rendering-style references.

Replace the shield-and-staff motif with an EMPTY royal seat and a long Zulu prestige staff resting against one side. Make the seat the dominant shape: a simple, broad nineteenth-century armchair with upright back, short arms and sturdy legs, viewed slightly from the front. Suggest a folded hide across the seat with one broad edge, without fur or animal pattern. The slender staff has a small rounded carved finial and rises a little above the seat. Keep both objects together as one compact symbol. No seated person: this represents royal government rather than allegiance to an individual. Do not reproduce the Gothic throne, crown-like finial or ornaments from Imperious. No shield, European crown, gilding, heraldry or invented ceremonial symbols.

Render ALL central objects and their shadows entirely in greyscale: neutral charcoal, mid-grey and pale-grey highlights. Even the seat, hide and staff are achromatic. Match Vanilla's simplified, softly shaded icon volumes: broad planes, restrained depth and minimal surface detail. No brown wood, beige hide, gold metal, green reflections, wood grain, photorealistic texture or miniature product-render finish.

Leave clear space around the motif. It must remain readable at 60 × 80 px and be suitable for a final 240 × 320 px asset. Retain the target's frame and background colours unchanged. No text, lettering, rank stars or extra scene elements.
```

## 2. amaKhosi partisan

Runtime trait: `sb_court_alignment_chiefly_trait`.

Inputs:

1. [Selected card — edit target](../output/imagegen/character_traits_2026_10_19/amakhosi_partisan_v2.png)
2. [Vanilla Direct — style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png)
3. [Vanilla Imperious — style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)

```text
Edit Image 1 into one refined Victoria 3 character-trait card. Preserve its jade frame, inset border, coloured field, faint background ornament, framing and 3:4 proportions. Keep the card opaque and its exterior transparent. Image 1 is the edit target only; use Images 2 and 3, the unmodified Vanilla cards, as the exclusive rendering-style references.

Retain the three Zulu chiefly knobkerries in their open fan, including their slightly different rounded or faceted heads. All three heads must remain equal in prominence and reach the same upper visual level: no taller central staff. Keep clear gaps between the upper shafts. Simplify the small collars and carving.

Correct the bottom: extend all three shafts down to and UNDER the lower inner frame, so that the frame naturally occludes their ends. Do not cut them off together in empty space above the border. Preserve the border itself and do not let the shafts protrude outside the card. No binding, fourth staff or dominant royal object.

Render every staff entirely in greyscale: neutral charcoal, mid-grey and pale-grey highlights, with broad, smooth shading like the Vanilla references. No natural brown wood, warm metal bindings, green tint, wood grain, fine scratches or glossy photorealistic finish. Simplify the volumes as game-icon artwork rather than merely desaturating realistic objects.

Retain the target's coloured frame and field unchanged. Keep the three separate heads legible at 60 × 80 px, suitable for a final 240 × 320 px asset. No text, lettering, rank stars or additional symbols.
```

## 3. Constitutionally unaligned

Runtime trait: `sb_court_alignment_neutral_trait`.

Inputs:

1. [Selected card — edit target](../output/imagegen/character_traits_2026_10_19/constitutionally_unaligned_v1.png)
2. [Vanilla Inexperienced — simplified figure style only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/inexperienced.png)
3. [Vanilla Pious — figure modelling only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)

```text
Edit Image 1 into one refined Victoria 3 character-trait card. Preserve its jade frame, inset border, coloured field, faint background ornament, framing and 3:4 proportions. Keep the card opaque and its exterior transparent. Image 1 is the edit target only; use Images 2 and 3, the unmodified Vanilla cards, as the exclusive rendering-style references.

Remove the shield completely. Replace it with one anonymous adult figure seen from the waist up, facing forwards with a level head and calm posture. Both forearms open gently outwards at the same height, elbows low, both empty palms facing upwards: a balanced weighing of two possibilities, with neither chosen. Keep the shoulders relaxed; this is deliberate neutrality, not a helpless shrug. The two hands must be separated clearly from the torso. Show a bare upper torso and a simple wrapped garment at the waist, with a single understated bead band at the neck. Keep the figure schematic and dignified, without detailed facial features or a named historical identity. No staff, shield, throne, crown, faction badge, scales, question marks, book or tool.

Render the entire figure, clothing and beads in neutral greyscale, using smooth charcoal masses and a few broad highlights. Match Vanilla's abstract figure treatment; no natural skin colour, pores, hair strands, individual bead colours or realistic fabric. Do not copy the European clothing or question marks from Inexperienced. Do not use the praying pose from Pious.

Let the lower torso fade softly into the field, as a Vanilla figure icon does. Preserve full readability and contrast rather than making the card look disabled. Keep the coloured frame and field unchanged. The balanced two-handed silhouette must read at 60 × 80 px, suitable for a final 240 × 320 px asset. No text or extra objects.
```

## 4. Supports the incumbent

Runtime trait: `sb_court_endorsement_incumbent_trait`.

Inputs:

1. [Selected card — edit target](../output/imagegen/character_traits_2026_10_19/supports_incumbent_v1.png)
2. [Vanilla Compliant — two-figure hierarchy and simplification](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/compliant.png)
3. [Vanilla Pious — greyscale figure modelling](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)

```text
Edit Image 1 into one refined Victoria 3 character-trait card. Preserve its aubergine frame, inset border, coloured field, faint background ornament, framing and 3:4 proportions. Keep the card opaque and its exterior transparent. Image 1 is the edit target only; use Images 2 and 3, the unmodified Vanilla cards, as the exclusive rendering-style references.

Replace the close-up clasped hands with a compact symbolic scene of EXACTLY TWO anonymous adults. One supporter kneels on one knee in the foreground, body turned towards the incumbent, head gently bowed and one hand against the chest. The incumbent sits upright on a simple broad seat behind and beside the supporter, holding a slender Zulu prestige staff vertically. Arrange their silhouettes so both the kneeling posture and seated figure remain distinct. The kneeling supporter is respectful, not crawling or prostrate. The incumbent looks towards the supporter without threatening or pointing down at them.

Use schematic nineteenth-century Zulu dress: simple wraps, bare forearms and minimal beadwork, with no detailed faces. The seat is plain and uncrowned so this pledge can represent service to either a king or a head chief. No European regalia, weapons, chains, additional attendants or landscape.

Make all people, clothing, beads, seat and staff entirely greyscale: neutral charcoal and grey, with pale-grey highlights. Match Vanilla's simplified figure silhouettes and broad soft modelling. No brown skin or wood, coloured clothes, detailed anatomy, fabric texture, photorealistic people or theatrical lighting. This is a small emblematic vignette, not an illustrated historical scene.

Keep the approved coloured card unchanged outside the replacement motif and its soft shadow. Maintain clear negative space and legibility at 60 × 80 px, suitable for a final 240 × 320 px asset. No text or rank stars.
```

## 5. Supports a rival claimant

Runtime trait: `sb_court_endorsement_claimant_trait`.

Inputs:

1. [Selected card — edit target](../output/imagegen/character_traits_2026_10_19/supports_rival_claimant_v1.png)
2. [Vanilla Elder — foreground/background figure separation](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/elder.png)
3. [Vanilla Compliant — simplified two-person interaction](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/refinement/compliant.png)

```text
Edit Image 1 into one refined Victoria 3 character-trait card. Preserve its aubergine frame, inset border, coloured field, faint background ornament, framing and 3:4 proportions. Keep the card opaque and its exterior transparent. Image 1 is the edit target only; use Images 2 and 3, the unmodified Vanilla cards, as the exclusive rendering-style references.

Replace the offering hand and diagonal staff with two anonymous adult figures in the foreground, facing one another and shaking hands. Frame them approximately from the thighs upwards. Their joined hands form a clear bridge between the two separate torsos. One is the supporter; the other is the rival claimant, distinguished only by a slender Zulu prestige staff held upright in the free hand. Keep that staff secondary to the handshake.

Behind them, in the upper field, place a smaller, subdued silhouette of the CURRENT incumbent seated on a plain seat. Keep this background incumbent low in contrast and clearly separate from the foreground pair. The image must read as an alliance with someone other than the existing ruler, not as shaking hands with the ruler. There are exactly two active foreground figures and one small background incumbent. No crowd or surrounding court scene.

Use schematic Zulu wraps and restrained beadwork, no crowns or European regalia. Render EVERY person, garment, staff and seat in neutral greyscale. Make the foreground charcoal with broad grey highlights and the distant incumbent a softer mid-grey. Match Vanilla's abstract figure construction, without detailed faces, natural skin colour, fabric texture or realistic lighting. No modern suits, conspiratorial masks or weapon exchange.

Preserve the approved coloured frame and field. Prioritise the two heads and joined arms at 60 × 80 px; the background figure is a secondary cue. Suitable for a final 240 × 320 px asset. No text, rank stars or additional objects.
```

## 6. Personally uncommitted

Runtime trait: `sb_court_endorsement_uncommitted_trait`.

Inputs:

1. [Selected card — edit target](../output/imagegen/character_traits_2026_10_19/personally_uncommitted_v1.png)
2. [Vanilla Direct — hand modelling and restraint](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png)
3. [Vanilla Pious — smooth greyscale volumes](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/pious.png)

```text
Edit Image 1 into one refined Victoria 3 character-trait card. Preserve its aubergine frame, inset border, coloured field, faint background ornament, framing and 3:4 proportions. Keep the card opaque and its exterior transparent. Image 1 is the edit target only; use Images 2 and 3, the unmodified Vanilla cards, as the exclusive rendering-style references.

Retain the existing single open, empty hand, upward-facing palm, short forearm, restrained wrist band and soft fade towards the bottom. Preserve its pose and placement. The hand offers no pledge, holds no staff and clasps no other hand. Keep a coherent thumb and four fingers, with broad separation rather than detailed joints. Simplify the wrist beads to a few unobtrusive grey forms.

Rebuild the hand as a Vanilla-style greyscale icon: neutral charcoal shadow, mid-grey body and a few soft pale-grey highlights. Remove ALL natural skin colour, cream beads, warm reflections, pores, veins, nails and fine creases. The anatomy should be readable through simple volumes, not photographic skin rendering. Do not merely apply a desaturation filter to the realistic original.

The central hand and beads must remain achromatic while the approved frame and field retain their aubergine colours. Keep this a large single-hand silhouette, distinct from the two-handed figure used for constitutional neutrality. Legible at 60 × 80 px and suitable for a final 240 × 320 px asset. No text, lettering, rank stars or added objects.
```

## 7. Claimant

Proposed artwork distinction only; this prompt does not add a runtime trait.

Inputs:

1. [Selected card — edit target](../output/imagegen/character_traits_2026_10_19/claimant_v1.png)
2. [Vanilla Direct — hand modelling and restraint](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/direct.png)
3. [Vanilla Imperious — dark symbolic volumes](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)

```text
Edit Image 1 into one refined Victoria 3 character-trait card. Preserve its reddish-copper frame, inset border, coloured field, faint background ornament, framing and 3:4 proportions. Keep the card opaque and its exterior transparent. Image 1 is the edit target only; use Images 2 and 3, the unmodified Vanilla cards, as the exclusive rendering-style references.

Retain the firm hand gripping and raising the long Zulu prestige staff. Preserve the tall composition, upper finial, hand placement and the way the forearm meets the lower inner border. Keep the staff's rounded geometric head and only the most readable collar detail. The clenched grip asserts a claim personally; it must not become an open offering hand or handshake. Keep the fingers coherent and the thumb visibly closing the grip.

Rebuild the hand, beads and staff entirely in neutral greyscale. Use charcoal silhouettes, broad mid-grey planes and restrained pale-grey highlights, matching Vanilla's soft sculptural icon treatment. Remove brown skin and wood, cream beads, gold bands, fine wood grain, skin creases and photographic material detail. Any binding is represented by one or two grey bands, not coloured metal. This is a simplified symbol, not a desaturated product photograph.

Preserve the approved coloured card outside the central motif and its shadow. Keep the border unobscured and the staff clear at 60 × 80 px, suitable for a final 240 × 320 px asset. No crown, text, rank stars or additional objects.
```

## 8. Mountain King

Runtime trait: `sb_moshoeshoe_lifeline`. The subject is Basotho, not Zulu.

Inputs:

1. [Selected card — edit target](../output/imagegen/character_traits_2026_10_19/mountain_king_v1.png)
2. [Vanilla Mountain Commander — landscape simplification only](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/mountain_commander.png)
3. [Vanilla Imperious — dark symbolic volumes](/Users/depro/.codex/visualizations/2026/09/04/01a06e15-4e0f-72a2-9928-6a6706be2336/character-icon-brief/vanilla-only/imperious.png)

```text
Edit Image 1 into one refined Victoria 3 character-trait card. Preserve its reddish-copper frame, inset border, coloured field, faint background ornament, framing and 3:4 proportions. Keep the card opaque and its exterior transparent. Image 1 is the edit target only; use Images 2 and 3, the unmodified Vanilla cards, as the exclusive rendering-style references.

Retain the broad, flat-topped Thaba Bosiu plateau with steep sides and the small upright staff in the foreground. Keep the characteristic wide summit and overall silhouette from the target; do not substitute the Alpine peak in Mountain Commander. The mountain remains the dominant mass. Preserve the staff as a small secondary sign of the ruler and stronghold.

Simplify the mountain into a few large, softly shaded charcoal and grey rock planes. Remove tan sandstone colour, granular rock texture, tiny scree, grass, realistic erosion detail and scenic atmospheric rendering. Use pale-grey highlights on the upper ledges and clear dark recesses, with depth comparable to Vanilla's symbolic mountain icon. The entire landscape and staff must be achromatic; no brown, gold or copper light on the central image. Do not merely desaturate the detailed original.

Keep this an isolated greyscale relief on the approved coloured field, with a gentle fade at the lower edge. No sky, clouds, sun, snow, castle, crown or rank star. Preserve the border and background unchanged. Readable at 60 × 80 px and suitable for a final 240 × 320 px asset. No text or extra objects.
```

## Inspection before acceptance

- Central imagery is neutral greyscale throughout; all colour belongs to the preserved frame and field.
- Surface detail and figure modelling match the Vanilla references, rather than realistic originals with their saturation removed.
- Constitutional neutrality, personal non-commitment and uSuthu have clearly different silhouettes.
- The incumbent card reads as a kneeling pledge; the rival card reads first as a foreground alliance, with the incumbent visibly separate behind it.
- The royal seat has no imported fantasy heraldry. The neutral gesture has no question marks or disabled-state treatment.
- All three chiefly staff heads remain equal, and their shafts finish naturally beneath the lower inner frame.
- Compare the set at 240 × 320 and 60 × 80 px. The two-person pledge and three-person rival composition need particular scrutiny; do not solve poor readability by adding more props.
- Keep the first-pass artwork and its exact prompts intact. Save subsequent generated variants separately. DDS conversion and runtime integration remain separate work.
