# flake8: noqa

import textwrap
import time
import threading

# Requests is the only supported HTTP library
import requests

import qonversion
from qonversion.logger import logger


def create_http_client(*args, **kwargs):
    return RequestsClient(*args, **kwargs)


class HTTPClient(object):
    MAX_DELAY = 2
    INITIAL_DELAY = 0.5

    def _sleep_time_seconds(self, num_retries):
        # Apply exponential backoff with INITIAL_DELAY on the number of num_retries so far as inputs.

        # Do not allow the number to exceed max_network_retry_delay.
        sleep_seconds = min(
            HTTPClient.INITIAL_DELAY * (2 ** (num_retries - 1)),
            HTTPClient.MAX_DELAY,
        )

        # But never sleep less than the base sleep seconds.
        sleep_seconds = max(HTTPClient.INITIAL_DELAY, sleep_seconds)

        return sleep_seconds

    def _get_max_network_retries(self):
        # Configured retries, isolated here for tests
        return qonversion.max_network_retries

    def request_with_retries(self, method, url, headers, post_data=None):
        num_retries = 0

        while True:
            try:
                response = self.request(method, url, headers, post_data)
                connection_error = None
            except qonversion.error.APIConnectionError as e:
                connection_error = e
                response = None

            if self._should_retry(response, connection_error, num_retries):
                if connection_error:
                    logger.info(
                        "Encountered a retryable error %s"
                        % connection_error.error_message
                    )
                num_retries += 1
                sleep_time = self._sleep_time_seconds(num_retries)
                logger.info(
                    (
                        "Initiating retry %i for request %s %s after sleeping %.2f seconds."
                        % (num_retries, method, url, sleep_time)
                    )
                )
                time.sleep(sleep_time)
            else:
                if response is not None:
                    return response
                else:
                    raise connection_error

    def request(self, method, url, headers, post_data=None):
        raise NotImplementedError(
            "HTTPClient subclasses must implement `request`"
        )

    def _should_retry(self, response, api_connection_error, num_retries):
        if num_retries >= self._get_max_network_retries():
            return False

        if response is None:
            # Underlying error (like connection error, timeout error e.t.c.)
            # will determine the need of request retry
            return api_connection_error.should_retry

        _, status_code, _ = response

        # Retry on 500, 503, and other internal errors.
        if status_code >= 500:
            return True

        return False

    def close(self):
        raise NotImplementedError(
            "HTTPClient subclasses must implement `close`"
        )


class RequestsClient(HTTPClient):
    name = "requests"

    def __init__(self, timeout=80, session=None, **kwargs):
        super(RequestsClient, self).__init__(**kwargs)
        self._session = session
        self._timeout = timeout
        self._thread_local = threading.local()

    def request(self, method, url, headers, post_data=None):
        kwargs = {}

        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = self._session or requests.Session()

        try:
            try:
                result = self._thread_local.session.request(
                    method,
                    url,
                    headers=headers,
                    data=post_data,
                    timeout=self._timeout,
                    **kwargs
                )
            except TypeError as e:
                raise TypeError(
                    "Version of the 'requests' library is not compatible "
                    "or out of date. Underlying error was: %s" % (e,)
                )

            content = result.content
            status_code = result.status_code
        except Exception as e:
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            self._handle_request_error(e)

        return content, status_code, result.headers

    def _handle_request_error(self, e):

        msg = "Unexpected error communicating with Qonversion."
        err = "%s: %s" % (type(e).__name__, str(e))

        # Retry only timeout and connect error
        if isinstance(e, requests.exceptions.SSLError):
            msg = "Could not verify SSL certificate."
            should_retry = False
        elif isinstance(
            e,
            (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        ):
            should_retry = True
        # Catch remaining request exceptions
        elif isinstance(e, requests.exceptions.RequestException):
            should_retry = False
        else:
            msg += " It looks like there's probably a configuration issue locally."
            err = "A %s was raised" % (type(e).__name__,)
            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"
            should_retry = False

        msg = textwrap.fill(msg) + "\n\n(Network error: %s)" % (err,)
        raise qonversion.error.APIConnectionError(
            msg, should_retry=should_retry
        )

    def close(self):
        if getattr(self._thread_local, "session", None) is not None:
            self._thread_local.session.close()
