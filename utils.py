import os

import shell


def _get_cache_root():
    root = os.environ.get("GIT_UTIL_ROOT", None)
    assert root, "No GIT_UTIL_ROOT environment variable."
    return root


CACHE_ROOT = _get_cache_root()


def _get_git_root():
    stdout, *_ = shell.run(["git", "rev-parse", "--show-toplevel"])
    return stdout.strip()


GIT_ROOT = _get_git_root()


def relpath_from_root(path):
    return os.path.relpath(os.path.join(GIT_ROOT, path))
