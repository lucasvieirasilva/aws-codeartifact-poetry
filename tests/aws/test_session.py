"""aws_codeartifact_poetry.aws.session unit tests."""

from unittest.mock import MagicMock, patch

import boto3

from aws_codeartifact_poetry.aws import session

IAM_ROLE = 'arn:aws:iam::123456789011:role/testing-role'


def test_session_default():
    """Should return the default boto3 object."""
    result = session.get_session()

    assert type(result) is boto3.Session


@patch("aws_codeartifact_poetry.aws.session.boto3")
def test_session_profile(mock_boto: MagicMock):
    """Should create a session using the profile name."""
    profile = 'fake-profile'
    session.get_session(profile=profile)
    mock_boto.Session.assert_called_once_with(profile_name=profile, region_name='us-east-1')


def test_session_with_role_without_context():
    """Should return the default boto3 object."""
    result = session.get_session(role=IAM_ROLE)

    assert type(result) is boto3.Session


@patch("aws_codeartifact_poetry.aws.session.boto3")
def test_session_with_role_and_context(mock_boto3: MagicMock):
    """Should assume an IAM role and return a session with the temporary credentials."""
    mock_boto3.client().assume_role.return_value = {
        'Credentials': {
            'AccessKeyId': 'fake-access-key-id',
            'SecretAccessKey': 'fake-secret-access-key',
            'SessionToken': 'fake-session-token'
        }
    }
    mock_boto3.Session = boto3.Session

    result = session.get_session(role=IAM_ROLE, context='fake-context')

    assert type(result) is boto3.Session
    assert result.get_credentials().access_key == 'fake-access-key-id'
    assert result.get_credentials().secret_key == 'fake-secret-access-key'
    assert result.get_credentials().token == 'fake-session-token'
