import os
import sys

import shell
import utils


def replace():
    with open(utils.CACHE_PATH, "r") as f:
        lines = [s.rstrip() for s in f.readlines()]
        assert lines[0] == "##status", "The last command you ran was not status"
        lines = lines[1:]
        args = []
        for arg in sys.argv[1:]:
            try:
                i = int(arg)
                assert 0 <= i - 1 < len(lines), f"No file numbered {i}"
                args.append(lines[i - 1])
            except ValueError:
                args.append(arg)
        print(" ".join(args))


if __name__ == "__main__":
    replace()
