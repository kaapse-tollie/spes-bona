"""Export the ideology artwork as lossless BGRA8 DDS with a full mip chain."""

from io import BytesIO
import struct

from PIL import Image


def save_mipmapped_dds(image, path):
    assert image.mode == "RGBA"
    levels = [image]
    while levels[-1].size != (1, 1):
        previous = levels[-1]
        size = (max(1, previous.width // 2), max(1, previous.height // 2))
        # Pillow filters RGBA through premultiplied alpha, avoiding dark fringes.
        levels.append(previous.resize(size, Image.Resampling.BOX))

    buffer = BytesIO()
    image.save(buffer, format="DDS")
    original = buffer.getvalue()
    header = bytearray(original[:128])
    flags = struct.unpack_from("<I", header, 8)[0]
    caps = struct.unpack_from("<I", header, 108)[0]
    struct.pack_into("<I", header, 8, flags | 0x20000)  # DDSD_MIPMAPCOUNT
    struct.pack_into("<I", header, 28, len(levels))
    struct.pack_into("<I", header, 108, caps | 0x400008)  # MIPMAP | COMPLEX
    path.write_bytes(bytes(header) + original[128:] + b"".join(
        level.tobytes("raw", "BGRA") for level in levels[1:]
    ))
    return [list(level.size) for level in levels]
