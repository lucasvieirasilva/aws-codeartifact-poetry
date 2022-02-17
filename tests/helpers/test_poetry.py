"""aws_codeartifact_poetry.helpers.poetry unit tests."""


import os
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import boto3
import pytest
from botocore.stub import Stubber
from moto.core.models import ACCOUNT_ID

from aws_codeartifact_poetry.helpers import poetry

AWS_CODEARTIFACT_TOKEN = 'faketoken'
AWS_CODEARTIFACT_ENDPOINT = 'https://awscodeartifactfakeendpoint.com'

POETRY_REPO_NAME = 'aws'

WIN32_AUTH_TOML_PATH = 'AppData/Roaming/pypoetry/auth.toml'
BOTO3_CLIENT_MOCK_TARGET = 'boto3.client'

DEFAULT_AWS_REGION = 'us-east-1'

WIN_POETRY_PATH = 'AppData/Roaming/pypoetry'


@pytest.fixture()
def mock_codeartifact():
    """AWS CodeArtifact Mock fixture."""
    client = boto3.client('codeartifact', region_name=DEFAULT_AWS_REGION)

    with Stubber(client) as stubber:
        stubber.add_response('get_repository_endpoint', {
            'repositoryEndpoint': AWS_CODEARTIFACT_ENDPOINT
        })
        stubber.add_response('get_authorization_token', {
            'authorizationToken': AWS_CODEARTIFACT_TOKEN
        })

        yield client


@patch('aws_codeartifact_poetry.helpers.cmd.exec_cmd')
@patch('aws_codeartifact_poetry.helpers.poetry.sys', MagicMock(platform='linux'))
def test_codeartifact_login_non_windows(
    mock_exec_cmd: MagicMock,
    mock_codeartifact: MagicMock,
    mock_sts
):
    """Should get the AWS CodeArtifact endpoint and credentials and run poetry config commands."""
    with patch(BOTO3_CLIENT_MOCK_TARGET) as mock_boto3:
        mock_boto3.return_value = mock_codeartifact

        poetry.codeartifact_login(
            session=boto3,
            domain='mydomain',
            domain_owner=ACCOUNT_ID,
            repository='myrepo'
        )

        mock_exec_cmd.assert_has_calls([
            call(['poetry', 'config', f'repositories.{POETRY_REPO_NAME}', AWS_CODEARTIFACT_ENDPOINT], working_dir='.'),
            call(
                ['poetry', 'config', f'http-basic.{POETRY_REPO_NAME}', 'aws', AWS_CODEARTIFACT_TOKEN],
                working_dir='.',
                hide_secrets=[AWS_CODEARTIFACT_TOKEN]
            )
        ])


@patch('aws_codeartifact_poetry.helpers.cmd.exec_cmd')
@patch('pathlib.Path.home', MagicMock(return_value='/'))
@patch('aws_codeartifact_poetry.helpers.poetry.sys', MagicMock(platform='win32'))
def test_codeartifact_login_windows_without_auth_toml(
    mock_exec_cmd: MagicMock,
    mock_codeartifact: MagicMock,
    mock_sts,
    motofs
):
    """Should authenticate in CodeArtifact and run poetry config command and create the auth.toml file."""
    with patch(BOTO3_CLIENT_MOCK_TARGET) as mock_boto3:
        mock_boto3.return_value = mock_codeartifact

        poetry.codeartifact_login(
            session=boto3,
            domain='mydomain',
            domain_owner=ACCOUNT_ID,
            repository='myrepo'
        )

        mock_exec_cmd.assert_has_calls([
            call(['poetry', 'config', f'repositories.{POETRY_REPO_NAME}', AWS_CODEARTIFACT_ENDPOINT], working_dir='.')
        ])

        with open(os.path.join(Path.home(), WIN32_AUTH_TOML_PATH), 'r') as auth_toml:
            assert f'[http-basic.{POETRY_REPO_NAME}]\nusername = "aws"\n' + \
                f'password = "{AWS_CODEARTIFACT_TOKEN}"\n' == auth_toml.read()


