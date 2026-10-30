# Visual assets and presentation checks

Read when: Image reconstruction, compositing, export checks or visual presentation.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="asset-01"></a>

## ASSET-01 — Preserve coherent source geometry

Align source images before comparing
pixels. When reconstructing a frame or background, retain a consistent rim,
bevel and alpha rather than combining incompatible edges. Keep raw sources
and editable layers, and verify hashes when relocating them.

<a id="asset-02"></a>

## ASSET-02 — Match material structure as well as hue

Tonal range, dark silhouette
edges, contact shadows and highlights do different work. Calculate effects
before clipping so cropped shapes do not acquire false edges. Preserve aspect
ratio and centre the perceived subject rather than transparent-image bounds.

For intentional rim overlap, a mask restricted to fully opaque frame pixels can
cut an object at the antialiased outer edge. Let the complete subject use the
frame's soft alpha; when retaining the circular silhouette, restore that native
alpha after compositing. Check lower staff tips as well as heads before clipping.

<a id="asset-03"></a>

## ASSET-03 — Review at the size the player sees

Native-size icons and small previews
reveal problems enlarged inspection misses; enlarged views reveal edge and
alpha defects. Verify export dimensions, decoded pixels and intended unchanged
regions. File checks and approved previews do not establish in-game rendering.

Check DDS mip levels and header flags as well as the full-size pixels. Pillow's
ordinary DDS save writes only the base image; Vanilla's 220-pixel ideology icons
normally include eight levels down to 1 pixel. Missing reductions can leave rough
edges when the game samples a small icon even though a separately resized PNG
preview looks smooth. Preserve the approved base level and export a complete,
alpha-aware mip chain. For 220 × 220 icons, the levels are 220, 110, 55, 27, 13,
6, 3 and 1 pixels square. Use the shared
[DDS exporter](../../tools/dds_mipmaps.py) for future SB icons; verify the stored
level count, mipmap flags and payload sizes as well as unchanged base-level
pixels. SB's omitted levels were confirmed from the DDS headers;
the corrected files pass static checks, with engine rendering pending DP.
