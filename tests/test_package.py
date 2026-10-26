"""Release selection and privacy checks use synthetic leaks only."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'PUBLIC_FILES.txt').write_text('PUBLIC_FILES.txt\nsample.md\n')
        self.sample = self.root / 'sample.md'
        self.sample.write_text('A synthetic public document.\n')

    def check(self):
        return subprocess.run([sys.executable, str(ROOT / 'scripts/check_package.py'), '--root', str(self.root)],
                              capture_output=True, text=True, timeout=5)

    def test_clean_selection_passes(self):
        self.assertEqual(self.check().returncode, 0)

    def test_sensitive_patterns_fail_without_echoing_data(self):
        values = ['/' + 'home' + '/synthetic-person/private',
                  'synthetic' + '@' + 'mail.invalid',
                  'sk-' + 'A' * 48,
                  '-----BEGIN ' + 'PRIVATE KEY-----',
                  '.'.join(['192', '168', '20', '31']),
                  'telegram:' + '123456' + '789012']
        for value in values:
            self.sample.write_text(value)
            with self.subTest(kind=value[:4]):
                result = self.check()
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn(value, result.stdout)

    def test_unselected_file_fails(self):
        (self.root / 'unreviewed.txt').write_text('unexpected')
        self.assertNotEqual(self.check().returncode, 0)

    def test_symlink_fails(self):
        self.sample.unlink()
        self.sample.symlink_to(self.root / 'PUBLIC_FILES.txt')
        self.assertNotEqual(self.check().returncode, 0)

    def test_missing_file_fails(self):
        self.sample.unlink()
        self.assertNotEqual(self.check().returncode, 0)

    def test_parent_path_cannot_enter_release(self):
        (self.root / 'PUBLIC_FILES.txt').write_text('PUBLIC_FILES.txt\n../outside.md\n')
        self.assertNotEqual(self.check().returncode, 0)


if __name__ == '__main__':
    unittest.main()
