"""Failure-path checks for the desktop builder; no network or game mutations."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('builder', Path(__file__).resolve().parents[1] / 'desktop/compiler.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuilderChecks(unittest.TestCase):
    def test_deploy_stops_on_failed_test(self):
        calls = []
        with patch.object(builder, 'build', lambda log: calls.append('build')), \
             patch.object(builder, 'test', side_effect=RuntimeError('failed')), \
             patch.object(builder, 'package', lambda log: calls.append('package')), \
             patch.object(builder, 'run', lambda log: calls.append('run')):
            with self.assertRaisesRegex(RuntimeError, 'failed'):
                builder.deploy()
        self.assertEqual(calls, ['build'])

    def test_deploy_order(self):
        calls = []
        with patch.object(builder, 'build', lambda log: calls.append('build')), \
             patch.object(builder, 'test', lambda log: calls.append('test')), \
             patch.object(builder, 'package', lambda log: calls.append('package')), \
             patch.object(builder, 'run', lambda log: calls.append('run')):
            builder.deploy()
        self.assertEqual(calls, ['build', 'test', 'package', 'run'])

    def test_checksum_failure_removes_bad_download(self):
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            name = f'electron-v{builder.ELECTRON}-win32-x64.zip'
            archive = cache / name
            archive.write_bytes(b'damaged archive')
            (cache / f'SHASUMS256-v{builder.ELECTRON}.txt').write_text('0' * 64 + '  ' + name)
            with patch.object(builder, 'CACHE', cache), patch.object(builder, 'download') as download:
                with self.assertRaisesRegex(RuntimeError, 'checksum mismatch'):
                    builder.runtime(lambda message: None)
                download.assert_not_called()
            self.assertFalse(archive.exists())

    def test_package_rejects_invalid_build_without_touching_existing_zip(self):
        with tempfile.TemporaryDirectory() as folder:
            archive = Path(folder) / 'existing.zip'
            archive.write_bytes(b'previous good package')
            with patch.object(builder, 'ARCHIVE', archive), \
                 patch.object(builder, 'verify_build', side_effect=RuntimeError('stale build')):
                with self.assertRaisesRegex(RuntimeError, 'stale build'):
                    builder.package()
            self.assertEqual(archive.read_bytes(), b'previous good package')

    def test_invalid_pe_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / 'fake.exe'
            file.write_bytes(b'not a Windows executable')
            with self.assertRaisesRegex(RuntimeError, 'Invalid Windows executable'):
                builder.verify_pe(file)


if __name__ == '__main__':
    unittest.main()
