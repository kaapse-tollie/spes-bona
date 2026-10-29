"""Re-use native special-card pixels and the approved Mountain King foreground."""
from pathlib import Path
import hashlib
import json

import numpy as np
from PIL import Image, ImageFilter

OUT = Path(__file__).resolve().parent
NATIVE = Path.home() / 'Library/Application Support/Steam/steamapps/common/Victoria 3/game/gfx/interface/icons/character_trait_icons/special_character_traits'
FOREGROUND = OUT.parent / 'character_traits_foregrounds_2026_10_19/mountain_king_foreground_240.png'

sources = sorted(NATIVE.glob('*.dds'))
images = np.stack([np.asarray(Image.open(path).convert('RGBA')) for path in sources])
assert images.shape[1:] == (320, 240, 4)
packed = np.ascontiguousarray(images).view(np.uint32)[..., 0]
counts = (packed[:, None, :, :] == packed[None, :, :, :]).sum(axis=1)
y, x = np.indices((320, 240))
base = images[counts.argmax(axis=0), y, x].copy()

# Native cards have no separate blank template. Common pixels recover the frame
# and most of the field. For disputed pixels, estimate nearby background colour
# and choose the closest actual Vanilla pixel at that same coordinate.
known = counts.max(axis=0) >= 5
weight = np.asarray(Image.fromarray((known * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(12)), dtype=float) / 255
estimate = np.empty((320, 240, 3))
for channel in range(3):
    blurred = Image.fromarray((base[:, :, channel] * known).astype('uint8')).filter(ImageFilter.GaussianBlur(12))
    estimate[:, :, channel] = np.asarray(blurred, dtype=float) / np.maximum(weight, 1 / 255)
closest = ((images[:, :, :, :3].astype(float) - estimate) ** 2).sum(axis=3).argmin(axis=0)
base[~known] = images[closest, y, x][~known]

foreground = Image.open(FOREGROUND).convert('RGBA')
assert foreground.size == (240, 320)
card = Image.alpha_composite(Image.fromarray(base), foreground)
pixels = np.asarray(card)
alpha = np.asarray(foreground)[:, :, 3]
frame = (x < 24) | (x >= 216) | (y < 40) | (y >= 278)
assert not np.any(alpha[frame])
assert np.array_equal(pixels[frame], base[frame])
assert np.array_equal(pixels[:, :, 3], base[:, :, 3])
assert np.array_equal(pixels[alpha == 255], np.asarray(foreground)[alpha == 255])

png = OUT / 'mountain_king_special_card.png'
dds = OUT / 'mountain_king_special_card.dds'
card.save(png)
card.save(dds)
assert Image.open(dds).convert('RGBA').tobytes() == card.tobytes()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    'method': 'Deterministic assembly from Vanilla special-card pixels; no new image generation or foreground resampling.',
    'sources': [{'path': str(path), 'sha256': digest(path)} for path in sources],
    'foreground': {'path': str(FOREGROUND), 'sha256': digest(FOREGROUND)},
    'png': {'path': png.name, 'sha256': digest(png)},
    'dds': {'path': dds.name, 'sha256': digest(dds)},
    'checks': {'size': [240, 320], 'mode': 'RGBA', 'frame_and_stars_untouched_by_composite': True, 'native_alpha_preserved': True, 'opaque_subject_pixels_unchanged': True, 'png_dds_pixel_parity': True},
    'runtime_path': 'gfx/interface/icons/character_trait_icons/sb_moshoeshoe_lifeline.dds',
    'runtime_rendering': 'Pending DP',
}
(OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Built {png.name} and {dds.name}; native frame/stars and approved foreground verified.')
