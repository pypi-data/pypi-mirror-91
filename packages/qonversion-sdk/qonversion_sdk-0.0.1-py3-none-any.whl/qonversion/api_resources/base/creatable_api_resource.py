from qonversion import api_requestor, utils
from qonversion.api_resources.base.api_resource import APIResource


class CreatableAPIResource(APIResource):
    @classmethod
    def create(cls, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url()
        response = requestor.request("post", url, params)

        return utils.convert_to_qobject(response, api_key)
