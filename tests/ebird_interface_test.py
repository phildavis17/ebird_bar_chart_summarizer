import pytest

from app.ebird_interface import TAXONOMIC_INDEX_DICT, hotspot_name_from_loc_id

def test_get_hotspot_name():
    assert hotspot_name_from_loc_id("L109516") == "Prospect Park"
    assert hotspot_name_from_loc_id("L351189") == "Calvert Vaux Park (Dreier-Offerman Park)"
    assert hotspot_name_from_loc_id("L385839") == "Salt Marsh Nature Center at Marine Park"

def test_tax_dict():
    assert TAXONOMIC_INDEX_DICT["Common Ostrich"] == 1
    assert TAXONOMIC_INDEX_DICT["bird sp."] == 35000
