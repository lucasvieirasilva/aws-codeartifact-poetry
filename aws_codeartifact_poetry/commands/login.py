"""AWS codeartifact login command (aws-codeartifact-poetry login --help)."""

import shutil
from typing import Optional

import click

from aws_codeartifact_poetry.aws import session
from aws_codeartifact_poetry.helpers import poetry
from aws_codeartifact_poetry.helpers.catch_exceptions import CLIError, catch_exceptions


@click.command(help='Login to AWS CodeArtifact')
@click.option(
    '--repository',
    help='Your CodeArtifact repository name',
    type=str,
    required=True
)
@click.option(
    '--domain',
    help='Your CodeArtifact domain name',
    type=str,
    required=True
)
@click.option(
    '--domain-owner',
    help='The AWS account ID that owns your CodeArtifact domain',
    type=str,
    required=True
)
@click.option(
    '--profile',
    help='AWS Profile.',
    type=str,
    required=False
)
@click.option(
    '--region',
    help='AWS Region name',
    default='us-east-1',
    show_default=True,
    type=str,
    required=False
)
@catch_exceptions
def login(
    repository: str,
    domain: str,
    domain_owner: str,
    profile: Optional[str],
    region: Optional[str]
):
    """
    Authenticate in the AWS CodeArtifact repository and set the credentials in the poetry configuration.

    Args:
        domain (`str`): AWS CodeArtifact domain name
        domain_owner (`str`): AWS CodeArtifact domain onwer
        repository (`str`): AWS CodeArtifact repository name
        profile (`str`, optional): AWS Profile
        region (`str`, optional): AWS Region, default `us-east-1`
    """
    if shutil.which('poetry') is not None:
        poetry.codeartifact_login(
            session=session.get_session(
                region=region,
                profile=profile
            ),
            domain=domain,
            domain_owner=domain_owner,
            repository=repository
        )
        click.echo("Poetry login successful using AWS CodeArtifact")
    else:
        raise CLIError("Executable 'poetry' not found in your environment")
