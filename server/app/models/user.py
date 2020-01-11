from mongoengine import *
from flask import request, g
from functools import wraps

from app.extensions import redis
from .base_document import BaseDocument
from .admin import Admin
from app.utils.user_type import UserType

class User(BaseDocument):
    name = StringField(required=True, default='', db_field='n')
    family = StringField(required=True, default='', db_field='f')

    username = StringField(required=True, unique=True, max_length=20, min_length=5, db_field='u')
    password = StringField(required=True, max_length=20, min_length=8, db_field='p')
    
    phone_number = StringField(required=True, unique=True, db_field='pn')

    meta = {'collection': 'users'}

    def to_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "family" : self.family,
            "username" : self.username,
            "phone_number" : self.phone_number
        }
    
    def populate(self,json):
        self.name = json['name']
        self.family = json['family']
        if 'username' in json:
            self.username = json['username']

    def check_password(self, password): #TODO
        return password == self.password

    @classmethod
    def check_user(cls):
        access_token = request.headers.get('Access-Token', None)
        if not access_token:
            return False
        
        user_id = redis.get('uat%s' % access_token)
        if not user_id:
            return False

        try:
            g.user = cls.objects.get(id = user_id)
            g.user_type = UserType.USER
        except DoesNotExist:
            return False

        return True

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if Admin.check_admin() or User.check_user():
            return f(*args, **kwargs)
        else:
            abort(401)
    return wrapper

