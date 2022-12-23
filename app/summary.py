from typing import Optional

import app.ebird_interface as ebird_interface

class Summarizer:
    """
    A class which holds multiple Barchart objects, and is able to summarize their data in a few ways.
    """
    def __init__(self, barcharts: list, name: Optional[str] = None) -> None:
        self.name = name
        loc_ids = []
        for barchart in barcharts:
            loc_ids.append(barchart.loc_id)
        loc_ids.sort()
        self.loc_ids = tuple(loc_ids)
        self.hotspot_names: tuple = self._collect_hotspot_names(self.loc_ids)
        self.species: set = None
        self.other_taxa: set = None
        self.periods: tuple = None
        self.observations: dict = None

    @staticmethod
    def _collect_hotspot_names(loc_ids: tuple) -> tuple:
        return tuple([ebird_interface.hotspot_name_from_loc_id(loc_id) for loc_id in loc_ids])

    def simulate(self, active_hotspots: Optional[set] = None):
        """Generates a simulated outcome of a trip using the current hotspots."""
        pass

    def build_summary_dict(self) -> dict:
        """Generates a large dictionary that contains all the observation data for all the hotspots included in this summary."""
        pass

def test():
    print("ok")

if __name__ == "__main__":
    test()
