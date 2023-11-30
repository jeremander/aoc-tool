from pathlib import Path
import shutil
import sys

from aoctool.drivers._base import LanguageDriver
from aoctool.utils import make_directory


class PythonDriver(LanguageDriver):

    language = 'python'
    file_extension = 'py'

    def get_exec_path(self, src_path: Path, build_dir: Path) -> Path:
        return build_dir / src_path.name

    def compile_source(self, src_path: Path, build_dir: Path) -> None:
        exec_path = self.get_exec_path(src_path, build_dir)
        if (not build_dir.exists()):
            make_directory(build_dir)
        shutil.copy(src_path, exec_path)

    def get_run_args(self, exec_path: Path) -> list[str]:
        return [sys.executable, str(exec_path)]
