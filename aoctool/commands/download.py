"""Download data from Advent of Code website."""

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pathlib import Path
import shutil

from aoctool.utils import Puzzle, make_directory, parser_config


@dataclass
class DataDownloader:
    puzzle: Puzzle
    output_dir: Path

    @property
    def puzzle_dir(self) -> Path:
        return self.output_dir / self.puzzle.name

    def download(self) -> None:
        if (not self.puzzle_dir.exists()):
            make_directory(self.puzzle_dir)
        _ = self.puzzle.input_data  # ensures data is downloaded
        input_data_path = self.puzzle_dir / 'input.txt'
        shutil.copy(self.puzzle.input_data_path, input_data_path)
        print(f'Saved {input_data_path}')
        description_path = self.puzzle_dir / 'description.html'
        shutil.copy(self.puzzle.prose0_path, description_path)
        print(f'Saved {description_path}')


def configure_parser(parser: ArgumentParser) -> None:
    parser_config['date'](parser)
    parser_config['session'](parser)
    parser_config['output_dir'](parser)

def run(args: Namespace) -> None:
    puzzle = Puzzle.from_args(args)
    downloader = DataDownloader(puzzle, Path(args.output_dir))
    downloader.download()