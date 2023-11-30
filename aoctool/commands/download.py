"""Download data from Advent of Code site."""

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pathlib import Path
import shutil

from aocd.models import Puzzle

from aoctool.utils import configure_date_args, configure_session_arg, get_puzzle_from_args


@dataclass
class DataDownloader:
    puzzle: Puzzle
    output_dir: Path

    @property
    def puzzle_dir(self) -> Path:
        return self.output_dir / f'{self.puzzle.year}_{self.puzzle.day:02d}'

    def download(self) -> None:
        if (not self.puzzle_dir.exists()):
            print(f'Creating {self.puzzle_dir}')
            self.puzzle_dir.mkdir(parents = True)
        _ = self.puzzle.input_data  # ensures data is downloaded
        input_data_path = self.puzzle_dir / 'input.txt'
        shutil.copy(self.puzzle.input_data_path, input_data_path)
        print(f'Saved {input_data_path}')
        description_path = self.puzzle_dir / 'description.html'
        shutil.copy(self.puzzle.prose0_path, description_path)
        print(f'Saved {description_path}')


def configure_parser(parser: ArgumentParser) -> None:
    configure_date_args(parser)
    configure_session_arg(parser)
    parser.add_argument('-o', '--output-dir', default = 'data', help = 'output root directory')

def run(args: Namespace) -> None:
    puzzle = get_puzzle_from_args(args)
    downloader = DataDownloader(puzzle, Path(args.output_dir))
    downloader.download()