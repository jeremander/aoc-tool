from pathlib import Path

import pytest

from aoctool.utils import command2str, log, write_file


def test_log(capsys):
    log('Hello')
    result = capsys.readouterr()
    assert result.out == ''
    assert result.err == 'Hello\n'

def test_write_file(tmpdir, capsys):
    path = tmpdir / 'out.text'
    write_file('Hello', Path(path))
    with open(path) as f:
        assert f.read() == 'Hello'
    assert capsys.readouterr().err == f'Saved {path}\n'

@pytest.mark.parametrize(['cmd', 'cmd_str'], [
    (['prog', 'arg1', '--arg2'], 'prog arg1 --arg2'),
    (['prog', 'two parts'], "prog 'two parts'"),
])
def test_command2str(cmd, cmd_str):
    assert command2str(cmd) == cmd_str
