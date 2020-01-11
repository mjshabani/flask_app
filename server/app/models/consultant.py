from flask import abort, request, g
from mongoengine import *
from functools import wraps

from app.extensions import redis
from .base_document import BaseDocument
from .admin import Admin
from app.utils.uid import uid
from app.utils.user_type import UserType


class Consultant(BaseDocument):
    username = StringField(required=True, unique=True, max_length=20, min_length=5, db_field='u')
    password = StringField(required=True, max_length=20, min_length=8, db_field='p')

    title = StringField(required=True, default='', db_field='t')
    name = StringField(required=True, default='', db_field='n')
    family = StringField(required=True, default='', db_field='f')
    
    summary_info = StringField(required=True, default='', db_field='si')
    further_info = StringField(required=True, default='', db_field='fi')

    address = StringField(required=True, default='', db_field='a')
    phone_number = StringField(required=True, default='', db_field='pn')

    meta = {'collection': 'consultants'}

    def populate(self, json):
        self.title = json["title"]
        self.name = json["name"]
        self.family = json["family"]
        self.summary_info = json["summary_info"]
        self.further_info = json["further_info"]
        self.address = json["address"]
        self.phone_number = json["phone_number"]

    def to_json(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "name" : self.name,
            "family" : self.family,
            "summary_info" : self.summary_info,
            "further_info" : self.further_info,
            "address" : self.address,
            "phone_number" : self.phone_number,
        }

    def check_password(self, password): #TODO
        return password == self.password
        
    @classmethod
    def check_user(cls):
        access_token = request.headers.get('Access-Token', None)
        if not access_token:
            return False
        
        consultant_id = redis.get('cat%s' % access_token)
        if not consultant_id:
            return False

        try:
            g.user = cls.objects.get(id=consultant_id)
            g.user_type = UserType.CONSULTANT
        except DoesNotExist:
            return False

        return True


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if Admin.check_admin() or Consultant.check_user():
            return f(*args, **kwargs)
        else:
            abort(401)
    return wrapper