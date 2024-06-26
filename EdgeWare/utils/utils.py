import logging
import os
import sys
import time

from utils.paths import LOG_PATH


def init_logging(filename, source=None):
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)

    log_time = time.asctime().replace(" ", "_").replace(":", "-")
    log_file = f"{log_time}-{filename}.txt"
    logging.basicConfig(filename=LOG_PATH / log_file, format="%(levelname)s:%(message)s", level=logging.DEBUG, force=True)
    if source:
        logging.info(f"Started {source} logging successfully.")

    return log_file


def is_linux():
    return "linux" in sys.platform


def is_windows():
    return "win32" in sys.platform


if is_linux():
    from .linux import *
elif is_windows():
    from .windows import *
else:
    raise RuntimeError("Unsupported operating system: {}".format(sys.platform))
