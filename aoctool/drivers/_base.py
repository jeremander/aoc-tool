from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any, ClassVar, NamedTuple, Optional, TypeAlias

import aocd
from jinja2 import Template
import subprocess_tee

from aoctool.utils import Part, Puzzle, command2str, log, make_directory, write_file


# type for compile-time diagnostics
CompileInfo: TypeAlias = dict[str, Any]

class RunResult(NamedTuple):
    solution: Optional[int]
    returncode: int
    stderr: str

# type for runtime diagnostics
RunInfo: TypeAlias = dict[str, Any]

TEMPLATE_DIR = Path(__file__).parent.with_name('templates')


class LanguageDriver(ABC):
    """Class for scaffolding and solving an AoC puzzle using a script from a particular programming language."""

    language: ClassVar[str]        # name of language
    file_extension: ClassVar[str]  # file extension used for files in the language
    is_compiled: ClassVar[bool]    # whether the language is a compiled language

    @property
    def template_dir(self) -> Path:
        """Path to the project scaffold template for the language."""
        return TEMPLATE_DIR / self.language

    def get_src_path(self, puzzle: Puzzle, scaffold_dir: Path) -> Path:
        """Given a puzzle and scaffold directory, gets the source path."""
        return scaffold_dir / f'{puzzle.name}.{self.file_extension}'

    def make_scaffold(self, puzzle: Puzzle, input_data_path: Path, scaffold_dir: Path) -> None:
        """Sets up scaffolding for a project in the given language.
        By default, renders the files in the template directory into the scaffold directory."""
        log(f'Rendering {self.template_dir}')
        kwargs = {
            'language': self.language.capitalize(),
            'puzzle': puzzle,
            'input_data_path': str(input_data_path.resolve()),
        }
        for path in self.template_dir.rglob('*'):
            if path.is_file():
                # apply substitutions in filename itself
                template_path = path.with_name(path.name.format(**kwargs))
                with open(path) as f:
                    template = Template(f.read())
                scaffold = template.render(**kwargs)
                dest_path = scaffold_dir / str(template_path.relative_to(self.template_dir))
                write_file(scaffold, dest_path)

    def get_exec_path(self, src_path: Path, build_dir: Path) -> Path:
        """Given the source path and build directory, gets a path to the file that will be compiled."""
        return build_dir / src_path.stem

    @abstractmethod
    def compile_source(self, scaffold_dir: Path, src_path: Path, build_dir: Path) -> None:
        """Given a scaffold directory, source path, and build directory, compiles the source into an executable.
        The executable path should be the result of `self.get_exec_path(src_path, build_dir)`."""

    def get_run_args(self, exec_path: Path) -> list[str]:
        """Given an executable path, gets a list of arguments which will be run as a subprocess.
        An additional argument, either '1' or '2', will be appended indicating which part of the puzzle to run.
        When run, the command will write integer output to stdout, and diagnostic info to stderr."""
        # by default, simply call the executable itself
        return [str(exec_path)]

    def parse_run_info(self, stderr: str) -> RunInfo:
        return {}


