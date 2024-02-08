import re
from pathlib import Path

from setuptools import setup

from extensions import NLOptBuild, NLOptBuildExtension

from wheel.bdist_wheel import bdist_wheel

with open("README.md") as f:
    long_description = f.read()

with open(Path(__file__).parent / "extern" / "nlopt" / "CMakeLists.txt") as f:
    content = f.read()
    version = []
    for s in ("MAJOR", "MINOR", "BUGFIX"):
        m = re.search(f"NLOPT_{s}_VERSION *['\"](.+)['\"]", content)
        version.append(m.group(1))
    version = ".".join(version)


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp"):
            # on CPython, our wheels are abi3 and compatible back to 3.6
            return "cp36", "abi3", plat

        return python, abi, plat


setup(
    version=version,
    install_requires=["numpy >=1.18.5"],
    ext_modules=[NLOptBuildExtension("nlopt._nlopt", version)],
    cmdclass={"build_ext": NLOptBuild,
              "bdist_wheel": bdist_wheel_abi3},
    zip_safe=False,
)
