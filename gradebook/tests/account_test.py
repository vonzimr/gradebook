import unittest
from flask import json
from gradebook import create_app
from gradebook.database import db
from gradebook.blueprints.accounts.models import User, Role
from gradebook.blueprints.accounts.add_user_roles import create_user_roles

class AccountTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('../configurations/testing.cfg')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            create_user_roles(self.app, db)


    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_db_roles_len(self):
        with self.app.app_context():
            roles = Role.query.all()
            assert len(roles) == 3

    def test_all_roles_exist(self):
        with self.app.app_context():
            assert Role.query.filter_by(name='teacher').count()  == 1
            assert Role.query.filter_by(name='administrator').count() == 1
            assert Role.query.filter_by(name='specialist').count() == 1


    def test_add_teacher(self):
        with self.app.app_context():
            self.create_user('test_user', 'test@test.com', 'password', 'teacher')
            user = User.query.filter_by(username='test_user').first()

            assert user.username == 'test_user'
            assert user.email == 'test@test.com'
            assert user.password != 'password'
            assert user.get_roles() == ['teacher']

    def create_user(self, username, email, password, role):
        payload = dict(username=username, password=password,
                       email=email, role=role)

        return self.client.post('/accounts/create', data=json.dumps(payload), content_type='application/json')

    def get_user_info(self, user, password):
        request = self.app.post('/accounts/login',
                          json = dict(username = username,
                                      password = password),
                                content_type = 'application/json')


        token   = request['access-token']
        headers = {'Authorization' : 'Bearer ' + token}

        return self.app.get('/accounts/login', headers=headers)

