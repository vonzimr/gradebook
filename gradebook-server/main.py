import click
import unittest
from gradebook import create_app
from gradebook.blueprints.accounts.add_user_roles import create_user_roles
app = create_app('../configurations/dev.cfg')


@app.cli.command()
def test():
    u = unittest.defaultTestLoader.discover("./gradebook", pattern="*_test.py")
    runner = unittest.TextTestRunner()
    runner.run(u)

@app.cli.command()
def add_roles():
    create_user_roles(app)


