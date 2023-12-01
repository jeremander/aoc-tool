from pathlib import Path
import subprocess

import toml

from aoctool.drivers._base import LanguageDriver
from aoctool.utils import Puzzle, command2str, log


class RustDriver(LanguageDriver):

    language = 'rust'
    file_extension = 'rs'

    def make_scaffold(self, puzzle: Puzzle, input_data_path: Path, scaffold_dir: Path) -> None:
        super().make_scaffold(puzzle, input_data_path, scaffold_dir)
        # create a Cargo.toml file in the same directory as the source file
        manifest_path = scaffold_dir / 'Cargo.toml'
        src_path = self.get_src_path(puzzle, scaffold_dir)
        manifest = {
            'package': {'name': f'aoc_{src_path.stem}', 'version': '0.1.0'},
            'bin': [{'name': src_path.stem, 'path': str(src_path.relative_to(scaffold_dir))}],
            'dependencies': {},
        }
        with open(manifest_path, 'w') as f:
            toml.dump(manifest, f)
        log(f'Created {manifest_path}')

    def get_exec_path(self, src_path: Path, build_dir: Path) -> Path:
        return build_dir / 'release' / src_path.stem

    def compile_source(self, scaffold_dir: Path, src_path: Path, build_dir: Path) -> None:
        manifest_path = scaffold_dir / 'Cargo.toml'
        build_cmd = ['cargo', 'build', '--release', '--manifest-path', str(manifest_path), '--target-dir', str(build_dir)]
        build_cmd_str = command2str(build_cmd)
        log(build_cmd_str)
        subprocess.run(build_cmd)
