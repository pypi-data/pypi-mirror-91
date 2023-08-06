import json
import qonversion


class QError(Exception):
    def __init__(
        self, message=None, json_body=None, http_status=None, error_code=None
    ):
        super(QError, self).__init__(message)

        self._message = message
        self.http_status = http_status
        if json_body and isinstance(json_body, str):
            json_body = json.loads(json_body)
        self.json_body = json_body
        self.error_code = error_code
        self.error = self.construct_error_object()

    def __str__(self):
        return self._message or "<empty message>"

    # Returns the underlying `Exception` (base class) message
    @property
    def error_message(self):
        return self._message

    def __repr__(self):
        return "%s(code=%r, message=%r, http_status=%r)" % (
            self.__class__.__name__,
            self.error_code,
            self._message,
            self.http_status,
        )

    def construct_error_object(self):
        from qonversion.api_resources import ErrorObject

        if (
            self.json_body is None
            or "error" not in self.json_body
            or not isinstance(self.json_body["error"], dict)
        ):
            return None

        return ErrorObject.construct_from(
            self.json_body["error"], qonversion.api_key
        )


class APIError(QError):
    pass


class APIConnectionError(QError):
    def __init__(
        self, message, http_status=None, json_body=None, should_retry=False
    ):
        super(APIConnectionError, self).__init__(
            message, http_status, json_body
        )
        self.should_retry = should_retry


class AuthenticationError(QError):
    pass


class InvalidRequestError(QError):
    pass
