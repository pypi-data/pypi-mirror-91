"""
Upload images to image hosting services
"""

from .. import errors
from ..utils.imghosts import ImageHostBase
from . import QueueJobBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class ImageHostJob(QueueJobBase):
    """
    Upload images to an image hosting service

    :param ImageHostBase imghost: Return value of :func:`.utils.imghosts.imghost`
    :param image_paths: Sequence of paths to image files
    :param images_total: Number of images that are going to be uploaded. The
        only purpose of this value is to provide it via the :attr:`images_total`
        property to calculate progress.

    If `image_paths` is given, the job finishes after all images are uploaded.

    If `image_paths` is not given, calls to :meth:`upload` are expected and
    :meth:`finalize` must be called after the last call.

    `image_paths` and `images_total` must not be given at the same time.
    """

    name = 'imghost'
    label = 'Image URLs'

    # Don't cache output and rely on caching in ImageHostBase. Otherwise, a
    # single failed/cancelled upload would throw away all the gathered URLs.
    cache_id = None

    def initialize(self, *, imghost, enqueue=(), images_total=0):
        assert isinstance(imghost, ImageHostBase), f'Not an ImageHostBase: {imghost!r}'
        imghost.cache_directory = self.cache_directory
        self._imghost = imghost
        self._images_uploaded = 0
        if enqueue and images_total:
            raise RuntimeError('You must not give both arguments "enqueue" and "images_total".')
        else:
            if images_total > 0:
                self.images_total = images_total
            else:
                self.images_total = len(enqueue)

    async def _handle_input(self, image_path):
        try:
            info = await self._imghost.upload(image_path, cache=not self.ignore_cache)
        except errors.RequestError as e:
            self.error(e)
        else:
            _log.debug('Uploaded image: %r', info)
            self._images_uploaded += 1
            self.send(info)

    @property
    def exit_code(self):
        if self.is_finished:
            if self.images_uploaded > 0 and self.images_uploaded == self.images_total:
                return 0
            else:
                return 1

    @property
    def images_uploaded(self):
        """Number of uploaded images"""
        return self._images_uploaded

    @property
    def images_total(self):
        """Expected number of images to upload"""
        return self._images_total

    @images_total.setter
    def images_total(self, value):
        self._images_total = int(value)

    def set_images_total(self, value):
        self.images_total = value
