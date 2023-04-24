from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_read_main():
    """Test for root endpoint"""
    response = client.get("/")
    assert response.status_code == 200


@patch("app.utils.get_berries_data")
@patch("app.utils.get_growth_times")
def test_get_berries_stats(mock_get_growth_times, mock_get_berries_names):
    """Testing /allBerriesStats endpoint"""
    mock_get_berries_names.return_value = {
        "Berry_A": "https://pokeapi.co/api/v2/berry/1/",
        "Berry_B": "https://pokeapi.co/api/v2/berry/2/",
        "Berry_C": "https://pokeapi.co/api/v2/berry/3/",
        "Berry_D": "https://pokeapi.co/api/v2/berry/4/",
        "Berry_E": "https://pokeapi.co/api/v2/berry/5/",
    }
    mock_get_growth_times.return_value = [1, 2, 3, 4, 5]

    response = client.get("/allBerryStats")
    assert response.status_code == 200

    expected_response = {
        "berries_names": ["Berry_A", "Berry_B", "Berry_C", "Berry_D", "Berry_E"],
        "min_growth_time": 1,
        "median_growth_time": 3,
        "max_growth_time": 5,
        "variance_growth_time": 2.5,
        "mean_growth_time": 3,
        "frequency_growth_time": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1},
    }
    for key, val in response.json().items():
        assert key in expected_response.keys()
        assert val == expected_response[key]


@patch("app.utils.generate_histogram")
def test_get_frequency_histogram(mock_get_growth_times):
    """Testing the /histogram endpoint"""
    mock_get_growth_times.return_value = "plain_html"

    response = client.get("/histogram")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "text/html; charset=utf-8" == response.headers.get("content-type")
