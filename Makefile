.PHONY: release test


artifacts: test
	python setup.py sdist bdist_wheel


prepforbuild:
	pip install --upgrade twine setuptools wheel


uploadtest:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


release:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


testcov:
	pytest --cov-report html --cov=essentials tests/


test:
	pytest -v -W ignore


check:
	flake8 .
	isort --check-only .
	black --check .
	mypy .
