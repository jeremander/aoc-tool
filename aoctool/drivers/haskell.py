from pathlib import Path
import subprocess

from aoctool.drivers._base import LanguageDriver
from aoctool.utils import Puzzle, command2str, log


class HaskellDriver(LanguageDriver):

    language = 'haskell'
    file_extension = 'hs'

    def make_scaffold(self, puzzle: Puzzle, input_data_path: Path, scaffold_dir: Path) -> None:
        super().make_scaffold(puzzle, input_data_path, scaffold_dir)
        src_path = self.get_src_path(puzzle, scaffold_dir)
        # use 'cabal init' to create a cabal file in the same directory as the source file
        name = src_path.stem
        manifest_path = scaffold_dir / f'{name}.cabal'
        cmd = ['cabal', 'init', '--non-interactive', '--exe', '--minimal', '--package-name', name, '--package-dir', str(scaffold_dir.resolve()), '--application-dir', '.', '--main-is', src_path.name]
        cmd_str = f'cd {scaffold_dir} && ' + command2str(cmd)
        log(cmd_str)
        subprocess.run(cmd, cwd = scaffold_dir, stdout = subprocess.DEVNULL)
        assert manifest_path.exists()
        log(f'Created {manifest_path}')
        # remove changelog file
        changelog_path = scaffold_dir / 'CHANGELOG.md'
        changelog_path.unlink()
        # (also needs to be removed from cabal file)
        with open(manifest_path, 'r+') as f:
            lines = [line for line in f if (not line.startswith('extra-doc-files'))]
            f.seek(0)
            f.write(''.join(lines))
            f.truncate(f.tell())

    def compile_source(self, scaffold_dir: Path, src_path: Path, build_dir: Path) -> None:
        cmd = ['cabal', 'install', '--builddir', 'build', '--installdir', 'build', '--overwrite-policy', 'always']
        cmd_str = f'cd {scaffold_dir} && ' + command2str(cmd)
        log(cmd_str)
        subprocess.run(cmd, cwd = scaffold_dir, stdout = subprocess.DEVNULL)
