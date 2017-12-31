import click
import unittest
from gradebook import create_app
app = create_app('../configurations/dev.cfg')


@app.cli.command()
def test():
    u = unittest.defaultTestLoader.discover("./gradebook", pattern="*_test.py")
    runner = unittest.TextTestRunner()
    runner.run(u)
