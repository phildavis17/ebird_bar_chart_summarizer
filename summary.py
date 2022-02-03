from typing import Optional

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
        self.loc_ids = loc_ids


        self.hotspot_names: tuple = None
        self.species: set = None
        self.other_taxa: set = None
        self.periods: tuple = None
        self.observations: dict = None

    def simulate(self, active_hotspots: Optional[set] = None):
        """Generates a simulated outcome of a trip using the current hotspots."""
        pass