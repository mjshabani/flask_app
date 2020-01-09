from mongoengine import *
from enum import Enum

class Status(Enum):
    Free = 0
    Reserved = 1
    Reserving = 2

class ConsultionTime(Document):
    id = StringField(db_field='id')

    begin_time = DateTimeField(required=True, db_field='bt')
    duration = IntField(required=True, min_value=5, max_value=180, db_field='d')
    status = IntField(required=True, min_value=0, max_value=len(Status)-1, db_field='s')
    
    
    meta = {'collection': 'consultion_times'}