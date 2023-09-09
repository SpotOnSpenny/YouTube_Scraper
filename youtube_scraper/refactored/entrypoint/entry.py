# ----- External Dependencies -----
from docopt import docopt
from InquirerPy import inquirer

# ----- Python Standard Library -----

# ----- Internal Dependencies -----
from youtube_scraper.refactored.utilities.logger import start_logger


def main():
    # ----- Define Usage/Args for Doc Opt -----
    usage = """A fully realized command line utility for YouTube ad collection and monitoring.
    Part of the M2K project at the University of Calgary.

    Usage:
        m2k_scrape monitor -l <log_level> [-r <port> | -c <file_name>] [-p <profile>] [-t <time>]
        m2k_scrape collect -l <log_level> [-r <port> | -c <file_name>] [-p <profile>] [-n <number>]
        m2k_scrape json
        m2k_scrape (-h | -v)

    Options:
        -l, --log-level     REQUIRED: Specify the level of log messages you'd like to be logged. [default: INFO]
        -r, --log-location  REQUIRED: Specify the desired location of logs output by the script. [default: REMOTE]
        -p, --profile       Specify the age/gender profile you'd like to use to collect/monitor ads. If not specified, interactive mode will be used.
        -t, --time          Specify how long you'd like to monitor ads for continuously in hours.
        -n, --number        Specify the number of ads you'd like to collect. If not specified, interactive mode will be used.
        -h, --help          Provides (this) explanation of options and arguments for the utility.
        -v, --version       Provides the current version of the script installed.

    Arguments:
        <log_level>         The level of logs you'd like to be logged. Can be: 'debug', 'info', 'warn', 'error' or 'critical'.
        <port>              The port on your PaperTrail account, required if -r is specified.
        <file_name>         The name of the .txt file that you'd like to log to in the /logs folder of the worknig directory. If none specified, will save to a .txt named todays date.
        <profile>           The age/gender profile you'd like to use. Can be: '4M', '4F', '6M', '7F', '9F' or '10M'.
        <number>            The number of ads that you'd like to search for. Must be an integer.
        <time>              The number of hours that you'd like to monitor ads for. Must be an integer.
    """
    # ----- Create Args Dictionary -----
    args = docopt(usage, version="0.0.5")

    # ----- Set Up Logging -----
    if args["--remote"]:  # if specified, start logging remotely
        logger = start_logger(
            args["<log_level>"], args["<profile>"], "remote", port=int(args["<port>"])
        )
    else:  # if else, start logging by file
        logger = start_logger(
            args["<log_level>"], args["<profile>"], "file", filename=args["<file_name>"]
        )

    print(args)
    # ----- Monitor -----
    # Check to ensure nessescary information was provided, and start interactive mode if it was not
    if args["monitor"]:
        needed = ["<profile>", "<time>"]
        for arg in needed:
            if args[arg]:
                needed.remove(arg)
    interactive_mode("monitor", args, needed)

    # ----- Collect -----

    # ----- Convert Ads to JSON -----


def interactive_mode(mode, args, needed):
    print(f"{mode} mode was selected, but some needed information was missing!")
    if "<profile>" in needed:
        args["<profile>"] = inquirer.select(
            message="Please select which demographic you'd like to check for ads with:",
            choices=[
                "4F",
                "4M",
                "6M",
                "7F",
                "9F",
                "10M",
                "None",
            ],
        )
    if "<time>" in needed:
        valid_time = False
        while valid_time == False:
            time_target = input(
                "Please provide a number of hours that you'd like to monitor ads for:"
            )
            if time_target.isdigit():  # check that target is a number
                if 1 <= int(time_target):  # check that target is greater than 0
                    args["<time>"] = int(
                        time_target
                    )  # set target to be an integer for use later
                    valid_time = True
                    continue
                else:
                    print(
                        "Time invalid! Please provide a number greater than 0!"
                    )  # print error when conditions not met
            else:
                print(
                    "Time invalid! Pleae ensure you enter the number as a digit."
                )  # print error when conditions not met
    # TODO add target and other needed for other modes
    print(args)
    return args
