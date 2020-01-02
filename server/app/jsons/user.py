from jsl import Document, StringField


class User(Document):
    name = StringField()
    family = StringField()