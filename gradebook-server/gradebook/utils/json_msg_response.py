from flask import jsonify, make_response, request


def json_msg_response(msg, status_code):
        return make_response(jsonify({"msg": msg}), status_code)

