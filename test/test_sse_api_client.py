# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.mock import MagicMock, patch

import pytest

from src.sse_api_client import SSE_API


def _json_response(payload):
    response = MagicMock()
    response.json.return_value = payload
    response.raise_for_status = MagicMock()
    return response


@pytest.fixture
def client():
    api = SSE_API("https://api.sse.cisco.com", "client-id", "client-secret")
    api.token = "test-token"
    return api


def test_list_api_keys_fetches_all_pages(client):
    page_one = {
        "message": "OK",
        "offset": 0,
        "limit": 100,
        "total": 150,
        "keys": [{"id": f"key-{i}"} for i in range(100)],
    }
    page_two = {
        "message": "OK",
        "offset": 100,
        "limit": 100,
        "total": 150,
        "keys": [{"id": f"key-{i}"} for i in range(100, 150)],
    }
    with patch.object(
        client,
        "Query",
        side_effect=[_json_response(page_one), _json_response(page_two)],
    ) as mock_query:
        result = client.ListApiKeys()

    assert mock_query.call_count == 2
    assert mock_query.call_args_list[0].kwargs["params"] == {"offset": 0, "limit": 100}
    assert mock_query.call_args_list[1].kwargs["params"] == {
        "offset": 100,
        "limit": 100,
    }
    assert len(result["keys"]) == 150
    assert result["total"] == 150
    assert result["keys"][0]["id"] == "key-0"
    assert result["keys"][-1]["id"] == "key-149"


def test_list_virtual_appliances_fetches_all_pages(client):
    page_one = [{"originId": i} for i in range(100)]
    page_two = [{"originId": i} for i in range(100, 125)]
    with patch.object(
        client,
        "Query",
        side_effect=[_json_response(page_one), _json_response(page_two)],
    ) as mock_query:
        result = client.ListVirtualAppliances()

    assert mock_query.call_count == 2
    assert mock_query.call_args_list[0].kwargs["params"] == {"page": 1, "limit": 100}
    assert mock_query.call_args_list[1].kwargs["params"] == {"page": 2, "limit": 100}
    assert len(result) == 125
    assert result[0]["originId"] == 0
    assert result[-1]["originId"] == 124


def test_list_roaming_computers_fetches_all_pages(client):
    page_one = [{"deviceId": f"device-{i}"} for i in range(100)]
    page_two = [{"deviceId": f"device-{i}"} for i in range(100, 130)]
    with patch.object(
        client,
        "Query",
        side_effect=[_json_response(page_one), _json_response(page_two)],
    ) as mock_query:
        result = client.ListRoamingComputers()

    assert mock_query.call_count == 2
    assert mock_query.call_args_list[0].kwargs["params"] == {"page": 1, "limit": 100}
    assert mock_query.call_args_list[1].kwargs["params"] == {"page": 2, "limit": 100}
    assert len(result) == 130
    assert result[0]["deviceId"] == "device-0"
    assert result[-1]["deviceId"] == "device-129"
