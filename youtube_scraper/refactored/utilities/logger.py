# ----- External Dependencies -----

# ----- Python Standard Library -----
import logging
from logging.handlers import SysLogHandler
import os
from dotenv import load_dotenv

# ----- Internal Dependencies -----


def start_logger():
    # ----- Load env variables and use to instantiate remote logging -----
    try:
        load_dotenv("../.env")
    except Exception as e:
        print("couldn't load .env")
        print(e)
    try:
        port = os.environ["REMOTE_PORT"]
    except KeyError:
        print(
            "No remote port was specified in the .env file. Please ensure the environment variables are set up correctly."
        )
        exit(1)
    syslog = SysLogHandler(address=("logs.papertrailapp.com", port))
    logger = logging.getLogger()
    format = "| %(asctime)s | DOC_OPT_TEST | %(levelname)s - %(message)s"
    formatter = logging.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S")
    syslog.setFormatter(formatter)
    logger.addHandler(syslog)
    logger.setLevel(logging.DEBUG)
    return logger
