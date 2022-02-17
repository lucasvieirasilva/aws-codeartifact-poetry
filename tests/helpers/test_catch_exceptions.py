"""aws_codeartifact_poetry.helpers.catch_exceptions unit tests."""

import pytest
from _pytest.logging import LogCaptureFixture

from aws_codeartifact_poetry.helpers.catch_exceptions import CLIError, catch_exceptions


def test_catch_exceptions(caplog: LogCaptureFixture):
    """Should handle the exception, log the error and exit with code 1."""
    @catch_exceptions
    def some_stuff():
        raise CLIError('unit tests1')

    with pytest.raises((CLIError, SystemExit)) as sys_exit:
        some_stuff()

    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 1
    assert 'unit tests1' in caplog.text


def test_catch_exceptions_no_exception():
    """Should continue the function normally."""
    @catch_exceptions
    def some_stuff():
        return 'success'

    result = some_stuff()

    assert result == 'success'
