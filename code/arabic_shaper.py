"""Dependency-free Arabic shaper for game engines that cannot shape text.

Input:  logical Arabic (normal Unicode, reading order).
Output: logical order string made of Presentation Forms (U+FE70..U+FEFC,
        U+FB50.. for extra letters). Visual reordering is a separate step
        (see rtl_layout.py) because it must happen per wrapped line.

Why our own shaper instead of arabic_reshaper only:
  * control codes / placeholders must stay byte-exact and can be declared
    "transparent" for joining (DELTARUNE: pause code inside a word must not
    break the joining of the letters around it);
  * we must know exactly which glyphs are produced to build a font bank;
  * engines differ in what they need (strip harakat, lam-alef or not).
"""
from __future__ import annotations

import re
import unicodedata

# letter: (isolated, final, initial, medial); None = form does not exist
FORMS = {
    'ء': ('ﺀ', None, None, None),          # ء
    'آ': ('ﺁ', 'ﺂ', None, None),      # آ
    'أ': ('ﺃ', 'ﺄ', None, None),      # أ
    'ؤ': ('ﺅ', 'ﺆ', None, None),      # ؤ
    'إ': ('ﺇ', 'ﺈ', None, None),      # إ
    'ئ': ('ﺉ', 'ﺊ', 'ﺋ', 'ﺌ'),  # ئ
    'ا': ('ﺍ', 'ﺎ', None, None),      # ا
    'ب': ('ﺏ', 'ﺐ', 'ﺑ', 'ﺒ'),  # ب
    'ة': ('ﺓ', 'ﺔ', None, None),      # ة
    'ت': ('ﺕ', 'ﺖ', 'ﺗ', 'ﺘ'),  # ت
    'ث': ('ﺙ', 'ﺚ', 'ﺛ', 'ﺜ'),  # ث
    'ج': ('ﺝ', 'ﺞ', 'ﺟ', 'ﺠ'),  # ج
    'ح': ('ﺡ', 'ﺢ', 'ﺣ', 'ﺤ'),  # ح
    'خ': ('ﺥ', 'ﺦ', 'ﺧ', 'ﺨ'),  # خ
    'د': ('ﺩ', 'ﺪ', None, None),      # د
    'ذ': ('ﺫ', 'ﺬ', None, None),      # ذ
    'ر': ('ﺭ', 'ﺮ', None, None),      # ر
    'ز': ('ﺯ', 'ﺰ', None, None),      # ز
    'س': ('ﺱ', 'ﺲ', 'ﺳ', 'ﺴ'),  # س
    'ش': ('ﺵ', 'ﺶ', 'ﺷ', 'ﺸ'),  # ش
    'ص': ('ﺹ', 'ﺺ', 'ﺻ', 'ﺼ'),  # ص
    'ض': ('ﺽ', 'ﺾ', 'ﺿ', 'ﻀ'),  # ض
    'ط': ('ﻁ', 'ﻂ', 'ﻃ', 'ﻄ'),  # ط
    'ظ': ('ﻅ', 'ﻆ', 'ﻇ', 'ﻈ'),  # ظ
    'ع': ('ﻉ', 'ﻊ', 'ﻋ', 'ﻌ'),  # ع
    'غ': ('ﻍ', 'ﻎ', 'ﻏ', 'ﻐ'),  # غ
    'ف': ('ﻑ', 'ﻒ', 'ﻓ', 'ﻔ'),  # ف
    'ق': ('ﻕ', 'ﻖ', 'ﻗ', 'ﻘ'),  # ق
    'ك': ('ﻙ', 'ﻚ', 'ﻛ', 'ﻜ'),  # ك
    'ل': ('ﻝ', 'ﻞ', 'ﻟ', 'ﻠ'),  # ل
    'م': ('ﻡ', 'ﻢ', 'ﻣ', 'ﻤ'),  # م
    'ن': ('ﻥ', 'ﻦ', 'ﻧ', 'ﻨ'),  # ن
    'ه': ('ﻩ', 'ﻪ', 'ﻫ', 'ﻬ'),  # ه
    'و': ('ﻭ', 'ﻮ', None, None),      # و
    # ى is dual-joining in Unicode, but in real Arabic text it only ends a
    # word; its initial/medial forms (FBE8/FBE9) are missing from most fonts.
    'ى': ('ﻯ', 'ﻰ', None, None),      # ى
    'ي': ('ﻱ', 'ﻲ', 'ﻳ', 'ﻴ'),  # ي
    # letters for foreign sounds (used by DELTARUNE / Persian loanwords)
    'پ': ('ﭖ', 'ﭗ', 'ﭘ', 'ﭙ'),  # پ
    'چ': ('ﭺ', 'ﭻ', 'ﭼ', 'ﭽ'),  # چ
    'ڇ': ('ﭾ', 'ﭿ', 'ﮀ', 'ﮁ'),  # ڇ
    'ڤ': ('ﭪ', 'ﭫ', 'ﭬ', 'ﭭ'),  # ڤ
    'گ': ('ﮒ', 'ﮓ', 'ﮔ', 'ﮕ'),  # گ
}

