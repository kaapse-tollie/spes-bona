"""Reconstruct ideology backgrounds by copying exposed, aligned Vanilla pixels."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent
MOD = HERE.parents[2]
DESTINATION = MOD / "gfx/interface/icons/ideology_icons"
Y, X = np.mgrid[:220, :220]
RADIUS = np.hypot(X - 110, Y - 110)
FACE = RADIUS < 84
CORE = RADIUS < 75

# Integer translations into the pacifist canvas, established by overlapping the
# native frame/alpha and comparing exposed texture. No resampling is involved.
SOURCES = {
    "sb_ideology_background": [
        ("unused/pacifist.dds", 0, 0),
        ("unused/feminist.dds", -1, 0),
        ("communist.dds", 0, 0),
        ("shinto_moralist.dds", 0, -2),
        ("orthodox_patriarch.dds", 0, -1),
        ("buddhist_moralist.dds", 1, -1),
        ("isolationist.dds", 1, 0),
    ],
    "sb_ideology_leader_background": [
        ("ideology_leader/ideology_leader_pacifist.dds", 0, 0),
        ("ideology_leader/unused/ideology_leader_feminist.dds", -1, 1),
        ("ideology_leader/ideology_leader_communist.dds", -2, 2),
        ("ideology_leader/mitogaku.dds", -1, 1),
        ("ideology_leader/unused/ideology_leader_orthodox_patriarch.dds", 0, 0),
        ("ideology_leader/unused/ideology_leader_buddhist_moralist.dds", 0, 0),
        ("ideology_leader/isolationist.dds", -1, 0),
    ],
}
COLOURS = np.array([
    [170, 70, 70], [75, 155, 205], [80, 175, 85], [220, 170, 60],
    [150, 110, 200], [70, 185, 180], [200, 120, 90],
], dtype=np.uint8)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def translate(pixels, dx, dy):
    result = np.zeros_like(pixels)
    y0, y1 = max(0, -dy), min(220, 220 - dy)
    x0, x1 = max(0, -dx), min(220, 220 - dx)
    result[y0 + dy:y1 + dy, x0 + dx:x1 + dx] = pixels[y0:y1, x0:x1]
    return result


def extract(source, stem):
    arrays, records = [], []
    for name, dx, dy in SOURCES[stem]:
        path = source / name
        image = Image.open(path).convert("RGBA")
        assert image.size == (220, 220), path
        arrays.append(translate(np.array(image), dx, dy))
        records.append({"path": name, "sha256": sha256(path), "translation_xy": [dx, dy]})
    images = np.stack(arrays)
    red, green, blue, alpha = np.moveaxis(images.astype(np.int16), -1, 0)
    leader = "leader" in stem
    if leader:
        background = (green > 1.4 * red) & (blue > 1.3 * red) & (green > blue)
        brightness = green
    else:
        background = (red > 1.4 * green) & (red < 4 * green) & (blue > green) & (blue < .8 * red)
        brightness = red
    background &= alpha == 255
    exposed = background.any(axis=0)
    assert np.all(exposed[CORE]), "A foreground-covered central pixel needs another donor."

    # Burgundy wins over copper, and teal wins over silver. When several donors
    # expose the field, the brightest matching field pixel avoids cast shadows.
    # This selects one original pixel: no channel mixing, filtering or blending.
    selected = np.argmax(np.where(background, brightness, -1), axis=0).astype(np.uint8)
    selected[~(FACE & exposed)] = 0
    result = images[selected, Y, X]
    assert np.array_equal(result[~FACE], images[0][~FACE])
    assert np.array_equal(result[..., 3], images[0, ..., 3])
    for i, record in enumerate(records):
        chosen = selected == i
        assert np.array_equal(result[chosen], images[i][chosen])
        record["selected_face_pixels"] = int((chosen & FACE).sum())
    return Image.fromarray(result), selected, {
        "sources": records,
        "rim_source": records[0]["path"],
        "rim_and_exterior_rgba_matches_source": True,
        "entire_alpha_matches_source": True,
        "all_pixels_copied_from_registered_sources": True,
        "uncovered_core_pixels": 0,
        "rim_preserved_from_radius": 84,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("game_root", type=Path, help="Installed Victoria 3/game directory")
    args = parser.parse_args()
    source = args.game_root / "gfx/interface/icons/ideology_icons"
    DESTINATION.mkdir(parents=True, exist_ok=True)
    manifest = {"method": "Pacifist base, integer-aligned sparse donors, field-colour comparison and direct source-pixel copying. No generated, interpolated, blended, filtered or resampled pixels.", "size": [220, 220], "backgrounds": {}}
    preview = Image.new("RGB", (500, 270), "#30343a")
    maps = Image.new("RGB", (760, 540), "#30343a")
    preview_draw, map_draw = ImageDraw.Draw(preview), ImageDraw.Draw(maps)
    for i, stem in enumerate(SOURCES):
        image, selected, evidence = extract(source, stem)
        exports = {}
        for extension in ["png", "dds"]:
            path = DESTINATION / f"{stem}.{extension}"
            image.save(path)  # Lossless uncompressed RGBA DDS.
            decoded = Image.open(path).convert("RGBA")
            assert decoded.size == (220, 220) and decoded.tobytes() == image.tobytes()
            exports[extension] = {"path": str(path.relative_to(MOD)), "sha256": sha256(path)}
        label = "Leader ideology" if i else "Group ideology"
        manifest["backgrounds"][stem] = {**evidence, "exports": exports, "png_dds_pixels_identical": True}
        preview.paste(image, (15 + i * 250, 12), image)
        preview_draw.text((15 + i * 250, 244), label, fill="white")
        source_map = COLOURS[selected].copy()
        source_map[~FACE] = [48, 52, 58]
        maps.paste(Image.fromarray(source_map), (12, 12 + i * 270))
        map_draw.text((12, 244 + i * 270), label, fill="white")
        for j, (name, dx, dy) in enumerate(SOURCES[stem]):
            yy = 20 + i * 270 + j * 31
            map_draw.rectangle((250, yy, 265, yy + 15), fill=tuple(COLOURS[j]))
            map_draw.text((275, yy), name, fill="white")
            map_draw.text((275, yy + 12), f"translation: ({dx}, {dy})", fill="#b0b7bc")
        Image.fromarray(selected, "L").save(HERE / f"{stem}_source_indices.png")
        print(f"{stem}: {len(evidence['sources'])} aligned donors, full central coverage, every pixel from an original source; PNG/DDS match.")
    preview.save(HERE / "preview.png")
    maps.save(HERE / "source_selection.png")
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
