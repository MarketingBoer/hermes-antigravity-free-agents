#!/usr/bin/env python3
"""Run two synthetic rounds in temporary storage. No services or accounts."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='maintenance-kit-demo-') as folder:
        directory = Path(folder)
        component = directory / 'component.txt'
        component.write_text('synthetic version one')
        control = directory / 'control.json'
        control.write_text('{}')
        config = {
            'state_dir': str(directory / 'state'), 'workspace': str(directory / 'workspace'),
            'agy_command': [sys.executable, str(ROOT / 'tests/fixtures/fake_agy.py'), str(control)],
            'models': {'routine': 'fixture-routine', 'changed': 'fixture-changed'},
            'components': {'demo-component': str(component)},
            'checks': [{'name': 'demo-health', 'argv': [sys.executable, '-c', 'raise SystemExit(0)']}],
        }
        path = directory / 'config.json'
        path.write_text(json.dumps(config))
        for index in range(2):
            if index:
                component.write_text('synthetic version two')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/weekly.py'), '--config', str(path)],
                                    text=True, capture_output=True, timeout=10)
            if result.returncode:
                print('Synthetic demo failed.')
                return 1
            state = json.loads((directory / 'state/state.json').read_text())
            if state['status'] != 'ok':
                print('Synthetic demo was blocked.')
                return 1
            print(f"Synthetic round {index + 1}: {state['model']}")
            print(result.stdout.strip())
    print('Demo complete. Temporary synthetic state removed. No service contacted.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
