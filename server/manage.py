from flask_script import Manager

from server import create_app
from server.app.configs import DefaultConfig
app = create_app(DefaultConfig)
manager = Manager(app)

@manager.command
def run():
    print "hello"

if __name__ == "__main__":
    manager.run()