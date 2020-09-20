import os
import platform
import shutil
import sys
from pathlib import Path
from subprocess import check_call
from typing import Dict, List

from setuptools import Extension
from setuptools.command.build_ext import build_ext


class NLOptBuildExtension(Extension):
    def __init__(self, name: str, version: str):
        super().__init__(name, sources=[])
        # Source dir should be at the root directory
        self.source_dir = Path(__file__).parent.absolute()
        self.version = version


class NLOptBuild(build_ext):
    def run(self):
        try:
            check_call(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed")

        for ext in self.extensions:
            if isinstance(ext, NLOptBuildExtension):
                self.build_extension(ext)

    @property
    def nlopt_dir(self):
        return Path(__file__).parent / "tern" / "nlopt"

    @property
    def config(self):
        return "Debug" if self.debug else "Release"

    def cmake_args(self, ext_dir: str):
        prefix = "NLOPT_BUILD"

        args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            # don't build for matlab and others
            "-DNLOPT_GUILE=OFF",
            "-DNLOPT_MATLAB=OFF",
            "-DNLOPT_OCTAVE=OFF"]

        if platform.system() == "Windows":
            args += [
                "-LAH",
                f'-DCMAKE_PREFIX_PATH="{prefix}"',
                f'-DCMAKE_INSTALL_PREFIX="{prefix}"'
            ]
        elif platform.system() in ("Linux", "Darwin"):
            args += [
                f"-DCMAKE_PREFIX_PATH={prefix}",
                f"-DCMAKE_INSTALL_PREFIX={prefix}",
                "-DCMAKE_INSTALL_LIBDIR=lib",
            ]
        else:
            raise RuntimeError(f"Unsupported os: {platform.system()}")

        return args

    def build_extension(self, ext: Extension):
        # - make sure path ends with delimiter
        # - required for auto-detection of auxiliary "native" libs
        ext_dir = Path(self.get_ext_fullpath(ext.name)).parent.absolute().as_posix()
        if not ext_dir.endswith(os.path.sep):
            ext_dir += os.path.sep

        if platform.system() == "Windows":
            self._build_windows(ext)
            return

        exit(1)

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + ext_dir,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += [f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={ext_dir}"]
            if sys.maxsize > 2 ** 32:
                cmake_args += ["-A", "x64"]
            build_args += (["--", "/m"])
        else:
            build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = f'{env.get("CXXFLAGS", "")} -DVERSION_INFO="{self.distribution.get_version()}"'

        build_temp = Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)

        check_call(["cmake", ext.sourcedir, *cmake_args], cwd=self.build_temp, env=env)
        check_call(["cmake", "--build", ".", *build_args], cwd=self.build_temp)

        nlopt_py = next(Path(self.build_temp).rglob("nlopt.py"))
        nlopt_py.rename(Path(ext_dir) / "__init__.py")

    def _build_windows(self, ext: NLOptBuildExtension):
        ext_dir = Path(self.get_ext_fullpath(ext.name)).parent.absolute()
        _ed = ext_dir.as_posix()
        if not _ed.endswith(os.path.sep):
            _ed += os.path.sep

        build_dir = create_directory(Path(self.build_temp))

        # package builds in 2 steps, first to compile the nlopt package and second to build the DLL
        execute_command(
            cmd=[
                "cmake",
                "-LAH",
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={_ed}",
                f"-DPYTHON_EXECUTABLE={sys.executable}",
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{self.config.upper()}={_ed}",
                "-DNLOPT_GUILE=OFF",
                "-DNLOPT_MATLAB=OFF",
                "-DNLOPT_OCTAVE=OFF",
                ext.source_dir.as_posix()
            ],
            cwd=build_dir,
            env={
                **os.environ.copy(),
                "CXXFLAGS": f'{os.environ.get("CXXFLAGS", "")} -DVERSION_INFO="{self.distribution.get_version()}"'
            })

        # build the DLL
        execute_command([
            'cmake',
            '--build',
            '.',
            '--config',
            self.config,
            "--",
            "-m"
        ], cwd=build_dir)

        # Copy over the important bits
        nlopt_py = build_dir / "extern" / "nlopt" / "src" / "swig" / "nlopt.py"
        if not nlopt_py.exists():
            raise RuntimeError("swig python file was not generated")

        shutil.copy2(nlopt_py, ext_dir / "nlopt.py")
        with open(ext_dir / "__init__.py", 'w') as f:
            f.write(f"""
from .nlopt import *

__version__ = '{ext.version}'
""".strip() + "\n")


def create_directory(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(exist_ok=True, parents=True)
    return path


def execute_command(cmd: List[str], cwd: Path, env: Dict[str, str] = os.environ):
    print(cwd.as_posix(), ':', ' '.join(cmd))
    check_call(cmd, cwd=cwd, env=env)
