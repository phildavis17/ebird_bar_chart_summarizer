import pytest

from barchart import Barchart
from pathlib import Path


def test_parse_file_name():
    fn = Path("ebird_L128138__1900_2021_1_12_barchart.txt")
    parts = Barchart._parse_barchart_filename(fn)
    assert parts["loc_id"] == "L128138"
    assert parts["start_year"] == "1900"
    assert parts["end_year"] == "2021"
    assert parts["start_month"] == "1"
    assert parts["end_month"] == "12"

def test_combined_average():
    tests = [
        (([1, 2, 3], [1, 2, 3]), 1.0),
        (([2], [1]), 0.5),
        (([0, 0, 0], [5, 3, 5]), 0.0),
    ]
    for entry in tests:
        data, expected = entry
        samps, obs = data
        assert Barchart._combined_average(samps, obs) == expected

def test_clean_sp_name():
    spuh = 'goose sp. (<em class="sci">Anser/Branta sp.</em>)'
    domestic = 'Mallard (Domestic type) (<em class="sci">Anas platyrhynchos (Domestic type)</em>)'
    slash = 'Blue-winged/Cinnamon Teal (<em class="sci">Spatula discors/cyanoptera</em>)'
    one_word = 'Gadwall (<em class="sci">Mareca strepera</em>)'
    two_word = 'Wood Duck (<em class="sci">Aix sponsa</em>)'
    clean = 'Wood Duck'

    assert Barchart.clean_sp_name(spuh) == "goose sp."
    assert Barchart.clean_sp_name(domestic) == "Mallard (Domestic type)"
    assert Barchart.clean_sp_name(slash) == "Blue-winged/Cinnamon Teal"
    assert Barchart.clean_sp_name(one_word) == "Gadwall"
    assert Barchart.clean_sp_name(two_word) == "Wood Duck"
    assert Barchart.clean_sp_name(clean) == "Wood Duck"



def test_is_good_species():
    spuh = "goose sp."
    domestic = "Mallard (Domestic type)"
    slash = "Blue-winged/Cinnamon Teal"
    cross = "Western x Glaucous-winged Gull"
    species_1 = "Gadwall"
    species_2 = "Vaux's Swift"

    assert not Barchart.is_good_species(spuh)
    assert not Barchart.is_good_species(domestic)
    assert not Barchart.is_good_species(slash)
    assert not Barchart.is_good_species(cross)
    assert Barchart.is_good_species(species_1)
    assert Barchart.is_good_species(species_2)

    