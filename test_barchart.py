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
def sample_barchart() -> "Barchart":
    test_bc_path = Path(__file__).parent / "data" / "testing" / "ebird_L109516__1900_2021_1_12_barchart.txt/"
    return Barchart.new_from_csv(test_bc_path)
    

def test_extant(sample_barchart):
    """Tests that a barchart object has actually been created."""
    assert sample_barchart is not None


def test_ingest_filename(sample_barchart: "Barchart"):
    """Tests that information from the filename has ben properly ingested."""
    assert sample_barchart.loc_id == "L109516"
    assert sample_barchart.start_year == 1900
    assert sample_barchart.end_year == 2021
    assert sample_barchart.start_month == 1
    assert sample_barchart.end_month == 12


def test_get_hotspot_name(sample_barchart: "Barchart"):
    """
    Tests that the hotspot's name has been properly collected.
    
    NOTE: the method that does this is cached, so this either
    tests that the cache is working, or it will ping eBird,
    which will be painfully slow.
    """
    assert sample_barchart.name == "Prospect Park"


def test_ingest_file_data_coarse(sample_barchart: "Barchart"):
    """Tests that *some* data is present."""
    assert sample_barchart.sample_sizes
    assert sample_barchart.observations
    assert sample_barchart.species
    assert sample_barchart.other_taxa


def test_ingest_file_data_medium(sample_barchart: "Barchart"):
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


def test_ingest_file_data_fine(sample_barchart: "Barchart"):
    """Checks that the data has correct values."""
    assert sample_barchart.sample_sizes[0] == 601
    assert sample_barchart.sample_sizes[47] == 363
    assert sample_barchart.observations["Snow Goose"][0] == 32
    assert sample_barchart.observations["Snow Goose"][47] == 35
    assert sample_barchart.observations["bird sp."][0] == 2
    assert sample_barchart.observations["bird sp."][47] == 1


def test_period_range(sample_barchart: "Barchart"):
    """Tests the construction of a period range list."""
    assert sample_barchart._build_period_range(1, 1) == [1]
    assert sample_barchart._build_period_range(1, 2) == [1, 2]
    assert sample_barchart._build_period_range(5, 8) == [5, 6, 7, 8]
    assert sample_barchart._build_period_range(46, 1) == [46, 47, 0, 1]


def test_period_summary_extant(sample_barchart: "Barchart"):
    """Tests that some form of summary is being generated."""
    test_dict = sample_barchart.build_summary_dict([1])
    assert test_dict is not None


def test_period_summary_basic(sample_barchart: "Barchart"):
    """Tests the construction of a summary dict under the simplest conditions."""
    sp_dict = sample_barchart.build_summary_dict([0])
    ot_dict = sample_barchart.build_summary_dict([47], include_sub_species=True)
    assert "Summer Tanager" in sample_barchart.observations
    assert "Snow Goose" in sp_dict
    assert "bird sp." not in sp_dict
    assert "Summer Tanager" not in sp_dict
    assert sp_dict["Snow Goose"] == 0.05324
    assert "Snow Goose" in ot_dict
    assert "bird sp." in ot_dict
    assert "Summer Tanager" not in ot_dict
    assert ot_dict["Snow Goose"] == 0.09642
    assert ot_dict["bird sp."] == 0.00275


def test_period_summary_medium(sample_barchart: "Barchart"):
    """Tests the construction of a summary dict under slightly more complex conditions."""
    sp_dict = sample_barchart.build_summary_dict([0, 1, 2, 3])
    ot_dict = sample_barchart.build_summary_dict([44, 45, 46, 47], include_sub_species=True)
    assert sp_dict["Snow Goose"] == 0.03861
    assert ot_dict["Snow Goose"] == 0.05191
    


def test_period_summary_complex(sample_barchart: "Barchart"):
    """Tests the construction of a summary dict under complex conditions."""
    sp_dict = sample_barchart.build_summary_dict([46, 47, 0, 1])
    ot_dict = sample_barchart.build_summary_dict([46, 47, 0, 1], include_sub_species=True)
    assert sp_dict["Snow Goose"] == 0.05158