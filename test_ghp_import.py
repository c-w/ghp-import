import os
import shutil
import stat
import subprocess
import tempfile
import unittest

from ghp_import import GhpError, ghp_import


def remove_readonly(func, path, exc_info):
    # Git creates read-only object files on Windows.
    os.chmod(path, stat.S_IWRITE)
    func(path)


class ImportTests(unittest.TestCase):
    def setUp(self):
        repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, repo, onerror=remove_readonly)
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(repo)
        subprocess.check_call(['git', 'init', '-q'])
        subprocess.check_call(['git', 'config', 'user.name', 'Test'])
        subprocess.check_call(
            ['git', 'config', 'user.email', 'test@example.org'])
        os.makedirs(os.path.join('site', 'assets'))
        with open(os.path.join('site', 'assets', 'style.css'), 'wb') as f:
            f.write(b'body {}')

    def test_prefix_in_git_tree(self):
        prefix = os.path.join('docs', 'v1')
        ghp_import('site')
        ghp_import('site', prefix=prefix, nojekyll=True)
        paths = subprocess.check_output(
            ['git', 'ls-tree', '-r', '--name-only', 'gh-pages']).splitlines()
        self.assertEqual(paths, [
            b'assets/style.css',
            b'docs/v1/.nojekyll',
            b'docs/v1/assets/style.css',
        ])
        os.remove(os.path.join('site', 'assets', 'style.css'))
        ghp_import('site', prefix=prefix)
        self.assertEqual(subprocess.check_output(
            ['git', 'ls-tree', '-r', '--name-only', 'gh-pages']).splitlines(),
            [b'assets/style.css'])

    def test_failed_import_raises_ghp_error(self):
        for size in (0, 256 * 1024):
            with open(os.path.join('site', 'index.html'), 'wb') as f:
                f.write(b'x' * size)
            with self.assertRaises(GhpError) as error:
                ghp_import('site', branch='bad..name')
            self.assertIn('fast-import', error.exception.message)
