import calendar
import csv
import logging
import math

from pathlib import Path
from typing import Collection, Sized


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


    @staticmethod
    def _parse_barchart_filename(csv_path: Path) -> dict:
        pass

    @ staticmethod
    def clean_sp_name(sp_name: str) -> str:
        """Returns a species name stripped of html information, if present."""
        pass

    @staticmethod
    def combined_average(samp_sizes: Collection, obs:Collection) -> float:
        pass

