from json import loads

from pkg_resources import resource_listdir, resource_string


def __resource_str_utf8(pkg: str, filename: str) -> str:
    return resource_string(pkg, filename).decode('utf-8')


def __filtered_files(pkg: str, ext: str) -> list:
    return [file
            for file in resource_listdir(pkg, '')
            if file.endswith(ext) and file != '__init__.py']


def __files_content_by_ext(pkg: str, ext: str) -> dict:
    filenames = __filtered_files(pkg, ext)
    return {filename: __resource_str_utf8(pkg, filename)
            for filename in filenames}


def lang_templates(lang: str) -> dict:
    pkg = f'tess.resources.templates.{lang}'
    ext = f'.{lang}'
    return __files_content_by_ext(pkg, ext)


def test_case_templates() -> dict:
    return __files_content_by_ext('tess.resources.templates.cases', '.txt')


def generator_template(_id: str) -> dict:
    templates = __files_content_by_ext('tess.resources.templates.generators',
                                       '.py')
    selected = templates[_id]
    return {'generator.py': selected}


def runners_meta() -> dict:
    return loads(__resource_str_utf8('tess.resources.config', 'runners.json'))
