NLopt Python
============

[![PyPI version](https://badge.fury.io/py/nlopt.svg)](https://pypi.org/project/nlopt/)
[![PyPI downloads](https://img.shields.io/pypi/dm/nlopt.svg)](https://pypi.org/project/nlopt/)
[![Python versions](https://img.shields.io/pypi/pyversions/nlopt.svg)](https://pypi.org/project/nlopt/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build](https://github.com/DanielBok/nlopt-python/actions/workflows/build.yml/badge.svg)](https://github.com/DanielBok/nlopt-python/actions/workflows/build.yml)
[![Nightly Build](https://github.com/DanielBok/nlopt-python/actions/workflows/nightly-build.yml/badge.svg)](https://github.com/DanielBok/nlopt-python/actions/workflows/nightly-build.yml)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-blue.svg)](https://nlopt.readthedocs.io/en/latest/NLopt_Python_Reference/)

Python wheels for [NLopt](https://github.com/stevengj/nlopt), a library for nonlinear optimization. NLopt provides
a common interface to a large collection of optimization algorithms, both global and local, gradient-based and
derivative-free, for constrained or unconstrained problems.

This project exists to make installing NLopt in Python as simple as `pip install nlopt` — no compiler, SWIG, or
system NLopt installation required. Prebuilt wheels are published for Windows, macOS, and Linux.

## Installation

```bash
pip install nlopt
```

Prebuilt wheels are available for Python 3.10+ on Windows, macOS, and Linux (x86_64 and arm64). If no matching
wheel is found for your platform, pip will fall back to building from source, which requires SWIG and a C++
compiler.

## Usage

```python
import nlopt
import numpy as np

def objective(x, grad):
    return x[0] ** 2 + x[1] ** 2

opt = nlopt.opt(nlopt.LN_COBYLA, 2)
opt.set_min_objective(objective)
opt.set_lower_bounds([-10, -10])
opt.set_upper_bounds([10, 10])
opt.set_xtol_rel(1e-6)

x = opt.optimize(np.array([1.0, 1.0]))
print(f"Minimum found at {x}, value = {opt.last_optimum_value()}")
```

## Documentation

Full API documentation, including the list of supported algorithms, is available at
[nlopt.readthedocs.io](https://nlopt.readthedocs.io/en/latest/NLopt_Python_Reference/).

## Releases

Builds run nightly and publish dev versions to [TestPyPI](https://test.pypi.org/project/nlopt/) so regressions
surface before a real release. Stable releases are cut from tagged GitHub Releases and published to
[PyPI](https://pypi.org/project/nlopt/). The vendored `extern/nlopt` submodule is checked daily against upstream
and bumped automatically via PR when a new NLopt version is released.

## License

This project wraps [NLopt](https://github.com/stevengj/nlopt), whose underlying routines are covered by a mix
of licenses (mainly MIT and LGPL) depending on the algorithm — see [LICENSE](LICENSE) for details. The Python
packaging in this repository is licensed under MIT.
