# Advent of Code
# Date:     {{puzzle.date_string}}
# Language: {{language}}

import argparse
from typing import Optional, TypeAlias

from aoc{{puzzle.year}}{{'%02d' % puzzle.day}} import parse, part1, part2


INPUT_DATA_PATH = '{{input_data_path}}'

solve_funcs = {1: part1, 2: part2}

def solve(part: int) -> Optional[int]:
    solver = solve_funcs[part]
    with open(INPUT_DATA_PATH) as f:
        input_data = f.read()
    value = parse(input_data)
    if (value is None):
        raise NotImplementedError
    return solver(value)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Run Advent of Code puzzle for {{puzzle.date_string}}')
    parser.add_argument('part', type = int, choices = (1, 2), help = 'which part of the puzzle to run')
    args = parser.parse_args()
    solution = solve(args.part)
    if (solution is None):
        exit(1)
    else:
        print(solution)
