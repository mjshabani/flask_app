from jsl import Document, DateTimeField, IntField, StringField


class CreateConsultionTime(Document):
    begin_time = DateTimeField(required=True)
    duration = IntField(required=True, minimum=5, maximum=180)
    consultant = StringField(required=False)