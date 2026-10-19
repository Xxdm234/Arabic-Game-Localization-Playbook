"""Font selection and glyph-bank helpers.

  coverage  : which shaped glyphs a TTF lacks (Tajawal/Cairo/Almarai have no
              isolated presentation forms; Aref Ruqaa has none at all)
  fallback  : map a missing presentation form to its base letter when the
              base letter's default glyph IS that form (NFKC single char)
  sheet     : render candidate fonts side by side at the game's real pixel
              size, 1-bit, to choose by MEASUREMENT (Yuppie Psycho: dots of
              ب ت ث must stay distinct at 12 px)
  bank      : assign single-byte slots for engines without Unicode, skipping
              bytes the original text uses and engine command bytes (FE/FF)

    python font_tools.py coverage Tajawal-Bold.ttf all_shaped_text.txt
    python font_tools.py sheet 12 out.png NotoSansArabic.ttf Tajawal-Bold.ttf
"""
from __future__ import annotations

import sys
import unicodedata

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

SAMPLE = 'بيت ثابت تثبيت — نجم عين جيم — لا إله إلا — ﻻ ٠١٢٣ 123 ؟،؛'


def cmap_of(path: str) -> set[int]:
    f = TTFont(path, lazy=True)
    return set(f.getBestCmap().keys())


def coverage(font_path: str, chars: set[str]) -> dict[str, str | None]:
    """{char: None if present, base-letter fallback, or '!' if unrecoverable}."""
    cm = cmap_of(font_path)
    out = {}
    for c in sorted(chars):
        if ord(c) in cm or c.isspace():
            continue
        base = unicodedata.normalize('NFKC', c)
        out[c] = base if len(base) == 1 and ord(base) in cm else '!'
    return out


def sheet(px: int, out_png: str, fonts: list[str], text: str = SAMPLE) -> None:
    """1-bit rendering at real size, then x4 nearest upscale for viewing."""
    from arabic_shaper import shape
    from rtl_layout import visual_line
    vis = visual_line(shape(text))
    rows = []
    for fp in fonts:
        f = ImageFont.truetype(fp, px)
        w = int(f.getlength(vis)) + 8
        im = Image.new('1', (w, px * 2), 1)
        d = ImageDraw.Draw(im)
        d.fontmode = '1'                    # no antialiasing, like a bitmap font
        d.text((4, px // 3), vis, font=f, fill=0)
        rows.append(im.convert('L').resize((w * 4, px * 8), Image.NEAREST))
    W, H = max(r.width for r in rows), sum(r.height for r in rows)
    canvas = Image.new('L', (W, H), 255)
    y = 0
    for r in rows:
        canvas.paste(r, (0, y))
        y += r.height
    canvas.save(out_png)


def assign_bank(needed: list[str], used_bytes: set[int], start: int = 0x80,
                forbidden: tuple[int, ...] = (0xFE, 0xFF),
                extra_free: tuple[int, ...] = ()) -> dict[str, int]:
    """Stable single-byte mapping. Keep the ORDER of `needed` fixed between
    builds (sort once, store in a seed file) or every savestate/old build that
    caches the font breaks (WA4: glyph_freq seed)."""
    free = [b for b in list(range(start, 0x100)) + list(extra_free)
            if b not in used_bytes and b not in forbidden]
    if len(needed) > len(free):
        raise SystemExit(f'need {len(needed)} slots, only {len(free)} free')
    return {ch: free[i] for i, ch in enumerate(needed)}


if __name__ == '__main__':
    if sys.argv[1] == 'coverage':
        chars = set(open(sys.argv[3], encoding='utf-8').read())
        for c, fb in coverage(sys.argv[2], chars).items():
            print(f'U+{ord(c):04X} {c} -> {fb}')
    elif sys.argv[1] == 'sheet':
        sheet(int(sys.argv[2]), sys.argv[3], sys.argv[4:])
