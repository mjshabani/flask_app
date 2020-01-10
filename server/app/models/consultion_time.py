from mongoengine import *
from enum import Enum

from app.utils.datetime import string_to_datetime
from .consultant import Consultant
from .base_document import BaseDocument

class Status(Enum):
    Free = 0
    Reserved = 1
    Reserving = 2

class ConsultionTime(BaseDocument):
    begin_time = DateTimeField(required=True, db_field='bt')
    duration = IntField(required=True, min_value=5, max_value=180, db_field='d')
    status = IntField(required=True, min_value=0, max_value=len(Status)-1, db_field='s')

    consultant = ReferenceField(Consultant, required=True, reverse_delete_rule=CASCADE, db_field='c')
    
    def populate(self, json):
        self.begin_time = string_to_datetime(json['begin_time']) #TODO verify begin time
        self.duration = json['duration'] # verify duration and overlapping
        self.status = Status.Free
        self.consultant = Consultant.objects.get_or_404(id=json['consultant'])
    
    meta = {'collection': 'consultion_times'}