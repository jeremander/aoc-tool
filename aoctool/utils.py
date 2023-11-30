from argparse import ArgumentParser, Namespace
from datetime import datetime
import os
from pathlib import Path
import string

from aocd.models import Puzzle, User


AnyPath = str | Path

START_YEAR = 2015
DEFAULT_SESSION_KEY_PATH = Path.home() / '.adventofcode.session'


####################
# HELPER FUNCTIONS #
####################

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

# def save_file(text: str, path: AnyPath) -> None:
#     with open(path, 'w') as f:
#         f.write(text)
#     print(f'Saved {path}')


############
# ARGPARSE #
############

def configure_date_args(parser: ArgumentParser) -> None:
    now = datetime.now()
    parser.add_argument('-d', '--day', type = int, default = now.day, help = 'day of December (1-25)')
    parser.add_argument('-y', '--year', type = int, default = now.year, help = 'year')

def configure_session_arg(parser: ArgumentParser) -> None:
    parser.add_argument('-s', '--session', help = 'session key (hex string)')

def validate_args(args: Namespace) -> None:
    now = datetime.now()
    if hasattr(args, 'day'):
        assert (1 <= args.day <= 25), 'day must be in range 1-25'
    if hasattr(args, 'year'):
        assert (START_YEAR <= args.year <= now.year), f'year must be in range {START_YEAR}-{now.year}'

def get_puzzle_from_args(args: Namespace) -> Puzzle:
    if (args.session is None):
        token = get_default_session_cookie()
    else:
        token = args.session
    user = User(token)
    return Puzzle(args.year, args.day, user = user)
