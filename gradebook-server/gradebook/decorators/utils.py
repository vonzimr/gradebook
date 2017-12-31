from functools import wraps
from flask import jsonify, make_response, request

def json_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            resp = make_response(jsonify({'msg': 'Missing JSON'}), 400)
            return resp
        else:
            return func(*args, **kwargs)

    return wrapper
