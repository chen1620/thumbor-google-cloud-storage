from google.cloud import storage
from google.cloud.storage import Client, Bucket

class Bucket(object):
    _client: Client = None
    _bucket: Bucket = None

    """
    This handles the bucket operations
    """
    def __init__(self, project_id, bucket_id):
        """
        Constructor for the Bucket class
        :param project_id: The project ID of the Google Cloud project
        :param bucket_id: The bucket ID of the Google Cloud Storage bucket
        :param retry: The retry object to use for the client
        """
        self._client = storage.Client(project=project_id)
        self._bucket = self._client.get_bucket(bucket_id)

    
    async def exists(self, path):
        """
        This method is used to check if the given path exists in the bucket
        :param path: The path to check if exists
        """
        blob = self._bucket.blob(path)
        return blob.exists()
    
    async def get(self, path):
        """
        This method is used to get the object from the bucket
        :param path: The path to get the object from
        """
        blob = self._bucket.blob(path)
        return blob.download_as_string()
    
    async def get_signed_url(self, path, method='GET', expiration=3600):
        """
        This method is used to generate a signed URL for given path and method
        :param path: The path for the object to generate the signed URL
        :param method: The method to generate the signed URL, default is GET
        :param expiration: The expiration time of the signed URL, default is 1 hour
        """
        blob = self._bucket.blob(path)
        return blob.generate_signed_url(method=method, expiration=expiration, version='v4')
    
    async def put(self, path, data, metadata=None):
        """
        This method is used to upload the object to the bucket
        :param path: The path to upload the object to
        :param data: The data to upload
        :param metadata: The metadata to upload with the object
        """
        blob = self._bucket.blob(path)
        blob.upload_from_string(data, content_type=metadata.get('Content-Type') if metadata else None)
    
    async def delete(self, path):
        """
        This method is used to delete the object from the bucket
        :param path: The path to delete the object from
        """
        blob = self._bucket.blob(path)
        blob.delete()

