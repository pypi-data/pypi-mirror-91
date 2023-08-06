import platform
from urllib.parse import urlencode, urlsplit, urlunsplit
from typing import Dict, Optional

import qonversion
from qonversion import error, http_client, version
from qonversion.logger import logger
from qonversion.response import QResponse


class APIRequestor(object):
    def __init__(self, api_key=None, client=None, api_base=None):
        self.api_base = api_base or qonversion.api_base
        self.api_key = api_key

        if client:
            self._client = client
        else:
            self._client = http_client.create_http_client()

    def _build_api_url(self, url, query):
        scheme, netloc, path, base_query, fragment = urlsplit(url)

        if base_query:
            query = "%s&%s" % (base_query, query)

        return urlunsplit((scheme, netloc, path, query, fragment))

    def request(self, method, url, params=None, headers=None) -> QResponse:
        response_body, response_code, response_headers, api_key = self._request_raw(
            method.lower(), url, params, headers
        )
        response = self._interpret_response(
            response_body, response_code, response_headers
        )
        return response

    def handle_error_response(
        self, response_body, response_code, response_data
    ):
        try:
            error_data = response_data["error"]
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (response_body, response_code),
                http_status=response_code,
            )

        err = self._get_specific_api_error(
            response_body, response_code, error_data
        )
        raise err

    def _get_specific_api_error(
        self, response_body, response_code, error_data
    ):
        logger.info(
            "Qonversion API error received",
            error_code=error_data.get("code"),
            error_type=error_data.get("type"),
            error_message=error_data.get("message"),
            error_param=error_data.get("param"),
        )

        if response_code == 400:
            return error.InvalidRequestError(
                error_data.get("message"), response_body, response_code
            )
        elif response_code == 401:
            return error.AuthenticationError(
                error_data.get("message"), response_body, response_code
            )
        else:
            return error.APIError(
                error_data.get("message"), response_body, response_code
            )

    def _get_request_headers(self, api_key):
        user_agent = "Qonversion PythonBindings/%s" % (version.VERSION,)

        ua = {
            "bindings_version": version.VERSION,
            "lang": "python",
            "publisher": "qonversion",
        }
        for attr, func in [
            ["lang_version", platform.python_version],
            ["platform", platform.platform],
            ["uname", lambda: " ".join(platform.uname())],
        ]:
            try:
                # It can be value or a function
                val = func()
            except Exception as e:
                val = "!! %s" % (e,)
            ua[attr] = val

        headers = {
            "User-Agent": user_agent,
            "Authorization": "Bearer %s" % (api_key,),
            "Content-Type": "application/json",
        }

        return headers

    def _request_raw(
        self,
        method,
        url,
        params: Optional[Dict] = None,
        supplied_headers: Optional[Dict] = None,
    ):
        """
        Low level implementation of request issuing
        """

        if self.api_key:
            q_api_key = self.api_key
        else:
            from qonversion import api_key

            q_api_key = api_key

        if q_api_key is None:
            raise error.AuthenticationError(
                "No API key provided. (HINT: set your API key using qonversion.api_key = <API-KEY>"
            )

        abs_url = "%s%s" % (self.api_base, url)
        encoded_params = urlencode(params or {})

        if method == "get" or method == "delete":
            if params:
                abs_url = self._build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == "post":
            post_data = params or ""
        else:
            raise error.APIConnectionError(
                "Unrecognized HTTP method %r. This may indicate a bug in the "
                "Qonversion bindings.  Please contact hi@qonversion.io for "
                "assistance." % (method,)
            )

        headers = self._get_request_headers(q_api_key)
        if supplied_headers is not None:
            for key, value in supplied_headers.items():
                headers[key] = value

        logger.info("Request to Qonversion api", method=method, path=abs_url)
        logger.debug("Post details", post_data=encoded_params)

        response_body, response_code, response_headers = self._client.request_with_retries(
            method, abs_url, headers, post_data
        )

        logger.info(
            "Qonversion API response",
            path=abs_url,
            response_code=response_code,
        )
        logger.debug("API response body", body=response_body)

        return response_body, response_code, response_headers, q_api_key

    def _interpret_response(
        self, response_body, response_code, response_headers
    ):
        try:
            response = QResponse(
                response_body, response_code, response_headers
            )
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (response_body, response_code),
                http_status=response_code,
            )
        if not 200 <= response_code < 300:
            self.handle_error_response(
                response_body, response_code, response.data
            )

        return response
