from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from importlib import import_module
from pathlib import Path

from aoctool.utils import validate_args


def get_command_names() -> list[str]:
    path = Path(__file__).with_name('commands')
    return [p.stem for p in path.glob('*.py') if (not p.stem.startswith('_'))]

def main() -> None:
    parser = ArgumentParser(formatter_class = ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(help = 'command', dest = 'command')
    for name in get_command_names():
        mod = import_module(f'aoctool.commands.{name}')
        doc = mod.__doc__ or ''
        subparser = subparsers.add_parser(name, help = doc.lower().rstrip('.'), description = doc, formatter_class = ArgumentDefaultsHelpFormatter)
        mod.configure_parser(subparser)
    args = parser.parse_args()
    validate_args(args)
    mod.run(args)
