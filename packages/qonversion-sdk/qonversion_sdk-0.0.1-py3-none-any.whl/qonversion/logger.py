import qonversion
import os
import sys
import re
import logging

__all__ = ["logger"]


class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger("qonversion")

    def _console_log_level(self):

        qonversion_log_env = os.environ.get("QONVERSION_LOG")

        if qonversion.log in ["debug", "info"]:
            return qonversion.log
        elif qonversion_log_env in ["debug", "info"]:
            return qonversion_log_env
        else:
            return None

    def format_log(self, props):
        def _format(key, val):
            if not isinstance(val, str):
                val = str(val)
            if re.search(r"\s", val):
                val = repr(val)
            # key should already be a string
            if re.search(r"\s", key):
                key = repr(key)
            return u"{key}={val}".format(key=key, val=val)

        return u" ".join(
            [_format(key, val) for key, val in sorted(props.items())]
        )

    def debug(self, message, **params):
        msg = self.format_log(dict(message=message, **params))
        if self._console_log_level() == "debug":
            print(msg, file=sys.stderr)
        self.logger.debug(msg)

    def info(self, message, **params):
        msg = self.format_log(dict(message=message, **params))
        if self._console_log_level() in ["debug", "info"]:
            print(msg, file=sys.stderr)
        self.logger.info(msg)


logger = Logger()
