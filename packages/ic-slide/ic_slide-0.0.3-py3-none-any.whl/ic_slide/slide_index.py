from .auth import get_access_token, urljoin
from .config import StorageIndexUrl
import json
import requests
import logging

logger = logging.Logger(__name__)
storage_index_files_api_url = urljoin(
    StorageIndexUrl, "api/file-entry/all-organization-files")


def enumerate_slide_indices(filter_by_path=None, filter_by_name=None, filter_by_begin_time=None, filter_by_end_time=None):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "PathName": filter_by_path,
        "Name": filter_by_name,
        "CreationTimeRegion": filter_by_begin_time,
        "CreationTimeEnd": filter_by_end_time
    }
    logger.debug(f"enumerate slide indices with conditions: {params}.")
    response = requests.get(storage_index_files_api_url,
                            params=params,
                            headers=headers)
    indices = []
    if response.status_code >= 200 and response.status_code <= 299:
        content = json.loads(response.content)
        indices.extend(content)
    else:
        raise Exception(
            f"Can not get slide indices, {response.reason} {response.content}")
    return indices


def enumerate_distinct_slide_ids(**kwargs):
    logger.info("enumerate distinct slide ids.")
    indices = enumerate_slide_indices(**kwargs)
    storage_ids = [index["storageId"] for index in indices if index]
    return list(set(storage_ids))
