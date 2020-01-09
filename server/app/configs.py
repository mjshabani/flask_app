import os

class DefaultConfig(object):
    name = 'my app'
    DEBUG = True


    MONGODB_SETTINGS = {
        "db" : "flask_app",
        "host" : 'localhost',
        "port" : 27017
    }

    EXTENSIONS = ['mongoengine', 'redis', 'jsonschema']

    REDIS_URL = "redis://localhost:6379"

    # Directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    JSONSCHEMA_DIR = os.path.join(BASE_DIR, 'jsonschema')

    SECRET_KEY_TIMEOUT = 12 * 60 * 60 # 12 hours

class DevelopmentConfig(DefaultConfig):
    pass

class TestingConfig(DefaultConfig):
    pass

class DeploymentConfig(DefaultConfig):
    pass
