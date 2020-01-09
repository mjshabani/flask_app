from mongoengine import *

class Consultant(Document):
    id = StringField(db_field='id')

    title = StringField(max_length=20, min_length=2, db_field='t')
    name = StringField(max_length=20, min_length=2, db_field='n')
    family = StringField(max_length=20, min_length=2, db_field='f')
    
    username = StringField(required=True, unique=True, max_length=20, min_length=5, db_field='u')
    password = StringField(required=True, max_length=20, min_length=8, db_field='p')

    summary_info = StringField(db_field='si')
    further_info = StringField(db_field='fi')

    address = StringField(db_field='a')
    phone_number = StringField(db_field='pn')

    meta = {'collection': 'consultants'}


    def populate(self, json):
        pass
    def to_json(self):
        pass