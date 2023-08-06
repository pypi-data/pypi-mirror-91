import logging
AuthUri = 'http://private.intemedic.com:6001'
SlideCloudUrl = 'http://private.intemedic.com:6002'
StorageIndexUrl = 'http://private.intemedic.com:6003'

logger = logging.Logger(__name__)


def _configure(auth_url=None, slide_cloud_url=None, storage_index_url=None):
    if not auth_url:
        global AuthUri
        AuthUri = auth_url
        logger.info(f"Change auth uri to {auth_url}")
    if not slide_cloud_url:
        global SlideCloudUrl
        SlideCloudUrl = slide_cloud_url
        logger.info(f"Change slide cloud uri to {slide_cloud_url}")
    if not storage_index_url:
        global StorageIndexUrl
        StorageIndexUrl = storage_index_url
        logger.info(f"Change storage index to {storage_index_url}")


def configure(**kwargs):
    _configure(**kwargs)
