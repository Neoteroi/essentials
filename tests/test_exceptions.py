import pytest

from essentials.exceptions import AcceptedException, ObjectNotFound


def test_object_not_found_default_message():
    assert "Object not found" == str(ObjectNotFound())


@pytest.mark.parametrize("message", ["Product", "Product not found", "Cat not found"])
def test_object_not_found_message(message):
    exception = ObjectNotFound(message)
    assert str(exception) == message


def test_accepted_exception_default_message():
    assert (
        "The operation is accepted, " "but its completion is not guaranteed."
    ) == str(AcceptedException())


@pytest.mark.parametrize(
    "message",
    [
        "Lorem ipsum dolor sit amet",
        "Email sent, but its delivery is not guaranteed",
    ],
)
def test_accepted_exception_message(message):
    exception = AcceptedException(message)
    assert str(exception) == message
