""" handler.py """


import http.client
import logging
import logging.handlers
from typing import Any


class HttpHandler(logging.handlers.HTTPHandler):
    """ HttpHandler """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        host: str,
        url: str,
        method: str = "GET",
        secure: bool = False,
        credentials: Any = None,
        context: Any = None,
        timeout: int = 20,
    ) -> None:
        """__init__"""

        super().__init__(
            host,
            url,
            method=method,
            secure=secure,
            credentials=credentials,
            context=context,
        )
        self.timeout = timeout

    def getConnection(self, host: str, secure: bool) -> http.client.HTTPConnection:
        """getConnection"""

        return http.client.HTTPConnection(host, timeout=self.timeout)

    def serialized_record(self, record: logging.LogRecord) -> str:
        """serialized_record"""

        return self.format(record)

    def emit(self, record: logging.LogRecord) -> None:
        """emit"""
        try:
            connection = self.getConnection(self.host, self.secure)
            data = self.serialized_record(record)
            headers = {
                "Content-type": "application/json",
                "Content-length": str(len(data)),
            }
            connection.request(self.method, self.url, data, headers)
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)
