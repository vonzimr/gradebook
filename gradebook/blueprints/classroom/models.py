from gradebook.database import db
from passlib.apps import custom_app_context as flask_user_context

class Classroom(db.Model):
    _tablename_ = 'classroom'
    id          = db.Column(db.Integer, primary_key=True)
    grade       = db.Column(db.String(1))
    year        = db.Column(db.Date)
    students    = db.relationship("Student")


class Student(db.Model):
    _tablename_ = 'student'
    id           = db.Column(db.Integer, primary_key=True)
    first_name   = db.Column(db.String(120))
    last_name    = db.Column(db.String(120))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
