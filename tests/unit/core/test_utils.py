from pathlib import Path

from gbpt_api.core.utils import (  # combine_module_attrs,
    get_directory_names,
    get_directory_paths,
    module_path,
    root_path,
)

SRC_DIR = (Path(".").parent.parent.parent / "gbpt_api").resolve()


def test_module_path_gets_package_src_dir():
    """
    Ensure that the module_path retrieves the base src dir if no arguments
    are provided.
    """
    assert SRC_DIR == module_path()


def test_module_path_gives_back_a_pathlib_path():
    """
    Ensure that the type of module_path's return value is an instance of
    pathlib.Path.
    """
    assert isinstance(module_path(), Path)


def test_module_path_takes_an_optional_relative_path_from_src():
    """
    Ensure that we can pass in a relative path and it was use that to
    construct a path from the package src directory.
    """
    assert module_path("core/__init__.py") == (SRC_DIR / "core" / "__init__.py")


def test_get_directory_paths_retrieves_only_directories(fs):
    """
    Ensure that get_directory_paths is only fetchings directories from the
    path we pass it.
    """
    fs.create_file("/tmp/file.txt")
    fs.create_dir("/tmp/dir/")

    dirs = get_directory_paths("/tmp")

    assert dirs == [Path("/tmp/dir")]


def test_get_directory_paths_retrieves_only_top_level_directories(fs):
    """
    Ensure that get_directory_paths is only fetching top-level directories,
    not any nested directoreis.
    """
    fs.create_dir("/tmp/dir1/")
    fs.create_dir("/tmp/dir1/dir2/")

    dirs = get_directory_paths("/tmp")

    assert dirs == [Path("/tmp/dir1")]


def test_get_directory_paths_accepts_pathlib_paths(fs):
    """Ensure that a pathlib.Path can be passed to get_directory_paths."""
    dirs = get_directory_paths(Path("/tmp"))

    assert dirs == []


def test_get_directory_names_retrieves_str_names(fs):
    """
    Ensure that get_directory_names grabs all the names of the directories
    in the given path.
    """
    fs.create_dir("/tmp/dir1")
    fs.create_dir("/tmp/dir1/dir2")
    fs.create_file("/tmp/file.txt")

    dirs = get_directory_names("/tmp")

    assert dirs == ["dir1"]


def test_root_path_no_args():
    """
    Ensure that root_path without arguments gives back the project
    directory.
    """
    assert root_path() == SRC_DIR.parent


def test_root_path_relative_path():
    """
    Ensure that root_path with a relative path gives back the expected
    full path.
    """
    assert root_path("gbpt_api/core") == SRC_DIR / "core"
