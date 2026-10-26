#!/usr/bin/env python3
"""Check an explicit public file selection. Never print matched secret text."""
from __future__ import annotations

import argparse
import ipaddress
from pathlib import Path
import re

PATTERNS = {
    'personal-home-path': re.compile(r'/(?:home|Users)/[A-Za-z0-9_.-]+(?:/|\b)'),
    'email-address': re.compile(r'[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
    'private-key': re.compile(r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----'),
    'common-api-key': re.compile(r'\b(?:sk-(?:proj-)?[A-Za-z0-9_-]{24,}|AIza[A-Za-z0-9_-]{30,}|gh[pousr]_[A-Za-z0-9_]{24,})'),
    'bot-token': re.compile(r'\b\d{6,12}:[A-Za-z0-9_-]{25,}\b'),
    'chat-or-session-id': re.compile(r'\b\d{10,20}\b'),
    'credential-assignment': re.compile(r'''(?i)\b(?:api_key|access_token|password|secret)\s*[=:]\s*["']?[A-Za-z0-9_/-]{16,}'''),
}
IPV4 = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')


def check(root, denylist=()):
    manifest = root / 'PUBLIC_FILES.txt'
    selected = manifest.read_text(encoding='utf-8').splitlines()
    issues = []
    if not selected or len(selected) != len(set(selected)):
        return ['PUBLIC_FILES.txt: empty or duplicate selection']
    safe = set()
    for name in selected:
        path = Path(name)
        if not name or path.is_absolute() or '..' in path.parts or path.as_posix() != name:
            issues.append('PUBLIC_FILES.txt: invalid relative path')
            continue
        safe.add(name)
        target = root / path
        if any(part.is_symlink() for part in [target, *target.parents] if part != root.parent):
            issues.append(f'{name}: symlink is not permitted')
            continue
        if not target.is_file():
            issues.append(f'{name}: selected file is missing')
            continue
        if target.stat().st_size > 1000000:
            issues.append(f'{name}: file exceeds review size limit')
            continue
        try:
            content = target.read_text(encoding='utf-8')
        except UnicodeError:
            issues.append(f'{name}: expected UTF-8 text')
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                issues.append(f'{name}: {label}')
        for candidate in IPV4.findall(content):
            try:
                address = ipaddress.ip_address(candidate)
                if address.is_private and not address.is_loopback:
                    issues.append(f'{name}: private-network-address')
            except ValueError:
                pass
        if any(term.casefold() in content.casefold() for term in denylist if term):
            issues.append(f'{name}: private-review-marker')
    if 'PUBLIC_FILES.txt' not in safe:
        issues.append('PUBLIC_FILES.txt: must include itself')
    for path in root.rglob('*'):
        parts = path.relative_to(root).parts
        if '.git' in parts or '__pycache__' in parts:
            continue
        name = path.relative_to(root).as_posix()
        if path.is_symlink() and name not in safe:
            issues.append(f'{name}: unselected symlink')
        elif path.is_file() and name not in safe:
            issues.append(f'{name}: file is outside the public selection')
    return sorted(set(issues))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--denylist', type=Path, help='Optional private file with one exact review marker per line')
    args = parser.parse_args()
    try:
        denylist = args.denylist.read_text(encoding='utf-8').splitlines() if args.denylist else []
        issues = check(args.root.resolve(), denylist)
    except OSError:
        print('Package check failed: a required local file cannot be read.')
        return 1
    if issues:
        print('\n'.join(issues))
        return 1
    print('Public selection and heuristic privacy checks passed. Manual review remains required.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
