"""Assemble the generated rabbit on the established Vanilla special gold frame."""
from pathlib import Path
import hashlib
import json

import numpy as np
from PIL import Image, ImageFilter

OUT = Path(__file__).resolve().parent
NATIVE = Path.home() / 'Library/Application Support/Steam/steamapps/common/Victoria 3/game/gfx/interface/icons/character_trait_icons/special_character_traits'
RAW = OUT / 'fecund_foreground_generated.png'

# Same deterministic frame reconstruction as Mountain King's approved gold card.
sources = sorted(NATIVE.glob('*.dds'))
images = np.stack([np.asarray(Image.open(path).convert('RGBA')) for path in sources])
assert images.shape[1:] == (320, 240, 4)
packed = np.ascontiguousarray(images).view(np.uint32)[..., 0]
counts = (packed[:, None, :, :] == packed[None, :, :, :]).sum(axis=1)
y, x = np.indices((320, 240))
base = images[counts.argmax(axis=0), y, x].copy()
known = counts.max(axis=0) >= 5
weight = np.asarray(Image.fromarray((known * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(12)), dtype=float) / 255
estimate = np.empty((320, 240, 3))
for channel in range(3):
    blurred = Image.fromarray((base[:, :, channel] * known).astype('uint8')).filter(ImageFilter.GaussianBlur(12))
    estimate[:, :, channel] = np.asarray(blurred, dtype=float) / np.maximum(weight, 1 / 255)
closest = ((images[:, :, :, :3].astype(float) - estimate) ** 2).sum(axis=3).argmin(axis=0)
base[~known] = images[closest, y, x][~known]

raw = Image.open(RAW).convert('RGBA')
assert raw.getchannel('A').getextrema() == (0, 255)
bbox = raw.getchannel('A').point(lambda v: 255 if v >= 8 else 0).getbbox()
subject = raw.crop(bbox)
grey = subject.convert('L')
subject = Image.merge('RGBA', (grey, grey, grey, subject.getchannel('A')))
box = (29, 47, 211, 273)
scale = min((box[2]-box[0])/subject.width, (box[3]-box[1])/subject.height)
size = (round(subject.width*scale), round(subject.height*scale))
subject = subject.resize(size, Image.Resampling.LANCZOS)
xy = ((240-size[0])//2, box[3]-size[1])
foreground = Image.new('RGBA', (240, 320))
foreground.paste(subject, xy)
card = Image.alpha_composite(Image.fromarray(base), foreground)
pixels, alpha = np.asarray(card), np.asarray(foreground)[:, :, 3]
frame = (x < 24) | (x >= 216) | (y < 40) | (y >= 278)
assert not np.any(alpha[frame])
assert np.array_equal(pixels[alpha == 0], base[alpha == 0])
assert np.array_equal(pixels[:, :, 3], base[:, :, 3])
assert np.array_equal(pixels[frame], base[frame])

Image.fromarray(base).save(OUT / 'vanilla_special_base.png')
foreground.save(OUT / 'fecund_foreground_240.png')
png, dds = OUT/'fecund_special_card.png', OUT/'fecund_special_card.dds'
card.save(png)
card.save(dds)
assert Image.open(dds).convert('RGBA').tobytes() == card.tobytes()
card.resize((60,80), Image.Resampling.LANCZOS).save(OUT/'fecund_thumbnail.png')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    'generator': 'Built-in image_gen; exact prompt in prompt.md',
    'generation_source': '/Users/depro/.codex/generated_images/01a06e15-4e0f-72a2-9928-6a6706be2336/exec-d372317e-f67d-4b96-8647-208d8a413e40.png',
    'style_reference': '../mountain_king_special_2026_10_19/vanilla_special_reference_sheet.png',
    'sources': [{'path':str(p),'sha256':sha(p)} for p in sources],
    'raw': {'path':RAW.name,'sha256':sha(RAW),'size':list(raw.size)},
    'assembly': {'method':'Greyscale normalisation, alpha crop, aspect-preserving resize and native-frame composition',
                 'crop':list(bbox),'size':list(size),'position':list(xy)},
    'png': {'path':png.name,'sha256':sha(png)},
    'dds': {'path':dds.name,'sha256':sha(dds)},
    'checks': {'size':[240,320],'mode':'RGBA','native_frame_stars_and_alpha_preserved':True,'png_dds_pixel_parity':True},
    'runtime_path': 'gfx/interface/icons/character_trait_icons/sb_fecund.dds',
    'runtime_rendering': 'Pending DP',
}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built Fecund: 240 × 320 RGBA, native frame/stars/alpha preserved; PNG/DDS pixels match.')
