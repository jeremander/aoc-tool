from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path

import pytest

from aoctool.commands.download import DataDownloader
from aoctool.drivers import DRIVERS, AoCBuilder
from aoctool.utils import Part, Puzzle


@dataclass
class MockPuzzle(Puzzle):
    year: int
    day: int
    tmpdir: Path

    def __post_init__(self) -> None:
        with open(self.input_data_path, 'w') as f:
            f.write(self.input_data)
        with open(self.prose0_path, 'w') as f:
            f.write(self.prose0)

    @property
    def input_data_path(self) -> Path:
        return self.tmpdir / 'input_data.txt'

    @property
    def prose0_path(self) -> Path:
        return self.tmpdir / 'prose0.txt'

    @property
    def input_data(self) -> str:
        return 'input_data'

    @property
    def prose0(self) -> str:
        return 'prose0'

    @property
    def current_part(self) -> Part:
        return 1

def test_download(tmpdir, capsys):
    puzzle = MockPuzzle(2023, 1, tmpdir)
    downloader = DataDownloader(puzzle, Path(tmpdir))
    assert downloader.puzzle_dir == tmpdir / '2023' / '01'
    assert not downloader.puzzle_dir.exists()
    downloader.download()
    assert downloader.puzzle_dir.exists()
    with open(downloader.input_data_path) as f:
        assert f.read() == puzzle.input_data
    description_path = downloader.get_description_path(1)
    with open(description_path) as f:
        assert f.read() == puzzle.prose0
    stderr = capsys.readouterr().err
    assert f'Saved {downloader.input_data_path}' in stderr
    assert f'Saved {description_path}' in stderr

TEST_BUILDER_PARAMS = [
    {
        'language': 'python',
        'src_path': 'aoc202301.py',
        'build_dir': 'build',
        'exec_path': 'main.py',
        'scaffold_files': ['aoc202301.py', 'main.py', 'pyproject.toml'],
        'missing_data_err': ' No such file or directory',
        'not_implemented_err': 'NotImplementedError',
    }
]

@pytest.mark.parametrize('params', TEST_BUILDER_PARAMS, ids = itemgetter('language'))
def test_builder(params, tmpdir, capsys):
    puzzle = MockPuzzle(2023, 1, tmpdir)
    language = params['language']
    driver = DRIVERS[language]
    output_dir = Path(tmpdir)
    builder = AoCBuilder(driver, puzzle, output_dir = output_dir)

    # test paths
    puzzle_dir = tmpdir / '2023' / '01'
    assert builder.puzzle_dir == puzzle_dir
    assert builder.input_data_path == puzzle_dir / 'input.txt'
    assert builder.scaffold_dir == puzzle_dir / language
    assert builder.src_path == puzzle_dir / language / params['src_path']
    assert builder.build_dir == puzzle_dir / language / params['build_dir']
    assert builder.exec_path == puzzle_dir / language / params['exec_path']

    # test scaffolding
    assert not builder.puzzle_dir.exists()
    assert not builder.input_data_path.exists()
    builder.do_scaffold()
    assert builder.scaffold_dir.exists()
    assert builder.src_path.exists()
    if driver.is_compiled:
        assert not builder.build_dir.exists()
        assert not builder.exec_path.exists()
    for filename in params['scaffold_files']:
        assert (builder.scaffold_dir / filename).exists()
    # scaffolding again fails if force = False
    with pytest.raises(ValueError, match = 'Refusing to overwrite'):
        builder.do_scaffold()
    # scaffolding again succeeds if force = True
    builder.do_scaffold(True)

    # test compilation
    builder.do_compile()
    err = capsys.readouterr().err
    if driver.is_compiled:
        assert ('Compiling source file' in err)
        assert builder.build_dir.exists()
    else:
        assert ('No compilation required' in err)
    assert builder.exec_path.exists()

    # test running
    builder.do_run()
    result = capsys.readouterr()
    # run fails because input data is missing
    assert '❌' in result.out
    assert 'Computing solution for part 1 of the puzzle' in result.err
    assert params['missing_data_err'] in result.err
    # download input data
    downloader = DataDownloader(puzzle, output_dir)
    downloader.download()
    assert downloader.input_data_path.exists()
    builder.do_run()
    result = capsys.readouterr()
    assert '❌' in result.out
    assert params['not_implemented_err'] in result.err
    # TODO: simulate filling in implementations for successful run (use regex replacements?)
