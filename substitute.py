import sys
import os

import utils


def replace():
    expected_last_cmd = sys.argv[1]
    if not os.path.exists(utils.CACHE_PATH):
        return
    with open(utils.CACHE_PATH, "r") as f:
        lines = [s.rstrip() for s in f.readlines()]
        actual_last_cmd = lines[0][3:]
        lines = lines[1:]
        args = []
        for arg in sys.argv[2:]:
            try:
                i = int(arg)
                assert 0 <= i - 1 < len(lines), f"No file numbered {i}"
                assert (
                    expected_last_cmd == actual_last_cmd
                ), f"Expected last command to be {expected_last_cmd} but was {actual_last_cmd}"
                args.append(lines[i - 1])
            except ValueError:
                if arg.startswith("\\"):
                    arg = arg[1:]
                args.append(arg)
        print(" ".join(args))


if __name__ == "__main__":
    replace()
