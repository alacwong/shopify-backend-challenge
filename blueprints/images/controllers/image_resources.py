"""
REST endpoint for image search

These endpoints can be reached at /images/search/.
"""
from flask_apispec import marshal_with, doc

from ..schema import ImagesSchema, args_schema, file_schema
from .image_base_resource import ImageBaseResource
from webargs.flaskparser import use_args, use_kwargs
from ..models.image import Image
from ..util.fuzzy_string_matcher import get_closest_string
from ..util.auto_ml import predict


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
            page = 0

        if not limit:
            limit = 9

        tag = get_closest_string(tag)

        images = list(Image.objects(tag=tag))
        return {"images": images[page * limit : (page + 1) * limit]}


class ReverseImageResource(ImageResource):
    @use_args(file_schema, location="files")
    @use_args(args_schema, location='query')
    @marshal_with(ImagesSchema)
    def post(self, file_args, query_args):
        """
        reverse image search endpoint
        """

        image = file_args.get("file").read()
        if not image:
            return {}
        prediction = predict(image)

        limit = query_args.get("limit", 9)
        page = query_args.get("page", 0)

        images = {pred: list(Image.objects(tag=pred)) for pred in prediction}

        result = []
        for image in images:
            new_limit = int(limit * prediction[image])
            result.extend(images[image][page * new_limit : (page + 1) * new_limit])

        return {"images": result}
