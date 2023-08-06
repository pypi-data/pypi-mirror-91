from qonversion.api_resources.base import CreatableAPIResource
from qonversion.api_resources.base import RetrievableAPIResource


class User(RetrievableAPIResource, CreatableAPIResource):
    OBJECT_NAME = "user"
