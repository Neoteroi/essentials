# Essentials
Core classes and functions, reusable in any kind of Python application.

```bash
$ pip install essentials
```

**Features:**
* [exception classes to express common scenarios](https://github.com/RobertoPrevato/essentials/wiki/Common-exceptions)
* [implementation of models annotations, useful to implement validation of business objects](https://github.com/RobertoPrevato/essentials/wiki/Models-annotations)
* [friendly JSON encoder](https://github.com/RobertoPrevato/essentials/wiki/User-friendly-JSON-dumps), handling `datetime`, `date`, `time`, `UUID`, `bytes`
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
