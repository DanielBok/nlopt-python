import re
from pathlib import Path

from setuptools import setup

from extensions import NLOptBuild, NLOptBuildExtension

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
    version=version,
    python_requires=">=3.9",
    install_requires=["numpy >=2,<3"],
    setup_requires=["numpy >=2,<3"],
    ext_modules=[NLOptBuildExtension("nlopt._nlopt", version)],
    cmdclass={"build_ext": NLOptBuild},
    zip_safe=False,
)
