from re import A
import pytest

from ebird_interface import hotspot_name_from_loc_id

def test_get_hotspot_name():
    assert hotspot_name_from_loc_id("L109516") == "Prospect Park"
    assert hotspot_name_from_loc_id("L351189") == "Calvert Vaux Park (Dreier-Offerman Park)"
    assert hotspot_name_from_loc_id("L385839") == "Salt Marsh Nature Center at Marine Park"