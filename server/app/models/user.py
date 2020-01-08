from mongoengine import *
from flask import request
from server.app.extensions import redis

class User(Document):
    name = StringField()
    family = StringField()

    @classmethod
    def check_user(cls):
        access_token = request.headers.get('Access-Token', None)
        if not access_token:
            return False
        
        user_id = redis.get('uat%s' % access_token, None)
        if not user_id:
            return False

        user = cls.objects.get(id=user_id)
