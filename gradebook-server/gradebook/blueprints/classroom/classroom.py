from flask import current_app, Blueprint, request, jsonify, make_response
from functools import wraps
from flask_restful import Api, Resource, url_for, abort
from flask_jwt_extended import (JWTManager, get_jwt_identity,
                                jwt_required,
                               create_access_token, get_jwt_claims)

from .models import Classroom, Student
from gradebook.database import db
from gradebook.decorators import auth, json_required
from gradebook.utils import json_msg_response

from sqlalchemy.orm.exc import NoResultFound

classroom = Blueprint('classroom', __name__,
                  url_prefix = '/classroom')
api = Api(accounts)
jwt = JWTManager()

class Create(Resource):
    @jwt_required
    def post(self):
        pass

api.add_resource(Create, '/create')
