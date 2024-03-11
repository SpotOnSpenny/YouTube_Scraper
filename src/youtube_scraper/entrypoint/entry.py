# ----- External Dependencies -----
from docopt import docopt
from InquirerPy import inquirer

# ----- Python Standard Library -----
import os

# ----- Internal Dependencies -----
from youtube_scraper.utilities.logger import start_logger
from youtube_scraper.core.monitor import monitor
from youtube_scraper.core.convert_to_json import convert_to_json


def main():
    # ----- Define Usage/Args for Doc Opt -----
    usage = """A fully realized command line utility for YouTube ad collection and monitoring.
    Part of the M2K project at the University of Calgary.

    Usage:
        m2k_scrape monitor -l <log_level> [-r <port> | -c <file_name>] [-p <profile>] [-t <monitor_time>]
        m2k_scrape collect -l <log_level> [-r <port> | -c <file_name>] [-p <profile>] [-n <number>]
        m2k_scrape json -f <folder_path>
        m2k_scrape (-h | -v)

    Options:
        -l, --log-level     REQUIRED: Specify the level of log messages you'd like to be logged.
        -r, --remote        Tell the script to log remotely, along with what <port> on PaperTrail to log to
        -c, --central       Tell the script to log locally, along with an optional name for the .txt log file. If no name is specified, the log will be named the current date.
        -p, --profile       Specify the age/gender profile you'd like to use to collect/monitor ads. If not specified, interactive mode will be used.
        -t, --time          Specify how long you'd like to monitor ads for continuously in hours.
        -n, --number        Specify the number of ads you'd like to collect. If not specified, interactive mode will be used.
        -h, --help          Provides (this) explanation of options and arguments for the utility.
        -v, --version       Provides the current version of the script installed.
        -f, --folder-path   The absolute path to the folder containing the .csv files that you'd like to convert to .json files.

    Arguments:
        <log_level>         The level of logs you'd like to be logged. Can be: 'debug', 'info', 'warn', 'error' or 'critical'.
        <port>              The port on your PaperTrail account, required if -r is specified.
        <file_name>         The name of the .txt file that you'd like to log to in the /logs folder of the worknig directory. If none specified, will save to a .txt named todays date.
        <profile>           The age/gender profile you'd like to use. Can be: 'None', '4M', '4F', '6M', '7F', '9F', '10M', '18M' or '18F'.
        <number>            The number of ads that you'd like to search for. Must be an integer.
        <monitor_time>      The number of hours that you'd like to monitor ads for. Must be an integer.
    """
    # ----- Create Args Dictionary -----
    args = docopt(usage, version="0.0.5")

    # ----- Monitor -----
    # Check to ensure nessescary information was provided, and start interactive mode if it was not
    if args["monitor"]:
        # ----- Set Up Logging -----
        if args["--remote"]:  # if specified, start logging remotely
            logger = start_logger(
                args["<log_level>"].lower(),
                args["<profile>"].upper(),
                "remote",
                port=int(args["<port>"]),
            )
        else:  # if else, start logging by file
            logger = start_logger(
                args["<log_level>"].lower(),
                args["<profile>"].upper(),
                "file",
                filename=args["<file_name>"],
            )

        required = ["<profile>", "<monitor_time>"]
        needed = ["<profile>", "<monitor_time>"]
        allowed_profiles = ["4M", "4F", "6M", "7F", "9F", "10M", "18M", "18F", None]
        for arg in required:
            if args[arg]:
                if arg == "<profile>":
                    if args[arg].capitalize() == "None":
                        args[arg] = None
                        needed.remove(arg)
                    elif args[arg].upper() in allowed_profiles:
                        args[arg] = args[arg].upper()
                        needed.remove(arg)
                if arg == "<monitor_time>":
                    if args[arg].isdigit():  # check that target is a number
                        if 1 <= int(args[arg]):  # check that target is greater than 0
                            args[arg] = int(args[arg])
                            needed.remove(arg)
        args = interactive_mode("monitor", args, needed)
        # Start monitor function
        monitor(logger, args["<monitor_time>"], args["<profile>"])

    # ----- Collect -----

    # ----- Convert Ads to JSON -----
    if args["json"]:
        # Check to ensure the filepath was provided
        if not args["<folder_path>"]:
            print(
                "JSON mode was selected, but the folder path was not provided! Please provide the folder path and try again."
            )
            quit(1)
        # Check if the folder path is valid
        else:
            if not os.path.exists(args["<folder_path>"]):
                print(
                    "JSON mode was selected, but the folder path provided was invalid! Please provide a valid folder path and try again."
                )
                quit(1)
            else:
                for filepath in os.listdir(args["<folder_path>"]):
                    if filepath.endswith(".csv"):
                        convert_to_json(f"{args['<folder_path>']}/{filepath}")
                print("Conversion complete! See the folder provided for processed JSON files.")





def interactive_mode(mode, args, needed):
    if needed != []:
        print(
            f"{mode} mode was selected, but some needed information was missing, or was invalid!"
        )
    # TODO Add logging params here too, no reason not to include them here tbh
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
                "18M",
                "18F",
                "None",
            ],
        ).execute()
    if "<monitor_time>" in needed:
        valid_time = False
        while valid_time == False:
            time_target = input(
                "Please provide a number of hours that you'd like to monitor ads for:"
            )
            if time_target.isdigit():  # check that target is a number
                if 1 <= int(time_target):  # check that target is greater than 0
                    args["<monitor_time>"] = int(
                        time_target
                    )  # set target to be an integer for use later
                    valid_time = True
                    continue
                else:
                    print(
                        "Time invalid! Please provide a number greater than or equal to 1!"
                    )  # print error when conditions not met
            else:
                print(
                    "Time invalid! Please ensure you enter the number as a digit."
                )  # print error when conditions not met
    # TODO add target and other needed for other modes
    return args
