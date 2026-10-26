"""Exercise the adapter with real local child processes and synthetic data."""
from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/weekly.py'


class WeeklyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.control = self.root / 'control.json'
        self.component = self.root / 'component.txt'
        self.component.write_text('synthetic private content must stay local')
        self.config = {
            'state_dir': str(self.root / 'state'),
            'workspace': str(self.root / 'workspace'),
            'agy_command': [sys.executable, str(ROOT / 'tests/fixtures/fake_agy.py'), str(self.control)],
            'models': {'routine': 'fixture-routine', 'changed': 'fixture-changed'},
            'components': {'team': str(self.component)},
            'checks': [{'name': 'health', 'argv': [sys.executable, '-c', 'raise SystemExit(0)'], 'timeout_seconds': 2}],
            'analysis_timeout_seconds': 3,
        }
        self.path = self.root / 'config.json'
        self.control.write_text('{}')

    def execute(self, mode='ok', extra=()):
        self.control.write_text(json.dumps({'mode': mode}))
        self.path.write_text(json.dumps(self.config))
        result = subprocess.run([sys.executable, str(SCRIPT), '--config', str(self.path), *extra],
                                text=True, capture_output=True, timeout=15)
        return result

    def state(self):
        return json.loads((self.root / 'state/state.json').read_text())

    def calls(self):
        path = self.control.with_suffix('.calls')
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_first_run_saves_baseline_and_sends_no_file_contents(self):
        result = self.execute()
        self.assertEqual(result.returncode, 0, result.stderr)
        state = self.state()
        self.assertEqual(state['status'], 'ok')
        self.assertTrue(state['fingerprints'])
        call = next(c for c in self.calls() if not c['usage'])
        self.assertNotIn(self.component.read_text(), call['prompt'])
        self.assertNotIn(str(self.component), call['prompt'])
        self.assertNotIn(state['fingerprints']['team'], call['prompt'])
        self.assertIn('fixture-routine', call['argv'])
        self.assertNotIn('--effort', call['argv'])
        self.assertEqual((self.root / 'state/state.json').stat().st_mode & 0o777, 0o600)

    def test_saved_report_and_changes_select_changed_model(self):
        self.execute()
        old = self.state()
        self.component.write_text('changed synthetic component')
        self.execute()
        state = self.state()
        self.assertEqual(state['changed_components'], ['team'])
        self.assertEqual(state['model'], 'fixture-changed')
        self.assertEqual(state['resumed_from'], old['started_at'])
        call = [c for c in self.calls() if not c['usage']][-1]
        content = json.loads(call['prompt'])['message']['content']
        supplied = json.loads(content.split('\n', 1)[1])
        self.assertEqual(supplied['previous_report'], old['last_successful_report'])

    def test_invalid_answers_preserve_baseline_without_retry(self):
        self.execute()
        old = self.state()['fingerprints']
        self.component.write_text('changed')
        for mode in ['empty', 'malformed', 'wrong-type', 'tool', 'verbose', 'oversize']:
            with self.subTest(mode=mode):
                before = len(self.calls())
                self.assertEqual(self.execute(mode).returncode, 0)
                self.assertEqual(self.state()['status'], 'blocked')
                self.assertEqual(self.state()['fingerprints'], old)
                self.assertEqual(sum(not c['usage'] for c in self.calls()[before:]), 1)

    def test_failed_usage_never_starts_analysis(self):
        self.assertEqual(self.execute('usage-fails').returncode, 0)
        self.assertEqual(self.state()['status'], 'blocked')
        self.assertTrue(all(c['usage'] for c in self.calls()))

    def test_failed_usage_clears_previous_analysis_metadata(self):
        self.execute()
        self.assertEqual(self.state()['analysis_exit'], 0)
        self.execute('usage-fails')
        self.assertIsNone(self.state()['analysis_exit'])
        self.assertIsNone(self.state()['usage_after_exit'])
        self.assertEqual(self.state()['open_problem'], 'agy-usage')

    def test_output_limit_stops_the_child_before_it_finishes_writing(self):
        self.execute('oversize')
        self.assertEqual(self.state()['analysis_exit'], 125)
        self.assertFalse(self.control.with_suffix('.overflow-completed').exists())
        self.assertEqual(self.state()['open_problem'], 'agy-analysis')

    def test_fifo_component_does_not_block_or_start_analysis(self):
        self.component.unlink()
        os.mkfifo(self.component)
        result = self.execute()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.state()['status'], 'blocked')
        self.assertEqual(self.calls(), [])

    def test_timeout_preserves_progress(self):
        self.config['analysis_timeout_seconds'] = 1
        result = self.execute('timeout')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.state()['status'], 'blocked')
        self.assertNotIn('fingerprints', self.state())
        self.assertEqual(sum(not c['usage'] for c in self.calls()), 1)

    def test_corrupt_state_is_not_overwritten(self):
        state = self.root / 'state'
        state.mkdir()
        (state / 'state.json').write_text('broken')
        result = self.execute()
        self.assertEqual(result.returncode, 2)
        self.assertEqual((state / 'state.json').read_text(), 'broken')
        self.assertEqual(self.calls(), [])

    def test_lock_prevents_second_run(self):
        directory = self.root / 'state'
        directory.mkdir()
        with (directory / 'run.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.execute()
        self.assertEqual(result.returncode, 0)
        self.assertIn('already running', result.stdout)
        self.assertEqual(self.calls(), [])

    def test_failed_check_keeps_baseline_and_one_open_problem(self):
        self.execute()
        old = self.state()['fingerprints']
        self.component.write_text('changed')
        self.config['checks'][0]['argv'][-1] = 'print("RAW-PRIVATE-OUTPUT"); raise SystemExit(4)'
        result = self.execute()
        self.assertEqual(self.state()['fingerprints'], old)
        self.assertEqual(self.state()['open_problem'], 'health')
        self.assertEqual(self.state()['status'], 'blocked')
        self.assertNotIn('RAW-PRIVATE-OUTPUT', result.stdout)
        self.assertNotIn('RAW-PRIVATE-OUTPUT', (self.root / 'state/state.json').read_text())
        self.config['checks'][0]['argv'][-1] = 'raise SystemExit(0)'
        self.execute()
        self.assertIsNone(self.state()['open_problem'])

    def test_missing_component_blocks_without_model_call(self):
        self.component.unlink()
        result = self.execute()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.state()['status'], 'blocked')
        self.assertEqual(self.calls(), [])

    def test_validation_has_no_process_or_state_side_effects(self):
        result = self.execute(extra=('--check-config',))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'state').exists())
        self.assertEqual(self.calls(), [])

    def test_invalid_config_does_not_execute(self):
        for field, value in [('agy_command', 'shell command'), ('models', {}),
                             ('analysis_timeout_seconds', 200), ('components', {'private label!': str(self.component)})]:
            original = self.config[field]
            self.config[field] = value
            with self.subTest(field=field):
                self.assertEqual(self.execute().returncode, 2)
                self.assertEqual(self.calls(), [])
            self.config[field] = original

    def test_missing_agy_binary_is_a_short_blocked_report(self):
        self.config['agy_command'] = [str(self.root / 'missing-binary')]
        result = self.execute()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.state()['status'], 'blocked')
        self.assertNotIn(str(self.root), result.stdout)


if __name__ == '__main__':
    unittest.main()
