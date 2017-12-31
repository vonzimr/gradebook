from .models import Role
from gradebook.database import db
from sqlalchemy.exc import IntegrityError

def create_user_roles(app):
    roles = [
        Role(name="teacher", description="K-5 Teacher"),
        Role(name="administrator", description="All access privileges"),
        Role(name="specialist", description="Access to Specialist reports")]

    num_roles = 0

    with app.app_context():
        for role in roles:
            try:
                db.session.add(role)
                db.session.commit()
                num_roles+=1
            except IntegrityError:
                db.session.rollback()

    print("%s Roles added." % num_roles)
