import json
from sqlalchemy.orm import class_mapper
from datetime import datetime

def resp_result(status=200, data=None, message=""):
    if data:
        data = object_to_dict(data)
    else:
        data = {}

    result = {
        "status" : status,
        "data" : data,
        "message" : message
    }
    return json.dumps(result)



def object_to_dict(obj):
    columns = [column.key for column in class_mapper(obj.__class__).columns]
    get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (
        c, getattr(obj, c))
    return dict(map(get_key_value, columns))