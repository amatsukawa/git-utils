"""
Utility for running shell commands from python.
"""

import logging
import subprocess


def run(command, utf=True, fail_ok=False, verbose=False):
    # https://janakiev.com/blog/python-shell-commands/
    if verbose:
        logging.info(f"Running: {command}")
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as process:
        outputs = process.communicate()
        if utf:
            outputs = [o.decode("utf-8") for o in outputs]
        stdout, stderr = outputs
        if not fail_ok and process.returncode != 0:
            raise RuntimeError(f"Command {command} failed. stderr:\n{stderr}")
        return stdout, stderr, process.returncode


class Colors(object):
    # https://stackoverflow.com/questions/22886353/printing-colors-in-python-terminal
    PINK = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"


def red(text):
    print(Colors.RED + text + Colors.RESET)


def blue(text):
    print(Colors.BLUE + text + Colors.RESET)


def green(text):
    print(Colors.GREEN + text + Colors.RESET)


def pink(text):
    print(Colors.PINK + text + Colors.RESET)


def yellow(text):
    print(Colors.YELLOW + text + Colors.RESET)
