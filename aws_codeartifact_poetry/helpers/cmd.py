"""CMD helper functions."""

import logging
import os
import subprocess
import sys
from subprocess import CompletedProcess
from typing import List, Optional

from aws_codeartifact_poetry.helpers.catch_exceptions import CLIError

logger = logging.getLogger(__name__)


def copy_and_append_envs(new_envs: dict) -> dict:
    """
    Copy and append environment variables.

    Args:
        new_envs (`dict`): New environment variables `dict`

    Returns:
        `dict` environment variables `dict` object
    """
    copy_env = os.environ.copy()

    for key in new_envs.keys():
        copy_env[key] = new_envs[key]

    return copy_env


def exec_cmd(
    cmd: List[str],
    working_dir: str,
    return_stdout: bool = False,
    return_stderr: bool = False,
    combine_outputs: bool = False,
    env_vars: dict = {},
    hide_secrets: List[str] = [],
) -> str or tuple:
    """
    Execute subprocess command.

    Args:
        cmd (`list`): command list
        working_dir (`str`): working directory
        return_stdout (`bool`): flag to return stdout
        return_stderr (`bool`): flag to return stderr
        combine_outputs (`bool`): flag to combine stdout and stderr
        env_vars (`dict`): environment variables
        hide_secrets (`list`): list of secrets strings to be replaced

    Returns:
        `str`: if `return_stdout` is True this function returns the stdout
        `str`: if `return_stderr` is True this function returns the stderr
        `tuple`: if both is True this function returns a tuple with stdout and stderr
    """
    cmd_str = " ".join(cmd)
    for secret in hide_secrets:
        cmd_str = cmd_str.replace(secret, '****')

    logger.info(f'Running command: {cmd_str}')

    process_stderr = subprocess.PIPE if return_stderr else sys.stderr
    process_stdout = subprocess.PIPE if return_stdout else sys.stdout

    if combine_outputs:
        process_stdout = subprocess.PIPE
        process_stderr = subprocess.STDOUT

    process = subprocess.run(
        cmd,
        stderr=process_stderr,
        stdout=process_stdout,
        cwd=working_dir,
        encoding='utf-8',
        env=copy_and_append_envs(env_vars)
    )

    _handle_error(cmd_str, process, return_stdout, return_stderr, combine_outputs)

    if combine_outputs:
        return process.returncode, process.stdout.strip()

    if return_stdout and not return_stderr:
        return process.stdout.strip()

    if return_stderr and not return_stdout:
        return process.stderr.strip()

    if return_stdout and return_stderr:
        stdout = process.stdout
        stderr = process.stderr

        return stdout, stderr


def _handle_error(
    cmd_str: str,
    process: CompletedProcess,
    return_stdout: bool,
    return_stderr: bool,
    combine_outputs: bool
) -> Optional[tuple]:
    """
    Handlers the cmd when the exit code is different than 0.

    Args:
        cmd_str (`str`): command
        process (`CompletedProcess[str]`): subprocess.run output object
        return_stdout (`bool`): flag to return stdout
        return_stderr (`bool`): flag to return stderr
        combine_outputs (`bool`): flag to combine stdout and stderr
    """
    exit_code = process.returncode

    if exit_code != 0:
        if combine_outputs:
            return exit_code, process.stdout.strip()
        elif return_stdout or return_stderr:
            raise CLIError(f"Error executing command: {cmd_str}" +
                           f"\nexit_code: {exit_code}" +
                           f"\nstdout: '{process.stdout}'" +
                           f"\nstderr: '{process.stderr}'")
        else:
            raise CLIError(f'Error executing command: {cmd_str}')
