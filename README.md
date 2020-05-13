NLOpt Python
============

[![Build Status](https://travis-ci.com/DanielBok/nlopt-python.svg?branch=master)](https://travis-ci.com/DanielBok/nlopt-python) 
[![PyPI version](https://badge.fury.io/py/nlopt.svg)](https://badge.fury.io/py/nlopt)

This project setups a tool chain to build pypi wheels for the NLOpt 
library. NLOpt contains various routines for non-linear optimization.

If you find that your distribution is not supported, raise an issue or
better, send in a pull request. :) 

## Versions supported

The project supports Python versions 3.7 and above for Windows and Linux.
I haven't been able to build Mac binaries and haven't had time to figure
out the proper configuration on Travis so welcoming anyone who can do it
to add it in. 

## Installation

```bash
pip install nlopt
```

## Documentation

For more information on how to use NLOpt with python, refer to the [documentation](https://nlopt.readthedocs.io/en/latest/NLopt_Python_Reference/).

## Quick Test

After installation, to test that it works, run the following

```python
from nlopt.test import test_nlopt

test_nlopt()
```

If everything runs fine, it'll print a statement saying that all is well.

FAQ
===

### Where is the git repo hosting the build commands

[Right here]( https://github.com/DanielBok/nlopt-python.git)

I'll appreciate greatly if you could help me improve it!

### `AttributeError: module 'platform' has no attribute 'linux_distribution'`

If you see an error like that, it means that your pip is shared across all Python
versions. This is usually the case for Ubuntu where you use `python3-pip` across.

One solution is listed in this [Stackoverflow](https://stackoverflow.com/questions/58758447/how-to-fix-module-platform-has-no-attribute-linux-distribution-when-instal) 
answer
