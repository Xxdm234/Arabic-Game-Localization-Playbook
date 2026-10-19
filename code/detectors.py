"""Statistical detectors that find bugs no structural check sees.

All of them come from DELTARUNE's gaps.py / mixed.py / digits.py /
revwords.py / revlines.py and from the Freebird uncovered/ship audits.

    python detectors.py translated.tsv [source.tsv]
"""
from __future__ import annotations

import re
import sys
from collections import Counter

LETTERS_AR = re.compile('[ء-يٮ-ۓﭐ-﷿ﹰ-ﻼ]')
WORD_LATIN = re.compile(r'\b[A-Za-z]{3,}\b')
WORD_AR = re.compile('[ء-ي]+')
NUM = re.compile(r'\d+')


def untranslated(src: dict, tr: dict, allow: set[str] = frozenset()):
    """Visible English left behind (id present in source, no Arabic letters)."""
    for rid, en in src.items():
        if rid in allow or not WORD_LATIN.search(en):
            continue
        ar = tr.get(rid, en)
        if not LETTERS_AR.search(ar):
            yield rid, en


def mixed(tr: dict, allow_words: set[str] = frozenset()):
    """Half-translated lines: more dangerous than full English because a
    'has Arabic?' check passes them."""
    for rid, ar in tr.items():
        if LETTERS_AR.search(ar):
            latin = [w for w in WORD_LATIN.findall(ar) if w not in allow_words]
            if latin:
                yield rid, latin


def reversed_numbers(src: dict, tr: dict):
    """'06' instead of '60': the multiset of digits is equal but numbers not."""
    for rid, ar in tr.items():
        en = src.get(rid)
        if en is None:
            continue
        a, b = sorted(NUM.findall(en)), sorted(NUM.findall(ar))
        if a != b and sorted(''.join(a)) == sorted(''.join(b)):
            yield rid, a, b


def reversed_words(tr: dict, min_ratio: float = 20.0):
    """A rare word whose reverse is a common word was probably stored in the
    wrong direction (V = reverse(L) applied twice or not at all)."""
    freq = Counter(w for ar in tr.values() for w in WORD_AR.findall(ar))
    for w, c in freq.items():
        r = w[::-1]
        if len(w) > 2 and r != w and freq.get(r, 0) >= min_ratio * c:
            yield w, c, r, freq[r]


def main(argv) -> int:
    def load(p):
        d = {}
        for line in open(p, encoding='utf-8-sig'):
            rid, _, t = line.rstrip('\r\n').partition('\t')
            if rid:
                d[rid] = t
        return d
    tr = load(argv[1])
    src = load(argv[2]) if len(argv) > 2 else {}
    for rid, words in mixed(tr):
        print('MIXED', rid, words)
    for w, c, r, cr in reversed_words(tr):
        print('REVERSED?', w, c, '<->', r, cr)
    if src:
        for rid, en in untranslated(src, tr):
            print('ENGLISH', rid, en[:80])
        for rid, a, b in reversed_numbers(src, tr):
            print('DIGITS', rid, a, b)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
