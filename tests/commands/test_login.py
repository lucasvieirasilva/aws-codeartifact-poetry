"""aws_codeartifact_poetry.commands.login unit tests."""

from unittest.mock import ANY, MagicMock, patch

import boto3
from click.testing import CliRunner
from moto.core.models import ACCOUNT_ID

from aws_codeartifact_poetry.cli import cli

DOMAIN = 'fake-domain'
DOMAIN_OWNER = ACCOUNT_ID
REPO = 'fake-repo'


@patch('aws_codeartifact_poetry.helpers.poetry.codeartifact_login')
@patch('shutil.which')
@patch('aws_codeartifact_poetry.aws.session.get_session')
def test_login(
    mock_get_session: MagicMock,
    mock_shutil_which: MagicMock,
    mock_poetry_codeartifact_login: MagicMock,
    mock_cli_runner: CliRunner
):
    """Should run the login command."""
    mock_get_session.return_value = boto3

    mock_shutil_which.return_value = '/bin/poetry'

    with mock_cli_runner.isolated_filesystem():
        result = mock_cli_runner.invoke(cli, [
            'login',
            '--repository', REPO,
            '--domain', DOMAIN,
            '--domain-owner', DOMAIN_OWNER,
        ])

    mock_poetry_codeartifact_login.assert_called_once_with(
        session=ANY,
        domain=DOMAIN,
        domain_owner=DOMAIN_OWNER,
        repository=REPO
    )
    assert result.exit_code == 0


@patch('aws_codeartifact_poetry.helpers.poetry.codeartifact_login')
@patch('shutil.which')
@patch('aws_codeartifact_poetry.aws.session.get_session')
def test_login_using_poetry_tool_without_executable(
    mock_get_session: MagicMock,
    mock_shutil_which: MagicMock,
    mock_poetry_codeartifact_login: MagicMock,
    mock_cli_runner: CliRunner
):
    """Should raise an exception whe the poetry executable is not found."""
    mock_get_session.return_value = boto3
    mock_shutil_which.return_value = None

    with mock_cli_runner.isolated_filesystem():
        result = mock_cli_runner.invoke(cli, [
            'login',
            '--repository', REPO,
            '--domain', DOMAIN,
            '--domain-owner', DOMAIN_OWNER,
        ])

    mock_shutil_which.assert_called_once_with('poetry')
    mock_poetry_codeartifact_login.assert_not_called()
    assert result.exit_code == 1
