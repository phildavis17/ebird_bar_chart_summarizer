import pytest

from barchart import Barchart
from pathlib import Path


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


@pytest.fixture
def sample_barchart():
    test_bc_path = Path(__file__).parent / "data" / "testing" / "ebird_L109516__1900_2021_1_12_barchart.txt/"
    return Barchart.new_from_csv(test_bc_path)
    

def test_extant(sample_barchart):
    assert sample_barchart is not None


def test_ingest_filename(sample_barchart):
    assert sample_barchart.loc_id == "L109516"
    assert sample_barchart.start_year == 1900
    assert sample_barchart.end_year == 2021
    assert sample_barchart.start_month == 1
    assert sample_barchart.end_month == 12


def test_get_hotspot_name(sample_barchart):
    assert sample_barchart.name == "Prospect Park"


def test_ingest_file_data_coarse(sample_barchart):
    """Tests that *some* data is present."""
    assert sample_barchart.sample_sizes
    assert sample_barchart.observations
    assert sample_barchart.species
    assert sample_barchart.other_taxa


def test_ingest_file_data_medium(sample_barchart):
    """Checks that data has the right shape."""
    assert "Snow Goose" in sample_barchart.species
    assert "Snow Goose" in sample_barchart.observations
    assert "bird sp." in sample_barchart.other_taxa
    assert "bird sp." in sample_barchart.observations
    assert len(sample_barchart.sample_sizes) == 48
    assert len(sample_barchart.observations["Snow Goose"]) == 48
    assert len(sample_barchart.observations["bird sp."]) == 48
    assert len(sample_barchart.species) == 288
    assert len(sample_barchart.other_taxa) == 83
    assert len(sample_barchart.observations) == 371

def test_ingest_file_data_fine(sample_barchart):
    """Checks that the data has correct values."""
    assert sample_barchart.sample_sizes[0] == 601
    assert sample_barchart.sample_sizes[47] == 363
    assert sample_barchart.observations["Snow Goose"][0] == 32
    assert sample_barchart.observations["Snow Goose"][47] == 35
    assert sample_barchart.observations["bird sp."][0] == 2
    assert sample_barchart.observations["bird sp."][47] == 1

