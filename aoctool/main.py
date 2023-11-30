from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from importlib import import_module
from pathlib import Path
from types import ModuleType

from aoctool.utils import validate_args


def get_command_names() -> list[str]:
    path = Path(__file__).with_name('commands')
    return [p.stem for p in path.glob('*.py') if (not p.stem.startswith('_'))]

def get_module_for_command(name: str) -> ModuleType:
    return import_module(f'aoctool.commands.{name}')


def main() -> None:
    parser = ArgumentParser(formatter_class = ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help = 'command', dest = 'command')
    for name in get_command_names():
        mod = get_module_for_command(name)
        doc = mod.__doc__ or ''
        help_str = doc[0].lower() + doc[1:].rstrip('.')
        subparser = subparsers.add_parser(name, help = help_str, description = doc, formatter_class = ArgumentDefaultsHelpFormatter)
        mod.configure_parser(subparser)
    args = parser.parse_args()
    validate_args(args)
    mod = get_module_for_command(args.command)
    mod.run(args)
