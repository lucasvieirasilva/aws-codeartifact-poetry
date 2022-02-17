"""aws_codeartifact_poetry.helpers.cmd unit tests."""

import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest
from _pytest.logging import LogCaptureFixture

from aws_codeartifact_poetry.helpers.catch_exceptions import CLIError
from aws_codeartifact_poetry.helpers.cmd import exec_cmd
from aws_codeartifact_poetry.helpers.logging import setup_logging


@pytest.fixture(autouse=True)
def enable_logging():
    """Enable logging fixture."""
    setup_logging('aws_codeartifact_poetry', 'INFO', None)
    return None


@patch('subprocess.run')
def test_exec_cmd(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command and return exit code 0."""
    mock_exec_cmd.return_value.returncode = 0
    cmd = ['ls', '-la']
    working_dir = '.'

    exec_cmd(cmd, working_dir)

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=sys.stderr,
                                          stdout=sys.stdout,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
    assert 'Running command: ls -la' in caplog.text


@patch('subprocess.run')
def test_exec_cmd_non_zero_exit_code(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command and return exit code 1 and raise an exception."""
    mock_exec_cmd.return_value.returncode = 1
    cmd = ['ls', '-la']
    working_dir = '.'

    with pytest.raises(CLIError) as ex:
        exec_cmd(cmd, working_dir)

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=sys.stderr,
                                          stdout=sys.stdout,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
    assert 'Running command: ls -la' in caplog.text
    assert 'Error executing command: ls -la' in str(ex)


@patch('subprocess.run')
def test_exec_cmd_return_stdout(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command and return stdout as a string."""
    mock_exec_cmd.return_value.returncode = 0
    mock_exec_cmd.return_value.stdout = 'https://testing.com'
    cmd = ['dgx-deploy', 'spa', 'deploy']
    working_dir = '.'

    result = exec_cmd(cmd, working_dir, True)

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=sys.stderr,
                                          stdout=subprocess.PIPE,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
    assert 'Running command: dgx-deploy spa deploy' in caplog.text
    assert result == 'https://testing.com'


@patch('subprocess.run')
def test_exec_cmd_return_stdout_non_zero_exit_code(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command with return stdout flag and return exit code 1 and raise an exception."""
    mock_exec_cmd.return_value.returncode = 1
    mock_exec_cmd.return_value.stderr = 'error on upload files'
    mock_exec_cmd.return_value.stdout = 'uploading file.txt'
    cmd = ['dgx-deploy', 'spa', 'deploy']
    working_dir = '.'

    with pytest.raises(CLIError) as ex:
        exec_cmd(cmd, working_dir, True)

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=sys.stderr,
                                          stdout=subprocess.PIPE,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
    assert 'Running command: dgx-deploy spa deploy' in caplog.text
    assert "Error executing command: dgx-deploy spa deploy" in str(ex)
    assert "exit_code: 1" in str(ex)
    assert "stdout: 'uploading file.txt'" in str(ex)
    assert "stderr: 'error on upload files'" in str(ex)


@patch('subprocess.run')
def test_exec_cmd_return_stderr(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command and return stderr as a string."""
    mock_exec_cmd.return_value.returncode = 0
    mock_exec_cmd.return_value.stderr = 'some error'
    cmd = ['mkdir', 'dir']
    working_dir = '.'

    result = exec_cmd(cmd, working_dir, return_stderr=True)

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=subprocess.PIPE,
                                          stdout=sys.stdout,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
    assert 'Running command: mkdir dir' in caplog.text
    assert result == 'some error'


@patch('subprocess.run')
def test_exec_cmd_return_stdout_return_stderr(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command and return stdout and stderr as a tuple."""
    mock_exec_cmd.return_value.returncode = 0
    mock_exec_cmd.return_value.stderr = 'fake stderr message'
    mock_exec_cmd.return_value.stdout = 'fake stdout message'
    cmd = ['npm', 'install']
    working_dir = '.'

    stdout, stderr = exec_cmd(cmd, working_dir, True, True)

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
    assert 'Running command: npm install' in caplog.text
    assert stdout == 'fake stdout message'
    assert stderr == 'fake stderr message'


@patch('subprocess.run')
def test_exec_cmd_combine_outputs(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command and one output with stdout and stderr."""
    mock_exec_cmd.return_value.returncode = 0
    mock_exec_cmd.return_value.stdout = 'fake stdout message and fake stderr message'
    cmd = ['nx', 'run', 'build']
    working_dir = '.'

    exit_code, output = exec_cmd(cmd, working_dir, combine_outputs=True)

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=subprocess.STDOUT,
                                          stdout=subprocess.PIPE,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
    assert 'Running command: nx run build' in caplog.text
    assert output == 'fake stdout message and fake stderr message'
    assert exit_code == 0


@patch('subprocess.run')
def test_exec_cmd_combine_outputs_with_error(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command and one output with stdout and stderr."""
    mock_exec_cmd.return_value.returncode = 1
    mock_exec_cmd.return_value.stdout = 'error message'
    cmd = ['nx', 'run', 'test']
    working_dir = '.'

    exit_code, output = exec_cmd(cmd, working_dir, combine_outputs=True)

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=subprocess.STDOUT,
                                          stdout=subprocess.PIPE,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
    assert 'Running command: nx run test' in caplog.text
    assert exit_code == 1
    assert output == 'error message'


@patch('subprocess.run')
def test_exec_cmd_with_custom_env_vars(
    mock_exec_cmd: MagicMock
):
    """Should execute the command with custom environment variables."""
    mock_exec_cmd.return_value.returncode = 0
    cmd = ['npm', 'install']
    working_dir = '.'

    exec_cmd(cmd, working_dir, env_vars={'NODE_ENV': 'ci'})

    envs = os.environ.copy()
    envs.update({'NODE_ENV': 'ci'})

    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=sys.stderr,
                                          stdout=sys.stdout,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=envs)


@patch('subprocess.run')
def test_exec_cmd_with_hide_secrets(
    mock_exec_cmd: MagicMock,
    caplog: LogCaptureFixture
):
    """Should execute the command and replace secrets with `****`."""
    mock_exec_cmd.return_value.returncode = 0
    secret = 'my-secret-value'
    cmd = ['login', secret]
    working_dir = '.'

    exec_cmd(cmd, working_dir, hide_secrets=[secret])

    assert 'Running command: login ****' in caplog.text
    mock_exec_cmd.assert_called_once_with(cmd,
                                          stderr=sys.stderr,
                                          stdout=sys.stdout,
                                          cwd=working_dir,
                                          encoding='utf-8',
                                          env=os.environ.copy())
