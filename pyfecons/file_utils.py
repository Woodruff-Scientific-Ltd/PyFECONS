import os
from importlib import resources
from typing import Dict, List, Optional

from pyfecons.overrides import ReportOverrides


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