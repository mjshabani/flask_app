from mongoengine import *

class User(Document):
    name = StringField()
    family = StringField()