from flask import g, abort
from mongoengine import *

from .base_document import BaseDocument
from .user import User
from .consultation_time import ConsultationTime, Status

class Reservation(BaseDocument):
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE, db_field='u')
    consultation_time = ReferenceField(ConsultationTime, required=True, reverse_delete_rule=CASCADE, db_field='ct')
    
    meta = {'collection': 'reservations'}

    def to_json(self):
        return {
            'id' : self.id,
            'user' : self.user.to_json(),
            'consultation_time' : self.consultation_time.to_json()
        }

    def populate(self, json):
        self.user = g.user
        consultation_time = ConsultationTime.objects.get_or_404(id=json['consultation_time'])
        self.set_consultation_time(consultation_time)

    def set_consultation_time(self, consultation_time): # TODO check time with now
        if consultation_time.status != Status.FREE:
            raise Exception('consultation time is reserved')
        else:
            if self.consultation_time:
                self.consultation_time.status = Status.FREE
                self.consultation_time.save()
            consultation_time.status = Status.RESERVED
            consultation_time.save()
            self.consultation_time = consultation_time
            self.save()


    