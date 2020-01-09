from mongoengine import *
from .user import User
from .consultion_time import ConsultionTime

class Reservation(Document):
    id = StringField(db_field='id')

    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE, db_field='u')
    consultion_time = ReferenceField(ConsultionTime, required=True, reverse_delete_rule=CASCADE, db_field='ct')
    
    meta = {'collection': 'reservations'}