from gradebook.database import db
from passlib.apps import custom_app_context as flask_user_context
from sqlalchemy.orm.exc import NoResultFound

# Create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(db.Model):
    '''
    User object.
    Methods:
        - hash_pass(password): Store hash of password. Do not store the
        plaintext password, that is the purpose of this method.
        - verify_pass(password): Verify the password.
        '''

    __tablename__     = 'user'
    id                = db.Column(db.Integer, primary_key = True)
    username          = db.Column(db.String(80), unique = True, nullable = False)
    email             = db.Column(db.String(120), unique = True, nullable = False)
    password          = db.Column(db.String(255))
    roles             = db.relationship('Role',
                                        secondary=roles_users,
                                        backref  = db.backref('users', lazy='dynamic')
                                        )

    def hash_pass(self, password):
        self.password = flask_user_context.hash(password)

    def verify_pass(self, password):
        return flask_user_context.verify(password, self.password)

    def __repr__(self):
        return '<User: %r>' % self.username

    def get_roles(self):
        return [role.name for role in self.roles]

    def set_role(self, role):
        role = Role.query.filter_by(name=role).first()
        if role is None:
            raise NoResultFound
        self.roles.append(role)

    def as_dict(self):
        return {'username' : self.username,
                'email'    : self.email,
                'roles'    : self.get_roles(),
                'id'       : self.id
                }

class Role(db.Model):
    _tablename_ = 'role'
    id          = db.Column(db.Integer(), primary_key = True)
    name        = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))
