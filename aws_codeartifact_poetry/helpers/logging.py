"""Default CLI Logger class."""

import logging
from typing import Optional


def _get_formatter(custom_format: Optional[str] = None) -> logging.Formatter:
    """
    Get Logger Formatter [%(asctime)s] - %(message)s.

    Args:
        custom_format (`str`): custom format
    Returns:
        `logging.Formatter` logger formatter
    """
    fmt = "[%(asctime)s] - %(levelname)s - %(message)s"
    if custom_format:
        fmt = custom_format

    return logging.Formatter(
        fmt=fmt,
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def setup_logging(logger_name: str, log_level: str, file_output: Optional[str]) -> None:
    """
    Setups logging class.

    By default, the python logging module is configured to push logs to stdout
    as long as their level is at least INFO. The log format is set to
    "[%(asctime)s] - %(levelname)s - %(message)s" and the date format is set to
    "%Y-%m-%d %H:%M:%S".

    After this function has run, modules should:

    .. code:: python
        import logging
        logging.getLogger(__name__).info("my log message")

    Args:
        logger_name (`str`): The name of the logger to be configured.
        log_level (`str`): Setup log level.
        file_output (`str`, optional): file output to the logs.

    Returns:
        None
    """
    if log_level.upper() == 'DEBUG':
        logging.getLogger("botocore").setLevel(logging.INFO)
    else:
        logging.getLogger("botocore").setLevel(logging.CRITICAL)

    # Create the logger based on the name recieved
    logger = logging.getLogger(logger_name)

    # Configure the stream handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(_get_formatter())

    # Add the stream handler to the logger with the appropriate log level.
    logger.addHandler(console_handler)
    logger.setLevel(log_level)

    # Setup file handler if specified.
    if file_output:
        file_handler = logging.FileHandler(file_output)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

    return None