LAM = 'ل'
LAM_ALEF = {  # alef variant -> (isolated, final)
    'آ': ('ﻵ', 'ﻶ'),  # لآ
    'أ': ('ﻷ', 'ﻸ'),  # لأ
    'إ': ('ﻹ', 'ﻺ'),  # لإ
    'ا': ('ﻻ', 'ﻼ'),  # لا
}
TATWEEL = 'ـ'
HARAKAT = set('ًٌٍَُِّْٰ')


def joins_left(ch: str) -> bool:
    """Can this char connect to the NEXT letter (on its left side)?"""
    if ch == TATWEEL:
        return True
    f = FORMS.get(ch)
    return bool(f and f[2] is not None)


def joins_right(ch: str) -> bool:
    """Can this char connect to the PREVIOUS letter (on its right side)?"""
    if ch == TATWEEL:
        return True
    f = FORMS.get(ch)
    return bool(f and f[1] is not None)


def _units(text: str, token_re: re.Pattern | None):
    """Split into ('tok', s) for protected tokens and ('ch', c) for chars."""
    if token_re is None:
        return [('ch', c) for c in text]
    out, pos = [], 0
    for m in token_re.finditer(text):
        out.extend(('ch', c) for c in text[pos:m.start()])
        out.append(('tok', m.group(0)))
        pos = m.end()
    out.extend(('ch', c) for c in text[pos:])
    return out


def shape(text: str, *, token_re: re.Pattern | None = None,
          tokens_transparent: bool = False, lam_alef: bool = True,
          strip_harakat: bool = False) -> str:
    """Return logical-order presentation forms.

    token_re            protected spans copied byte-exact (codes, {vars}).
    tokens_transparent  True: a token between two letters does not break
                        their joining (pause code in the middle of a word).
                        False: a token acts like a space (safe default).
    lam_alef            use the lam-alef ligatures. Disable if the font bank
                        has no slot for them (they then render as two letters).
    strip_harakat       drop short vowels when the font has no glyphs for them
                        (missing glyph = empty box or invisible char in game).
    """
    text = unicodedata.normalize('NFC', text)
    units = _units(text, token_re)
    if strip_harakat:
        units = [u for u in units if not (u[0] == 'ch' and u[1] in HARAKAT)]

    def is_skippable(u):
        return (u[0] == 'ch' and u[1] in HARAKAT) or (u[0] == 'tok' and tokens_transparent)

    def neighbour(i, step):
        j = i + step
        while 0 <= j < len(units) and is_skippable(units[j]):
            j += step
        if 0 <= j < len(units) and units[j][0] == 'ch':
            return j, units[j][1]
        return j, None

    out, i, skip = [], 0, set()
    while i < len(units):
        kind, val = units[i]
        if i in skip:
            i += 1
            continue
        if kind == 'tok' or val not in FORMS and val != TATWEEL:
            out.append(val)
            i += 1
            continue
        if val == TATWEEL:
            out.append(val)
            i += 1
            continue
        _, prev = neighbour(i, -1)
        nj, nxt = neighbour(i, +1)
        connect_prev = prev is not None and joins_left(prev) and joins_right(val)
        if lam_alef and val == LAM and nxt in LAM_ALEF:
            iso, fin = LAM_ALEF[nxt]
            out.append(fin if connect_prev else iso)
            # keep marks that sat between lam and alef instead of losing them
            for k in range(i + 1, nj):
                out.append(units[k][1])
            skip.update(range(i + 1, nj + 1))
            i += 1
            continue
        connect_next = nxt is not None and joins_left(val) and joins_right(nxt)
        iso, fin, ini, med = FORMS[val]
        if connect_prev and connect_next:
            out.append(med)
        elif connect_prev:
            out.append(fin)
        elif connect_next:
            out.append(ini)
        else:
            out.append(iso)
        i += 1
    return ''.join(out)


def glyphs_used(shaped_texts) -> set[str]:
    """Every distinct char the font bank must contain (feed to font builder)."""
    used = set()
    for t in shaped_texts:
        used.update(t)
    return used


if __name__ == '__main__':
    tok = re.compile(r'\{[^}]*\}|\\[A-Za-z]+\[[^\]]*\]|\^\d')
    for s in ['سلام عليكم', 'لا إله', 'الآن', 'مرحباً بك', 'شيء', 'اسم^5ك', 'هيا {name}!']:
        print(s, '->', shape(s, token_re=tok, tokens_transparent=True))
