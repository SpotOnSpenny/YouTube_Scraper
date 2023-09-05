# ----- External Dependencies -----
from docopt import docopt

# ----- Python Standard Library -----

# ----- Internal Dependencies -----
from youtube_scraper.refactored.utilities.logger import start_logger


def main():
    # ----- Define Usage/Args for Doc Opt -----
    usage = """A fully realized command line utility for YouTube ad collection and monitoring.
    Part of the M2K project at the University of Calgary.

    Usage:
        m2k_scrape monitor -l <log_level> -r <log_location> [-p <profile>] [-n <number>]
        m2k_scrape collect -l <log_level> -r <log_location> [-p <profile>]
        m2k_scrape json -l <log_level> -r <log_location>
        m2k_scrape (-h | -v)

    Options:
        -l, --log-level     REQUIRED: Specify the level of log messages you'd like to be logged. [default: INFO]
        -r, --log-location  REQUIRED: Specify the desired location of logs output by the script. [default: REMOTE]
        -p, --profile       Specify the age/gender profile you'd like to use to collect/monitor ads. If not specified, interactive mode will be used.
        -n, --number        Specify the number of ads you'd like to collect. If not specified, interactive mode will be used.
        -h, --help          Provides (this) explanation of options and arguments for the utility.
        -v, --version       Provides the current version of the script installed.
    """
    # ----- Create Args Dictionary -----
    args = docopt(usage, version="0.0.5")

    # ----- Set Up Logging -----
    logger = start_logger()
    print("logger started")
