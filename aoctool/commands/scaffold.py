from argparse import ArgumentParser, Namespace
from pathlib import Path

from aoctool.drivers import DRIVERS
from aoctool.utils import Puzzle, make_directory, parser_config, write_file


def configure_parser(parser: ArgumentParser) -> None:
    parser_config['date'](parser)
    parser_config['language'](parser)
    parser_config['output_dir'](parser)
    parser.add_argument('-f', '--force', action = 'store_true', help = 'force overwrite of scaffold file')

def run(args: Namespace) -> None:
    puzzle = Puzzle.from_args(args)
    driver = DRIVERS[args.language]
    puzzle_dir = Path(args.output_dir) / puzzle.name
    input_data_path = puzzle_dir / 'input.txt'
    language_dir = puzzle_dir / args.language
    if (not language_dir.exists()):
        make_directory(language_dir)
    scaffold_path = language_dir / f'{puzzle.name}.{driver.file_extension}'
    if scaffold_path.exists() and (not args.force):
        raise ValueError(f'Refusing to overwrite scaffold file {scaffold_path} (to do so, use --force)')
    print(f'Rendering {driver.template_path} to {scaffold_path}')
    scaffold = driver.render_scaffold(puzzle, input_data_path)
    write_file(scaffold, scaffold_path)
