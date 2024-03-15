import logging
import os
import platform
import shutil
import sys
from pathlib import Path
from subprocess import check_call, CalledProcessError, check_output
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

        if platform.system() not in ("Windows", "Linux", "Darwin"):
            raise RuntimeError(f"Unsupported os: {platform.system()}")

        for ext in self.extensions:
            if isinstance(ext, NLOptBuildExtension):
                self.build_extension(ext)

    @property
    def config(self):
        return "Debug" if self.debug else "Release"

    def build_extension(self, ext: Extension):
        # - make sure path ends with delimiter
        # - required for auto-detection of auxiliary "native" libs
        ext_dir = Path(self.get_ext_fullpath(ext.name)).parent.absolute()
        _ed = ext_dir.as_posix()

        build_dir = create_directory(Path(self.build_temp))

        # package builds in 2 steps, first to compile the nlopt package and second to build the DLL
        cmd = [
            "cmake",
            "-LAH",
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={_ed}",
            f"-DPython_EXECUTABLE={sys.executable}",
            "-DNLOPT_GUILE=OFF",
            "-DNLOPT_MATLAB=OFF",
            "-DNLOPT_OCTAVE=OFF",
        ]

        if platform.system() == "Windows":
            cmd.append("-DPYTHON_EXTENSION_MODULE_SUFFIX=.abi3.pyd")
            cmd.insert(2, f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{self.config.upper()}={_ed}")
        else:
            cmd.append("-DPYTHON_EXTENSION_MODULE_SUFFIX=.abi3.so")

        cmd.append(ext.source_dir.as_posix())

        abi3_flag = "-DPy_LIMITED_API=0x03060000"
        execute_command(
            cmd=cmd,
            cwd=build_dir,
            env={
                **os.environ.copy(),
                "CXXFLAGS": f'{os.environ.get("CXXFLAGS", "")} -DVERSION_INFO="{self.distribution.get_version()}" {abi3_flag}'
            })

        # build the DLL
        execute_command([
            'cmake',
            '--build',
            '.',
            '--config',
            self.config,
            "--",
            "-m" if platform.system() == "Windows" else "-j2"
        ], cwd=build_dir)

        # Copy over the important bits
        nlopt_py = build_dir / "extern" / "nlopt" / "src" / "swig" / "nlopt.py"

        logging.info(f"Ext Dir - {ext_dir}\n" + '\n'.join(f'  - {file.as_posix()}' for file in ext_dir.rglob('*')))
        for folder in [ext_dir, nlopt_py.parent]:
            logging.info(f'Files in {folder.as_posix()}\n' + '\n'.join(f' - {f.name}' for f in folder.iterdir()))

        logging.info(f"Attempting to copy nlopt.py file from {nlopt_py.parent.as_posix()} to {ext_dir.as_posix()}")
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
    logging.info(f"Running Command: {cwd.as_posix()}: {' '.join(cmd)}")
    try:
        output = check_output(cmd, cwd=cwd.as_posix(), env=env)
        logging.info(output)
    except CalledProcessError as e:
        if isinstance(e.output, bytes):
            output = e.output.decode("utf-8")
        elif isinstance(e.output, str):
            output = e.output
        elif e.output is None:
            output = ""
        else:
            output = str(e.output)

        logging.info('\n'.join([f'{"-" * 20} ERROR {"-" * 20}', output, ]))
        raise e
