from mongoengine import Document, URLField, StringField


class Image(Document):

    url = URLField(required=True)
    tag = StringField()
