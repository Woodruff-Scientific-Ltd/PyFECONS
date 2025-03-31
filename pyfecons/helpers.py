import os
import requests
from importlib import resources
from urllib.parse import urljoin
from typing import Dict, List, Optional, Union

from pyfecons.overrides import ReportOverrides
from pyfecons.templates import load_document_template


def safe_round(value, digits):
    return None if value is None else round(value, digits)


def strip_url_params(url: str) -> str:
    """
    :param url: url
    :return: url without parametrs
    """
    query_index = url.find("?")
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
        with open(local_path, "wb") as f:
            f.write(response.content)
    return str(local_path)


def load_remote_included_files(
    cache_path: str, base_url: str, included_files: dict[str, str]
) -> dict[str, str]:
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
    blob_index = url.find("/blob/")
    base_path = url[: blob_index + 6]  # includes '/blob/'
    remote_path = url[blob_index + 6 :]  # excludes '/blob/'
    return base_path, remote_path


def load_github_images(
    cache_path: str, included_images: dict[str, str]
) -> dict[str, str]:
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
    """Get the base name of a file without its extension."""
    return os.path.splitext(os.path.basename(file_path))[0]


def get_local_included_files_map(
    included_files_path: str,
    local_included_files: list[str],
    overrides: Optional[ReportOverrides] = None,
) -> dict[str, str]:
    file_map = {}
    for tex_path in local_included_files:
        included_file_path = get_included_file_path(
            included_files_path, tex_path, overrides
        )
        file_map[tex_path] = included_file_path
    return file_map


def get_included_file_path(
    included_files_path: str, tex_path: str, overrides: Optional[ReportOverrides] = None
) -> str:
    if overrides is not None and tex_path in overrides.included_files.keys():
        return overrides.included_files[tex_path]
    else:
        return str(resources.files(included_files_path).joinpath(tex_path))


def load_customer_overrides(customer_dir: str) -> ReportOverrides:
    overrides = ReportOverrides()

    included_files_dir = os.path.join(customer_dir, "included_files")
    templates_dir = os.path.join(customer_dir, "templates")

    # Process included_files
    if os.path.exists(included_files_dir):
        for root, _, files in os.walk(included_files_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, included_files_dir)
                absolute_path = os.path.abspath(file_path)
                overrides.included_files[relative_path] = absolute_path

    # Process templates
    if os.path.exists(templates_dir):
        for file in os.listdir(templates_dir):
            file_path = os.path.join(templates_dir, file)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    overrides.templates[file] = f.read()

    return overrides
