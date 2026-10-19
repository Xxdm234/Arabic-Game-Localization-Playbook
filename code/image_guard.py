"""Prove that an edited texture changed ONLY inside the approved text regions.

Lessons behind it:
  * ImageChops.difference(a, b).getbbox() returns None for two different
    opaque images in RGBA mode (alpha difference is 0) -> use getextrema()
    per channel (DELTARUNE).
  * compare RGB even where alpha == 0: engines may sample it (RtMI).
  * a checker that never reads a layer cannot protect it: MI3 crashed because
    the writer wiped ZPLN (z-planes) after the pixels and the pixel check
    passed. Add an independent check for every data block you rewrite.
  * keep the transparency CLASS of the original (binary alpha stays binary;
    normal maps keep their channel meaning) - Tales of Monkey Island.

    python image_guard.py original.png edited.png "x0,y0,x1,y1" ["x0,y0,x1,y1" ...]
"""
from __future__ import annotations

import sys

from PIL import Image, ImageChops, ImageDraw


def _mask(size, regions):
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    for (x0, y0, x1, y1) in regions:
        d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=255)
    return m


def changed_outside(orig: Image.Image, new: Image.Image, regions) -> int:
    """Number of pixels that differ outside the editable regions (must be 0)."""
    if orig.size != new.size or orig.mode != new.mode:
        raise ValueError(f'size/mode changed: {orig.size}/{orig.mode} -> {new.size}/{new.mode}')
    a, b = orig.convert('RGBA'), new.convert('RGBA')
    diff = ImageChops.difference(a, b)
    outside = ImageChops.invert(_mask(a.size, regions))
    count = 0
    for band in diff.split():                       # R, G, B, A separately
        band = ImageChops.multiply(band, outside)
        if band.getextrema()[1] > 0:
            count = max(count, sum(1 for v in band.getdata() if v))
    return count


def alpha_class(img: Image.Image) -> str:
    if img.mode not in ('RGBA', 'LA', 'PA'):
        return 'opaque'
    vals = set(img.getchannel('A').getdata())
    if vals == {255}:
        return 'opaque'
    if vals <= {0, 255}:
        return 'binary'
    return 'gradient'


def main(argv) -> int:
    a, b = Image.open(argv[1]), Image.open(argv[2])
    regions = [tuple(int(v) for v in r.split(',')) for r in argv[3:]]
    n = changed_outside(a, b, regions)
    ca, cb = alpha_class(a), alpha_class(b)
    print(f'pixels changed outside regions: {n}; alpha class {ca} -> {cb}')
    return 0 if n == 0 and (ca == cb or ca == 'gradient') else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
