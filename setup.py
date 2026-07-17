import os
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

# CI sets this to a unique dev build number (e.g. "dev12345") for testpypi dry-run
# publishes, since testpypi rejects new files added to a release once it's >14 days old.
version_suffix = os.environ.get("NLOPT_VERSION_SUFFIX")
if version_suffix:
    version = f"{version}.{version_suffix}"


setup(
    version=version,
    python_requires=">=3.10",
    install_requires=["numpy >=2,<3"],
    setup_requires=["numpy >=2,<3"],
    ext_modules=[NLOptBuildExtension("nlopt._nlopt", version)],
    cmdclass={"build_ext": NLOptBuild},
    zip_safe=False,
)
