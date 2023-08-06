from qonversion import error
from qonversion.api_resources.base.api_resource import APIResource
from urllib.parse import quote_plus


class RetrievableAPIResource(APIResource):
    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        params["id"] = id
        instance = cls(api_key, **params)
        instance.restore()
        return instance

    def restore(self):
        self.restore_from(self.request("get", self.instance_url()))
        return self

    def instance_url(self):
        instance_id = self.id

        if not isinstance(instance_id, str):
            raise error.InvalidRequestError(
                "%s instance has invalid ID: %r, %s. ID should be of type `str`"
                % (type(self).__name__, id, type(instance_id))
            )
        base_url = self.class_url()
        extn = quote_plus(instance_id)
        return "%s/%s" % (base_url, extn)
