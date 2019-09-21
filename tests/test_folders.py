import pytest
from essentials.folders import get_file_extension, get_path_leaf, split_path


@pytest.mark.parametrize('value,expected_value', [
    ['hello.jpg', '.jpg'],
    ['hello.txt', '.txt'],
    ['hello.TXT', '.TXT'],
    [r'C:\root\hello.jpg', '.jpg'],
    ['/home/foo/hello.jpg', '.jpg'],
])
def test_get_file_extension(value, expected_value):
    assert get_file_extension(value) == expected_value


@pytest.mark.parametrize('value,expected_value', [
    [r'C:\root\hello.jpg', 'hello.jpg'],
    ['/home/foo/hello.jpg', 'hello.jpg'],
    ['/home/foo/', 'foo'],
    ['/home/foo', 'foo'],
    [r'C:\root\\', 'root'],
])
def test_get_path_leaf(value, expected_value):
    assert get_path_leaf(value) == expected_value


@pytest.mark.parametrize('value,expected_value', [
    [r'C:\root\hello.jpg', (r'C:\root', 'hello', '.jpg')],
    ['/home/foo/hello.jpg', ('/home/foo', 'hello', '.jpg')]
])
def test_split_path(value, expected_value):
    assert split_path(value) == expected_value
