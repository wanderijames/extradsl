"""Process CSV files

Example:

    > python -m extradsl.bin.csv ../../docs/examples/housing.csv \
        -c ../../docs/examples/extract1/extract1.json \
        -o ../../docs/examples/extract1/extract1_output.csv

"""
import argparse
from typing import Any, Optional

from ..io.local_csv import read_csv, write_csv
from ..parser import Config, Extraction


def create_parser() -> argparse.ArgumentParser:
    """Create parser"""

    parser = argparse.ArgumentParser()  # pylint: disable=invalid-name

    parser.add_argument(
        "filename", help="CSV file (Data source)"
    )

    parser.add_argument(
        "-c",
        "--config",
        help="ExtraDSL spec",
        required=True,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file name"
    )

    return parser


def main(args: Optional[argparse.Namespace] = None) -> Any:
    """client application"""
    # pylint: disable=assignment-from-no-return

    if args is None:
        parser = create_parser()
        args = parser.parse_args()

    table = read_csv(args.filename)
    # print(table, dir(table))
    conf = Config(args.config)
    extractions = conf.extract
    for extract in extractions:
        table = Extraction(table, extract).execute()

    if args.output:
        write_csv(args.output, table)


if __name__ == "__main__":

    response = main()
    if isinstance(response, list):
        for item in response:
            print(response)
