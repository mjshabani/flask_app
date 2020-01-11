from mongoengine import *
from enum import IntEnum

from app.utils.datetime import string_to_datetime, datetime_to_string
from .consultant import Consultant
from .base_document import BaseDocument

class Status(IntEnum):
    FREE = 0
    RESERVED = 1
    RESERVING = 2

class ConsultationTime(BaseDocument):
    begin_time = DateTimeField(required=True, db_field='bt')
    duration = IntField(required=True, min_value=5, max_value=180, db_field='d')
    status = IntField(required=True, min_value=0, max_value=len(Status)-1, db_field='s')

    consultant = ReferenceField(Consultant, required=True, reverse_delete_rule=CASCADE, db_field='c')

    meta = {'collection': 'consultation_times'}

    def populate(self, json):
        self.begin_time = string_to_datetime(json['begin_time']) #TODO verify begin time
        self.duration = json['duration'] # verify duration and overlapping
        self.consultant = Consultant.objects.get_or_404(id=json['consultant'])

    def to_json(self):
        return {
            'id' : self.id,
            'begin_time' : datetime_to_string(self.begin_time),
            'duration' : self.duration,
            'status' : self.status,
            'consultant' : self.consultant.to_json()
        }