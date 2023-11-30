from pathlib import Path

from aoctool.drivers._base import LanguageDriver


class PythonDriver(LanguageDriver):

    language = 'python'
    file_extension = 'py'

    def compile_source(self, src_path: Path, build_dir: Path) -> Path:
        print('(Python has no compilation, so do nothing)')
        return src_path
