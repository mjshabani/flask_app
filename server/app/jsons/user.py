from jsl import Document, StringField


class User(Document):
    name = StringField()
    family = StringField()


class AHMAGhUser(Document):
    name = StringField()
    family = StringField()

class AliUser(Document):
    name = StringField()
    family = StringField()

