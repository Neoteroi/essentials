import os
import shutil
import uuid

import pytest

from essentials.folders import (
    ensure_folder,
    get_file_extension,
    get_path_leaf,
    split_path,
)


@pytest.mark.parametrize(
    "value,expected_value",
    [
        ["hello.jpg", ".jpg"],
        ["hello.txt", ".txt"],
        ["hello.TXT", ".TXT"],
        [r"C:\root\hello.jpg", ".jpg"],
        ["/home/foo/hello.jpg", ".jpg"],
    ],
)
def test_get_file_extension(value, expected_value):
    assert get_file_extension(value) == expected_value


@pytest.mark.parametrize(
    "value,expected_value",
    [
        [r"C:\root\hello.jpg", "hello.jpg"],
        ["/home/foo/hello.jpg", "hello.jpg"],
        ["/home/foo/", "foo"],
        ["/home/foo", "foo"],
        [r"C:\root\\", "root"],
    ],
)
def test_get_path_leaf(value, expected_value):
    assert get_path_leaf(value) == expected_value


@pytest.mark.parametrize(
    "value,expected_value",
    [
        [r"C:\root\hello.jpg", (r"C:\root", "hello", ".jpg")],
        ["/home/foo/hello.jpg", ("/home/foo", "hello", ".jpg")],
    ],
)
def test_split_path(value, expected_value):
    assert split_path(value) == expected_value


def test_ensure_folder():
    folder_name = str(uuid.uuid4())

    ensure_folder(folder_name)

    assert os.path.isdir(folder_name)
    shutil.rmtree(folder_name)


def test_ensure_folder_deep():
    folder_id = str(uuid.uuid4())
    folder_name = os.path.join(folder_id, "hello")

    ensure_folder(folder_name)

    assert os.path.isdir(folder_name)
    shutil.rmtree(folder_id, ignore_errors=True)
