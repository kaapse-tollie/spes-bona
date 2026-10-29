# Ideology icon backgrounds

Native-pixel reconstruction from installed Vanilla icons, revised 29 October 2026. Both templates are in `gfx/interface/icons/ideology_icons/`:

| Background | Editable master | Game texture |
| --- | --- | --- |
| Burgundy field, bronze rim | `sb_ideology_background.png` | `sb_ideology_background.dds` |
| Teal field, silver rim | `sb_ideology_leader_background.png` | `sb_ideology_leader_background.dds` |

Each is **220 × 220 RGBA** with a transparent exterior. Overlay a transparent foreground on the PNG at the same canvas size, then export the finished icon as DDS. The supplied uncompressed DDS files decode to exactly the same pixels as their PNGs. Existing ideology definitions and icons are unchanged.

The reconstruction starts from **pacifist**, retaining its complete rim, exterior, alpha and uncovered bevel. The burgundy donors begin with `unused/pacifist.dds`, `unused/feminist.dds`, `communist.dds` and `shinto_moralist.dds`. Sparse Orthodox, Buddhist and isolationist icons cover the remaining foreground/shadow intersections. The teal version uses their leader equivalents, including `mitogaku.dds` for the Torii gate.

Sources need alignment before comparison: for example the burgundy feminist image shifts one pixel left and Shinto shifts two pixels up. These are integer translations, with no resampling. The script records each offset and source hash. It distinguishes burgundy from copper and teal from silver; when multiple sources expose the background colour, it selects the brightest background pixel to reject cast shadows.

**Every output pixel is copied whole from one aligned original.** The current reconstruction uses no image generation, smoothing, interpolation, channel averaging or blending. Source versions and their shadows can differ, so this is a reconstruction from exposed pixels rather than a claim to have recovered the original layered art file. Each choice can be inspected in `source_selection.png` and the two `*_source_indices.png` maps; index values refer to the ordered source lists in `manifest.json`.

Validation checks that the full central field has background coverage, every output pixel matches its recorded donor exactly, the rim/exterior and full alpha match pacifist, and PNG/DDS decoded pixels are identical. Visual inspection covers native size and enlarged views, particularly the inner-left edge.

Rebuild with Python, NumPy and Pillow:

```sh
python3 build_backgrounds.py '/path/to/Victoria 3/game'
```

The script writes these four templates plus its local preview, source maps and manifest. It does not modify Vanilla files or launch the game.
