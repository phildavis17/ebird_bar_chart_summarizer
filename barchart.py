import calendar
import csv
import logging
import math

from pathlib import Path
from typing import Collection, Sized, Protocol


class Barchart:
    """A class for storing and manipulating data from eBird Bar Chart Data csv files."""
    BC_FILE_SAMPLE_SIZE_ROW = 14
    BC_FILE_OBS_START_ROW = 16
    BC_FILE_PERIOD_COL_OFFSET = -2
    # ^^^ This offset makes it easier to access numbered period indicies
    #     row[n + BC_FILE_PERIOD_COL_OFFSET] will get period n
    
    def __init__(self) -> None:
        self.loc_id: str = ""
        self.name: str = ""
        self.start_year: int = 0
        self.end_year: int = 0
        self.start_month: int = 0
        self.end_month: int = 0
        self.sample_sizes: list = []
        self.observations: dict = {}
        self.species: set = set()
        self.other_taxa: set = set()

    @classmethod
    def new_from_csv(cls, csv_path: Path) -> "Barchart":
        new_barchart = Barchart()
        new_barchart._ingest_csv_data(csv_path)
        return new_barchart

    def _ingest_csv_data(self, csv_path: Path) -> None:
        filename_parts = self._parse_barchart_filename(csv_path)
        self.loc_id = filename_parts["loc_id"]
        self.name = filename_parts["name"]
        self.start_year = filename_parts["start_year"]
        self.end_year = filename_parts["end_year"]
        self.start_month = filename_parts["start_month"]
        self.end_month = filename_parts["end_month"]
        with open(csv_path, "r") as in_file:
            data_rows = [row for row in csv.reader(in_file, dialect="excel-tab")]
        self.sample_sizes = [int(float(s)) for s in data_rows[self.BC_FILE_SAMPLE_SIZE_ROW][1:]]
        for row in data_rows[self.BC_FILE_OBS_START_ROW:]:
            sp_name = self.clean_sp_name(row[0])
            obs_list = [int(obs * sample) for obs, sample in zip(row[1:], self.sample_sizes)]
            self.observations[sp_name] = obs_list
        for sp in self.observations:
            if self.is_good_species(sp):
                self.species.add(sp)
            else:
                self.other_taxa.add(sp)
        
    @staticmethod
    def _parse_barchart_filename(csv_path: Path) -> dict:
        """Returns a dict containing information extracted from the filename of an eBird barchart csv."""
        parts = csv_path.stem.split("_")
        parts_dict = {
            "loc_id": parts[1],
            "start_year": parts[2],
            "end_year": parts[3],
            "start_month": parts[4],
            "end_month": parts[5],
        }
        return parts_dict

    @ staticmethod
    def clean_sp_name(sp_name: str) -> str:
        """Returns a species name stripped of html information, if present."""
        return sp_name.split(" (<")[0]
    
    @staticmethod
    def is_good_species(sp_name: str) -> bool:
        """Returns True if the supplied species name contains substrings that indicate it is a sub-species level taxon."""
        flag_strings = (" sp.", " x ", "/", "Domestic", "hybrid")
        for flag in flag_strings:
            if flag.lower() in sp_name.lower():
                return False
        return True

    @staticmethod
    def combined_average(samp_sizes: Collection, obs:Collection) -> float:
        pass

