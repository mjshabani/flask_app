class DefaultConfig(object):
    name = 'my app'
    DEBUG = True


    MONGODB_SETTINGS = {
        "db" : "flask_app",
        "host" : 'localhost',
        "port" : 27017
    }

    EXTENSIONS = ['mongoengine']

class DevelopmentConfig(DefaultConfig):
    pass

class TestingConfig(DefaultConfig):
    pass

class DeploymentConfig(DefaultConfig):
    pass
