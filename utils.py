import os

import shell


def _get_cache_path():
    root = os.environ.get("GIT_UTILS_CACHE", None)
    assert root, "No GIT_UTIL_CACHE environment variable."
    return os.path.join(root, "cache")


CACHE_PATH = _get_cache_path()


def _get_git_root():
    stdout, *_ = shell.run(["git", "rev-parse", "--show-toplevel"])
    return stdout.strip()


GIT_ROOT = _get_git_root()


def relpath_from_root(path):
    return os.path.relpath(os.path.join(GIT_ROOT, path))
