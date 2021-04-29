from marshmallow import Schema, fields


class ImageSchema(Schema):
    tag = fields.Str(description='Keyword to search for this image')
    url = fields.Str(description='Url corresponding to image on the cloud')


class ImagesSchema(Schema):
    images = fields.List(fields.Nested(ImageSchema), description='List of image documents')


class PaginationSchema(Schema):
    limit = fields.Int(description="How many entries per page", default=5, example=10)
    pokemon = fields.Str(description="Name of pokemon images to be searched", example='Abra')


class ImageQuerySchema(PaginationSchema):
    page = fields.Int(description="Page number of table", default=1, example=0)
    limit = fields.Int(description="How many entries per page", default=5, example=10)
    pokemon = fields.Str(description="Pokemon image to be searched", example='Abra')


class FileSchema(Schema):
    file = fields.Field(description='Pokemon image to find similar images for')
