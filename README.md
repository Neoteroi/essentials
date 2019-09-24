[![Build Status](https://dev.azure.com/robertoprevato/Nest/_apis/build/status/RobertoPrevato.essentials?branchName=master)](https://dev.azure.com/robertoprevato/Nest/_build/latest?definitionId=28&branchName=master) [![pypi](https://img.shields.io/pypi/v/essentials.svg?color=blue)](https://pypi.org/project/essentials/) [![Test coverage](https://img.shields.io/azure-devops/coverage/robertoprevato/Nest/28.svg)](https://dev.azure.com/robertoprevato/Nest/_build?definitionId=28)

# Essentials
Core classes and functions, reusable in any kind of Python application.

```bash
$ pip install essentials
```

**Features:**
* [exception classes to express common scenarios](https://github.com/RobertoPrevato/essentials/wiki/Common-exceptions)
* [friendly JSON encoder](https://github.com/RobertoPrevato/essentials/wiki/User-friendly-JSON-dumps), handling `datetime`, `date`, `time`, `UUID`, `bytes`, and instances of classes implementing a `dict()` method, like [pydantic BaseModel](https://pydantic-docs.helpmanual.io)
* utilities to work with `folders` and paths
* [`StopWatch` implementation](https://github.com/RobertoPrevato/essentials/wiki/StopWatch-implementation)
* [a base class to handle classes that can be instantiated from configuration dictionaries](https://github.com/RobertoPrevato/essentials/wiki/Registry)
* [common decorator to support retries](https://github.com/RobertoPrevato/essentials/wiki/Retry-decorator)
* [common decorator to support logging function calls](https://github.com/RobertoPrevato/essentials/wiki/Logs-decorator)
* [common decorator to control raised exceptions](https://github.com/RobertoPrevato/essentials/wiki/Exception-handle-decorator)

## Documentation
Please refer to documentation in the project wiki: [https://github.com/RobertoPrevato/essentials/wiki](https://github.com/RobertoPrevato/essentials/wiki).

## Develop and run tests locally
```bash
pip install -r requirements.txt

# run tests using automatic discovery:
pytest

# with code coverage:
make testcov
```
