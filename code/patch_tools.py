"""Guarded binary edits, range patches and player-side installers.

Principles (Chrono Trigger, WA2-5, MI1-MI5, Tales, Harvest Moon):
  * never touch the original; work on a copy, keep ORIGINAL hash in a manifest
  * every in-place edit verifies the EXACT expected old bytes first
  * a distributable patch contains only differences, never game files
  * install = verify source hash -> write temp -> verify result hash ->
    atomic swap; uninstall = reverse patch (or saved backup) -> verify hash
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import zlib
from pathlib import Path


def sha256(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(chunk)
            if not b:
                return h.hexdigest()
            h.update(b)


def patch_bytes(path: str | Path, offset: int, expected: bytes, new: bytes) -> None:
    """Equal-length in-place patch that refuses to run on an unknown file."""
    if len(expected) != len(new):
        raise ValueError('equal-length patches only; use a relocation strategy otherwise')
    with open(path, 'r+b') as f:
        f.seek(offset)
        old = f.read(len(expected))
        if old == new:
            return                                  # already applied (idempotent)
        if old != expected:
            raise RuntimeError(f'{path}@{offset:#x}: expected {expected.hex()} found {old.hex()}')
        f.seek(offset)
        f.write(new)


def diff_ranges(a: bytes, b: bytes, merge_gap: int = 64) -> list[tuple[int, bytes]]:
    """Changed ranges of b relative to a (b may be longer: tail is one range).
    Ranges closer than merge_gap bytes are merged (WA5 mkrelease rule)."""
    out, i, n = [], 0, min(len(a), len(b))
    while i < n:
        if a[i] != b[i]:
            j = i
            last = i
            while j < n and (j - last) <= merge_gap:
                if a[j] != b[j]:
                    last = j
                j += 1
            out.append((i, b[i:last + 1]))
            i = last + 1
        else:
            i += 1
    if len(b) > len(a):
        out.append((len(a), b[len(a):]))
    return out


def make_patch(orig: Path, built: Path, out: Path, signature: str = 'ARPATCH1') -> dict:
    a, b = orig.read_bytes(), built.read_bytes()
    ranges = diff_ranges(a, b)
    payload = b''.join(d for _, d in ranges)
    manifest = {
        'signature': signature,
        'source': {'size': len(a), 'sha256': hashlib.sha256(a).hexdigest()},
        'result': {'size': len(b), 'sha256': hashlib.sha256(b).hexdigest()},
        'ranges': [[off, len(d)] for off, d in ranges],
        'payload_sha256': hashlib.sha256(payload).hexdigest(),
    }
    blob = json.dumps(manifest).encode()
    out.write_bytes(len(blob).to_bytes(4, 'little') + blob + zlib.compress(payload, 9))
    return manifest


def apply_patch(patch: Path, target: Path) -> str:
    raw = patch.read_bytes()
    n = int.from_bytes(raw[:4], 'little')
    m = json.loads(raw[4:4 + n])
    payload = zlib.decompress(raw[4 + n:])
    if hashlib.sha256(payload).hexdigest() != m['payload_sha256']:
        raise RuntimeError('patch payload corrupted')
    cur = sha256(target)
    if cur == m['result']['sha256']:
        return 'already-installed'
    if cur != m['source']['sha256']:
        raise RuntimeError('unsupported game version (hash mismatch); nothing written')
    tmp = target.with_name(target.name + '.ar_tmp')
    shutil.copyfile(target, tmp)
    with open(tmp, 'r+b') as f:
        f.truncate(m['result']['size'])
        pos = 0
        for off, ln in m['ranges']:
            f.seek(off)
            f.write(payload[pos:pos + ln])
            pos += ln
    if sha256(tmp) != m['result']['sha256']:
        tmp.unlink()
        raise RuntimeError('result hash mismatch; original untouched')
    bak = target.with_name(target.name + '.ar_old')
    os.replace(target, bak)          # swap; a crash here is recoverable from .ar_old
    os.replace(tmp, target)
    return 'installed (backup: %s)' % bak.name


if __name__ == '__main__':
    import tempfile
    d = Path(tempfile.mkdtemp())
    (d / 'orig.bin').write_bytes(b'HELLO WORLD' * 100)
    (d / 'new.bin').write_bytes(b'HELLO WORLD' * 50 + b'HELLO ARABI' + b'HELLO WORLD' * 49 + b'TAIL')
    make_patch(d / 'orig.bin', d / 'new.bin', d / 'p.bin')
    shutil.copy(d / 'orig.bin', d / 'game.bin')
    print(apply_patch(d / 'p.bin', d / 'game.bin'))
    print('ok' if (d / 'game.bin').read_bytes() == (d / 'new.bin').read_bytes() else 'FAIL')
    print(apply_patch(d / 'p.bin', d / 'game.bin'))
