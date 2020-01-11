from jsl import Document, StringField


class LoginAdmin(Document):
    username = StringField(required=True)
    password = StringField(required=True)
