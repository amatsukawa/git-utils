import os

import shell

CACHE_ROOT = os.environ.get("GIT_UTIL_ROOT", None)


def _get_git_root():
    stdout, *_ = shell.run(["git", "rev-parse", "--show-toplevel"])
    return stdout.strip()


GIT_ROOT = _get_git_root()


def relpath_from_root(path):
    return os.path.relpath(os.path.join(GIT_ROOT, path))
