"""Create a scaffold for solving a puzzle in a particular programming language."""

from argparse import ArgumentParser, Namespace

from aoctool.drivers import DRIVERS, AoCBuilder
from aoctool.utils import Puzzle, make_directory, parser_config


def configure_parser(parser: ArgumentParser) -> None:
    parser_config['date'](parser)
    parser_config['language'](parser)
    parser_config['output_dir'](parser)
    parser.add_argument('-f', '--force', action = 'store_true', help = 'force overwrite of scaffold file')

def run(args: Namespace) -> None:
    driver = DRIVERS[args.language]
    puzzle = Puzzle.from_args(args)
    builder = AoCBuilder(driver, puzzle, args.output_dir)
    if (not builder.language_dir.exists()):
        make_directory(builder.language_dir)
    if builder.scaffold_path.exists() and (not args.force):
        raise ValueError(f'Refusing to overwrite scaffold file {builder.scaffold_path} (to do so, use --force)')
    builder.do_scaffold()
