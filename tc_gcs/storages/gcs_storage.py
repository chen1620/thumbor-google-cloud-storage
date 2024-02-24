from json import loads, dumps
from os.path import splitext

from thumbor.storages import BaseStorage
from thumbor.utils import logger

from ..gcs.storage import GCSStorage

class Storage(GCSStorage, BaseStorage):
    """
    Google Cloud Storage (GCS) storage backend.
    """
    def __init__(self, context):
        """
        Constructor for the GcsStorage class.
        :param context: The Thumbor context to use for the storage backend.
        """
        BaseStorage.__init__(self, context)
        GCSStorage.__init__(self, context, 'TC_GCS_STORAGE')
        self.storage_expiration_seconds = context.config.get('STORAGE_EXPIRATION_SECONDS', 3600)

    async def put(self, path, file_bytes):
        """
        Put the given image data at the given path.
        :param path: The path to put the image data at.
        :param file_bytes: The image data to put at the given path.
        """
        try:
            await self.storage._put(self._normalize_path(path), file_bytes)
        except Exception as e:
            logger.exception('Could not upload image %s to GCS: %s', path, e)
        return None
        
        return path

    async def put_crypto(self, path):
        """
        Stores crypto data at given path
        :param string path: Path to store the data at
        :return: Path where the crypto data is stored
        """
        if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return

        if not self.context.server.security_key:
            raise RuntimeError(
                "STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be "
                "True if no SECURITY_KEY specified"
            )

        file_abspath = self._normalize_path(path)
        crypto_path = '%s.txt' % splitext(file_abspath)[0]

        try:
            await self._put(self.context.server.security_key.encode('utf-8'), crypto_path)
        except Exception as err:
            logger.exception('Unable to store crypto object: %s', err)
            return None

        logger.debug(
            "Stored crypto at %s (security key: %s)",
            crypto_path,
            self.context.server.security_key,
        )

        return file_abspath

    async def put_detector_data(self, path, data):
        """
        Stores detector data at given path
        :param string path: Path to store the data at
        :param string data:  Data to store
        :return: Path where the data is stored
        :rtype: string
        """
        file_abspath = self._normalize_path(path)

        path = '%s.detectors.txt' % splitext(file_abspath)[0]

        try:
            await self._put_object(dumps(data).encode('utf-8'), path)
        except Exception as err:
            logger.exception('Unable to store detector data: %s', err)
            return None

        return file_abspath

    async def get_crypto(self, path):
        """
        Retrieves crypto data at path
        :param string path: Path to search for crypto data
        """
        file_abspath = self._normalize_path(path)
        crypto_path = "%s.txt" % (splitext(file_abspath)[0])

        try:
            file_key = await self.storage.get(crypto_path)
        except Exception as err:
            logger.warn("[STORAGE] gcs blob not found at %s" % crypto_path)
            return None

        async with file_key['Body'] as stream:
            file_key = await stream.read()

        return file_key.decode('utf-8')

    async def get_detector_data(self, path):
        """
        Retrieves detector data from storage
        :param string path: Path where the data is stored
        """
        file_abspath = self._normalize_path(path)
        path = '%s.detectors.txt' % splitext(file_abspath)[0]

        try:
            file_key = await self.storage.get(path)
        except Exception:
            return None

        if not file_key or self.is_expired(file_key) or 'Body' not in file_key:
            return None

        async with file_key['Body'] as stream:
            return loads(await stream.read())

    async def get(self, path):
        """
        Gets data at path
        :param string path: Path for data
        """

        try:
            file = await super(Storage, self).get(path)
        except Exception:
            return None

        async with file['Body'] as stream:
            return await stream.read()

    async def exists(self, path):
        """
        Tells if data exists at given path
        :param string path: Path to check
        """
        file_abspath = self._normalize_path(path)
        return await self.storage.exists(file_abspath)

    async def remove(self, path):
        """
        Deletes data at path
        :param string path: Path to delete
        """
        return await self.storage.delete(self._normalize_path(path))
