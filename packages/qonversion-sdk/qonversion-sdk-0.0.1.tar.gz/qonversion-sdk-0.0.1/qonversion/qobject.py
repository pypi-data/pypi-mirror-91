import json

import qonversion.utils as utils
from typing import Dict, Optional
from qonversion.api_requestor import APIRequestor


class QObject(dict):
    def __init__(self, api_key=None, **params):
        super(QObject, self).__init__()
        object.__setattr__(self, "api_key", api_key)
        if "id" in params.keys():
            object.__setattr__(self, "id", params["id"])
        self._retrieve_params = params

    def __setattr__(self, k, v):
        if k[0] == "_" or k in self.__dict__:
            return super(QObject, self).__setattr__(k, v)
        self[k] = v
        return None

    def __getattr__(self, k):
        if k[0] == "_":
            raise AttributeError(k)
        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        if k[0] == "_" or k in self.__dict__:
            return super(QObject, self).__delattr__(k)
        else:
            del self[k]

    def __setitem__(self, k, v):
        super(QObject, self).__setitem__(k, v)

    @classmethod
    def api_base(cls):
        return None

    def __repr__(self):
        ident_parts = [type(self).__name__]
        return "<%s at %s> JSON: %s" % (
            " ".join(ident_parts),
            hex(id(self)),
            str(self),
        )

    def __str__(self):
        return json.dumps(
            self.to_dict(), sort_keys=True, indent=2, cls=QObjectEncoder
        )

    def to_dict(self):
        return dict(self)

    def restore_from(self, values: Dict, api_key: Optional[str] = None):
        self.__setattr__(
            "api_key", api_key or getattr(values, "api_key", None)
        )

        for key, value in values.items():
            super(QObject, self).__setitem__(
                key, utils.convert_to_qobject(value, api_key)
            )

    @classmethod
    def construct_from(cls, values: Dict, key: Optional[str] = None):
        instance = cls(api_key=key)
        instance.restore_from(values, api_key=key)
        return instance

    def request(self, method, url, params=None, headers=None):
        if params is None:
            params = self._retrieve_params
        response = APIRequestor(
            api_key=self.api_key, api_base=self.api_base()
        ).request(method, url, params, headers)

        return utils.convert_to_qobject(response, self.api_key)


class QObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        return super(QObjectEncoder, self).default(obj)
