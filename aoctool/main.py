"""Multilingual scaffolding for Advent of Code (AoC) puzzles."""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from importlib import import_module
from types import ModuleType

from aoctool.utils import validate_args


COMMANDS = [
    'download',
    'scaffold',
    'compile',
    'run',
]

def get_module_for_command(name: str) -> ModuleType:
    return import_module(f'aoctool.commands.{name}')

def main() -> None:
    parser = ArgumentParser(description = __doc__, formatter_class = ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help = 'command', dest = 'command')
    for name in COMMANDS:
        mod = get_module_for_command(name)
        doc = mod.__doc__ or ''
        help_str = doc[0].lower() + doc[1:].rstrip('.')
        subparser = subparsers.add_parser(name, help = help_str, description = doc, formatter_class = ArgumentDefaultsHelpFormatter)
        mod.configure_parser(subparser)
    args = parser.parse_args()
    validate_args(args)
    mod = get_module_for_command(args.command)
    mod.run(args)
