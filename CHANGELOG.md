# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.6] - 2024-11-07 :snake:
- Drop python3.6 and python3.7 support
- Use `obj.model_dump` instead of `obj.dict` for Pydantic V2
- Workflow maintenance
- Applies `black`, `flake8`, `isort`, `mypy`

## [1.1.5] - 2022-03-14 :tulip:
- Adds `py.typed` file
- Adds `ConflictException`

## [1.1.4] - 2020-11-08 :octocat:
- Completely migrates to GitHub Workflows
- Improves build to test Python 3.6 and 3.9
- Improves the `json.FriendlyEncoder` class to handle built-in `dataclasses`
- Adds a changelog
- Improves badges
