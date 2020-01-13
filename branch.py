import os
import sys

import shell
import utils


def git_branch():
    os.makedirs(os.path.dirname( utils.CACHE_PATH), exist_ok=True)
    stdout, *_ = shell.run(["git", "branch"])
    branches = stdout.split("\n")[:-1]  # ends in a "\n"
    with open(utils.CACHE_PATH, "w") as cache:
        cache.write("## branch\n")
        for i, branch in enumerate(branches):
            if branch.startswith("* "):
                shell.green(f"[{i+1}] {branch}")
            else:
                print(f"[{i+1}] {branch}")
            cache.write(f"{branch[2:]}\n")


if __name__ == "__main__":
    git_branch()
