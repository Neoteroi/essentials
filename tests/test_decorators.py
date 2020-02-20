import pytest
from pytest import raises
from . import CrashTest
from essentials.decorators import exception_handle


class DesiredExceptionWithContext(Exception):
    """Example exception"""


def test_exception_handle():
    @exception_handle(DesiredExceptionWithContext)
    def crashing():
        raise CrashTest()

    with raises(DesiredExceptionWithContext) as captured_exception:
        crashing()

    assert str(captured_exception.value) == str(CrashTest())


@pytest.mark.asyncio
async def test_exception_handle_async():
    @exception_handle(DesiredExceptionWithContext)
    async def crashing():
        raise CrashTest()

    with raises(DesiredExceptionWithContext) as captured_exception:
        await crashing()

    assert str(captured_exception.value) == str(CrashTest())
