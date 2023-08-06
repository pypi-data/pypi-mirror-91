from pathlib import Path

import click

from tess.src.directories import Directory
from tess.src.navigator import debug_solutions_absolute_path, list_files, \
    solutions_absolute_path


def source_files(ctx, args, incomplete):
    files = list_files(Directory.SOLUTIONS)
    return [file for file in files if incomplete in file]


def py_validations(line: str) -> str:
    if '"""@log' in line or '"""' in line:
        return ''
    elif '#@log' in line:
        return line.replace('#@log ', '')
    else:
        return line


def cpp_style_validations(line: str) -> str:
    if '/*@log' in line or '*/' in line:
        return ''
    elif '//@log' in line:
        return line.replace('//@log ', '')
    else:
        return line


def remove_log_comments(file: Path) -> str:
    with file.open() as f:
        lines = f.readlines()
        content = ''
        for line in lines:
            if file.suffix == '.py':
                line = py_validations(line)
            else:
                line = cpp_style_validations(line)
            content = content + line
    return content


def make_debug_file(filename: str):
    file = Path(f'{solutions_absolute_path()}/{filename}')
    file_content = remove_log_comments(file)
    new_file = Path(f'{debug_solutions_absolute_path()}/{file.name}')
    new_file.touch()
    new_file.write_text(file_content)
    click.echo('Debuggable file created.')
