"""Line wrapping + visual reordering for engines that draw left-to-right.

The rule learned on almost every project (Yuppie Psycho, MI1 SE, MI3, Tales,
RtMI, Harvest Moon...):

    WRAP THE LOGICAL TEXT FIRST, THEN SHAPE AND REVERSE EACH LINE.

If you reverse a whole sentence and let the engine wrap it, the engine wraps
from the start of the byte string, so the END of the Arabic sentence lands on
the first line.

Paragraph direction is always RTL for Arabic lines (python-bidi's
get_display(..., base_dir='R')); never let each wrapped line guess its own
direction from its first strong char, or a line starting with a Latin word
becomes an LTR paragraph.
"""
from __future__ import annotations

import re
from typing import Callable, Iterable

from arabic_shaper import shape

ARABIC_LETTERS = re.compile('[ء-يٮ-ۓۺ-ۼ'
                            'ﭐ-﷿ﹰ-ﻼ]')
LATIN_OR_DIGIT = re.compile(r'[A-Za-z0-9À-ɏ٠-٩۰-۹]')
MIRROR = str.maketrans('()[]{}<>«»‹›', ')(][}{><»«›‹')
# neutrals allowed INSIDE a Latin/number run when another Latin/digit follows:
# "MEMORY CARD 1", "3:26", "CTRL-F", "ATK: 6/MAG: 5", "20,000"
INNER_NEUTRALS = set(' .,:/-_+\'')
# attach to an adjacent number: "50%", "+25", "-54", "20,000+"
NUMBER_AFFIXES = set('%+-٪')


def _is_ltr(ch: str) -> bool:
    return bool(LATIN_OR_DIGIT.match(ch))


def _units(text: str, token_re: re.Pattern | None):
    if token_re is None:
        return [('ch', c) for c in text]
    out, pos = [], 0
    for m in token_re.finditer(text):
        out.extend(('ch', c) for c in text[pos:m.start()])
        out.append(('tok', m.group(0)))
        pos = m.end()
    out.extend(('ch', c) for c in text[pos:])
    return out


def visual_line(shaped: str, *, token_re: re.Pattern | None = None,
                attach_prefix: str = '', mirror: bool = True) -> str:
    """Reorder ONE already-shaped logical line for an LTR renderer.

    attach_prefix: symbols that should stick to the following Latin word
                   ('@' in "تعريب: @Name"); UAX#9 would otherwise move
                   them to the other side ("Name@").
    Tokens (engine codes) are atomic and keep their bytes; their position
    follows the reversal, like a neutral char.
    """
    units = _units(shaped, token_re)
    n = len(units)
    ltr = [False] * n
    for i, (k, v) in enumerate(units):
        if k == 'ch' and _is_ltr(v):
            ltr[i] = True
    # grow runs over inner neutrals that sit between two LTR chars
    i = 0
    while i < n:
        if ltr[i]:
            j = i + 1
            while j < n and units[j][0] == 'ch' and units[j][1] in INNER_NEUTRALS:
                j += 1
            if j < n and ltr[j] and j > i + 1:
                for k in range(i + 1, j):
                    ltr[k] = True
            i = j if j > i + 1 else i + 1
        else:
            i += 1
    # number affixes and requested prefixes
    for i, (k, v) in enumerate(units):
        if k != 'ch' or ltr[i]:
            continue
        prev_ltr = i > 0 and ltr[i - 1] and units[i - 1][1][-1:].isdigit()
        next_ltr = i + 1 < n and ltr[i + 1]
        if v in NUMBER_AFFIXES and (prev_ltr or (next_ltr and units[i + 1][1].isdigit())):
            ltr[i] = True
        elif v in attach_prefix and next_ltr:
            ltr[i] = True
    # build runs and reverse
    pieces, i = [], 0
    while i < n:
        if ltr[i]:
            j = i
            while j < n and ltr[j]:
                j += 1
            pieces.append(''.join(u[1] for u in units[i:j]))   # keep LTR order
            i = j
        else:
            k, v = units[i]
            if k == 'ch' and mirror:
                v = v.translate(MIRROR)
            pieces.append(v)
            i += 1
    return ''.join(reversed(pieces))


def wrap_logical(text: str, max_width: float, measure: Callable[[str], float],
                 balanced: bool = True) -> list[str]:
    """Split logical text on spaces so every SHAPED line fits max_width.

    measure() must measure what the engine will draw (shaped glyphs, with the
    engine's own advances), not the logical string. Hard breaks '\n' are kept.
    balanced=True avoids a long first line followed by a one-word last line.
    """
    out: list[str] = []
    for para in text.split('\n'):
        words = para.split(' ')
        lines, cur = [], ''
        for w in words:
            cand = w if not cur else cur + ' ' + w
            if cur and measure(cand) > max_width:
                lines.append(cur)
                cur = w
            else:
                cur = cand
        lines.append(cur)
        if balanced and len(lines) > 1:
            lines = _balance(words, len(lines), max_width, measure) or lines
        out.extend(lines)
    return out


def _balance(words, count, max_width, measure):
    """Smallest width limit that still gives `count` lines (binary search)."""
    lo, hi, best = 0.0, max_width, None
    for _ in range(18):
        mid = (lo + hi) / 2
        lines, cur, ok = [], '', True
        for w in words:
            cand = w if not cur else cur + ' ' + w
            if cur and measure(cand) > mid:
                lines.append(cur)
                cur = w
            else:
                cur = cand
            if measure(cur) > max_width:
                ok = False
        lines.append(cur)
        if ok and len(lines) <= count:
            best, hi = lines, mid
        else:
            lo = mid
    return best


def layout(text: str, max_width: float, measure_shaped: Callable[[str], float], *,
           token_re: re.Pattern | None = None, shape_kw: dict | None = None,
           attach_prefix: str = '', line_sep: str = '\n') -> str:
    """Full pipeline: logical text -> engine-ready visual text."""
    shape_kw = shape_kw or {}

    def m(s: str) -> float:
        return measure_shaped(shape(s, token_re=token_re, **shape_kw))

    lines = wrap_logical(text, max_width, m)
    vis = [visual_line(shape(ln, token_re=token_re, **shape_kw),
                       token_re=token_re, attach_prefix=attach_prefix) for ln in lines]
    return line_sep.join(vis)


def pad_right_align(visual_lines: Iterable[str], measure: Callable[[str], float],
                    target: float, pad_char: str, pad_width: float) -> list[str]:
    """Right-align lines in an engine that only aligns left (Tales, Chrono
    Trigger): prepend transparent padding glyphs to the LEFT of each visual line.
    Ordinary spaces are often trimmed or unstable; use a dedicated empty glyph."""
    out = []
    for ln in visual_lines:
        gap = max(0.0, target - measure(ln))
        out.append(pad_char * int(round(gap / pad_width)) + ln)
    return out


def has_arabic(s: str) -> bool:
    """Letters only. Do NOT include ، ؛ ؟ — an English line ending with ؟ would
    be counted as translated (DELTARUNE lesson)."""
    return bool(ARABIC_LETTERS.search(s))


if __name__ == '__main__':
    tok = re.compile(r'\{[^}]*\}')
    for s in ['حصلت على 50% من الذهب', 'بطاقة الذاكرة MEMORY CARD 1 جاهزة',
              'الوقت 3:26 الآن', 'اضغط CTRL-F للبحث', 'تعريب: @Name & Team',
              'قال {name} (بهدوء): مرحباً']:
        print(visual_line(shape(s, token_re=tok), token_re=tok, attach_prefix='@'))
