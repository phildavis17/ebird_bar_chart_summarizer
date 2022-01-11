from typing import Optional

class Summary:
    """
    A class to combine and summarize eBird bar chart data.
    """
    def __init__(self) -> None:
        self.loc_ids: tuple = None
        self.names: tuple = None
        self.species: set = None
        self.other_taxa: set = None
        self.periods: tuple = None
        self.observations: dict = None


    def simulate(self, active_hotspots: Optional[set] = None):
        pass

