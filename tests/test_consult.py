"""Test the on-demand CLI through real synthetic subprocesses."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ConsultTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'workspace'
        role = self.workspace / '.agents/agents/hermes-consultant/agent.md'
        role.parent.mkdir(parents=True)
        role.write_text('---\nname: hermes-consultant\ntools: []\n---\nUse no tools.\n')
        self.binary = self.root / 'fake-agy'
        shutil.copyfile(ROOT / 'tests/fixtures/fake_consult.py', self.binary)
        self.binary.chmod(0o700)
        self.control = self.root / 'control.json'
        self.task = {'question': 'Review the supplied synthetic function.', 'context': 'def first(items): return items[0]'}

    def execute(self, mode='ok', model='gemini-fixture-low', task=None):
        self.control.write_text(json.dumps({'mode': mode}))
        return subprocess.run([sys.executable, str(ROOT / 'scripts/consult.py'),
            '--agy', str(self.binary), '--workspace', str(self.workspace), '--model', model],
            input=json.dumps(self.task if task is None else task), text=True, capture_output=True,
            env=dict(os.environ, HOME=str(self.root), CONSULT_FIXTURE_CONTROL=str(self.control)), timeout=10)

    def calls(self):
        path = self.control.with_suffix('.calls')
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_one_explicit_model_call_returns_evidence_receipt(self):
        run = self.execute()
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        receipt = json.loads(run.stdout)
        self.assertEqual(receipt['status'], 'ok')
        self.assertEqual(receipt['model'], 'gemini-fixture-low')
        self.assertEqual(receipt['total_tokens'], 24)
        self.assertEqual([call['kind'] for call in self.calls()], ['models', 'usage', 'analysis'])
        analysis = self.calls()[-1]
        self.assertNotIn('--dangerously-skip-permissions', analysis['args'])
        self.assertNotIn('--effort', analysis['args'])
        self.assertIn('hermes-consultant', analysis['args'])
        self.assertIn(self.task['context'], analysis['prompt'])

    def test_unavailable_model_starts_no_inference(self):
        run = self.execute(model='claude-unavailable')
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)['reason'], 'model-unavailable')
        self.assertEqual([call['kind'] for call in self.calls()], ['models'])

    def test_exhausted_or_unknown_quota_starts_no_inference(self):
        for mode in ('empty-quota', 'usage-malformed'):
            with self.subTest(mode=mode):
                before = len(self.calls())
                run = self.execute(mode)
                self.assertEqual(run.returncode, 2)
                self.assertNotIn('analysis', [call['kind'] for call in self.calls()[before:]])

    def test_third_party_model_uses_its_own_quota_group(self):
        run = self.execute('empty-quota', model='claude-fixture')
        self.assertEqual(run.returncode, 0, run.stdout)
        self.assertEqual(json.loads(run.stdout)['quota_group'], '3p-weekly')
        before = len(self.calls())
        run = self.execute('empty-third-party', model='claude-fixture')
        self.assertEqual(run.returncode, 2)
        self.assertNotIn('analysis', [call['kind'] for call in self.calls()[before:]])

    def test_bad_result_or_observed_actions_are_rejected_without_retry(self):
        for mode in ('tool', 'helper', 'wrong-model', 'empty-answer', 'zero-tokens', 'analysis-fails'):
            with self.subTest(mode=mode):
                before = len(self.calls())
                run = self.execute(mode)
                self.assertEqual(run.returncode, 2)
                self.assertEqual(json.loads(run.stdout)['status'], 'blocked')
                self.assertEqual(sum(call['kind'] == 'analysis' for call in self.calls()[before:]), 1)

    def test_invalid_or_oversized_input_starts_no_commands(self):
        for task in ({'question': ''}, {'question': 'q', 'context': 'x' * 24001}, {'question': 'q', 'context': [], 'unknown': 3}):
            with self.subTest(task_type=type(task.get('context')).__name__):
                self.assertEqual(self.execute(task=task).returncode, 2)
                self.assertEqual(self.calls(), [])

    def test_missing_dedicated_role_starts_no_commands(self):
        (self.workspace / '.agents/agents/hermes-consultant/agent.md').unlink()
        self.assertEqual(self.execute().returncode, 2)
        self.assertEqual(self.calls(), [])

    def test_enabled_or_invalid_credit_settings_block_before_commands(self):
        settings = self.root / '.gemini/antigravity-cli/settings.json'
        settings.parent.mkdir(parents=True)
        for content in ('{"useG1Credits": true}', '{"useG1Credits": "false"}', 'broken'):
            settings.write_text(content)
            with self.subTest(content=content):
                run = self.execute()
                self.assertEqual(run.returncode, 2)
                self.assertEqual(self.calls(), [])

    def test_explicit_credit_opt_out_allows_native_quota_path(self):
        settings = self.root / '.gemini/antigravity-cli/settings.json'
        settings.parent.mkdir(parents=True)
        settings.write_text('{"useG1Credits": false}')
        run = self.execute()
        self.assertEqual(run.returncode, 0, run.stdout)


if __name__ == '__main__':
    unittest.main()
