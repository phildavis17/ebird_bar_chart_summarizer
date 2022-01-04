import calendar
import csv
import logging
import math

from pathlib import Path


class Barchart:
    """A class for storing and manipulating data from eBird Bar Chart Data csv files."""
    
    def __init__(self) -> None:
        self.loc_id: str = ""
        self.name: str = ""
        self.start_year: int = 0
        self.end_year: int = 0
        self.start_month: int = 0
        self.end_month: int = 0
        self.samp_sizes: dict = {}
        self.observations: dict = {}
        self.species: set = set()
        self.other_taxa: set = set()

    @staticmethod
    def new_from_csv(csv_path: Path) -> "Barchart":
        pass


