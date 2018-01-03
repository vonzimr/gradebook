from flask import current_app, Blueprint, request, jsonify, make_response
from functools import wraps
from flask_restful import Api, Resource, url_for, abort
from flask_jwt_extended import (JWTManager, get_jwt_identity,
                                jwt_required,
                               create_access_token, get_jwt_claims)

from .models import User, Role
from gradebook.database import db
from gradebook.decorators.utils import (json_msg_response, json_required,
                                       auth)

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

        if None in (username, password, email, role):
            return json_msg_response("Missing info in JSON", 400)


        #TODO: Better parsing of user input.
        if len(username) < 3:
            return json_msg_response("Username is too short", 400)


        if len(password) < 3:
            return json_msg_response("Password is too short", 400)

        if len(email) < 3:
            return json_msg_response("Invalid email", 400)


        if User.query.filter_by(username = username).first() is not None:
            return json_msg_response("Account already exists", 303)

        if User.query.filter_by(email = email).first() is not None:
            return json_msg_response("Email already in use", 303)

        user = User(username = username, email = email)
        user.hash_pass(password)
        try:
            user.set_role(role)
        except NoResultFound:
            return json_msg_response("Role does not exist", 400)

        db.session.add(user)
        db.session.commit()

        return json_msg_response("Account Created", 201)

class List(Resource):
    @jwt_required
    @auth("administrator")
    def get(self, role):
        accounts = User.query.filter(User.roles.any(name=role)).all()
        resp = make_response(jsonify([account.as_dict() for account in accounts]), 201)
        return resp

class UserInfo(Resource):
    @jwt_required
    @auth("administrator")
    def get(self, id):
        account = User.query.filter(User.id == id).first()
        if account is None:
            return json_msg_response("No user found.", 404)
        resp = make_response(jsonify(account.as_dict()), 200)
        return resp


api.add_resource(Login, '/login')
api.add_resource(Create, '/create')
api.add_resource(List, '/list/<string:role>')
api.add_resource(UserInfo, '/id/<int:id>')
