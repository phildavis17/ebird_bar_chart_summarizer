import calendar
import csv
import logging
from pathlib import Path
from typing import Collection

import ebird_interface


class Barchart:
    """
    A class for storing and manipulating data from eBird Bar Chart Data csv files.
    
    Stores all the data that can be extracted from an eBird Bar Chart file.
    """
    BC_FILE_SAMPLE_SIZE_ROW = 14
    BC_FILE_OBS_START_ROW = 16
    BC_FILE_PERIOD_COL_OFFSET = -2
    # ^^^ This offset makes it easier to access numbered period indicies
    #     row[n + BC_FILE_PERIOD_COL_OFFSET] will get period n
    MONTHS_BY_PERIOD = {
        "January": (0, 1, 2, 3),
        "February": (4, 5, 6, 7),
        "March": (8, 9, 10, 11),
        "April": (12, 13, 14, 15),
        "May": (16, 17, 18, 19),
        "June": (20, 21, 22, 23),
        "July": (24, 25, 26, 27),
        "August": (28, 29, 30, 31),
        "September": (32, 33, 34, 35),
        "October": (36, 37, 38, 39),
        "November": (40, 41, 42, 43),
        "December": (44, 45, 46, 47),
    }

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
        """Returns a Barchart object populated with data from an eBird CSV."""
        new_barchart = Barchart()
        new_barchart._ingest_csv_data(csv_path)
        return new_barchart

    def _ingest_csv_data(self, csv_path: Path) -> None:
        """
        Populates instance variables with data from a csv.
        
        Stores an integer number of samples, and an integer number of sightings,
        which can be used to create an occurance rate.
        """
        filename_parts = self._parse_barchart_filename(csv_path)
        self.loc_id = filename_parts["loc_id"]
        self.name = ebird_interface.hotspot_name_from_loc_id(self.loc_id)
        self.start_year = filename_parts["start_year"]
        self.end_year = filename_parts["end_year"]
        self.start_month = filename_parts["start_month"]
        self.end_month = filename_parts["end_month"]
        with open(csv_path, "r") as in_file:
            data_rows = [row for row in csv.reader(in_file, dialect="excel-tab")]
        self.sample_sizes = [int(float(s)) for s in data_rows[self.BC_FILE_SAMPLE_SIZE_ROW][1:] if s]
        for row in data_rows[self.BC_FILE_OBS_START_ROW:]:
            if not row:
                continue
            sp_name = self.clean_sp_name(row[0])
            obs_list = [int(float(obs) * sample) for obs, sample in zip(row[1:], self.sample_sizes)]
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
            "start_year": parts[3],
            "end_year": parts[4],
            "start_month": parts[5],
            "end_month": parts[6],
        }
        return parts_dict

    @ staticmethod
    def clean_sp_name(sp_name: str) -> str:
        """Returns a species name stripped of html information, if present."""
        return sp_name.partition(" (<")[0]
    
    @staticmethod
    def is_good_species(sp_name: str) -> bool:
        """Returns True if the supplied species name contains substrings that indicate it is a sub-species level taxon."""
        flag_strings = (" sp.", " x ", "/", "Domestic", "hybrid")
        for flag in flag_strings:
            if flag.lower() in sp_name.lower():
                return False
        return True
    
    @property
    def species_observations(self) -> dict:
        return {sp: self.observations[sp] for sp in self.species}

    @property
    def other_taxa_observations(self) -> dict:
        return {ot: self.observations[ot] for ot in self.other_taxa}

    @staticmethod
    def _combined_average(samp_sizes: Collection, obs: Collection) -> float:
        if len(samp_sizes) != len(obs):
            raise ValueError(f"Sample Sizes and Observation data of different lengths supplied.")
            # ^^^ The lengths of the sample sizes and observation data should always
            #     be the same, or else the math will seem right, but be wrong.
        if sum(samp_sizes) == 0:
            return 0.0
        return round(sum(obs) / sum(samp_sizes), 5)

    def build_summary_dict(self, start: int = 0, end: int = 47, include_sub_species: bool = False) -> dict:
        """
        Returns a dictionary of observation data summarized to a single number per species.
        """
        summary = {}
        for sp, obs in self.observations.items():
            if not(sp in self.species or include_sub_species):
                continue
            av_obs = self._combined_average(self.sample_sizes[start: end], obs[start: end])
            if av_obs:
                summary[sp] = av_obs
        return summary

    def __repr__(self) -> str:
        return f"<Barchart for {self.name}>"


def test():
    test_bc_path = Path(__file__).parent / "data" / "testing" / "ebird_L109516__1900_2021_1_12_barchart.txt/"
    test_bc = Barchart.new_from_csv(test_bc_path)
    #print(test_bc.build_summary_dict(start=14, end=16))
    #print(len(test_bc.observations))
    #print(test_bc.other_taxa)


if __name__ == "__main__":
    test()