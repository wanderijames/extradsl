"""Parse the JSON config"""
import json
import re
from typing import Any, Dict, Generator, List
from pyarrow import array, Table
import numpy as np


class Config:

    def __init__(self, filename: str):
        """Reads config"""
        with open(filename) as fin:
            self._config = json.load(fin)

    @property
    def input_opts(self) -> Dict[str, str]:
        """Input type and options"""
        return self._config.get("input", {})

    @property
    def extracts(self) -> List[List[Dict[str, Any]]]:
        """Get the exractions instructions"""
        return self._config["extract"]

    @property
    def extract(self) -> Generator[List[Dict[str, Any]], None, None]:
        """Get single instruction"""
        for extract_ in self.extracts:
            yield extract_


class Select:

    pattern = re.compile(r"(?!\d)\w+")

    def __init__(self, table: Table, statement: str):
        """"""
        self.table = table
        self.statement = statement

    def compute(self):
        """select statement with multiple columns"""
        exec_statement = re.sub(self.pattern, self.repl, self.statement)
        ans = eval(exec_statement)
        return array(ans)

    @staticmethod
    def repl(match_obj):
        column = match_obj.group(0).strip("'")
        return f"np.array(self.table.column('{column}'), copy=False)"


class Extraction:
    """Step extraction"""

    def __init__(self, table: Table, instructions: List[Dict[str, Any]]):
        self.table = table
        self.instructions = instructions
        self._source_columns = []

    def key_val(self, key: str) -> Any:
        """Get value for a key in instructions"""
        return [
            item for item in self.instructions if key in item]

    @property
    def source_columns(self):
        if self._source_columns:
            return self._source_columns
        key = "select"
        cols = [
            re.findall(Select.pattern, item[key]) for item in self.key_val(key)
        ]
        columns = set([])
        for c in cols:
            columns.update(set([a.strip("'") for a in c]))
        self._source_columns = list(columns)
        return self._source_columns

    def execute(self) -> Table:
        """Carry out the extraction"""
        new_table = self.table.select(self.source_columns)
        compute_statements = self.key_val("as")
        for d in compute_statements:
            new_table = new_table.append_column(
                d["as"],
                Select(new_table, d["select"]).compute()
            )
        print(new_table)
        return new_table


