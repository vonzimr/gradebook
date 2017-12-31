import unittest
from flask import json, jsonify
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
            create_user_roles(self.app)


    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_db_roles_len(self):
        with self.app.app_context():
            roles = Role.query.all()
            self.assertEqual(len(roles), 3)

    def test_all_roles_exist(self):
        with self.app.app_context():
            self.assertEqual(Role.query.filter_by(name='teacher').count(), 1)
            self.assertEqual(Role.query.filter_by(name='administrator').count(), 1)
            self.assertEqual(Role.query.filter_by(name='specialist').count(), 1)

    def test_missing_json(self):

        data = dict(username = 'test',
                    password = 'test')

        request = self.client.post('/accounts/login', data=data)

        self.assertEqual(request.status, '400 BAD REQUEST')

    def test_add_teacher(self):
        with self.app.app_context():
            self.create_user('test_user', 'test@test.com', 'password', 'teacher')
            user = User.query.filter_by(username='test_user').first()

            self.assertEqual(user.username,'test_user')
            self.assertEqual(user.email, 'test@test.com')
            self.assertNotEqual(user.password , 'password')
            self.assertEqual(user.get_roles(), ['teacher'])

    def create_user(self, username, email, password, role):
        payload = dict(username=username, password=password,
                       email=email, role=role)

        return self.client.post('/accounts/create', data=json.dumps(payload), content_type='application/json')

    def get_user_info(self, user, password):
        request = self.client.post('/accounts/login',
                          json = dict(username = username,
                                      password = password),
                                content_type = 'application/json')


        token   = request['access-token']
        headers = {'Authorization' : 'Bearer ' + token}

        return self.app.get('/accounts/login', headers=headers)

