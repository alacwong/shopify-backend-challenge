from marshmallow import Schema, fields


class ImageSchema(Schema):
    tag = fields.Str(description='Tag indicating type of name of Pokemon for the current image')
    url = fields.Str(description='Corresponding url pointing to Pokemon Image by Cloud Provider')


class ImagesSchema(Schema):
    images = fields.List(fields.Nested(ImageSchema), description='Collection of Image Documents')


class PaginationSchema(Schema):
    limit = fields.Int(description="Maximum number of entries per query", default=5, example=10)
    page = fields.Int(description="Query offset amount", default=1, example=0)


class ImageQuerySchema(PaginationSchema):
    pokemon = fields.Str(description="Text search term to fetch Pokemon of that name", example='Abra')


class FileSchema(Schema):
    file = fields.Field(description='File search term to fetch Pokemon of that look')