@patch('aws_codeartifact_poetry.helpers.cmd.exec_cmd')
@patch('pathlib.Path.home', MagicMock(return_value='/'))
@patch('aws_codeartifact_poetry.helpers.poetry.sys', MagicMock(platform='win32'))
def test_codeartifact_login_windows_with_auth_toml(
    mock_exec_cmd: MagicMock,
    mock_codeartifact: MagicMock,
    mock_sts,
    motofs
):
    """Should authenticate in CodeArtifact and run poetry config command and edit the auth.toml file."""
    with patch(BOTO3_CLIENT_MOCK_TARGET) as mock_boto3:
        mock_boto3.return_value = mock_codeartifact

        os.makedirs(os.path.join(Path.home(), WIN_POETRY_PATH))
        with open(os.path.join(Path.home(), WIN32_AUTH_TOML_PATH), 'w') as auth_toml:
            auth_toml.write('[http-basic.aws]\nusername = "aws"\npassword = "expired_token"\n')

        poetry.codeartifact_login(
            session=boto3,
            domain='mydomain',
            domain_owner=ACCOUNT_ID,
            repository='myrepo'
        )

        mock_exec_cmd.assert_has_calls([
            call(['poetry', 'config', f'repositories.{POETRY_REPO_NAME}', AWS_CODEARTIFACT_ENDPOINT], working_dir='.')
        ])

        with open(os.path.join(Path.home(), WIN32_AUTH_TOML_PATH), 'r') as auth_toml:
            assert f'[http-basic.{POETRY_REPO_NAME}]\nusername = "aws"' + \
                f'\npassword = "{AWS_CODEARTIFACT_TOKEN}"\n' == auth_toml.read()


@patch('aws_codeartifact_poetry.helpers.cmd.exec_cmd')
@patch('pathlib.Path.home', MagicMock(return_value='/'))
@patch('aws_codeartifact_poetry.helpers.poetry.sys', MagicMock(platform='win32'))
def test_codeartifact_login_windows_with_auth_toml_empty(
    mock_exec_cmd: MagicMock,
    mock_codeartifact: MagicMock,
    mock_sts,
    motofs
):
    """Should authenticate in CodeArtifact and run poetry conf command and edit the auth.toml file when it is empty."""
    with patch(BOTO3_CLIENT_MOCK_TARGET) as mock_boto3:
        mock_boto3.return_value = mock_codeartifact

        os.makedirs(os.path.join(Path.home(), WIN_POETRY_PATH))
        with open(os.path.join(Path.home(), WIN32_AUTH_TOML_PATH), 'w') as auth_toml:
            auth_toml.write('')

        poetry.codeartifact_login(
            session=boto3,
            domain='mydomain',
            domain_owner=ACCOUNT_ID,
            repository='myrepo'
        )

        mock_exec_cmd.assert_has_calls([
            call(['poetry', 'config', f'repositories.{POETRY_REPO_NAME}', AWS_CODEARTIFACT_ENDPOINT], working_dir='.')
        ])

        with open(os.path.join(Path.home(), WIN32_AUTH_TOML_PATH), 'r') as auth_toml:
            assert f'[http-basic.{POETRY_REPO_NAME}]\nusername = "aws"' + \
                f'\npassword = "{AWS_CODEARTIFACT_TOKEN}"\n' == auth_toml.read()


@patch('aws_codeartifact_poetry.helpers.cmd.exec_cmd')
@patch('pathlib.Path.home', MagicMock(return_value='/'))
@patch('aws_codeartifact_poetry.helpers.poetry.sys', MagicMock(platform='win32'))
def test_codeartifact_login_windows_with_auth_toml_other_configs(
    mock_exec_cmd: MagicMock,
    mock_codeartifact: MagicMock,
    mock_sts,
    motofs
):
    """Should authenticate in CodeArtifact and run poetry config command and edit the auth.toml file \
        when it is already have other repo configs."""
    with patch(BOTO3_CLIENT_MOCK_TARGET) as mock_boto3:
        mock_boto3.return_value = mock_codeartifact

        os.makedirs(os.path.join(Path.home(), WIN_POETRY_PATH))
        with open(os.path.join(Path.home(), WIN32_AUTH_TOML_PATH), 'w') as auth_toml:
            auth_toml.write('[http-basic.other]\nusername = "other"\npassword = "pass"\n')

        poetry.codeartifact_login(
            session=boto3,
            domain='mydomain',
            domain_owner=ACCOUNT_ID,
            repository='myrepo'
        )

        mock_exec_cmd.assert_has_calls([
            call(['poetry', 'config', f'repositories.{POETRY_REPO_NAME}', AWS_CODEARTIFACT_ENDPOINT], working_dir='.')
        ])

        with open(os.path.join(Path.home(), WIN32_AUTH_TOML_PATH), 'r') as auth_toml:
            assert '[http-basic.other]\nusername = "other"\npassword = "pass"\n\n' + \
                f'[http-basic.{POETRY_REPO_NAME}]\nusername = "aws"' + \
                f'\npassword = "{AWS_CODEARTIFACT_TOKEN}"\n' == auth_toml.read()
