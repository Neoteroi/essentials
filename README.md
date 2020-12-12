![Build](https://github.com/Neoteroi/essentials/workflows/Build/badge.svg)
[![pypi](https://img.shields.io/pypi/v/essentials.svg)](https://pypi.python.org/pypi/essentials)
[![versions](https://img.shields.io/pypi/pyversions/essentials.svg)](https://github.com/Neoteroi/essentials)
[![license](https://img.shields.io/github/license/Neoteroi/essentials.svg)](https://github.com/Neoteroi/essentials/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/Neoteroi/essentials/branch/master/graph/badge.svg?token=sBKZG2D1bZ)](https://codecov.io/gh/Neoteroi/essentials)

# Essentials
Core classes and functions, reusable in any kind of Python application.

```bash
$ pip install essentials
```

**Features:**
* [exception classes to express common scenarios](https://github.com/Neoteroi/essentials/wiki/Common-exceptions)
* [friendly JSON encoder](https://github.com/Neoteroi/essentials/wiki/User-friendly-JSON-dumps), handling `datetime`, `date`, `time`, `UUID`, `bytes`, built-in enums, and instances of classes implementing a `dict()` method, like [pydantic BaseModel](https://pydantic-docs.helpmanual.io)
* utilities to work with `folders` and paths
* [`StopWatch` implementation](https://github.com/Neoteroi/essentials/wiki/StopWatch-implementation)
* [a base class to handle classes that can be instantiated from configuration dictionaries](https://github.com/Neoteroi/essentials/wiki/Registry)
* [common decorator to support retries](https://github.com/Neoteroi/essentials/wiki/Retry-decorator)
* [common decorator to support logging function calls](https://github.com/Neoteroi/essentials/wiki/Logs-decorator)
* [common decorator to control raised exceptions](https://github.com/Neoteroi/essentials/wiki/Exception-handle-decorator)
* [caching functions](https://github.com/Neoteroi/essentials/wiki/Caching)

## Documentation
Please refer to documentation in the project wiki: [https://github.com/Neoteroi/essentials/wiki](https://github.com/Neoteroi/essentials/wiki).

## Develop and run tests locally
```bash
pip install -r requirements.txt

# run tests using automatic discovery:
pytest

# with code coverage:
make testcov
```
