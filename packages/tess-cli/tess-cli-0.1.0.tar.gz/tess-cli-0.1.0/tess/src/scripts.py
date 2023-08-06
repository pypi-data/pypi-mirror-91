from pathlib import Path

from pkg_resources import resource_string


def make_completion_script(shell, destination):
    path = Path(destination)
    if not path.exists():
        path.mkdir()
    file = Path(f'{path.absolute()}/tess-completion.sh')
    file.touch()
    if shell == 'bash':
        content = resource_string('tess.resources.scripts',
                                  'bash-completion.sh').decode('utf-8')
    elif shell in ['zsh', 'fish']:
        content = resource_string('tess.resources.scripts',
                                  'zsh-completion.sh').decode('utf-8')
    else:
        raise ValueError(f'Shell {shell} not supported.')
    file.write_text(content)
    return file.absolute()
