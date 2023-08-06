"""
Utilities
"""
from typing import Dict, Union

import subprocess
import re
import click
from loguru import logger


def cmd(command: str, return_success: bool = False) -> Union[str, bool]:
    logger.debug(f'Executing system command: [{command}]')
    if return_success:
        # only check if a command runs successfully
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        res = subprocess.run(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            logger.error(res.stdout.strip())
            raise SystemError(res.stderr)
        return res.stdout.strip()


def az_cmd(command: str, params: Dict, **kwargs) -> Union[str, bool]:
    """
    Wrapper for slightly easing az cli commands

    Args:
        command (str): base az cli command, e.g. 'az login' or 'az container create' (az part may be omitted)
        params (Dict): dict with parameter key values

    Returns:
        str: result of the command
    """
    prefix = '' if command[:3] == 'az ' else 'az '
    param_str = ' '.join([
        f'--{key.replace("_", "-")} "{value}"'
        for key, value in params.items()
    ])
    full_command = f'{prefix}{command} {param_str}'
    return cmd(full_command, **kwargs)


class ProjectNameType(click.ParamType):
    """
    Custom CLI parameter type for Python version specification
    """
    name = 'project-name'

    def convert(self, value, param, ctx):
        found = re.match(r'[a-z0-9]+(-[a-z0-9]+)*', value)
        if not found:
            self.fail(f'{value} is not a valid project name. Use lowercase-with-dashes', param, ctx, )
        return value


class PythonVersionType(click.ParamType):
    """
    Custom CLI parameter type for Python version specification
    """
    name = 'python-version'

    def convert(self, value, param, ctx):
        found = re.match(r'3\.[56789](\.\d)?', value)
        if not found:
            self.fail(f'{value} is not a valid Python version', param, ctx, )
        return value
