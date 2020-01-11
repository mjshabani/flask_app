from flask import g, abort
from mongoengine import *
from .user import User
from .consultation_time import ConsultationTime, Status

class Reservation(Document):
    id = StringField(db_field='id')

    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE, db_field='u')
    consultation_time = ReferenceField(ConsultationTime, required=True, reverse_delete_rule=CASCADE, db_field='ct')
    
    meta = {'collection': 'reservations'}

    def populate(self, json):
        self.user = g.user
        consultation_time = ConsultationTime.objects.get_or_404(id=json['consultation_time'])
        self.set_consultation_time(consultation_time)

    def set_consultation_time(self, consultation_time):
        if consultation_time.status != Status.FREE:
            raise Exception('consultation_time is reserved')
        else:
            if self.consultation_time:
                self.consultation_time.status = Status.FREE
                self.consultation_time.save()
            consultation_time.status = Status.RESERVED
            consultation_time.save()
            self.consultation_time = consultation_time
            self.save()


    