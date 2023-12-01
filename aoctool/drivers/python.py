from pathlib import Path
import subprocess

from aoctool.drivers._base import LanguageDriver
from aoctool.utils import Puzzle, command2str, log


class PythonDriver(LanguageDriver):

    language = 'python'
    file_extension = 'py'

    def make_scaffold(self, puzzle: Puzzle, input_data_path: Path, scaffold_dir: Path) -> None:
        super().make_scaffold(puzzle, input_data_path, scaffold_dir)
        manifest_path = scaffold_dir / 'pyproject.toml'
        src_path = self.get_src_path(puzzle, scaffold_dir)
        # use 'poetry init' to create a pyproject.toml file in the same directory as the source file
        name = f'aoc_{src_path.stem}'
        cmd = ['poetry', 'init', '--no-interaction', '--name', name, '--directory', str(scaffold_dir)]
        cmd_str = command2str(cmd)
        log(cmd_str)
        subprocess.run(cmd)
        assert manifest_path.exists()
        log(f'Created {manifest_path}')

    def get_exec_path(self, src_path: Path, build_dir: Path) -> Path:
        return src_path

    def compile_source(self, scaffold_dir: Path, src_path: Path, build_dir: Path) -> None:
        pass

    def get_run_args(self, exec_path: Path) -> list[str]:
        return ['poetry', 'run', 'python', str(exec_path)]
