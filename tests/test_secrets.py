import pytest

from essentials.exceptions import EnvironmentVariableNotFound
from essentials.secrets import Secret


def test_from_env_success(monkeypatch):
    """Test creating Secret from environment variable."""
    monkeypatch.setenv("TEST_SECRET", "secret_value")
    secret = Secret.from_env("TEST_SECRET")
    assert secret.get_value() == "secret_value"


def test_from_env_missing_raises_exception():
    """Test that missing environment variable raises EnvironmentVariableNotFound."""
    with pytest.raises(EnvironmentVariableNotFound):
        Secret.from_env("NON_EXISTENT_VAR").get_value()


def test_from_plain_text_success():
    """Test creating Secret from plain text."""
    secret = Secret.from_plain_text("my_secret")
    assert secret.get_value() == "my_secret"


def test_direct_constructor_with_env_var(monkeypatch):
    """Test direct constructor with environment variable reference."""
    monkeypatch.setenv("TEST_SECRET", "secret_value")
    secret = Secret("$TEST_SECRET")
    assert secret.get_value() == "secret_value"


def test_direct_constructor_with_direct_value():
    """Test direct constructor with direct_value=True."""
    secret = Secret("hardcoded_secret", direct_value=True)
    assert secret.get_value() == "hardcoded_secret"


def test_hardcoded_secret_without_permission_raises_error():
    """Test that hardcoded secrets without permission raise ValueError."""
    with pytest.raises(ValueError, match="Hardcoded secrets are not allowed"):
        Secret("hardcoded_secret")


def test_empty_secret_raises_error(monkeypatch):
    """Test that empty secret values raise ValueError."""
    monkeypatch.setenv("EMPTY_SECRET", "")
    with pytest.raises(ValueError, match="Secret value must be a non-empty string"):
        Secret.from_env("EMPTY_SECRET")


def test_str_representation_hides_value(monkeypatch):
    """Test that __str__ never exposes the actual value."""
    monkeypatch.setenv("TEST_SECRET", "secret_value")
    secret = Secret.from_env("TEST_SECRET")
    assert str(secret) == "******"


def test_repr_shows_env_var_name(monkeypatch):
    """Test that __repr__ shows environment variable name but not value."""
    monkeypatch.setenv("TEST_SECRET", "secret_value")
    secret = Secret.from_env("TEST_SECRET")
    assert repr(secret) == "Secret.from_env('TEST_SECRET')"


def test_repr_hides_hardcoded_value():
    """Test that __repr__ hides hardcoded secret values."""
    secret = Secret.from_plain_text("secret")
    assert repr(secret) == "Secret('******')"


def test_equality_with_string(monkeypatch):
    """Test that Secret can be compared with strings."""
    monkeypatch.setenv("TEST_SECRET", "secret_value")
    secret = Secret.from_env("TEST_SECRET")
    assert secret == "secret_value"
    assert secret != "wrong_value"


def test_equality_with_another_secret(monkeypatch):
    """Test that Secrets can be compared with each other."""
    monkeypatch.setenv("SECRET1", "same_value")
    monkeypatch.setenv("SECRET2", "same_value")
    monkeypatch.setenv("SECRET3", "different_value")

    secret1 = Secret.from_env("SECRET1")
    secret2 = Secret.from_env("SECRET2")
    secret3 = Secret.from_env("SECRET3")

    assert secret1 == secret2
    assert secret1 != secret3


def test_equality_with_incompatible_type(monkeypatch):
    """Test that comparison with incompatible types returns NotImplemented."""
    monkeypatch.setenv("TEST_SECRET", "secret_value")
    secret = Secret.from_env("TEST_SECRET")
    assert secret.__eq__(123) == NotImplemented
    assert secret != 123


def test_mixed_secret_sources_comparison(monkeypatch):
    """Test comparing secrets from different sources."""
    monkeypatch.setenv("ENV_SECRET", "same_value")
    env_secret = Secret.from_env("ENV_SECRET")
    plain_secret = Secret.from_plain_text("same_value")

    assert env_secret == plain_secret


def test_get_value_called_multiple_times(monkeypatch):
    """Test that get_value works consistently across multiple calls."""
    monkeypatch.setenv("TEST_SECRET", "secret_value")
    secret = Secret.from_env("TEST_SECRET")

    assert secret.get_value() == "secret_value"
    assert secret.get_value() == "secret_value"


def test_env_var_change_at_runtime(monkeypatch):
    """Test that Secret picks up environment variable changes."""
    monkeypatch.setenv("DYNAMIC_SECRET", "initial_value")
    secret = Secret.from_env("DYNAMIC_SECRET")
    assert secret.get_value() == "initial_value"

    monkeypatch.setenv("DYNAMIC_SECRET", "changed_value")
    assert secret.get_value() == "changed_value"


def test_constructor_validation_with_empty_env_var(monkeypatch):
    """Test constructor validation when env var exists but is empty."""
    monkeypatch.setenv("EMPTY_VAR", "")
    with pytest.raises(ValueError, match="Secret value must be a non-empty string"):
        Secret("$EMPTY_VAR")


def test_from_plain_text_with_empty_string():
    """Test that from_plain_text with empty string raises ValueError."""
    with pytest.raises(ValueError, match="Secret value must be a non-empty string"):
        Secret.from_plain_text("")


def test_secrets_support_utf8_chars():
    secret = Secret("ØØ Void", direct_value=True)
    assert secret == "ØØ Void"


def test_secrets_work_with_invalid_unicode():
    secret = Secret("ØØ Void", direct_value=True)
    assert secret != "Hello\ud800World"  # invalid unicode


def test_secrets_with_special_characters():
    """Test secrets with various special Unicode characters."""
    secret = Secret("🔐密码🌟", direct_value=True)
    assert secret == "🔐密码🌟"
