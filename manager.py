# from flask import Flask
#
# app = Flask(__name__)
from flask_script import Manager

from app import app
manager = Manager(app)

# manager.add_command()

# @app.route('/')
# def hello_world():
#     return 'Hello World!'#
@manager.command
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # app.run()
    manager.run()
