"""Protect the player's real saves and settings around every test run.

Ritual learned the hard way (DELTARUNE lost filech5_0 once; MI2 backed up
the wrong LOCALAPPDATA inside a sandbox):
    1. snapshot: copy + SHA-256 manifest, stored INSIDE the project
       (scratch folders get cleaned)
    2. run the test copy of the game
    3. verify: compare hashes; restore only with the user's permission if the
       player may have played since the snapshot

    python save_guard.py snapshot "%LOCALAPPDATA%\\DELTARUNE" backups\\saves_20261019
    python save_guard.py verify   "%LOCALAPPDATA%\\DELTARUNE" backups\\saves_20261019
    python save_guard.py restore  "%LOCALAPPDATA%\\DELTARUNE" backups\\saves_20261019
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

SANDBOX_HINTS = ('\\Packages\\', '/Packages/', 'sandbox')


def manifest(root: Path) -> dict[str, str]:
    out = {}
    for p in sorted(root.rglob('*')):
        if p.is_file():
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def refuse_sandbox(path: Path) -> None:
    s = str(path)
    if any(h.lower() in s.lower() for h in SANDBOX_HINTS):
        raise SystemExit(f'refusing: {s} looks like a sandbox-redirected profile, '
                         'not the real save folder the game writes to')


def snapshot(src: Path, dst: Path) -> None:
    refuse_sandbox(src)
    if dst.exists():
        raise SystemExit(f'{dst} exists; never overwrite an older backup')
    shutil.copytree(src, dst / 'files')
    (dst / 'manifest.json').write_text(json.dumps(manifest(src), indent=1), encoding='utf-8')
    print(f'snapshot of {len(manifest(src))} files -> {dst}')


def verify(src: Path, dst: Path) -> bool:
    before = json.loads((dst / 'manifest.json').read_text(encoding='utf-8'))
    now = manifest(src)
    changed = sorted(k for k in before.keys() | now.keys() if before.get(k) != now.get(k))
    for k in changed:
        print('CHANGED', k, before.get(k, 'absent')[:12], '->', now.get(k, 'absent')[:12])
    print('identical' if not changed else f'{len(changed)} files differ')
    return not changed


def restore(src: Path, dst: Path) -> None:
    refuse_sandbox(src)
    files = dst / 'files'
    for p in files.rglob('*'):
        if p.is_file():
            t = src / p.relative_to(files)
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t)
    verify(src, dst)


if __name__ == '__main__':
    cmd, a, b = sys.argv[1], Path(os.path.expandvars(sys.argv[2])), Path(sys.argv[3])
    {'snapshot': snapshot, 'verify': verify, 'restore': restore}[cmd](a, b)
