from functools import wraps
from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_claims


def json_msg_response(msg, status_code):
        return make_response(jsonify({"msg": msg}), status_code)

def json_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return json_msg_response("Missing JSON", 400)
        else:
            return func(*args, **kwargs)

    return wrapper



def check_role(claims, role):
    if 'roles' not in claims.keys():
        return json_msg_response("invalid claims", 400)
    elif role not in claims['roles']:
        return json_msg_response("%s role required" % role, 403)
    else:
        return

def auth(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = check_role(get_jwt_claims(), role)

            if resp is not None:
                return resp
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator
