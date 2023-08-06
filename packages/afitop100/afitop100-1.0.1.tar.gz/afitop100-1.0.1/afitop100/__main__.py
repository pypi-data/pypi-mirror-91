import sys
import logging
import argparse
from afitop100 import AFITop100

logger = logging.getLogger("afitop100")


def main():
    """🧙‍✨ where the magic happens ✨‍🧙"""

    parser = argparse.ArgumentParser(
        prog="afitop100", usage="%%(prog) [options]", description="Get the AFI Top 100 List(s)"
    )
    parser.add_argument("-o", "--out", type=str, default="json", help="Output format -o json or -o csv")
    parser.add_argument(
        "-y", "--year", type=int, default=0, help="Limit the output to a specific year -y 1998 or -y 2007"
    )
    arguments = parser.parse_args()

    afi(arguments)


def afi(arguments):
    """Get the AFI list from wikipedia and present in the format requested in the cli parameters"""
    afi_100 = AFITop100()
    afi_100.scrape_afi_list()

    if arguments.out.lower().strip() == "json":
        print(afi_100.get_afi_list_json(arguments.year))
    elif arguments.out.lower().strip() == "csv":
        print(afi_100.get_afi_list_csv(arguments.year))


if __name__ == "__main__":
    sys.exit(main())