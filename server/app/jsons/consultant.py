from jsl import Document, StringField


class CreateConsultant(Document):
    username = StringField(required=True, max_length=20, min_length=5)
    password = StringField(required=True, max_length=20, min_length=8)

class EditConsultant(Document):
    title = StringField(required=True, max_length=20, min_length=2)
    name = StringField(required=True, max_length=20, min_length=2)
    family = StringField(required=True, max_length=20, min_length=2)
    summary_info = StringField(required=True)
    further_info = StringField(required=True)
    address = StringField(required=True)
    phone = StringField(required=True)
