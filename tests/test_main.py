import utils
from main import app
from unittest.mock import patch
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


@patch("utils.get_berries_names")
@patch("utils.get_growth_times")
def test_get_berries_stats():
    mock_get_berries_names.return_value = ["Berry A", "Berry B", "Berry C"]
    mock_get_growth_times.return_value = [1, 3, 5, 7]

    response = client.get("/allBerryStats")
    assert response.status_code == 200

    key_list = ["berries_names", "min_growth_time", "median_growth_time", "max_growth_time", "variance_growth_time",
                "mean_growth_time", "frequency_growth_time"]
    for key in response.json().keys():
        assert key in key_list
