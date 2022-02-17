"""AWS CodeArtifact Poetry CLI Definition."""

from typing import Optional

import click
from click import Context

from aws_codeartifact_poetry.commands.login import login
from aws_codeartifact_poetry.helpers.catch_exceptions import catch_exceptions
from aws_codeartifact_poetry.helpers.logging import setup_logging


@click.group(help='AWS CodeArtifact Poetry CLI.')
@click.option(
    '--loglevel',
    help='Log level.',
    required=False,
    default='WARNING',
    show_default=True,
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False)
)
@click.option(
    '--log-file',
    help='Log file name',
    required=False,
    type=str
)
@catch_exceptions
@click.pass_context
def cli(ctx: Context, loglevel: str, log_file: Optional[str]):
    """
    CLI group root function (aws-codeartifact-poetry --help).

    Args:
        ctx (`Context`): click context
        loglevel (`str`): loglevel
        log_file (`str`, optional): output log file
    """
    ctx.ensure_object(dict)
    ctx.obj['loglevel'] = loglevel

    setup_logging(__package__, loglevel, log_file)


cli.add_command(login)
