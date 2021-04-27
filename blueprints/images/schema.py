from marshmallow import Schema, fields


class ImageSchema(Schema):
    tag = fields.Str()
    url = fields.Str()
