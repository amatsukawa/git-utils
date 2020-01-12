#!/usr/bin/env python

import argparse
import os

import shell
import utils


def _call_git_status(args):
    stdout, *_ = shell.run(["git", "status", "--porcelain", "-b"] + args)
    paths = stdout.split("\n")[:-1]
    branch = paths[0][3:]  # starts with "## ".
    return branch, [(p[:2], p[3:]) for p in paths[1:]]


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


_MERGE_LEGEND = """
\tDD unmerged, both deleted
\tAU unmerged, added by us
\tUD unmerged, deleted by them
\tUA unmerged, added by them
\tDU unmerged, deleted by us
\tAA unmerged, both added
\tUU unmerged, both modified
"""


def _print_and_cache_status(index, tree, conflicts, untracked):
    i = 1

    if not index and not tree and not conflicts and not untracked:
        print("\nClean status.")
        return

    with open(os.path.join(utils.CACHE_ROOT, "cache"), "w") as cache:
        cache.write("##status\n")
        if index:
            print("\nChanges to be committed:")
            for status, path in index:
                cache.write(f"{path}\n")
                _print_path(i, status[0], path)
                i += 1

        if tree:
            print("\nWorking tree:")
            for status, path in tree:
                cache.write(f"{path}\n")
                _print_path(i, status[1], path)
                i += 1

        if untracked:
            print("\nUntracked:")
            for status, path in untracked:
                cache.write(f"{path}\n")
                _print_path(i, status, path)
                i += 1

        if conflicts:
            print("\nConflicts:")
            for status, path in conflicts:
                cache.write(f"{path}\n")
                _print_path(i, status, path)
                i += 1
            print(_MERGE_LEGEND)


def git_status():
    parser = argparse.ArgumentParser()
    args, unknown = parser.parse_known_args()
    os.makedirs(utils.CACHE_ROOT, exist_ok=True)
    branch, paths = _call_git_status(unknown)
    separated = _separate_paths(paths)
    print(f"On branch {branch}")
    _print_and_cache_status(*separated)
    print()


if __name__ == "__main__":
    git_status()
