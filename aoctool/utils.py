from argparse import ArgumentParser, Namespace
from datetime import datetime
import os
from pathlib import Path
import shlex
import string
import sys
from typing import Iterable, Literal

import aocd.models
from aocd.models import User


AnyPath = str | Path
Part = Literal[1, 2]

START_YEAR = 2015
DEFAULT_SESSION_KEY_PATH = Path.home() / '.adventofcode.session'

VALID_LANGUAGES = [
    'haskell',
    'python',
    'rust'
]


####################
# HELPER FUNCTIONS #
####################

def log(msg: str) -> None:
    print(msg, file = sys.stderr)

def get_default_session_cookie() -> str:
    """Gets the session cookie from the user's AOC_SESSION environment variable or default file."""
    hex_set = set(string.hexdigits)
    if ('AOC_SESSION' in os.environ):
        key = os.environ['AOC_SESSION']
    else:
        with open(DEFAULT_SESSION_KEY_PATH) as f:
            key = f.read().strip()
    assert (len(key) == 128)
    assert all(c in hex_set for c in key)
    return key

def make_directory(path: Path) -> None:
    log(f'Creating directory {path}')
    path.mkdir(parents = True)

def write_file(text: str, path: AnyPath) -> None:
    with open(path, 'w') as f:
        f.write(text)
    log(f'Saved {path}')

def command2str(cmd: Iterable[str]) -> str:
    return ' '.join(map(shlex.quote, cmd))


class Puzzle(aocd.models.Puzzle):

    @property
    def name(self) -> str:
        return f'{self.year}_{self.day:02d}'

    @property
    def date_string(self) -> str:
        return f'{self.year}-12-{self.day:02d}'

    @property
    def current_part(self) -> Part:
        """Gets the current part of the puzzle.
        If part 1 is not complete, returns 1.
        Otherwise, returns 2."""
        return 2 if self.answered_a else 1

    @classmethod
    def from_args(cls, args: Namespace) -> 'Puzzle':
        if (getattr(args, 'session', None) is None):
            token = get_default_session_cookie()
        else:
            token = args.session
        user = User(token)
        return cls(args.year, args.day, user = user)


############
# ARGPARSE #
############

def configure_date_args(parser: ArgumentParser) -> None:
    now = datetime.now()
    parser.add_argument('-y', '--year', type = int, default = now.year, help = 'year')
    parser.add_argument('-d', '--day', type = int, default = now.day, help = 'day of December (1-25)')

def configure_session_arg(parser: ArgumentParser) -> None:
    parser.add_argument('-s', '--session', help = 'session key (hex string)')

def configure_language_arg(parser: ArgumentParser) -> None:
    parser.add_argument('-l', '--language', required = True, choices = VALID_LANGUAGES, help = 'programming language of choice')

def configure_output_dir_arg(parser: ArgumentParser) -> None:
    parser.add_argument('-o', '--output-dir', type = Path, default = Path('data'), help = 'output root directory')

parser_config = {
    'date': configure_date_args,
    'session': configure_session_arg,
    'language': configure_language_arg,
    'output_dir': configure_output_dir_arg,
}

def validate_args(args: Namespace) -> None:
    now = datetime.now()
    if hasattr(args, 'day'):
        assert (1 <= args.day <= 25), 'day must be in range 1-25'
    if hasattr(args, 'year'):
        assert (START_YEAR <= args.year <= now.year), f'year must be in range {START_YEAR}-{now.year}'
