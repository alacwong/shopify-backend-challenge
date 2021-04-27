"""
REST endpoint for image search

These endpoints can be reached at /images/search/.
"""
from flask_apispec import marshal_with, doc

from ..schema import ImageSchema
from .image_base_resource import ImageBaseResource


@doc(description="""Image resource""",)
class ImageResource(ImageBaseResource):

    @marshal_with(ImageSchema)
    def get(self):
        """
        Return a paginated list of images.
        """
        return {'url': 'url', 'tag': 'tag'}


