"""Logging configuration: messages go to a log file, not the console."""
import logging

from . import config


def setup_logging(log_file=None):
    path = log_file or config.LOG_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=path,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
