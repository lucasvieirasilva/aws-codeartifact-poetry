"""boto3 session helper."""
import boto3


def get_session(region="us-east-1", profile=None, role=None, context=None):
    """
    boto3 session builder.

    Args:
        region (`str`): the AWS Region, default us-east-1
        profile (`str`, optional): the AWS Profile to be used
        role (`str`, optional): the AWS Role to be assumed (Required if profile is not defined)
        context (`str`, optional): the Role Session Name to be used when assuming role \
            (Required if profile is not defined)
    Returns:
        `boto3.Session` boto3 session
    """
    if profile is not None:
        return boto3.Session(
            profile_name=profile,
            region_name=region
        )

    if role is not None and context is not None:
        sts_client = boto3.client('sts')
        response = sts_client.assume_role(
            RoleArn=role,
            RoleSessionName=context
        )

        credentials = response['Credentials']
        return boto3.Session(
            region_name=region,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    return boto3.Session(region_name=region)
