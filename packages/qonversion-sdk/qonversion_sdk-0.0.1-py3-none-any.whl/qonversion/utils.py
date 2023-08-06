import qonversion


def get_object_map():
    # import is here for fixing the circular import
    from qonversion.object_map import OBJECT_MAP

    return OBJECT_MAP


def convert_to_qobject(data, api_key=None):
    if isinstance(data, qonversion.response.QResponse):
        data = data.data
    if isinstance(data, list):
        return [convert_to_qobject(item, api_key) for item in data]
    elif isinstance(data, dict) and not isinstance(
        data, qonversion.qobject.QObject
    ):
        data = data.copy()
        class_name = data.get("object")
        if isinstance(class_name, str):
            metaclass = get_object_map().get(
                class_name, qonversion.qobject.QObject
            )
        else:
            metaclass = qonversion.qobject.QObject

        return metaclass.construct_from(data, api_key)
    else:
        return data
