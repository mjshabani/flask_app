from jsl import Document, StringField


class AdminLogin(Document):
    username = StringField(required=True)
    password = StringField(required=True)
