from dataclasses import dataclass
from pathlib import Path

from aoctool.commands.download import DataDownloader
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
