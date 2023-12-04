"""Download data from Advent of Code website."""

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pathlib import Path
import shutil

from aoctool.utils import Part, Puzzle, log, make_directory, parser_config


@dataclass
class DataDownloader:
    puzzle: Puzzle
    output_dir: Path

    @property
    def puzzle_dir(self) -> Path:
        return self.output_dir / str(self.puzzle.year) / f'{self.puzzle.day:02d}'

    @property
    def input_data_path(self) -> Path:
        return self.puzzle_dir / 'input.txt'

    def get_description_path(self, part: Part) -> Path:
        return self.puzzle_dir / f'description.part{part}.html'

    def download(self) -> None:
        log(f'Downloading puzzle data and description for {self.puzzle.date_string}')
        if (not self.puzzle_dir.exists()):
            make_directory(self.puzzle_dir)
        _ = self.puzzle.input_data  # ensures input data is downloaded
        shutil.copy(self.puzzle.input_data_path, self.input_data_path)
        log(f'Saved {self.input_data_path}')
        part = self.puzzle.current_part  # ensures description is downloaded
        description_path = self.get_description_path(part)
        prose_path_attr = f'prose{part - 1}_path'
        shutil.copy(getattr(self.puzzle, prose_path_attr), description_path)
        log(f'Saved {description_path}')


def configure_parser(parser: ArgumentParser) -> None:
    parser_config['date'](parser)
    parser_config['session'](parser)
    parser_config['output_dir'](parser)

def run(args: Namespace) -> None:
    puzzle = Puzzle.from_args(args)
    downloader = DataDownloader(puzzle, args.output_dir)
    downloader.download()