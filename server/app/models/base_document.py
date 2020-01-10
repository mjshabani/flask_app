from mongoengine import *
from flask_mongoengine import Document
from app.utils.uid import uid
from app.utils.datetime import create_datetime

class BaseDocument(Document):
    id = StringField(primary_key=True, db_field='id')
    create_time = DateTimeField(db_field='ct')

    meta = {'abstract': True,}

    def __init__(self, *args, **kwargs):
        super(BaseDocument, self).__init__(*args, **kwargs)
        if not self.id:
            self.id = uid()
        if not self.create_time:
            self.create_time = create_datetime()