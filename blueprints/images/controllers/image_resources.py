"""
REST endpoint for image search

These endpoints can be reached at /images/search/.
"""
from flask_apispec import marshal_with, doc, use_kwargs

from ..schema import ImagesSchema, ImageQuerySchema, FileSchema, PaginationSchema
from .image_base_resource import ImageBaseResource
from webargs.flaskparser import use_args
from ..models.image import Image
from ..util.fuzzy_string_matcher import get_closest_string
from ..util.auto_ml import predict


@doc(
    description="""Search for a paginated list of images by keyword""",
)
class ImageResource(ImageBaseResource):
    @marshal_with(ImagesSchema)
    @use_kwargs(ImageQuerySchema, location='query')    # for documentation
    def get(self, **kwargs):
        """
        Search for images by text using fuzzy string matching
        """

        tag = kwargs.get("pokemon")
        page = kwargs.get("page")
        limit = kwargs.get("limit")

        if not tag:
            return {}

        if not page:
            page = 0

        if not limit:
            limit = 9

        tag = get_closest_string(tag)

        images = list(Image.objects(tag=tag))
        return {"images": images[page * limit : (page + 1) * limit]}


@doc(
    description="""Search for similar images by uploading an image"""
)
class ReverseImageResource(ImageResource):
    @use_kwargs(FileSchema, location="files")
    @use_kwargs(PaginationSchema, location='query')
    @marshal_with(ImagesSchema)
    def post(self, **kwargs):
        """
        reverse image search based on tag classification with auto ml
        """

        image = kwargs.get("file").read()
        if not image:
            return {}
        prediction = predict(image)

        limit = kwargs.get("limit", 9)
        page = kwargs.get("page", 0)

        images = {pred: list(Image.objects(tag=pred)) for pred in prediction}

        result = []
        for image in images:
            new_limit = int(limit * prediction[image])
            result.extend(images[image][page * new_limit : (page + 1) * new_limit])

        return {"images": result}
