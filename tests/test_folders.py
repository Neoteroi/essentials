import os
import pytest
import uuid
import shutil
from essentials.folders import get_file_extension, get_path_leaf, split_path, ensure_folder


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


def test_ensure_folder():
    folder_name = str(uuid.uuid4())

    ensure_folder(folder_name)

    assert os.path.isdir(folder_name)
    shutil.rmtree(folder_name)


def test_ensure_folder_deep():
    folder_name = os.path.join(str(uuid.uuid4()), 'hello')

    ensure_folder(folder_name)

    assert os.path.isdir(folder_name)
    shutil.rmtree(folder_name)
