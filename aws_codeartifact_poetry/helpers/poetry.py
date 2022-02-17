"""Poetry functions."""

import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import toml
from boto3.session import Session

from aws_codeartifact_poetry.helpers import cmd

logger = logging.getLogger(__name__)


def codeartifact_login(
    session: Session,
    domain: str,
    domain_owner: str,
    repository: str,
    session_duration: int = 43200,
    poetry_repository_name: str = 'aws',
    poetry_http_basic_user: str = 'aws'
) -> None:
    """
    Authenticate in the AWS CodeArtifact and save in the poetry configuration.

    Args:
        session (`Session`): boto3 session
        domain (`str`): AWS CodeArtifact domain name
        domain_owner (`str`): AWS CodeArtifact domain onwer
        repository (`str`): AWS CodeArtifact repository name
        session_duration (`int`): AWS CodeArtifact session duration in seconds, default value `43200` (12 hours)
        poetry_repository_name (`str`): Poetry repository name, default value `aws`
        poetry_http_basic_user (`str`): Poetrt http basic credentials user name, default value `aws`
    """
    client = session.client('codeartifact')
    logger.debug("Getting AWS CodeArtifact repository endpoint")
    repository_endpoint_resp = client.get_repository_endpoint(
        domain=domain,
        domainOwner=domain_owner,
        repository=repository,
        format='pypi'
    )

    repository_endpoint = repository_endpoint_resp['repositoryEndpoint']
    logger.debug(f"AWS CodeArtifact Endpoint: {repository_endpoint}")

    logger.debug("Getting AWS CodeArtifact Authorization Token")
    token_resp = client.get_authorization_token(
        domain=domain,
        domainOwner=domain_owner,
        durationSeconds=session_duration
    )

    logger.debug("AWS CodeArtifact Authorization Token obtained successfully")
    auth_token = token_resp['authorizationToken']

    cmd.exec_cmd([
        'poetry', 'config', f'repositories.{poetry_repository_name}',
        repository_endpoint
    ], working_dir='.')

    if sys.platform == 'win32':
        pypoetry_user_folder = str(Path(Path.home(), 'AppData/Roaming/pypoetry'))
        auth_toml_path = str(Path(pypoetry_user_folder, 'auth.toml'))
        logger.info(f"Writing AWS CodeArtifact Credentials in '{auth_toml_path}' file")
        if os.path.exists(auth_toml_path):
            logger.info(f"File '{auth_toml_path}' already exists, updating the credentials")
            with open(auth_toml_path, 'r+') as auth_toml:
                toml_data = toml.loads(auth_toml.read())

                if 'http-basic' not in toml_data:
                    toml_data['http-basic'] = {}

                http_basic_section = toml_data.get('http-basic')

                if poetry_repository_name not in http_basic_section:
                    http_basic_section[poetry_repository_name] = {}

                aws_section = http_basic_section.get(poetry_repository_name)
                aws_section['username'] = poetry_http_basic_user
                aws_section['password'] = auth_token

                auth_toml.seek(0)
                auth_toml.write(toml.dumps(toml_data))
                auth_toml.truncate()
        else:
            logger.info(f"File '{auth_toml_path}' does not exist, creating the file with the credentials")
            os.makedirs(pypoetry_user_folder, exist_ok=True)
            with open(auth_toml_path, 'w') as auth_toml:
                auth_toml.write(toml.dumps({
                    'http-basic': {
                        poetry_repository_name: {
                            'username': poetry_http_basic_user,
                            'password': auth_token
                        }
                    }
                }))
    else:
        cmd.exec_cmd([
            'poetry', 'config', f'http-basic.{poetry_repository_name}',
            poetry_http_basic_user, auth_token
        ], working_dir='.', hide_secrets=[auth_token])
    logger.info(f"Poetry login successful using AWS CodeArtifact repository {repository_endpoint}")

    hours = session_duration / 60 / 60
    session_date = datetime.now() + timedelta(seconds=session_duration)

    logger.info(f"Login expires in {int(hours)} hours at {str(session_date)}")
