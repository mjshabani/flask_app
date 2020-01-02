class DefaultConfig(object):
    name = 'my app'
    DEBUG = True


    MONGODB_SETTINGS = {
        "db" : "flask_app"
    }

class DevelopmentConfig(DefaultConfig):
    pass

class TestingConfig(DefaultConfig):
    pass

class DeploymentConfig(DefaultConfig):
    pass
