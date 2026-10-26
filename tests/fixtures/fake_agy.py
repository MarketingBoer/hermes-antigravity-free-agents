"""Synthetic AGY process for offline tests. Never contacts a service."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import time

control = Path(sys.argv[1])
settings = json.loads(control.read_text())
usage = '/usage' in sys.argv
prompt = '' if usage else sys.stdin.read()
with control.with_suffix('.calls').open('a') as stream:
    stream.write(json.dumps({'usage': usage, 'argv': sys.argv[2:], 'prompt': prompt}) + '\n')
mode = settings.get('mode', 'ok')
if usage:
    print('{}')
    raise SystemExit(7 if mode == 'usage-fails' else 0)
if mode == 'timeout':
    time.sleep(10)
if mode == 'malformed':
    print('not-json')
    raise SystemExit(0)
if mode == 'oversize':
    print('x' * 2000000)
    control.with_suffix('.overflow-completed').write_text('unexpected')
    raise SystemExit(0)
if mode == 'wrong-type':
    print(json.dumps({'event': 'result', 'result': {'status': 'SUCCESS', 'response': []}}))
    raise SystemExit(0)
if mode == 'tool':
    print(json.dumps({'event': 'step_update', 'step_update': {'tool_name': 'fixture-tool'}}))
response = '' if mode == 'empty' else '- Synthetic check complete.\n- HQ: no follow-up required.'
if mode == 'verbose':
    response = '- ' + 'word ' * 160
print(json.dumps({'event': 'init', 'init': {'model': 'synthetic'}}))
print(json.dumps({'event': 'result', 'result': {
    'status': 'SUCCESS', 'response': response, 'usage': {'total_tokens': 12}}}))
