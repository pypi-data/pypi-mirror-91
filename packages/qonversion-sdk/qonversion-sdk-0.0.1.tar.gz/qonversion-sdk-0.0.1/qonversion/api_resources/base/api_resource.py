from qonversion.qobject import QObject


class APIResource(QObject):
    @classmethod
    def class_url(cls):
        if cls == APIResource:
            raise NotImplementedError(
                "Can't access to actions in APIResource class"
            )
        # Replace dots (.) in object names (if exists) with forward slashes (/)
        # for correct object URLs receiving
        base_url = cls.OBJECT_NAME.replace(".", "/")
        return "/v2/%ss" % (base_url,)
