import pytest
import logging
from pytest import raises
from reprlib import repr
from essentials.decorators.logs import log
from . import CrashTest


def test_log_decorator(caplog):
    caplog.set_level(logging.INFO)

    @log()
    def hello_world():
        return 'Hello World'

    hello_world()

    assert 'hello_world' in caplog.text
    first_record = caplog.records[0]
    second_record = caplog.records[1]
    assert first_record.message.startswith('tests.test_decorators_logs.hello_world; called;')
    assert second_record.message.startswith('tests.test_decorators_logs.hello_world; completed;')
    assert 'elapsed' in second_record.message
    assert 'call id' in first_record.message
    assert 'call id' in second_record.message


@pytest.mark.asyncio
async def test_log_decorator_async(caplog):
    caplog.set_level(logging.INFO)

    @log()
    async def hello_world():
        return 'Hello World'

    await hello_world()

    assert 'hello_world' in caplog.text
    first_record = caplog.records[0]
    second_record = caplog.records[1]
    assert first_record.message.startswith('tests.test_decorators_logs.hello_world; called;')
    assert second_record.message.startswith('tests.test_decorators_logs.hello_world; completed;')
    assert 'elapsed' in second_record.message
    assert 'call id' in first_record.message
    assert 'call id' in second_record.message


def test_log_decorator_exceptions_handling(caplog):
    caplog.set_level(logging.INFO)

    @log()
    def hello_world():
        raise CrashTest()

    with raises(CrashTest):
        hello_world()

    assert 'hello_world' in caplog.text
    first_record = caplog.records[0]
    second_record = caplog.records[1]
    assert first_record.message.startswith('tests.test_decorators_logs.hello_world; called;')
    assert second_record.message.startswith('tests.test_decorators_logs.hello_world; unhandled exception;')
    assert 'elapsed' in second_record.message
    assert 'call id' in first_record.message
    assert 'call id' in second_record.message


@pytest.mark.asyncio
async def test_log_decorator_async_exceptions_handling(caplog):
    caplog.set_level(logging.INFO)

    @log()
    async def hello_world():
        raise CrashTest()

    with raises(CrashTest):
        await hello_world()

    assert 'hello_world' in caplog.text
    first_record = caplog.records[0]
    second_record = caplog.records[1]
    assert first_record.message.startswith('tests.test_decorators_logs.hello_world; called;')
    assert second_record.message.startswith('tests.test_decorators_logs.hello_world; unhandled exception;')
    assert 'elapsed' in second_record.message
    assert 'call id' in first_record.message
    assert 'call id' in second_record.message


@pytest.mark.parametrize('input_name,input_count', [
    ['Burtleby', 5],
    ['True', 2],
])
def test_log_decorator_with_arguments_and_return_value(caplog, input_name, input_count):
    caplog.set_level(logging.INFO)

    @log(log_arguments=True, log_return_value=True)
    def hello_world(name, *, exclamation_marks_count):
        return f'Hello, {name}' + exclamation_marks_count * '!'

    value = hello_world(input_name, exclamation_marks_count=input_count)

    assert 'hello_world' in caplog.text
    first_record = caplog.records[0]
    second_record = caplog.records[1]
    assert repr((input_name,)) in first_record.message
    assert repr({'exclamation_marks_count': input_count}) in first_record.message
    assert value in second_record.message
