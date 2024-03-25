import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = (
    "%(levelname)s:     %(message)s  %(pathname)s:%(funcName)s:%(lineno)d"
)


class LogLevel(StrEnum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(log_level: str) -> None:
    log_level = str(log_level).upper()  # cast to string
    log_levels = list(LogLevel)

    if log_level not in log_levels:
        # we use error as the default log level
        logging.basicConfig(level=LogLevel.error)
        return

    if log_level == LogLevel.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)
