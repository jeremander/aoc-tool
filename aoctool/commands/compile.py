"""Compile a source file to an executable for a particular programming language."""

from argparse import ArgumentParser, Namespace

from aoctool.drivers import DRIVERS, AoCBuilder
from aoctool.utils import Puzzle, parser_config


def configure_parser(parser: ArgumentParser) -> None:
    parser_config['date'](parser)
    parser_config['language'](parser)
    parser_config['output_dir'](parser)

def run(args: Namespace) -> None:
    driver = DRIVERS[args.language]
    puzzle = Puzzle.from_args(args)
    builder = AoCBuilder(driver, puzzle, args.output_dir)
    builder.do_compile()
