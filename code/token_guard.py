"""Compare every translated line with its source before a build.

What it catches (each one broke a real build):
  * a control code dropped or duplicated  (DELTARUNE: one missing % hangs the
    dialogue box; WA2: speaker colour code count must match)
  * codes moved to another line / line count changed (Chrono Cross, WA5)
  * numbers changed or reversed            ("06" instead of "60")
  * printf placeholders reordered          (WA4/ACF: %1 %2 order after RTL)
  * forbidden chars that are reserved font slots (MI1: | ~ # =)
  * byte length over a fixed slot          (Impostor Factory, WA2, HM)

Usage:
    python token_guard.py source.tsv translated.tsv  [--profile gamemaker]
TSV format: id<TAB>text  (one record per line; '\\n' written literally).
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

PROFILES = {
    # add your engine here; order matters (longest/most specific first)
    'generic': [r'\{[^{}]*\}', r'<[^<>]+>', r'%(?:\d+\$)?[-+ 0#]*\d*(?:\.\d+)?[sdifxXcuo]', r'%%'],
    'rpgmaker': [r'\\[A-Za-z]+\[[^\]]*\]', r'\\[A-Za-z]+', r'\\[.|!<>^{}$]'],
    # DELTARUNE: ^N pauses and & breaks are the translator's freedom ->
    # remove them from this list if you allow changing their count.
    'gamemaker': [r'\\n', r'\\[A-Za-z][0-9A-Za-z]?', r'\^\d', r'~\d', r'%%?', r'/', r'&', r'#'],
    'scumm': [r'\xFF[\x01-\xFF]', r'\^'],
    'telltale': [r'\{[^{}]*\}', r'\[[^\[\]]*\]', r'<[^<>]+>', r'\*[^*]+\*'],
}
NUM = re.compile(r'[0-9\u0660-\u0669\u06F0-\u06F9]+')
EAST = str.maketrans('٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹', '01234567890123456789')


def tokens(text: str, patterns: list[str]) -> list[str]:
    rx = re.compile('|'.join(f'(?:{p})' for p in patterns))
    return rx.findall(text)


def check(rid: str, src: str, ar: str, patterns: list[str], *, keep_order: bool = False,
          forbidden: str = '', max_bytes: int | None = None, encode=None,
          check_numbers: bool = True, check_lines: bool = True) -> list[str]:
    errs = []
    ts, ta = tokens(src, patterns), tokens(ar, patterns)
    if Counter(ts) != Counter(ta):
        missing = Counter(ts) - Counter(ta)
        extra = Counter(ta) - Counter(ts)
        errs.append(f'{rid}: codes differ; missing={dict(missing)} extra={dict(extra)}')
    elif keep_order and ts != ta:
        errs.append(f'{rid}: code order changed {ts} -> {ta}')
    if check_lines and src.count('\\n') != ar.count('\\n'):
        errs.append(f'{rid}: line count {src.count(chr(92)+"n")+1} -> {ar.count(chr(92)+"n")+1}')
    if check_numbers:                       # digits inside codes (^1, {v2}) are not numbers
        rx = re.compile('|'.join(f'(?:{p})' for p in patterns))
        ns = sorted(NUM.findall(rx.sub(' ', src).translate(EAST)))
        na = sorted(NUM.findall(rx.sub(' ', ar).translate(EAST)))
        if ns != na:
            errs.append(f'{rid}: numbers {ns} -> {na}')
    bad = sorted({c for c in ar if c in forbidden})
    if bad:
        errs.append(f'{rid}: reserved chars used {bad}')
    if max_bytes is not None and encode is not None:
        size = len(encode(ar))
        if size > max_bytes:
            errs.append(f'{rid}: {size} bytes > slot {max_bytes}')
    return errs


def read_tsv(path: str) -> dict[str, str]:
    rows = {}
    with open(path, encoding='utf-8-sig') as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip('\r\n')
            if not line or line.startswith('#'):
                continue
            rid, _, text = line.partition('\t')     # split on FIRST tab only
            if rid in rows:
                raise SystemExit(f'{path}:{n}: duplicate id {rid}')
            rows[rid] = text
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('translated')
    ap.add_argument('--profile', default='generic', choices=sorted(PROFILES))
    ap.add_argument('--keep-order', action='store_true')
    ap.add_argument('--forbidden', default='')
    a = ap.parse_args(argv)
    src, tr = read_tsv(a.source), read_tsv(a.translated)
    pats = PROFILES[a.profile] + (PROFILES['generic'] if a.profile != 'generic' else [])
    errs = []
    for rid, ar in tr.items():
        if rid not in src:
            errs.append(f'{rid}: unknown id (not in source)')
            continue
        errs += check(rid, src[rid], ar, pats, keep_order=a.keep_order, forbidden=a.forbidden)
    for e in errs:
        print(e)
    print(f'checked {len(tr)} records, {len(errs)} problems', file=sys.stderr)
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
