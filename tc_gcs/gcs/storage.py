from hashlib import sha1
from os.path import join
from datetime import datetime
from dateutil.tz import tzutc

from .bucket import Bucket

class GCSStorage():
    """Google Cloud Storage (GCS) storage backend."""
    @property
    def is_auto_webp(self):
        """
        Determine if the storage backend should automatically convert images to WebP.
        :return: True if the storage backend should automatically convert images to WebP, False otherwise.
        """
        return self.context.config.AUTO_WEBP and hasattr(self.context, 'request') and self.context.request.accepts_webp
    
    @property
    def storage(self):
        """
        Get the storage object to use for the storage backend.
        :return: The storage object to use for the storage backend.
        """
        return Bucket(self._get_config('PROJECT_ID'), self._get_config('BUCKET_ID'))
    
    def __init__(self, context, config_prefix):
        """
        Constructor for the GcsStorage class.
        :param context: The Thumbor context to use for the storage backend.
        :param config_prefix: The prefix to use for the configuration keys.
        """
        self.context = context
        self.config_prefix = config_prefix

    async def get(self, path):
        """
        Get the image data for the given path.
        :param path: The path to get the image data for.
        :return: The image data for the given path.
        """
        return await self.storage.get(self._normalize_path(path))
    
    async def is_expired(self, path):
        """
        Tell if the image at the given path has expired.
        :param path: The path to check if the image has expired.
        :return: True if the image has expired, False otherwise.
        :rtype: bool
        """
        if path and 'LastModified' in path:
            expire_in_seconds = self.storage_expiration_seconds

            # Never expire
            if expire_in_seconds is None or expire_in_seconds == 0:
                return False

            timediff = datetime.now(tzutc()) - path['LastModified']

            return timediff.seconds > expire_in_seconds
        else:
            #If our key is bad just say we're expired
            return True
        
    async def _put(self, path, bytes, metadata=None):
        """
        Put the image data for the given path.
        :param path: The path to put the image data for.
        :param bytes: The image data to put.
        :param metadata: The metadata to put with the image data.
        """
        return await self.storage.put(path, bytes, metadata)
    
    def _get_config(self, config_key):
        """
        Get the configuration value for the given key.
        :param config_key: requested config
        :return: resolved config
        """
        return getattr(self.context.config, '{}_{}'.format(self.config_prefix, config_key))
    
    def _normalize_path(self, path):
        """
        Normalize the given path.
        :param path: The path to normalize.
        :return: The normalized path.
        """
        path = path.lstrip('/')  # Remove leading '/'
        path_segments = [path]

        root_path = self._get_config('ROOT_PATH')
        if root_path and root_path is not '':
            path_segments.insert(0, root_path)

        if self.is_auto_webp:
            path_segments.append("webp")

        if self._should_randomize_key():
            path_segments.insert(0, self._generate_digest(path_segments))

        normalized_path = join(path_segments[0], *path_segments[1:]).lstrip('/') if len(path_segments) > 1 else path_segments[0]
        if normalized_path.endswith('/'):
            normalized_path += self.context.config.TC_GCS_ROOT_IMAGE_NAME

        return normalized_path

    def _should_radomize_key(self):
        """
        Determine if the storage backend should randomize the image key.
        :return: True if the storage backend should randomize the image key, False otherwise.
        """
        return self.context.config.TC_GCS_RANDOMIZE_KEY
    
    def _generate_digest(self, segements):
        """
        Generate the digest for the given segments.
        :param segements: The segments to generate the digest for.
        :return: The digest for the given segments.
        """
        return sha1('.'.join(segements).encode('utf-8')).hexdigest()
    
