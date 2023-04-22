from main import app
from unittest.mock import patch
from fastapi.testclient import TestClient


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


@patch("utils.get_berries_names")
@patch("utils.get_growth_times")
def test_get_berries_stats(mock_get_growth_times, mock_get_berries_names):
    mock_get_berries_names.return_value = ["Berry A", "Berry B", "Berry C"]
    mock_get_growth_times.return_value = [1, 2, 3, 4, 5]

    response = client.get("/allBerryStats")
    assert response.status_code == 200

    expected_response = {
        "berries_names": ["Berry A", "Berry B", "Berry C"],
        "min_growth_time": 1,
        "median_growth_time": 3,
        "max_growth_time": 5,
        "variance_growth_time": 2.5,
        "mean_growth_time": 3,
        "frequency_growth_time": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1}
    }
    for key, val in response.json().items():
        assert key in expected_response.keys()
        assert val == expected_response[key]
