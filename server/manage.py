#! /usr/bin/env python3

from flask_script import Manager

from app import create_app
from app.configs import DefaultConfig
app = create_app(DefaultConfig)
manager = Manager(app)

@manager.command
def run():
    app.run(port=8080)

@manager.command
def url_map():
    print(app.url_map)

if __name__ == "__main__":
    manager.run()