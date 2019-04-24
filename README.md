NLOpt Python
============

[![Build Status](https://travis-ci.com/DanielBok/nlopt-python.svg?branch=master)](https://travis-ci.com/DanielBok/nlopt-python) 
[![PyPI version](https://badge.fury.io/py/nlopt.svg)](https://badge.fury.io/py/nlopt)

This project setups a tool chain to build pypi wheels for the NLOpt library. NLOpt contains various routines for non-linear optimization.

If you find that your distribution is not supported, raise an issue or better, send in a pull request. :) 

## Versions supported

The project supports Python versions 3.6 and above.

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