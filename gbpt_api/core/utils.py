from importlib import import_module
from pathlib import Path
from typing import Union

from gbpt_api.core.logger import get_logger

logger = get_logger(__name__)


def module_path(path: Union[str, Path] = Path(".")) -> Path:
    """Finds the absolute path of a file relative to the package directory.

    Args:
        path: The path of the file you're looking for.

    Returns:
        The absolute path of the file.
    """
    return Path.joinpath(Path(__file__).parent.parent, path).resolve()


def root_path(path: Union[str, Path] = Path(".")) -> Path:
    """Finds the absolute path of a file relative to the root directory.

    Args:
        path: The path of the file you're looking for, relative to the project
            directory.

    Returns:
        The absolute path of the file.
    """
    return Path.joinpath(Path(module_path()).parent, path).resolve()


def combine_module_attrs(attr: str, package_path: Union[str, Path]) -> list:
    """Retrieves all the module API routers to attach onto the main app.

    Every package should have a `get_routers` function in their main
    __init__.py if they want to expose API routers which returns a list
    of all the API routers for that module.

    Args:
        package_path: The path to the package to retrieve api routers from.
            This directory should be named the same as the package
            to import.

    Returns:
        A single list of all the app's API Routers.
    """
    if not isinstance(package_path, Path):
        package_path = Path(package_path)

    result = []

    for module_name in get_directory_names(package_path):
        module = import_module(f"{package_path.name}.{module_name}")

        module_attr = getattr(module, attr, None)
        if module_attr is None or not callable(module_attr):
            logger.debug(
                f"Could not find a callable `{attr}` "
                f"attribute on `{module}`. Got `{module_attr}`."
            )
            continue

        output = module_attr()
        if isinstance(output, list):
            result.extend(output)
        else:
            result.append(output)

    return result


def get_directory_names(path: Union[str, Path]) -> list[str]:
    """Retrieves top-level directory names.

    Args:
        path: Path to fetch top-level directory names from.

    Returns:
        A list of top-level directory names inside of the path.
    """
    module_names = []

    for dir_path in get_directory_paths(path):
        module_names.append(dir_path.name)

    return module_names


def get_directory_paths(path: Union[str, Path]) -> list[Path]:
    """Retrieve the directories in a given path, one level deep.

    Args:
        path: Path to fetch top-level directory paths from.

    Returns:
        The full path to each top-level directory inside the path.
    """
    if not isinstance(path, Path):
        path = Path(path).resolve()

    dirs = []
    for dir_path in path.iterdir():
        if dir_path.is_dir():
            dirs.append(dir_path)

    return dirs
