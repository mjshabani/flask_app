from flask import Flask, current_app
from flask_json_schema import JsonValidationError
from mongoengine import DoesNotExist


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

def register_error_handlers(app):
    def bad_request(e):
        return 'Bad Request' , 400
    def unauthorized(e):
        return 'Unauthorized', 401
    def not_found(e):
        return 'Not Found', 404
    def internal_error(e):
        return 'Internal Error', 500

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)

    app.register_error_handler(JsonValidationError, bad_request)
    app.register_error_handler(DoesNotExist, not_found)
    app.register_error_handler(Exception, internal_error)
    

    
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_controllers(app)
    initialize_extensions(app)
    register_error_handlers(app)
    return app