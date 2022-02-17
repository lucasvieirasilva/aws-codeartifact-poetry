"""aws_codeartifact_poetry.aws.session unit tests."""

from unittest.mock import MagicMock, patch

import boto3
from moto.core.models import ACCOUNT_ID

from aws_codeartifact_poetry.aws import session

IAM_ROLE = f'arn:aws:iam::{ACCOUNT_ID}:role/testing-role'


def test_session_default(mock_sts):
    """Should return the default boto3 object."""
    result = session.get_session()

    assert boto3 == result
    assert type(result) is not boto3.Session


@patch("aws_codeartifact_poetry.aws.session.boto3")
def test_session_profile(mock_boto: MagicMock):
    """Should create a session using the profile name."""
    profile = 'fake-profile'
    session.get_session(profile=profile)
    mock_boto.Session.assert_called_once_with(profile_name=profile, region_name='us-east-1')


def test_session_with_role_without_context(mock_sts):
    """Should return the default boto3 object."""
    result = session.get_session(role=IAM_ROLE)

    assert boto3 == result
    assert type(result) is not boto3.Session


def test_session_with_role_and_context(mock_sts):
    """Should assume an IAM role and return a session with the temporary credentials."""
    result = session.get_session(role=IAM_ROLE, context='fake-context')

    assert type(result) is boto3.Session
    assert result.get_credentials().access_key is not None
    assert result.get_credentials().secret_key is not None
