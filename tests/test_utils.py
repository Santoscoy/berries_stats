import utils
import pytest
import json
from unittest.mock import patch
from unittest import TestCase
from collections import Counter
from tests.fig_base64 import fig_base64


@pytest.mark.parametrize(
    "url, expected_result", [
        ("https://api.test.com", {"key": "value"})
    ]
)
def test_get_content(url, expected_result):
    with patch("utils.requests.get") as mock_get:
        mock_response = expected_result
        mock_get.return_value.content.decode.return_value = json.dumps(mock_response)
        content = utils.get_content(url)

        assert content == expected_result


@patch("utils.get_content")
@patch("utils.get_berries_count")
def test_get_berries_data(mock_get_berries_count, mock_get_content):
    mock_get_berries_count.return_value = 5
    mock_get_content.return_value = {
        "results": [
            {
                "name": "test1",
                "url": "https://api/1/"
            },
            {
                "name": "test2",
                "url": "https://api/2/"
            },
            {
                "name": "test3",
                "url": "https://api/3/"
            },
            {
                "name": "test4",
                "url": "https://api/4/"
            },
            {
                "name": "test5",
                "url": "https://api/5/"
            },
        ]
    }
    expected_result = {
        "test1": "https://api/1/",
        "test2": "https://api/2/",
        "test3": "https://api/3/",
        "test4": "https://api/4/",
        "test5": "https://api/5/",
    }
    assert utils.get_berries_data() == expected_result


@patch("utils.get_content")
def test_get_count(mock_get_content):
    mock_get_content.return_value = {"count": 10}
    count = utils.get_berries_count()
    assert count == 10


def test_get_growth_times():
    urls = ["https://api/1/", "https://api/2/", "https://api/3/" ]
    contents = [
        {"growth_time": 10},
        {"growth_time": 12},
        {"growth_time": 14},
    ]

    def mock_get_content(url):
        index = urls.index(url)
        return contents[index]

    with patch("utils.get_content", side_effect=mock_get_content):
        grow_time_list = utils.get_growth_times(urls)

        expected_result = [10, 12, 14]
        assert grow_time_list == expected_result


class UtilsTest(TestCase):
    def setUp(self):
        self.growth_time_list = [1, 2, 3, 4, 5]

    def test_get_max_growth_time(self):
        assert utils.get_max_growth_time(self.growth_time_list) == 5

    def test_get_median_growth_time(self):
        assert utils.get_median_growth_time(self.growth_time_list) == 3.0

    def test_get_min_growth_time(self):
        assert utils.get_min_growth_time(self.growth_time_list) == 1

    def test_get_variance_growth_time(self):
        assert utils.get_variance_growth_time(self.growth_time_list) == 2.5

    def test_get_mean_growth_time(self):
        assert utils.get_mean_growth_time(self.growth_time_list) == 3

    def test_get_growth_time_frequencies(self):
        expected_result = Counter({1: 1, 2: 1, 3: 1, 4: 1, 5: 1})
        assert utils.get_growth_time_frequencies(self.growth_time_list) == expected_result

    def test_generate_histogram(self):
        with patch('utils.get_growth_times', return_value=self.growth_time_list):
            result = utils.generate_histogram()

            expected_html = f'<html><head><title>Histogram</title></head><body>' \
                            f'<img src="data:image/png;base64,{fig_base64}"></body></html>'

            assert result.strip() == expected_html

    def test_generate_html(self):
        string = "test"
        assert utils.generate_html(string) == '<html><head><title>Histogram</title></head><body>' \
                                              '<img src="data:image/png;base64,test"></body></html>'
