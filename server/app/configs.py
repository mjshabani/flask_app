class DefaultConfig(object):
    name = 'my app'
    DEBUG = True


    MONGODB_SETTINGS = {
        "db" : "flask_app",
        "host" : '192.168.1.35',
        "port" : 12345,
        "username" : 'flask_app',
        "password" : 'psswrd_flask_app',
    }

    EXTENSIONS = ['mongoengine']

class DevelopmentConfig(DefaultConfig):
    pass

class TestingConfig(DefaultConfig):
    pass

class DeploymentConfig(DefaultConfig):
    pass
