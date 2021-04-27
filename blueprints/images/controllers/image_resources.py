"""
REST endpoint for image search

These endpoints can be reached at /images/search/.
"""
from flask_apispec import marshal_with, doc

from ..schema import ImagesSchema, args_schema
from .image_base_resource import ImageBaseResource
from webargs.flaskparser import use_args
from ..models.image import Image


@doc(
    description="""Image resource""",
)
class ImageResource(ImageBaseResource):
    @marshal_with(ImagesSchema)
    @use_args(args_schema, location="query")
    def get(self, args):
        """
        Return a paginated list of images.
        """

        tag = args.get("pokemon")
        page = args.get("page")
        limit = args.get("limit")

        if not tag:
            return {}

        if not page:
            page = 1

        if not limit:
            limit = 5

        images = list(Image.objects(tag=tag))
        return {"images": images[page * limit : (page + 1) * limit]}
