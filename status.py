import os
import sys

import shell
import utils


def _call_git_status():
    stdout, *_ = shell.run(["git", "status", "--porcelain", "-b"] + sys.argv[1:])
    lines = stdout.split("\n")[:-1]
    branch = lines[0][3:]  # starts with "## ".
    return branch, [(p[:2], p[3:]) for p in lines[1:]]


def _separate_paths(paths):
    index, tree, conflicts, untracked = [], [], [], []
    for t in paths:
        status, path = t
        path = utils.relpath_from_root(path)
        if status in ("??", "!!"):
            untracked.append((status, path))
            continue
        if "U" in status or status in ("DD", "AA"):
            conflicts.append((status, path))
            continue
        matched = False
        if status[0] != " ":
            index.append((status, path))
            matched = True
        if status[1] != " ":
            tree.append((status, path))
            matched = True
        if not matched:
            raise ValueError(f"Unknown status {status}.")

    return index, tree, conflicts, untracked


def _print_path(i, status, path):
    if status == "A":
        # added
        shell.yellow(f"\t[{i}] {status} {path}")
    elif status == "M":
        # modified
        shell.green(f"\t[{i}] {status} {path}")
    elif status in ("DD", "AA") or "U" in status:
        # Conflict
        shell.red(f"\t[{i}] {status} {path}")
    elif status == "D":
        # deleted
        shell.red(f"\t[{i}] {status} {path}")
    elif status in ("R", "C"):
        # renamed, copied
        shell.blue(f"\t[{i}] {status} {path}")
    elif status in ("??", "!!"):
        # untracked
        shell.pink(f"\t[{i}] {status} {path}")
    else:
        raise ValueError(f"Unknown status '{status}'.")


def _write_cache(cache, status, path):
    if status in ("R", "C"):
        _, path = path.split(" -> ")
    cache.write(f"{path}\n")


_MERGE_LEGEND = """
\tDD unmerged, both deleted
\tAU unmerged, added by us
\tUD unmerged, deleted by them
\tUA unmerged, added by them
\tDU unmerged, deleted by us
\tAA unmerged, both added
\tUU unmerged, both modified
"""


def _print_and_cache_status(paths, i, cache):
    for status, path in paths:
        _print_path(i, status, path)
        _write_cache(cache, status, path)
        i += 1
    return i


def _print_and_cache_statuses(index, tree, conflicts, untracked):
    i = 1

    if not index and not tree and not conflicts and not untracked:
        print("\nClean status.")
        return

    with open(utils.CACHE_PATH, "w") as cache:
        cache.write("##status\n")
        if index:
            print("\nChanges to be committed:")
            index = [(s[0], p) for s, p in index]
            i = _print_and_cache_status(index, i, cache)

        if tree:
            print("\nWorking tree:")
            tree = [(s[1], p) for s, p in tree]
            i = _print_and_cache_status(tree, i, cache)

        if untracked:
            print("\nUntracked:")
            i = _print_and_cache_status(untracked, i, cache)

        if conflicts:
            print("\nConflicts:")
            i = _print_and_cache_status(untracked, i, cache)
            print(_MERGE_LEGEND)


def git_status():
    os.makedirs(os.path.dirname( utils.CACHE_PATH), exist_ok=True)
    branch, paths = _call_git_status()
    separated = _separate_paths(paths)
    print(f"On branch {branch}")
    _print_and_cache_statuses(*separated)
    print()


if __name__ == "__main__":
    git_status()
