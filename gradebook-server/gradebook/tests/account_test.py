import itertools
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

    def test_create_missing_data(self):
        payload = dict(username="test", password="testing",
                       email="test@test.com", role="teacher")

        for i  in range(0, len(payload.keys()) -1):
            for keyperm in itertools.permutations(payload.keys(), i):
                partial_data = {key : payload[key] for key in keyperm}
                resp = self.client.post('/accounts/create',
                                        data=json.dumps(partial_data),
                                        content_type='application/json')

                self.assertEqual(resp.status, "400 BAD REQUEST")


    def test_create_missing_username(self):
        resp = self.create_user("", "testing@test.com", "test", "teacher")


        self.assertEqual(resp.status, "400 BAD REQUEST")

    def test_create_missing_password(self):
        resp = self.create_user("test", "testing@test.com", "", "teacher")

        self.assertEqual(resp.status, "400 BAD REQUEST")

    def test_create_missing_email(self):
        resp = self.create_user("test", "", "password", "teacher")

        self.assertEqual(resp.status, "400 BAD REQUEST")

    def test_create_missing_role(self):
        resp = self.create_user("test", "test@test.com", "password", "")

        self.assertEqual(resp.status, "400 BAD REQUEST")


    def test_create_invalid_role(self):
        resp = self.create_user("test", "test@test.com", "password", "slimeperson")

        self.assertEqual(resp.status, "400 BAD REQUEST")

    def test_duplicate_add(self):
        self.create_user("test", "testing@test.com", "test", "teacher")
        duplicate_username = self.create_user("test", "testing@test.com", "test", "teacher")
        duplicate_email    = self.create_user("test2", "testing@test.com", "test", "teacher")


        self.assertEqual(duplicate_username.status, "303 SEE OTHER")
        self.assertEqual(duplicate_email.status, "303 SEE OTHER")

    def test_add_teacher(self):
        with self.app.app_context():
            response = self.create_user('test_user', 'test@test.com', 'password', 'teacher')

            self.assertEqual(response.status, "201 CREATED")

            user = User.query.filter_by(username='test_user').first()

            self.assertEqual(user.username,'test_user')
            self.assertEqual(user.email, 'test@test.com')
            self.assertNotEqual(user.password , 'password')
            self.assertEqual(user.get_roles(), ['teacher'])

    def test_add_specialist(self):
        with self.app.app_context():
            response = self.create_user('test_user', 'test@test.com',
                                        'password', 'specialist')

            self.assertEqual(response.status, "201 CREATED")

            user = User.query.filter_by(username='test_user').first()

            self.assertEqual(user.username,'test_user')
            self.assertEqual(user.email, 'test@test.com')
            self.assertNotEqual(user.password , 'password')
            self.assertEqual(user.get_roles(), ['specialist'])


    def test_add_admin(self):
        with self.app.app_context():
            response = self.create_user('test_user', 'test@test.com',
                                        'password', 'administrator')

            self.assertEqual(response.status, "201 CREATED")

            user = User.query.filter_by(username='test_user').first()

            self.assertEqual(user.username,'test_user')
            self.assertEqual(user.email, 'test@test.com')
            self.assertNotEqual(user.password , 'password')
            self.assertEqual(user.get_roles(), ['administrator'])

    def test_list_teachers(self):
        username = 'test'
        password = 'testing'
        self.create_user(username, 'test@test.com', password, 'administrator')
        self.create_user("test_teacher", 'testing@test.com', password, 'specialist')

        self.add_test_users("teacher", 20)
        request = self.client.get('/accounts/list/teacher',
                                  headers=self.get_auth_header(username,password))

        num_teachers = len(json.loads(request.data))


        self.assertEqual(num_teachers, 20)

        request = self.client.get('/accounts/list/teacher',
                                  headers=self.get_auth_header("test_teacher", password))

        self.assertEqual(request.status, "403 FORBIDDEN")

    def add_test_users(self, role, n):
        for i in range(0, n):
            self.create_user(role + str(i)*5, str(i)*5 +"@" + str(i)*5 + ".com", str(i)*5, role)



    def create_user(self, username, email, password, role):
        payload = dict(username=username, password=password,
                       email=email, role=role)

        return self.client.post('/accounts/create', data=json.dumps(payload), content_type='application/json')

    def get_auth_header(self, username, password):
        request = self.client.post('/accounts/login',
                          data = json.dumps(dict(username = username,
                                      password = password)),
                                content_type = 'application/json')

        token   = json.loads(request.data)['access-token']
        headers = {'Authorization' : 'Bearer ' + token}
        return headers

    def get_user_info(self, user, password):
        return self.app.get('/accounts/login',
                            headers=self.get_auth_header(user, password))

