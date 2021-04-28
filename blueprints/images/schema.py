from marshmallow import Schema, fields


class ImageSchema(Schema):
    tag = fields.Str()
    url = fields.Str()


class ImagesSchema(Schema):
    images = fields.List(fields.Nested(ImageSchema))


args_schema = {
    "page": fields.Int(description="Page number of table", default=1),
    "limit": fields.Int(description="How many entries per page", default=5),
    "pokemon": fields.Str(description="Pokemon image to be searched"),
}

file_schema = {
    "file": fields.Field(),
    "page": fields.Int(description="Page number of table", default=1),
    "limit": fields.Int(description="How many entries per page", default=5),
}
