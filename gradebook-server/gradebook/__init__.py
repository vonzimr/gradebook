from flask import Flask

#Application Factory
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    #Database
    from gradebook.database import db, migrate

    #Initialize the Account Blueprint
    from gradebook.blueprints.accounts.models import User, Role
    from gradebook.blueprints.accounts.accounts import accounts
    from auth import jwt
    app.register_blueprint(accounts)

    #Initialize Flask Modules
    migrate.init_app(app, db)
    db.init_app(app)
    jwt.init_app(app)

    #Add existing user roles to database.
    return app
