from flask import Flask, current_app


def register_controllers(flask_app):
    from app import controllers
    from importlib import import_module
    for item in controllers.controllers:
        module = import_module('app.controllers.%s' % item)
        flask_app.register_blueprint(getattr(module, 'api'))

def initialize_extensions(flask_app):
    from app import extensions

    exts = flask_app.config['EXTENSIONS']
    for item in exts:
        getattr(extensions, item).init_app(flask_app)
    
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_controllers(app)
    initialize_extensions(app)
    return app