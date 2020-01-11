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

    SECRET_KEY_TIMEOUT = 6 * 60 * 60 # 6 hours
    USER_TEMP_TOKEN_TIMEOUT =  5 * 60 # 5 minutes
    USER_ACCESS_TOKEN_TIMEOUT = 24 * 60 * 60 # 24 hours
    CONSULTANT_ACCESS_TOKEN_TIMEOUT = 12 * 60 * 60 # 12 hours

class DevelopmentConfig(DefaultConfig):
    pass

class TestingConfig(DefaultConfig):
    pass

class DeploymentConfig(DefaultConfig):
    pass
