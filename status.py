import shell


def git_status():
    stdout, *_ = shell.run(["git", "status", "--porcelain", "-z"])
    paths = stdout.split("\0")[:-1]  # stdout ends with "\0"
    return [(p[:2], p[3:]) for p in paths]


def separate_paths(paths):
    at_least_one = False
    index, tree, untracked = [], [], []
    for t in paths:
        status, path = t
        if status[0] not in (" ", "?"):
            index.append(t)
            at_least_one = True
        if status[1] not in (" ", "?"):
            tree.append(t)
            at_least_one = True
        if status == "??" or status == "!!":
            untracked.append(t)
            at_least_one = True
        if not at_least_one:
            raise ValueError(f"Unknown status {status}.")

    return index, tree, untracked


def print_path(i, status, path):
    if status == "A":
        shell.yellow(f"\t[{i}] {path}")
    if status == "M":
        shell.green(f"\t[{i}] {path}")


def print_status(paths):
    index, tree, untracked = separate_paths(paths)
    i = 0
    print("\nChanges to be committed:")
    for status, path in index:
        print_path(i, status[0], path)
        i += 1
    print("\nWorking tree:")
    for status, path in tree:
        print_path(i, status[1], path)
        i += 1
    print("\nUntracked:")
    for status, path in untracked:
        shell.pink(f"\t[{i}] {path}")
        i += 1


def main():
    paths = git_status()
    print_status(paths)
    print()


if __name__ == "__main__":
    main()
