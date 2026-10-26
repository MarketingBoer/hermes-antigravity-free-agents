#!/usr/bin/env python3
"""Synthetic native CLI for on-demand consultation tests. No network access."""
import json
import os
from pathlib import Path
import sys

control = Path(os.environ['CONSULT_FIXTURE_CONTROL'])
settings = json.loads(control.read_text())
args = sys.argv[1:]
kind = 'models' if args == ['models'] else 'usage' if '/usage' in args else 'analysis'
prompt = sys.stdin.read() if kind == 'analysis' else ''
with control.with_suffix('.calls').open('a') as stream:
    stream.write(json.dumps({'kind': kind, 'args': args, 'prompt': prompt}) + '\n')
mode = settings.get('mode', 'ok')
if kind == 'models':
    print('gemini-fixture-low\tSynthetic Gemini')
    print('claude-fixture\tSynthetic Claude')
elif kind == 'usage':
    if mode == 'usage-malformed':
        print('{}')
    else:
        print(json.dumps({'status': 'SUCCESS', 'command': {'name': 'usage', 'data': {'groups': [
            {'buckets': [{'id': 'gemini-weekly', 'remaining_fraction': 0 if mode == 'empty-quota' else 0.8}]},
            {'buckets': [{'id': '3p-weekly', 'remaining_fraction': 0 if mode == 'empty-third-party' else 0.9}]}
        ]}}}))
else:
    if mode == 'analysis-fails':
        raise SystemExit(9)
    model = args[args.index('--model') + 1]
    print(json.dumps({'event': 'init', 'init': {'model': 'unexpected-model' if mode == 'wrong-model' else model}}))
    if mode in ('tool', 'helper'):
        print(json.dumps({'event': 'step_update', 'step_update':
                         {'step_type': 'tool'} if mode == 'tool' else {'subagent_info': {'subagents': [{}]}}}))
    print(json.dumps({'event': 'result', 'result': {'status': 'SUCCESS',
        'response': '' if mode == 'empty-answer' else 'Synthetic finding: the example needs an empty-input check.',
        'usage': {'total_tokens': 0 if mode == 'zero-tokens' else 24}}}))
