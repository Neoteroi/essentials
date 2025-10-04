import os
import secrets

from essentials.exceptions import EnvironmentVariableNotFound


class Secret:
    """
    A type that encourages loading secrets from environment variables, and discourages
    programmers from hardcoding secrets in source code. This also avoids accidental
    exposure of secrets in logs or error messages, by overriding __str__ and __repr__,
    and causes exception if someone tries to JSON encode it using the built-in
    JSON module. For convenience, it can be compared directly to strings.
    It uses constant-time comparison to prevent timing attacks, with
    `secrets.compare_digest`.
    Another benefit is that environment variables can be changed at runtime, so
    applications can pick up secret changes without needing to be restarted.

    my_secret = Secret.from_env("MY_SECRET_ENV_VAR")

    >>> str(my_secret)
    '******'
    >>> repr(my_secret)
    "Secret('******')"
    """

    def __init__(
        self, value: str, *, direct_value: bool = False, encoding: str = "utf8"
    ) -> None:
        """
        Create an instance of Secret.

        Args:
            value: The name of an environment variable reference (prefixed with $), or
                   a secret if direct_value=True.
            direct_value: Must be set to True to allow passing secrets directly
            encoding: The encoding to be used when comparing strings with
                    secrets.compare_digest.

        Raises:
            ValueError: If a secret is provided without explicit permission.
        """
        if not value.startswith("$") and not direct_value:
            raise ValueError(
                "Hardcoded secrets are not allowed. Either:\n"
                "1. Use Secret.from_env('ENV_VAR_NAME') for environment variables\n"
                "2. Use Secret('$ENV_VAR_NAME') for env var references\n"
                "3. Set direct_value=True if you need to handle a secret value "
                "directly."
            )
        self._value = value
        self._encoding = encoding
        # Validate that we can retrieve a value
        value = self.get_value()
        if not isinstance(value, str) or not value:
            raise ValueError("Secret value must be a non-empty string")

    @classmethod
    def from_env(cls, env_var: str) -> "Secret":
        """Obtain a secret from an environment variable."""
        return cls(f"${env_var}")

    @classmethod
    def from_plain_text(cls, value: str) -> "Secret":
        """
        Create a Secret from a plain text value.

        This is intended for secrets that are:
        - Generated at runtime
        - Loaded from secure storage (databases, key vaults, etc.)
        - Received from secure APIs

        WARNING: Don't hardcode secrets in source code! This method should only
        be used with variables containing secrets obtained from secure sources.

        Args:
            value: The secret value as plain text

        Returns:
            Secret: A new Secret instance
        """
        return cls(value, direct_value=True)

    def get_value(self) -> str:
        """Get the secret value."""
        if self._value.startswith("$"):
            env_var = self._value[1:]  # Remove $ prefix
            value = os.getenv(env_var)
            if value is None:
                raise EnvironmentVariableNotFound(env_var)
            return value
        return self._value

    def _get_value_bytes(self) -> bytes:
        return self.get_value().encode(self._encoding)

    def __str__(self) -> str:
        return "******"  # Never expose the actual value

    def __repr__(self) -> str:
        # Never expose the actual value
        # Show the source (env var name) but never the value
        if self._value.startswith("$"):
            env_var = self._value[1:]
            return f"Secret.from_env('{env_var}')"
        return "Secret('******')"  # For hardcoded secrets

    def __eq__(self, other: object) -> bool:
        # Allow comparison with strings for convenience
        if isinstance(other, str):
            # Using constant-time comparison to prevent timing attacks, with
            # secrets.compare_digest.
            return secrets.compare_digest(
                self._get_value_bytes(), other.encode(self._encoding, errors="ignore")
            )

        if not isinstance(other, Secret):
            return NotImplemented

        return secrets.compare_digest(self._get_value_bytes(), other._get_value_bytes())
