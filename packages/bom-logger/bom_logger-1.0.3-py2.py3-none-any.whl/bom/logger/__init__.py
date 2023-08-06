""" __init__.py """


import logging
import logging.config
import logging.handlers

from bom.configuration.config import Config  # pylint: disable=import-error

from . import formatter  # pylint: disable=import-error
from . import handler  # pylint: disable=import-error


def setup_logger(
    config: Config,
) -> None:
    """ setup_logger """

    assert config

    json_formatter = formatter.JsonFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(json_formatter)
    stream_handler.set_name("root_stream_handler")
    http_handler = handler.HttpHandler(
        config.get_string("bomt1me.logger.path"),
        config.get_string("bomt1me.logger.url"),
        method=config.get_string("bomt1me.logger.method"),
        timeout=config.get_float("bomt1me.logger.timeout"),
    )
    http_handler.setFormatter(json_formatter)
    http_handler.set_name("root_http_handler")
    root = logging.getLogger()
    while root.hasHandlers():
        root.removeHandler(root.handlers[0])
    root.addHandler(stream_handler)
    root.addHandler(http_handler)
    root.setLevel(logging.DEBUG)
