from flask import current_app, Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource, url_for, abort
from flask_jwt_extended import (JWTManager, get_jwt_identity,
                                jwt_required,
                               create_access_token, get_jwt_claims)

from .models import User, Role
from gradebook.database import db
from gradebook.decorators.utils import json_required

from sqlalchemy.orm.exc import NoResultFound

accounts = Blueprint('accounts', __name__,
                  url_prefix = '/accounts')
api = Api(accounts)
jwt = JWTManager()




@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'roles' : user.get_roles()}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

def json_msg_response(msg, status_code):
        return make_response(jsonify({"msg": msg}), status_code)

class Login(Resource):
    @jwt_required
    def get(self):
        return {"identity" : get_jwt_identity(),
                "claims": get_jwt_claims()}

    @json_required
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            return json_msg_response("No username or password specified", 400)

        user = User.query.filter_by(username = username).first()

        if user is None:
            return json_msg_response("Username or password is incorrect.", 401)

        if user.verify_pass(password):
            return {'access-token': create_access_token(user)}
        else:
            return json_msg_response("Username or password is incorrect.", 401)


class Create(Resource):
    @json_required
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        email    = request.json.get('email')
        role     = request.json.get('role')
        resp = {}

        if None in (username, password, email, role):
            resp['msg'] = "Missing info in JSON"
            return make_response(jsonify(resp), 400)


        if len(username) < 3:
            resp['msg'] = "Username is too short."
            return make_response(jsonify(resp), 400)


        if len(password) < 3:
            resp['msg'] = "Password is too short."
            return make_response(jsonify(resp), 400)

        if len(email) < 3:
            resp['msg'] = "email is too short."
            return make_response(jsonify(resp), 400)


        if User.query.filter_by(username = username).first() is not None:
            response = make_response(jsonify({"msg": "Account Already Exists"}), 303)
            return response

        user = User(username = username, email = email)
        user.hash_pass(password)
        try:
            user.set_role(role)
        except NoResultFound:
            response = make_response(jsonify({"msg": "Role does not exist."}), 400)
            return response

        db.session.add(user)
        db.session.commit()

        response = make_response(jsonify({"msg": "Account Created"}), 201)
        return response


api.add_resource(Login, '/login')
api.add_resource(Create, '/create')
