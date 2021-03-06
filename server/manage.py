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

@manager.command
def admin():
    from app.models.admin import Admin
    from mongoengine import DoesNotExist
    try:
        admin = Admin.objects.get(username='admin')
    except DoesNotExist:
        admin = Admin()
        admin.username = 'admin'
        admin.password = 'admin123456789'
        admin.save()
    print('admin_username : %s' % admin.username)
    print('admin_password : %s' % admin.password)
        

@manager.command
def jsonschema():
    from app.jsons import write_schemas_to_file
    write_schemas_to_file()

if __name__ == "__main__":
    manager.run()