# ----- External Dependencies -----

# ----- Python Standard Library -----
import logging
from logging.handlers import SysLogHandler
import os
from datetime import datetime

# ----- Internal Dependencies -----


def start_logger(level, profile, locale="file", filename=None, port=None):
    # ----- Load env variables and use to instantiate remote logging -----
    logger = logging.getLogger()
    match locale:
        case "remote":
            try:
                syslog = SysLogHandler(address=("logs.papertrailapp.com", port))
                format = "%(asctime)s | {} | %(levelname)s - %(message)s".format(
                    profile
                )
                formatter = logging.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S")
                syslog.setFormatter(formatter)
                logger.addHandler(syslog)
            except Exception as e:
                print(e)
        case "file":
            working_directory = os.getcwd()  # get current directory
            log_path = os.path.join(working_directory, "m2k_scrape/logs")
            if not filename:
                filename = datetime.now().date()
            try:
                os.makedirs(log_path)
            except FileExistsError:
                pass
            logging.basicConfig(
                filename=f"{log_path}/{filename}.txt",
                filemode="a",
                format="%(asctime)s | {} | %(levelname)s - %(message)s".format(profile),
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        case _:
            print(locale)
            print(
                "The specified logging argument is not a valid option. Please use 'file' to log to a .txt file, or 'remote' to log to PaperTrail."
            )
    match level:
        case "debug":
            logger.setLevel(logging.DEBUG)
        case "info":
            logger.setLevel(logging.INFO)
        case "warn":
            logger.setLevel(logging.WARN)
        case "error":
            logger.setLevel(logging.ERROR)
        case "critical":
            logger.setLevel(logging.CRITICAL)
        case _:
            print(level)
            print(
                "The specified log level was invalid. Please use 'debug', 'info', 'warn', 'error' or 'critical'."
            )

    return logger
