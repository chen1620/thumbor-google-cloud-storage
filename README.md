# Thumbor Google Cloud Storage

Thumbor Storage, Thumbor Loader and Thumbor Result Storage for [Google Cloud Storage](https://cloud.google.com/storage), aka `GCS`.

The thumbor storage can be customized as follows: [Storages](https://thumbor.readthedocs.io/en/latest/custom_storages.html), [Image Loaders](https://thumbor.readthedocs.io/en/latest/custom_loaders.html), [Result Storages](https://thumbor.readthedocs.io/en/latest/custom_result_storages.html).

## Installation
```
pip install tc_gcs
```

## Authentiation
Authentication is handled by the Google Cloud Storage SDK, see google-cloud-storage SDK [documentation](https://googleapis.dev/python/storage/latest/index.html).

## Configuration

### Storage settings
```
TC_GCS_STORAGE_PROJECT_ID = '' # GCS project id for Storage
TC_GCS_STORAGE_BUCKET_ID = '' # GCS bucket id for Storage
TC_GCS_STORAGE_ROOT_PATH = '' # GCS path prefix for Storage bucket
```

### Key settings
```
TC_GCS_RANDOMIZE_KEYS=False # Adds some randomization in the GCS keys for the Storage and Result Storage. Defaults to False for Backwards Compatibility, set it to True for performance.
TC_GCS_ROOT_IMAGE_NAME='root_image' # Sets a default name for requested images ending with a trailing /. Those images will be stored in result_storage and storage under the name set in this configuration.
```
