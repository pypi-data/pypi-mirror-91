import importlib.util
import os
from pathlib import Path

from tess.src.directories import Directory


def make_dirs(path):
    dirs = {name: f'{path}/{name}' for name in Directory.init()}
    for _dir in dirs:
        d = Path(_dir)
        d.mkdir(parents=True, exist_ok=True)
    return dirs


def make_file(path, name, content):
    with open(f'{path}/{name}', 'w') as file:
        file.write(content)


def make_files(path, files):
    for name, content in files.items():
        make_file(path, name, content)


def contains_file(path, filename):
    for _dir, _, files in os.walk(path):
        if filename in files:
            return True
        return False


def contains_dir(path, name):
    for _, dirs, _ in os.walk(path):
        if name in dirs:
            return True
        return False


def find_root_directory(cwd):
    dir_name = '.tess'
    path = Path(cwd)
    if contains_dir(path.cwd(), dir_name):
        return path.cwd()
    else:
        for parent in path.parents:
            if contains_dir(parent, dir_name):
                return parent
    raise FileNotFoundError('This directory is not a tess project.')


def cases_absolute_path():
    root_dir = find_root_directory(os.getcwd())
    return f'{root_dir}/{Directory.CASES}'


def solutions_absolute_path():
    root_dir = find_root_directory(os.getcwd())
    return f'{root_dir}/{Directory.SOLUTIONS}'


def build_absolute_path():
    root_dir = find_root_directory(os.getcwd())
    return f'{root_dir}/{Directory.BUILD}'


def debug_solutions_absolute_path():
    root_dir = find_root_directory(os.getcwd())
    return f'{root_dir}/{Directory.DEBUG_SOLUTIONS}'


def debug_build_absolute_path():
    root_dir = find_root_directory(os.getcwd())
    return f'{root_dir}/{Directory.DEBUG_BUILD}'


def list_files(_dir: Directory, _ext=None) -> list:
    root_dir = find_root_directory(os.getcwd())
    source_files = []
    for _, _, filenames in os.walk(f'{root_dir}/{_dir}'):
        if _ext:
            for filename in filenames:
                _, ext = os.path.splitext(filename)
                if ext == _ext:
                    source_files.append(filename)
        else:
            source_files.extend(filenames)
        break
    return source_files


def load_external_module(name: str, path: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
