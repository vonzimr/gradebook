from flask import current_app, Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource, url_for, abort
from flask_jwt_extended import (JWTManager, get_jwt_identity,
                                jwt_required,
                               create_access_token, get_jwt_claims)

from .models import User, Role
from gradebook.database import db
from gradebook.decorators.utils import json_required

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
            abort(400)

        user = User.query.filter_by(username = username).first()
        if user is None:
            abort(400)

        if user.verify_pass(password):
            return {'access-token': create_access_token(user)}
        else:
            abort(401)


class Create(Resource):
    @json_required
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        email    = request.json.get('email')
        if username is None or password is None:
            abort(400)
        if User.query.filter_by(username = username).first() is not None:
            abort(400)

        user = User(username = username, email = email)
        user.hash_pass(password)
        user.roles.append(Role.query.filter_by(name="teacher").first())
        db.session.add(user)
        db.session.commit()





api.add_resource(Login, '/login')
api.add_resource(Create, '/create')
