# `aoctool`: Advent of Code Multilingual Scaffolding Tool

`aoctool` is a command-line tool designed to help with solving daily [Advent of Code](https://adventofcode.com) puzzles in various programming languages. It sets up language-specific scaffolding so you only need to fill in certain code blocks with your main solution logic.

Currently supported languages:

- Python
- Rust
- Haskell (coming soon!)

## Installation

`aoctool` itself is written in Python. So make sure you have Python 3 and `pip` available.

To install, clone the repository:

```text
git clone https://github.com/jeremander/aoc-tool
```

Then from inside the repo,

```text
pip install .
```

TODO: make this available on PyPI.

You may have to install toolchains specific for your programming language(s) of interest. For example, with Rust you would need to have `cargo` installed, etc.

## How to use

To view the help menu and subcommands, run:

```text
aoctool --help
```

### Setting up authentication

First authenticate yourself to the AoC [website](https://adventofcode.com/2023/auth/login), then extract the session cookie from your browser. This cookie will allow `aoctool` to query the site's API.

The token will be a 128-long hex string. You have several options for making it accessible to `aoctool`:

1. Save the string to a file in your home directory called `.adventofcode.session` (with the leading dot).
2. Store the string in an environment variable called `AOC_SESSION`.
3. Pass it in directly on the command line with `--session`.

### General options

Most of the tool's subcommands will include some or all of the following arguments:

- `--year`: which year's puzzle you want to solve
- `--day`: which day of December it is
- `--session`: your session cookie for authentication
- `--language`: which programming language you want to use
- `--output-dir`: directory where output files will be saved

### Download daily puzzle

To download a puzzle, use:

```text
aoctool download
```

You can optionally provide the `--year` and `--day` to specify the puzzle date; by default it will retrieve today's puzzle (if today is in the December 1-25 range).

This will download Part 1 of the puzzle as an HTML file, along with the input data text file to be passed into your solver program. If you have already solved Part 1, it will fetch part 2.

The data will be saved into a puzzle directory (newly created if not already existent), `<output_dir>/<year>/<day>`

### Set up solution scaffold

Once you've chosen a programming language to work with, you can run:

```text
aoctool scaffold --language <language>
```

You can optionally provide the other arguments specifying the puzzle date. This will create a new subdirectory `<language>` within the puzzle directory. This directory will be populated with a source file containing the scaffold for a new puzzle solution.

As an example, suppose today is December 1, 2023. If I run:

```text
aoctool scaffold --language python
```

It will create a directory `data/2023/01/python` containing a source file `2023_01.py`, which looks like:

```python
# Advent of Code
# Date:     2023-12-01
# Language: Python

import sys
from typing import Optional, TypeAlias


# define your own Value type for the problem
Value: TypeAlias = object


##################################################

# fill these in

def parse(input_data: str) -> Optional[Value]:
    """Parse input into the Value type."""
    return None

def part1(value: Value) -> Optional[int]:
    """Solve part 1."""
    return None

def part2(value: Value) -> Optional[int]:
    """Solve part 2."""
    return None

...
```

### Solve the puzzle

Next, you would fill in the placeholders within the scaffold file in order to solve the puzzle. There are three functions which need to be filled in:

- `parse`: parses input data into some kind of data structure (which you yourself define) most appropriate for solving the puzzle
- `part1`: given the parsed data, return the solution to Part 1 of the puzzle (as an integer)
- `part2`: same as above, but for Part 2

### Compile the code

Once you think you've solved the puzzle, you can compile the code with:

```text
aoctool compile --language <language>
```

This will compile the code using the appropriate language toolchain, and place the built executable in a `build/` subdirectory of your language directory. In the case of non-compiled languages like Python, there is no real compilation to do, so it will simply copy the original source file into the `build/` directory.

#### Adding dependencies

Sometimes your code may depend on external libraries. A rudimentary attempt has been made to set up the scaffolding for a "project" so that dependencies can be added using the usual toolchains.

- **Python**: Uses [Poetry](https://python-poetry.org) to manage dependencies. A `pyproject.toml` file is provided so you can add dependencies to the `[tool.poetry.dependencies]` section manually, or use `poetry add <dependency>`.
- **Rust**: Uses [Cargo](https://doc.rust-lang.org/cargo/) to manage dependencies. A `Cargo.toml` file is provided so you can add dependencies into its `[dependencies]` section, or use `cargo add <dependency>`.
- **Haskell**: Uses `cabal` to manage dependencies. An `aoc.cabal` file is provided... TODO: implement this.

### Run the code

To run the executable, do:

```text
aoctool run --language <language>
```

If all goes well, this should print out the integer solution to the puzzle computed by your compiled code. By default, it will solve Part 1 or 2 depending on whether you've already submitted Part 1, but you can override this behavior with a `--part` option.

### Submit your solution

Once you have the integer solution, you can manually enter it on the AoC website, or you can rerun the `aoctool run` command with the additional flag `--submit`. This will upload your solution and report back whether it was successful.

### 🚧 Coming soon 🚧

- Time profiling (to compare runtime performance of different languages)
- Character/word/line counts (to compare "verbosity" of different languages)
