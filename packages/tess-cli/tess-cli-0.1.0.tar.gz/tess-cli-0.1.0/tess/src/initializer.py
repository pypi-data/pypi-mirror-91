from os import walk

from tess.src import resources as res
from tess.src.directories import Directory
from tess.src.navigator import make_dirs, make_files


def make_template(path, lang, empty):
    for _, dirs, _ in walk(path):
        if Directory.TESS in dirs:
            raise SystemError('This is a tess project, already.')
    dirs = make_dirs(path)
    if empty:
        make_files(path, res.generator_template('empty.py'))
    else:
        make_files(path, res.generator_template('sum_template.py'))
        make_files(dirs[Directory.CASES], res.test_case_templates())
        make_files(dirs[Directory.SOLUTIONS], res.lang_templates(lang))
