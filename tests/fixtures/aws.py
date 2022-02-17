"""Common AWS fixtures."""

import os
import pathlib

import boto3
import botocore
import moto
import pytest
from moto.core import ACCOUNT_ID
from pyfakefs.fake_filesystem import FakeFilesystem

DEFAULT_AWS_REGION = 'us-east-1'


@pytest.fixture()
def setup_aws_credentials_env_vars():
    """Setups fake AWS Credentials env vars."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_REGION'] = DEFAULT_AWS_REGION
    os.environ['ACCOUNT_ID'] = ACCOUNT_ID

    boto3.setup_default_session(region_name=DEFAULT_AWS_REGION)
    return None


@pytest.fixture()
def mock_sts(setup_aws_credentials_env_vars):
    """Mock STS."""
    with moto.mock_sts():
        yield boto3.client('sts', region_name=DEFAULT_AWS_REGION)


@pytest.fixture()
def motofs(fs: FakeFilesystem):
    """Fix moto library when fake filesystem is enabled."""
    for module in [boto3, botocore]:
        module_dir = pathlib.Path(module.__file__).parent
        fs.add_real_directory(module_dir, lazy_read=False)

    return fs
