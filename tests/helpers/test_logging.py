"""aws_codeartifact_poetry.helpers.logging unit tests."""

import io
import logging
from unittest.mock import MagicMock, patch

from aws_codeartifact_poetry.helpers.logging import _get_formatter, setup_logging


# This mock avoids the creation of a file in disk when the file_handler is created.
# instead, we return a bytes stream
@patch('logging.FileHandler._open')
def test_logging_with_file_handler(mock_file_handler: MagicMock):
    """Test setup_logging with a file handler."""
    mock_file_handler.return_value = io.BytesIO()
    setup_logging('test', 'DEBUG', 'testfile')
    assert len(logging.getLogger('test').handlers) == 2
    assert logging.getLogger("botocore").level == logging.INFO


def test_logging_with_info():
    """Test setup_logging with INFO level."""
    setup_logging('test2', 'INFO', '')
    assert len(logging.getLogger('test2').handlers) == 1
    assert logging.getLogger("botocore").level == logging.CRITICAL


def test__get_formatter():
    """Test _get_formatter with a custom format."""
    result = _get_formatter("[%(asctime)s] - %(levelname)s - %(message)s")
    assert isinstance(result, logging.Formatter)
