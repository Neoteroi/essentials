# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.7] - 2025-10-01 :fallen_leaf:

- Add a `Secret` class to handle secrets in code instead of using plain `str`. This
  approach offers several advantages:

1. It encourages loading secrets from environment variables, and discourages programmers
   from hardcoding secrets in source code.
1. Avoids accidental exposure of secrets in logs or error messages, by overriding
   __str__ and __repr__.
1. It causes exception if someone tries to JSON encode it using the built-in JSON
   module, unlike `str`.
1. For convenience, it can be compared directly to strings. It uses constant-time
   comparison to prevent timing attacks, with the built-in `secrets.compare_digest`.
1. Environment variables can be changed at runtime, using this class applications can
   pick up secret changes without needing to be restarted.

- Add an `EnvironmentVariableNotFound` exception that can be used when an expected env
  variable is not set.
- Handle `timedelta` objects in the `FriendlyEncoder` class, by @arthurbrenno.
- Improve the order of `if` statements in the `FriendlyEncoder` class to prioritize the
  most frequently encountered types first, which should provide better performance in
  typical use cases.

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
