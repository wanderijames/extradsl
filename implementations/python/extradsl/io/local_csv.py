"""Read and write CSV"""
import csv
from typing import Dict, Optional
from pyarrow import csv as pcsv, Table


def read_csv(
        filename: str,
        read_opts: Optional[Dict[str, str]] = None,
        convert_opts: Optional[Dict[str, str]] = None) -> Table:
    """Read csv from """
    parse_options = None
    convert_options = None
    if read_opts:
        parse_options = pcsv.ParseOptions(
            delimiter=read_opts.get('delimiter', ','),
            quote_char=read_opts.get('quotechar', '"'),
            escape_char=read_opts.get('escapechar', False)
        )
    if convert_opts:
        convert_options = pcsv.ConvertOptions(**convert_opts)
    return pcsv.read_csv(
        filename,
        parse_options=parse_options,
        convert_options=convert_options
    )


def to_csv_data(table):
    """Convert table to csv"""
    col_data = table.to_pydict()
    cols = list(col_data.keys())
    num_columns = len(cols)
    values = zip(*list(col_data.values()))
    for val in values:
        row = {cols[index]: val[index] for index in range(num_columns)}
        yield row


def write_csv(
        filename: str,
        table: Table,
        write_opts: Optional[Dict[str, str]] = None) -> None:
    """Write CSV"""
    # print(table)
    # print(table.column_names)
    with open(filename, 'w') as fout:
        writer = csv.DictWriter(fout, fieldnames=table.column_names)
        writer.writeheader()
        writer.writerows(to_csv_data(table))
