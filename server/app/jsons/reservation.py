from jsl import Document, StringField

class CreateReservation(Document):
    consultation_time = StringField(required=True)
