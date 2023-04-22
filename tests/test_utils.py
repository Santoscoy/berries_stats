import utils
import pytest
import json
from unittest import TestCase
from unittest.mock import patch


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

