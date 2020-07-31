"""Parse the JSON config"""
import json
from typing import Any, Dict, Generator, List
from pyarrow import Table


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


class Extraction:
    """Step extraction"""

    def __init__(self, table: Table, instructions: List[Dict[str, Any]]):
        self.table = table
        self.instructions = instructions
        self._source_columns = []
        self._sink_columns = []

    @property
    def source_columns(self):
        if self._source_columns:
            return self._source_columns
        self._source_columns = [
            item["column_name"] for item in self.instructions]
        return self._source_columns

    @property
    def sink_columns(self):
        if self._sink_columns:
            return self._sink_columns
        self._sink_columns = [
            item["rename"] for item in self.instructions]
        return self._sink_columns

    def execute(self) -> Table:
        """Carry out the extraction"""
        return self.table.select(self.source_columns)


