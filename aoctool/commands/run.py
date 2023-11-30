"""Run an executable to compute the puzzle solution."""

from argparse import ArgumentParser, Namespace

from aoctool.drivers import aoc_builder_from_args
from aoctool.utils import parser_config


def configure_parser(parser: ArgumentParser) -> None:
    parser_config['date'](parser)
    parser_config['language'](parser)
    parser_config['output_dir'](parser)
    parser.add_argument('--submit', action = 'store_true', help = 'submit solution to AoC server')

def run(args: Namespace) -> None:
    builder = aoc_builder_from_args(args)
    if args.submit:
        builder.do_submit()
    else:
        builder.do_run()
