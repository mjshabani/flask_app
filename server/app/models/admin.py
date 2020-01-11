from flask import request, g, abort
from app.extensions import redis
from functools import wraps
from mongoengine import *

from .base_document import BaseDocument
from app.utils.user_type import UserType

class Admin(BaseDocument):
    username = StringField(required=True, unique=True, max_length=20, min_length=5, db_field='u')
    password = StringField(required=True, max_length=20, min_length=8, db_field='p')

    meta = {'collection': 'admins'}

    def check_password(self, password): #TODO
        return password == self.password

    @classmethod
    def check_admin(cls):
        secret_key = request.headers.get('Secret-Key', None)
        if not secret_key:
            return False
        
        admin_username = redis.get('ask%s' % secret_key)
        if not admin_username:
            return False

        try:
            g.user = cls.objects.get(username=admin_username)
            g.user_type = UserType.ADMIN
        except DoesNotExist:
            return False

        return True

    @classmethod
    def authenticate(cls, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if cls.check_admin():
                return f(*args, **kwargs)
            else:
                abort(401)
        return wrapper

