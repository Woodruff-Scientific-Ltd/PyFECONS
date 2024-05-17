import os
import requests
from importlib import resources
from urllib.parse import urljoin


def safe_round(value, digits):
    return None if value is None else round(value, digits)


def strip_url_params(url: str) -> str:
    """
    :param url: url
    :return: url without parametrs
    """
    query_index = url.find('?')
    if query_index != -1:
        return url[:query_index]
    return url


def download_file(cache_path: str, base_url: str, remote_path: str) -> str:
    """
    Download a file from remote repository if it doesn't exist locally at the specified version.
    :param cache_path: local cache directory
    :param base_url: base url of the file
    :param remote_path: of the file. In GitHub this will look like commit_hash/path/to/file
    :return cached or downloaded local file path
    """
    # strips ? for github image urls
    local_path = os.path.join(cache_path, strip_url_params(remote_path))
    if not os.path.exists(local_path):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        response = requests.get(urljoin(base_url, remote_path))
        response.raise_for_status()  # Ensure we notice bad responses
        with open(local_path, 'wb') as f:
            f.write(response.content)
    return str(local_path)


def load_remote_included_files(cache_path: str, base_url: str, included_files: dict[str, str]) -> dict[str, str]:
    """
    Create report content with given cost calculation inputs and output data.
    :param cache_path: local cache directory
    :param base_url: base url of files
    :param included_files: map of tex file path -> remote file path
    :return: map of tex file path -> local file path
    """
    loaded_files = {}
    for tex_path, remote_path in included_files.items():
        loaded_files[tex_path] = download_file(cache_path, base_url, remote_path)
    return loaded_files


def split_github_image_url(url: str) -> tuple[str, str]:
    """
    :param url: of github image including /blob/
    :return: base_path of url before and including /blob/ and remote_path for part of URL after
    """
    blob_index = url.find('/blob/')
    base_path = url[:blob_index + 6]  # includes '/blob/'
    remote_path = url[blob_index + 6:]  # excludes '/blob/'
    return base_path, remote_path


def load_github_images(cache_path: str, included_images: dict[str, str]) -> dict[str, str]:
    """
    Create report content with given cost calculation inputs and output data.
    :param cache_path: local cache directory
    :param included_images: map of tex file path -> remote file url
    :return: map of tex file path -> local file path
    """
    loaded_files = {}
    for tex_path, url in included_images.items():
        base_path, remote_path = split_github_image_url(url)
        loaded_files[tex_path] = download_file(cache_path, base_path, remote_path)
    return loaded_files


def base_name(file_path: str) -> str:
    return os.path.basename(file_path)


def base_name_without_extension(file_path: str) -> str:
    return os.path.splitext(base_name(file_path))[0]


def get_local_included_files_map(included_files_path: str, local_included_files: dict[str, str]) -> dict[str, str]:
    file_map = {}
    for tex_path, template_file in local_included_files.items():
        res_path = resources.files(included_files_path).joinpath(template_file)
        file_map[tex_path] = str(res_path)
    return file_map
