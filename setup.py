import re
import os
import sys
from pathlib import Path
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import platform
import subprocess as subp


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = Path(sourcedir).absolute()


class CMakeBuild(build_ext):
    def run(self):
        try:
            subp.check_call(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        # - make sure path ends with delimiter
        # - required for auto-detection of auxiliary "native" libs
        extdir = str(Path(self.get_ext_fullpath(ext.name)).parent.absolute())
        if not extdir[-1] == os.path.sep:
            extdir += os.path.sep

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += [
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
            ]
            if sys.maxsize > 2 ** 32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )
        build_temp = Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)

        def cmd(*args, **kwds):
            # Path objects not accepted on Windows
            subp.check_call([str(x) for x in args], **kwds)

        cmd("cmake", ext.sourcedir, *cmake_args, cwd=self.build_temp, env=env)
        cmd("cmake", "--build", ".", *build_args, cwd=self.build_temp)

        nlopt_py = next(Path(self.build_temp).rglob("nlopt.py"))
        nlopt_py.rename(Path(extdir) / "__init__.py")


with open("README.md") as f:
    long_description = f.read()

with open(Path(__file__).parent / "extern" / "nlopt" / "CMakeLists.txt") as f:
    content = f.read()
    version = []
    for s in ("MAJOR", "MINOR", "BUGFIX"):
        m = re.search(f"NLOPT_{s}_VERSION *['\"](.+)['\"]", content)
        version.append(m.group(1))
    version = ".".join(version)

setup(
    name="nlopt",
    version=version,
    description="Library for nonlinear optimization, wrapping many algorithms for "
    "global and local, constrained or unconstrained, optimization",
    license="MIT",  # placeholder, refer to the LICENSE file for more details
    python_requires=">=3.6",
    install_requires=["numpy >=1.14"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Bok",
    author_email="daniel.bok@outlook.com",
    maintainer="Hans Dembinski",
    maintainer_email="hans.dembinski@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    project_urls={
        "Documentation": "https://nlopt.readthedocs.io/en/latest/",
        "Tracker": "https://github.com/HDembinski/nlopt-python",
    },
    ext_modules=[CMakeExtension("nlopt._nlopt")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
)
