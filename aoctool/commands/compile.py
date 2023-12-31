"""Compile a source file to an executable for a particular programming language."""

from argparse import ArgumentParser, Namespace

from aoctool.drivers import aoc_builder_from_args
from aoctool.utils import parser_config


def configure_parser(parser: ArgumentParser) -> None:
    parser_config['date'](parser)
    parser_config['language'](parser)
    parser_config['output_dir'](parser)

def run(args: Namespace) -> None:
    builder = aoc_builder_from_args(args)
    builder.do_compile()
