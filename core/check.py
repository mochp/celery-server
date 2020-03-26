from core.sql import getMenuFeature

def check_format_all(jsondata):
    try:
        assert jsondata["data"]
        status = True
    except Exception as e:
        status = False
    finally:
        return status


def check_obj_format(obj):
    try:
        assert obj["url"]
        assert obj["type"]
        assert obj["modelId"]
        status = True
    except Exception as e:
        status = False
    return status


def check_obj_modelId(obj):
    if obj["modelId"] in [400, 500, 600]:
        return True
    try:
        getMenuFeature(obj["modelId"])
        status = True
    except Exception as e:
        status = False
    return status
