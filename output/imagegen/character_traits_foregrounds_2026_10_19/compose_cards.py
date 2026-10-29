"""Composite the saved transparent subjects onto unchanged native card bases."""

from pathlib import Path
import hashlib
import json
import textwrap

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent
BASES = OUT.parent / "character_card_templates_gradient_2026_10_19"
# Layout boxes are in native card pixels; bottom-aligned forms pass under the frame.
LAYOUT = {
    "usuthu_loyalist": ((30, 42, 210, 290), "centre"),
    "amakhosi_partisan": ((28, 38, 212, 310), "bottom"),
    "constitutionally_unaligned": ((28, 42, 212, 290), "centre"),
    "supports_incumbent": ((28, 50, 212, 290), "centre"),
    "supports_rival_claimant": ((28, 32, 212, 310), "bottom"),
    "personally_uncommitted": ((30, 42, 210, 290), "centre"),
    "claimant": ((48, 28, 192, 310), "bottom"),
    "mountain_king": ((26, 94, 214, 286), "centre"),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    path = OUT / "manifest.json"
    manifest = json.loads(path.read_text())
    base_hashes = {p.name: sha(p) for p in BASES.iterdir() if p.is_file()}
    field = Image.new("L", (240, 320), 0)
    # Native source's stepped inner edge. The frame itself is never composited over.
    points = [(38, 16), (202, 16), (202, 32), (218, 32), (218, 287), (202, 287), (202, 303), (38, 303), (38, 287), (22, 287), (22, 32), (38, 32)]
    ImageDraw.Draw(field).polygon(points, fill=255)
    field.save(OUT / "inner_field_mask.png")
    preview = Image.new("RGB", (1080, 1000), "#282827")
    draw = ImageDraw.Draw(preview)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
    small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
    draw.text((16, 12), "SB character traits - transparent subjects on fixed gradient bases", fill="#eeeae2", font=font)
    draw.text((16, 38), "Native 240 x 320 cards and 60 x 80 previews; earlier artwork preserved", fill="#bbb8b2", font=small)
    for index, item in enumerate(manifest["items"]):
        raw_path = OUT / item["selected_foreground"]
        raw = Image.open(raw_path).convert("RGBA")
        bbox = raw.getchannel("A").point(lambda a: 255 if a >= 8 else 0).getbbox()
        cropped = raw.crop(bbox)
        # Remove negligible generated channel tints without changing the preserved raw.
        grey = cropped.convert("L")
        cropped = Image.merge("RGBA", (grey, grey, grey, cropped.getchannel("A")))
        box, alignment = LAYOUT[item["id"]]
        scale = min((box[2] - box[0]) / cropped.width, (box[3] - box[1]) / cropped.height)
        size = (round(cropped.width * scale), round(cropped.height * scale))
        subject = cropped.resize(size, Image.Resampling.LANCZOS)
        xy = (box[0] + (box[2] - box[0] - size[0]) // 2,
              box[3] - size[1] if alignment == "bottom" else box[1] + (box[3] - box[1] - size[1]) // 2)
        foreground = Image.new("RGBA", (240, 320))
        foreground.paste(subject, xy)
        foreground.putalpha(ImageChops.multiply(foreground.getchannel("A"), field))
        base_path = BASES / f"0_base_icon_{item['family']}.png"
        base = Image.open(base_path).convert("RGBA")
        card = Image.alpha_composite(base, foreground)
        untouched = np.asarray(foreground)[:, :, 3] == 0
        assert np.array_equal(np.asarray(card)[untouched], np.asarray(base)[untouched])
        assert card.getchannel("A").tobytes() == base.getchannel("A").tobytes()
        assert np.array_equal(np.asarray(card)[np.asarray(field) == 0], np.asarray(base)[np.asarray(field) == 0])
        stem = item["id"]
        fg_path = OUT / f"{stem}_foreground_240.png"
        png = OUT / f"{stem}_card.png"
        dds = OUT / f"{stem}_card.dds"
        foreground.save(fg_path)
        card.save(png)
        card.save(dds)
        assert Image.open(dds).convert("RGBA").tobytes() == card.tobytes()
        item["composition"] = {
            "selected_raw_sha256": sha(raw_path), "base_path": str(base_path), "base_sha256": sha(base_path),
            "source_crop_alpha_ge_8": list(bbox), "greyscale_normalisation": True,
            "resized_to": list(size), "offset": list(xy), "layout_box": list(box),
            "foreground": fg_path.name, "png": png.name, "dds": dds.name,
            "png_sha256": sha(png), "dds_sha256": sha(dds),
            "base_frame_and_uncovered_pixels_unchanged": True, "base_alpha_unchanged": True,
        }
        x = 15 + (index % 4) * 270
        y = 72 + (index // 4) * 462
        preview.paste(card, (x, y), card)
        draw.multiline_text((x, y + 326), textwrap.fill(item["title"], width=25), fill="#eeeae2", font=font, spacing=3)
        thumb = card.resize((60, 80), Image.Resampling.LANCZOS)
        preview.paste(thumb, (x + 180, y + 369), thumb)
        draw.text((x, y + 400), "60 x 80 preview", fill="#bbb8b2", font=small)
    assert base_hashes == {p.name: sha(p) for p in BASES.iterdir() if p.is_file()}
    preview.save(OUT / "review_sheet.png")
    manifest["status"] = "Eight foregrounds generated and composited; visual review in progress; no runtime integration"
    manifest["composition_method"] = "Greyscale normalisation; aspect-preserving crop/scale; native stepped-field clipping; alpha composite; unchanged fixed bases"
    manifest["base_files_preserved"] = base_hashes
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("Composited eight PNG/DDS pairs. Frame, exterior alpha and uncovered base pixels are exact; all bases unchanged.")


if __name__ == "__main__":
    main()
