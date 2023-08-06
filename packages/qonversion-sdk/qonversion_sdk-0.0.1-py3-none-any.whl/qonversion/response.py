import json
from collections import OrderedDict


class QResponse(object):
    def __init__(self, body, code, headers):
        self.body = body
        self.code = code
        self.headers = headers
        # leave keys sorted the same way as in raw json
        self.data = json.loads(body, object_pairs_hook=OrderedDict)
