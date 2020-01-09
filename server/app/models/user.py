from mongoengine import *
from flask import request, g
from app.extensions import redis
from functools import wraps

class User(Document):
    id = StringField(db_field='id')
    
    name = StringField(required=True, max_length=20, min_length=2, db_field='n')
    family = StringField(required=True, max_length=20, min_length=2, db_field='f')

    username = StringField(required=True, unique=True, max_length=20, min_length=5, db_field='u')
    passwrod = StringField(required=True, max_length=20, min_length=8, db_field='p')
    
    phone_number = StringField(required=True, db_field='pn')

    meta = {'collection': 'users'}

    @classmethod
    def check_user(cls):
        access_token = request.headers.get('Access-Token', None)
        if not access_token:
            return False
        
        user_id = redis.get('uat%s' % access_token, None)
        if not user_id:
            return False

        try:
            g.user = cls.objects.get(id = user_id)
            g.user_type = 'normal_user'
        except DoesNotExist:
            return False

    @classmethod
    def authenticate(cls, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if check_user():
                return f(*args, **kwargs)
            else:
                abort(401)
        return wrapper

