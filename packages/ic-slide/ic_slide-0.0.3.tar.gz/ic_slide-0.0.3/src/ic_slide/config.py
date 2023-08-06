import logging
AuthUri = 'http://private.intemedic.com:6001'
SlideCloudUrl = 'http://private.intemedic.com:6002'
StorageIndexUrl = 'http://private.intemedic.com:6003'
Micron_Per_Pixel_X = 0.35093510
Micron_Per_Pixel_Y = 0.35150376

logger = logging.Logger(__name__)


def _configure(auth_url=None,
               slide_cloud_url=None,
               storage_index_url=None,
               micron_per_pixel_x=None,
               micron_per_pixel_y=None):
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
    if not micron_per_pixel_x:
        global Micron_Per_Pixel_X
        Micron_Per_Pixel_X = float(micron_per_pixel_x)
        logger.info(f"Change micron per pixel to {micron_per_pixel_x}")
    if not micron_per_pixel_y:
        global Micron_Per_Pixel_Y
        Micron_Per_Pixel_Y = float(micron_per_pixel_y)
        logger.info(f"Change micron per pixel to {micron_per_pixel_y}")


def configure(**kwargs):
    _configure(**kwargs)
