import ntpath
import os
from typing import Tuple


def ensure_folder(path) -> None:
    os.makedirs(path, exist_ok=True)


def split_path(filepath) -> Tuple[str, str, str]:
    """Splits a file path into folder path, file name and extension"""
    head, tail = ntpath.split(filepath)
    filename, extension = os.path.splitext(tail)
    return head, filename, extension


def get_file_extension(filepath) -> str:
    _, file_extension = os.path.splitext(filepath)
    return file_extension


def get_path_leaf(path) -> str:
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
