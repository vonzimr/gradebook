from functools import wraps
from flask import request
from gradebook.utils import json_msg_response
def json_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return json_msg_response("Missing JSON", 400)
        else:
            return func(*args, **kwargs)

    return wrapper

