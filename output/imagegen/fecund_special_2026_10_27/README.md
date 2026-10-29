# Fecund — Mpande's special character card

![Fecund card](fecund_special_card.png)

Rabbit foreground generated with the **built-in image_gen tool**. Only the original Vanilla special-character reference sheet supplied its style. The exact [prompt](prompt.md), untouched [generated foreground](fecund_foreground_generated.png), native-size layer, PNG, lossless RGBA DDS and [source/hash manifest](manifest.json) are retained here.

[build_card.py](build_card.py) follows Mountain King's approved deterministic assembly: reconstruct the common Vanilla special gold field, preserve its frame and four stars, crop/scale the transparent subject without changing its proportions, normalise the emblem to greyscale and composite within the native field. Earlier cards and generated sources remain untouched.

The installed DDS is `gfx/interface/icons/character_trait_icons/sb_fecund.dds`. All exports are 240 × 320 RGBA; decoded PNG/DDS pixels match exactly, and the native exterior alpha, frame, stars and uncovered pixels are preserved. Visual inspection covers the full card and its [60 × 80 thumbnail](fecund_thumbnail.png). In-game hover/rendering remains pending DP; no game was launched.

The permanent `sb_fecund` trait is assigned only to the existing Mpande template. Universal character effects are +5% Health, +10 Popularity and +5 Prominence. It is excluded from random generation and does not replace his existing traits. Description: “This character has a fruitful and abundant household.”