@dataclass
class AoCBuilder:
    """Class which performs the scaffolding, building, and running an AoC puzzle for a particular programmming language."""
    driver: LanguageDriver
    puzzle: Puzzle
    output_dir: Path

    @property
    def puzzle_dir(self) -> Path:
        """Path to the day's puzzle directory."""
        return self.output_dir / str(self.puzzle.year) / f'{self.puzzle.day:02d}'

    @property
    def input_data_path(self) -> Path:
        """Path to the input data file for the day's puzzle."""
        return self.puzzle_dir / 'input.txt'

    @property
    def scaffold_dir(self) -> Path:
        """Subdirectory of the puzzle directory for the specified language."""
        return self.puzzle_dir / self.driver.language

    @property
    def src_path(self) -> Path:
        """Path to the scaffolded source file."""
        return self.driver.get_src_path(self.puzzle, self.scaffold_dir)

    @property
    def build_dir(self) -> Path:
        """Build directory for compiled executables and other artifacts for the specified language."""
        return self.scaffold_dir / 'build'

    @property
    def exec_path(self) -> Path:
        return self.driver.get_exec_path(self.src_path, self.build_dir)

    @property
    def run_info_path(self) -> Path:
        """Path to the run info JSON file."""
        return self.scaffold_dir / 'run_info.json'

    def do_scaffold(self, force: bool = False) -> None:
        """Renders the scaffold template to a source file.
        If force = False, will refuse to clobber an existing scaffold directory."""
        if self.scaffold_dir.exists():
            if (not force):
                raise ValueError(f'Refusing to overwrite scaffold directory {self.scaffold_dir} (to do so, use --force)')
            log(f'Deleting {self.scaffold_dir}')
            shutil.rmtree(self.scaffold_dir)
        make_directory(self.scaffold_dir)
        log(f'Created scaffold project directory {self.scaffold_dir}')
        self.driver.make_scaffold(self.puzzle, self.input_data_path, self.scaffold_dir)
        src_path = self.driver.get_src_path(self.puzzle, self.scaffold_dir)
        log(f'To solve the puzzle, edit the code in: {src_path}')

    def do_compile(self) -> None:
        """Compiles the source file to an executable."""
        if (not self.src_path.exists()):
            raise FileNotFoundError(self.src_path)
        if self.driver.is_compiled:
            if (not self.build_dir.exists()):
                make_directory(self.build_dir)
            log(f'Compiling source file {self.src_path}')
        else:
            log(f'No compilation required ({self.driver.language} is a dynamic language)')
        self.driver.compile_source(self.scaffold_dir, self.src_path, self.build_dir)
        exec_path = self.driver.get_exec_path(self.src_path, self.build_dir)
        if (not exec_path.exists()):
            raise RuntimeError(f'Failed to compile {self.src_path}')
        if self.driver.is_compiled:
            log(f'Compiled to executable {exec_path}')
        else:
            log(f'Executable script is {exec_path}')

    def _get_run_result(self, part: Optional[Part] = None, profile: bool = False) -> RunResult:
        part = part or self.puzzle.current_part
        log(f'Computing solution for part {part} of the puzzle')
        if (not self.exec_path.exists()):
            raise FileNotFoundError(self.exec_path)
        args = self.driver.get_run_args(self.exec_path) + [str(part)]
        cmd_str = command2str(args)
        log(f'Running executable {self.exec_path}\n\n{cmd_str}\n')
        run = subprocess.run if profile else subprocess_tee.run
        proc = run(args, capture_output = True)  # type: ignore
        if (proc.returncode == 0):  # assume last line of output is the integer solution
            output_lines = proc.stdout.strip().splitlines()
            solution = int(output_lines[-1])
        else:
            solution = None
        return RunResult(solution, proc.returncode, proc.stderr)

    def do_run(self, part: Optional[Part] = None, profile: bool = False) -> None:
        """Runs the executable, printing out the solution to stdout.
        If profile = True, will compute runtime diagnostics and save them to a JSON file."""
        result = self._get_run_result(part = part, profile = profile)
        if (result.returncode == 0):
            if profile:
                run_info = self.driver.parse_run_info(result.stderr)
                log(f'Saving run info to {self.run_info_path}')
                with open(self.run_info_path, 'w') as f:
                    json.dump(run_info, f, indent = 4)
                print(result.solution)
        else:
            if profile:
                print(result.stderr, file = sys.stderr)
            print('❌')

    def do_submit(self, profile: bool = False) -> None:
        """Runs the executable to obtain the solution, then submits it to the AoC server."""
        result = self._get_run_result(profile = profile)
        if (result.returncode == 0):
            log(f'Submitting solution {result.solution}')
            part = 'a' if (self.puzzle.current_part == 1) else 'b'
            aocd.submit(result.solution, part = part, day = self.puzzle.day, year = self.puzzle.year)
        else:
            raise ValueError('Failed to compute a valid solution to the puzzle')
