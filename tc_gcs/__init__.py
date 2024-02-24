__author__ = 'Ngo Sach Nhat (Chen)'

from thumbor.config import Config

Config.define('TC_GCS_STORAGE_PROJECT_ID', None, 'Google Cloud Storage project id', 'GCS')
Config.define('TC_GCS_STORAGE_BUCKET_ID', None, 'Google Cloud Storage bucket id', 'GCS')
Config.define('TC_GCS_STORAGE_ROOT_PATH', '', 'Google Cloud Storage path prefix', 'GCS')

Config.define('TC_GCS_LOADER_PROJECT_ID', None, 'Google Cloud Storage project id for loader', 'GCS')
Config.define('TC_GCS_LOADER_BUCKET_ID', None, 'Google Cloud Storage bucket id for loader', 'GCS')
Config.define('TC_GCS_LOADER_ROOT_PATH', '', 'Google Cloud Storage path prefix for loader', 'GCS')

Config.define('TC_GCS_RESULT_STORAGE_PROJECT_ID', None, 'Google Cloud Storage project id for result Storage', 'GCS')
Config.define('TC_GCS_RESULT_STORAGE_BUCKET_ID', None, 'Google Cloud Storage bucket id for result Storage', 'GCS')
Config.define('TC_GCS_RESULT_STORAGE_ROOT_PATH', '', 'Google Cloud Storage path prefix for result Storage', 'GCS')

Config.define('TC_GCS_ENABLE_HTTP_LOADER', False, 'Enable HTTP Loader as well?', 'GCS')
Config.define('TC_GCS_ALLOWED_BUCKETS', False, 'List of allowed buckets to be requested', 'GCS')
Config.define('TC_GCS_STORE_METADATA', False, 'Google Cloud Storage store result with metadata', 'GCS')
Config.define('TC_GCS_RANDOMIZE_KEYS', False, 'Should Google Cloud Storage keys be randomized? Defaults to False for BC, for performance, should be set to True', 'GCS')
Config.define('TC_GCS_ROOT_IMAGE_NAME', '', 'When resizing a URL that ends in a slash, what should the corresponding cache key be?', 'GCS')
