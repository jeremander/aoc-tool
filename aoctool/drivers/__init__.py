from argparse import Namespace

from aoctool.drivers._base import AoCBuilder
from aoctool.drivers.python import PythonDriver
from aoctool.drivers.rust import RustDriver
from aoctool.utils import Puzzle


DRIVERS = {
    'python': PythonDriver(),
    'rust': RustDriver(),
}

def aoc_builder_from_args(args: Namespace) -> AoCBuilder:
    driver = DRIVERS[args.language]
    puzzle = Puzzle.from_args(args)
    return AoCBuilder(driver, puzzle, args.output_dir)
