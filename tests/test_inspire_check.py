import os
from unittest.mock import Mock

import pytest

os.environ.setdefault("OPENSEARCH_INSPIRE_HOST", "test")
os.environ.setdefault("OPENSEARCH_INSPIRE_USER", "test")
os.environ.setdefault("OPENSEARCH_INSPIRE_PASSWORD", "test")

from lib import arxiv_completness_check_script as completeness


@pytest.mark.parametrize(
    ("hits", "expected"),
    [([{"metadata": {"control_number": 1119090}}], 1119090), ([], None)],
)
def test_fetch_inspire_record_searches_arxiv_field(monkeypatch, hits, expected):
    response = Mock()
    response.json.return_value = {"hits": {"hits": hits}}
    request = Mock(return_value=response)
    monkeypatch.setattr(completeness.requests, "get", request)

    assert completeness._fetch_inspire_record_by_api("1206.4931") == expected
    request.assert_called_once_with(
        completeness.HEP_API_URL, params={"q": "arxiv:1206.4931"}
    )
