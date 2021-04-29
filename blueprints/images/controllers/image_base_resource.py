from flask_apispec import doc, marshal_with

from helpers import BaseResource, ErrorResponseSchema


@doc(tags=["Images"])
@marshal_with(ErrorResponseSchema, code=404)
@marshal_with(ErrorResponseSchema, code=422)
@marshal_with(ErrorResponseSchema, code=400)
class ImageBaseResource(BaseResource):
    pass
