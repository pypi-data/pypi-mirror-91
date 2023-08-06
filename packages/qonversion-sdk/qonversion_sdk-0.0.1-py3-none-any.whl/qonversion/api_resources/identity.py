from qonversion.api_resources.base import CreatableAPIResource


class Identity(CreatableAPIResource):
    OBJECT_NAME = "identity"

    @classmethod
    def class_url(cls):
        return "/v2/identities"
