from jsl import Document, StringField

PHONE_REGEX = "^09[0-9]{9}$"

class RegisterUser(Document):
    phone_number = StringField(required=True, pattern=PHONE_REGEX)
    username = StringField(required=True, min_length=5, max_length=20)

class VerifyUser(Document):
    long_code = StringField(required=True)
    short_code = StringField(required=True)

class ChangePassword(Document):
    password = StringField(required=True, min_length=8, max_length=20)

class LoginUser(Document):
    username = StringField(required=True, max_length=20, min_length=5)
    password = StringField(required=True, max_length=20, min_length=8)

class UpdateUser(Document):
    name = StringField(required=True)
    family = StringField(required=True)
    username = StringField(max_length=20, min_length=5)
    image = StringField(required=True)
