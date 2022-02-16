from json_memoize.json_memoize import memoize
import requests
import csv
from pathlib import Path

from bs4 import BeautifulSoup

# This will need to:
#  - scrape for locid -> hotspot name
#  - get eBird taxonomy file

_TAXONOMY_PATH = Path(__file__).parent.parent / "data" / "eBird_taxonomy_v2021.csv"
with open(_TAXONOMY_PATH, "r", encoding="latin_1") as taxonomy_file:
    taxonomy_reader = [row for row in csv.reader(taxonomy_file, dialect="excel")]

TAXONOMIC_INDEX_DICT = {row[3]: int(row[0]) for row in taxonomy_reader[1:]}


@memoize(app_name="ebird_barchart_summarizer")
def hotspot_name_from_loc_id(loc_id: str) -> str:
    """
    Scrapes the public eBird hotspot page for the supplied hotspot id, and returns that hotspot's name.
    Cached locally to avoid bugging eBird's servers too much.
    """
    base_url = "https://ebird.org/hotspot/"
    hotspot_url = base_url + loc_id
    response = requests.get(hotspot_url).text
    soup = BeautifulSoup(response, "html.parser")
    return soup.find("h1").text.strip()


def test():
    test_loc_ids = [
        "L109516",
        "L351189",
        "L385839",
    ]
    for loc in test_loc_ids:
        print(hotspot_name_from_loc_id(loc))

if __name__ == "__main__":
    test()