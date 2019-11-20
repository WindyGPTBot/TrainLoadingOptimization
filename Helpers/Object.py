
def get_deep_attr(obj, attrs):
    for attr in attrs.split("."):
        obj = getattr(obj, attr)
    return obj

def has_deep_attr(obj, attrs):
    try:
        get_deep_attr(obj, attrs)
        return True
    except AttributeError:
        return False