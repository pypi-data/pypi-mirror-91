import os
import random
import subprocess

import click

from tess.src.navigator import find_root_directory, load_external_module
from tess.src.runner import runner_args, run_timed_subprocess


def run_cmd(args, _in):
    output = subprocess.run(args,
                            input=_in,
                            encoding='utf-8',
                            capture_output=True)
    return output.stdout.strip()


def run_stress(model: str, solution: str, seed: int, number: int, args: list,
               line: int):
    root_dir = find_root_directory(os.getcwd())
    random.seed(seed)
    generator = load_external_module('generator', f'{root_dir}/generator.py')
    test_case_num = 1
    model_args = runner_args(model)
    solution_args = runner_args(solution)

    while number != 0:
        _in = generator.test_case(args, random)

        click.echo(f'\n\nTest case #{test_case_num}')
        test_case_num = test_case_num + 1

        click.echo(_in)

        model_out, model_time = run_timed_subprocess(model_args, _in)
        solution_out, solution_time = run_timed_subprocess(solution_args, _in)

        model_formatted_out = model_out.stdout.rstrip()
        solution_formatted_out = solution_out.stdout.rstrip()

        if line != 0:
            model_formatted_out = model_formatted_out.split('\n')[line - 1]
            solution_formatted_out = solution_formatted_out.split('\n')[
                line - 1]

        if model_formatted_out == solution_formatted_out:
            click.echo(f'Result: OK\t'
                       f'Model time: {model_time}ms\t'
                       f'Solution time: {solution_time}ms')
        else:
            click.echo('Result: Wrong answer')
            click.echo(f'\n[Model]\n{model_formatted_out}\n'
                       f'\n[Solution]\n{solution_formatted_out}')
            break

        number = number - 1
