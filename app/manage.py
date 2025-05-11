# ./app/cli.py
from .extensions import db
from flask.cli import with_appcontext, FlaskGroup
import click

#---Main Function to register all commands---
def register_commands(app):
    app.cli.add_command(create_test_user)
    


@click.command(name='create_test_user', help='Create a test user for the application.')
@with_appcontext
def create_test_user():
    print("test command")