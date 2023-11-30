from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from jinja2 import Template

from aoctool.utils import Puzzle, write_file


TEMPLATE_DIR = Path(__file__).parent.with_name('templates')


class LanguageDriver(ABC):
    """Class for scaffolding and solving an AoC puzzle using a script from a particular programming language."""

    language: ClassVar[str]        # name of language
    file_extension: ClassVar[str]  # file extension used for files in the language

    @property
    def template_path(self) -> Path:
        """Path to the language scaffold jinja template."""
        return TEMPLATE_DIR / f'{self.language}.jinja2'

    def render_scaffold(self, puzzle: Puzzle, input_data_path: Path) -> str:
        """Given a puzzle and input data, renders a scaffold to be saved as a source file."""
        with open(self.template_path) as f:
            template = Template(f.read())
        return template.render(language = self.language.capitalize(), puzzle = puzzle, input_data_path = str(input_data_path.resolve()))

    @abstractmethod
    def compile_source(self, src_path: Path, build_dir: Path) -> Path:
        """Given a source file and build directory, compiles the source into an executable and returns a path to the executable."""


@dataclass
class AoCBuilder:
    """Class which performs the scaffolding, building, and running an AoC puzzle for a particular programmming language."""
    driver: LanguageDriver
    puzzle: Puzzle
    output_dir: Path

    @property
    def puzzle_dir(self) -> Path:
        """Path to the day's puzzle directory."""
        return self.output_dir / self.puzzle.name

    @property
    def input_data_path(self) -> Path:
        """Path to the input data file for the day's puzzle."""
        return self.puzzle_dir / 'input.txt'

    @property
    def language_dir(self) -> Path:
        """Subdirectory of the puzzle directory for the specified language."""
        return self.puzzle_dir / self.driver.language

    @property
    def build_dir(self) -> Path:
        """Build directory for compiled executables and other artifacts for the specified language."""
        return self.language_dir / 'build'

    @property
    def scaffold_path(self) -> Path:
        """Path to the rendered scaffold source file."""
        return self.language_dir / f'{self.puzzle.name}.{self.driver.file_extension}'

    def do_scaffold(self) -> None:
        """Renders the scaffold template to a source file."""
        print(f'Rendering {self.driver.template_path}')
        scaffold = self.driver.render_scaffold(self.puzzle, self.input_data_path)
        write_file(scaffold, self.scaffold_path)
        print(f'Saved scaffold source file to {self.scaffold_path}')

    def do_compile(self) -> None:
        """Compiles the source file to an executable."""
        if (not self.scaffold_path.exists()):
            raise FileNotFoundError(self.scaffold_path)
        print(f'Compiling source file {self.scaffold_path}')
        exec_path = self.driver.compile_source(self.scaffold_path, self.build_dir)
        if (not exec_path.exists()):
            raise RuntimeError(f'Failed to compile {self.scaffold_path}')
        print(f'Compiled to executable {exec_path}')
