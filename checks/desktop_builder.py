"""Failure-path checks for the desktop builder; no network or game mutations."""
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('builder', Path(__file__).resolve().parents[1] / 'desktop/compiler.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuilderChecks(unittest.TestCase):
    def test_download_cleanup_with_legacy_unlink(self):
        original_unlink = Path.unlink

        # Python 3.7's signature does not accept missing_ok.
        def legacy_unlink(path):
            return original_unlink(path)

        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'runtime.zip'
            with patch.object(Path, 'unlink', legacy_unlink), \
                 patch.object(builder.urllib.request, 'urlopen', return_value=io.BytesIO(b'complete')):
                builder.download('https://example.invalid/runtime.zip', target, lambda message: None)
                self.assertEqual(target.read_bytes(), b'complete')
                self.assertFalse(target.with_suffix('.zip.part').exists())

    def test_failed_download_preserves_original_error(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'runtime.zip'
            with patch.object(builder.urllib.request, 'urlopen', side_effect=OSError('network failure')):
                with self.assertRaisesRegex(OSError, 'network failure'):
                    builder.download('https://example.invalid/runtime.zip', target, lambda message: None)
            self.assertFalse(target.with_suffix('.zip.part').exists())

    def test_stream_hash_handles_multiple_chunks(self):
        data = b'game assets' * 300000
        self.assertEqual(builder.stream_digest(io.BytesIO(data)), builder.hashlib.sha256(data).hexdigest())

    def test_archive_path_boundaries(self):
        root = Path('/runtime')
        self.assertTrue(builder.is_within(root / 'resources/app', root))
        self.assertFalse(builder.is_within(Path('/runtime-other/app'), root))

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
