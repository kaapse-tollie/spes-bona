"""Recolour the original blank DDS without resampling; retain the AI variants."""

from pathlib import Path
import hashlib
import json

from PIL import Image, ImageDraw, __version__ as pillow_version


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SOURCE = ROOT.parent / "Example Mods/mdof - Morgenrote dawn of flavour [1.13]/gfx/interface/icons/character_trait_icons/0_base_icon_grey.dds"
GENERATED = OUT.parent / "character_card_templates_2026_10_19"
PALETTES = {
    "jade": ("#355B50", "#79A397", "#D7E8DE"),
    "aubergine": ("#55405E", "#A48AAE", "#E9DEED"),
    "copper": ("#704A32", "#BD8964", "#EEDCC5"),
}
POSITIONS = (0, 80, 170, 220, 255)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rgb(hex_colour):
    return tuple(int(hex_colour[i : i + 2], 16) for i in (1, 3, 5))


def gradient(colours):
    stops = [rgb(c) for c in ("#000000", *colours, "#FFFFFF")]
    lut = []
    for level in range(256):
        segment = next(i for i in range(4) if level <= POSITIONS[i + 1])
        width = POSITIONS[segment + 1] - POSITIONS[segment]
        offset = level - POSITIONS[segment]
        lut.append(tuple(
            (a * (width - offset) + b * offset + width // 2) // width
            for a, b in zip(stops[segment], stops[segment + 1])
        ))
    return lut


def outline(im):
    bbox = im.getchannel("A").point(lambda a: 255 if a >= 128 else 0).getbbox()
    return {"bbox_alpha_ge_128": list(bbox), "width": bbox[2] - bbox[0], "height": bbox[3] - bbox[1]}


def main():
    # Protect every existing generated file, including the masters and manifest.
    before = {p.name: sha(p) for p in GENERATED.iterdir() if p.is_file()}
    source_sha = sha(SOURCE)
    assert source_sha == "0afbf0d28c1d7abdb03e65aeebc0d80e5950b6965d9c6e60aab192c0fba7750d"
    source = Image.open(SOURCE).convert("RGBA")
    assert source.size == (240, 320)
    alpha = source.getchannel("A")
    # Fixed integer Rec.601 luma, rounded to nearest; no spatial operations.
    luma = Image.new("L", source.size)
    raw = source.tobytes()
    luma.putdata([
        (299 * raw[i] + 587 * raw[i + 1] + 114 * raw[i + 2] + 500) // 1000
        for i in range(0, len(raw), 4)
    ])
    source.save(OUT / "0_base_icon_grey_source.png")
    manifest = {
        "source_dds": str(SOURCE), "source_sha256": source_sha,
        "pillow_version": pillow_version, "size": list(source.size),
        "method": "Integer Rec.601 luma; piecewise linear sRGB gradient LUT; original alpha copied verbatim; no resampling",
        "luma_formula": "(299*R + 587*G + 114*B + 500) // 1000",
        "stop_positions": list(POSITIONS), "source_outline": outline(source),
        "alpha_sha256": hashlib.sha256(alpha.tobytes()).hexdigest(), "items": [],
    }
    comparison = Image.new("RGB", (1064, 746), "#282827")
    draw = ImageDraw.Draw(comparison)
    draw.text((14, 10), "TOP: original DDS + pixel gradient maps | BOTTOM: original DDS + preserved AI bases", fill="#eeeae2")
    for row in (0, 1):
        draw.text((16, 35 + 350 * row), "Original DDS", fill="#eeeae2")
        comparison.paste(source, (16, 55 + 350 * row), source)
    for i, (name, colours) in enumerate(PALETTES.items()):
        lut = gradient(colours)
        recoloured = Image.merge("RGBA", tuple(luma.point([c[k] for c in lut]) for k in range(3)) + (alpha,))
        png = OUT / f"0_base_icon_{name}.png"
        dds = OUT / f"0_base_icon_{name}.dds"
        recoloured.save(png)
        recoloured.save(dds)  # Uncompressed RGBA avoids a second lossy DDS encoding.
        assert recoloured.getchannel("A").tobytes() == alpha.tobytes()
        assert Image.open(dds).convert("RGBA").tobytes() == recoloured.tobytes()
        assert outline(recoloured) == outline(source)
        old = Image.open(GENERATED / f"0_base_icon_{name}.png").convert("RGBA")
        manifest["items"].append({
            "family": name, "stop_colours": ["#000000", *colours, "#FFFFFF"],
            "png": png.name, "png_sha256": sha(png), "dds": dds.name, "dds_sha256": sha(dds),
            "alpha_identical_to_source": True, "outline": outline(recoloured),
            "png_dds_pixels_identical": True, "generated_outline": outline(old),
        })
        x = 16 + (i + 1) * 264
        for row, image in enumerate((recoloured, old)):
            draw.text((x, 35 + 350 * row), f"{name.title()} - {'gradient' if row == 0 else 'AI generated'}", fill="#eeeae2")
            comparison.paste(image, (x, 55 + 350 * row), image)
    comparison.save(OUT / "comparison.png")
    assert before == {p.name: sha(p) for p in GENERATED.iterdir() if p.is_file()}
    assert sha(SOURCE) == source_sha
    manifest["generated_files_preserved"] = before
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"source_outline": manifest["source_outline"], "files_preserved": len(before), "templates": [{"family": x["family"], "outline": x["outline"], "generated_outline": x["generated_outline"]} for x in manifest["items"]]}, indent=2))


if __name__ == "__main__":
    main()
