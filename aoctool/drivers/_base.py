from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar

from jinja2 import Template

from aoctool.utils import Puzzle


TEMPLATE_DIR = Path(__file__).parent.with_name('templates')


class LanguageDriver(ABC):
    """Class for scaffolding and solving an AoC puzzle using a script from a particular programming language."""

    language: ClassVar[str]        # name of language
    file_extension: ClassVar[str]  # file extension used for files in the language

    @property
    def template_path(self) -> Path:
        return TEMPLATE_DIR / f'{self.language}.jinja2'

    def render_scaffold(self, puzzle: Puzzle, input_data_path: Path) -> str:
        with open(self.template_path) as f:
            template = Template(f.read())
        return template.render(language = self.language.capitalize(), puzzle = puzzle, input_data_path = str(input_data_path.resolve()))
