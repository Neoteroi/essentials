# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.6] - 2025-03-29 :snake:

- Drop Python 3.6 and Python 3.7 support.
- Use `obj.model_dump` instead of `obj.dict` for Pydantic V2.
- Add support for `Decimal` in `FriendlyEncoder`.
- Apply `black`, `flake8`, `isort`, `mypy`.
- Replace `setup.py` with `pyproject.toml`.
- Workflow maintenance.

## [1.1.5] - 2022-03-14 :tulip:

- Add `py.typed` file.
- Add `ConflictException`.

## [1.1.4] - 2020-11-08 :octocat:

- Migrate to GitHub Workflows.
- Improve build to test Python 3.6 and 3.9.
- Improve the `json.FriendlyEncoder` class to handle built-in `dataclasses`.
- Add a changelog.
- Improve badges.
