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
    return response


@pytest.fixture
def client():
    api = SSE_API("https://api.sse.cisco.com", "client-id", "client-secret")
    api.token = "test-token"
    return api


@pytest.mark.parametrize(
    ("method_name", "item_key"),
    [
        ("ListVirtualAppliances", "originId"),
        ("ListRoamingComputers", "deviceId"),
    ],
)
def test_array_list_actions_fetch_all_numbered_pages(client, method_name, item_key):
    page_one = [{item_key: index} for index in range(100)]
    page_two = [{item_key: index} for index in range(100, 125)]

    with patch.object(
        client,
        "Query",
        side_effect=[_json_response(page_one), _json_response(page_two)],
    ) as query:
        result = getattr(client, method_name)()

    assert [call.kwargs["params"] for call in query.call_args_list] == [
        {"page": 1, "limit": 100},
        {"page": 2, "limit": 100},
    ]
    assert len(result) == 125
    assert result[0][item_key] == 0
    assert result[-1][item_key] == 124


def test_passive_dns_forwards_pagination_and_returns_page_info(client):
    payload = {
        "records": [{"name": "example.com", "type": "A", "rr": "192.0.2.1"}],
        "pageInfo": {
            "offset": 20,
            "limit": 10,
            "totalNumRecords": 31,
            "hasMoreRecords": True,
        },
    }

    with patch.object(client, "Query", return_value=_json_response(payload)) as query:
        records, page_info = client.GetPassiveDNS("example.com", offset=20, limit=10)

    assert query.call_args.kwargs["params"] == {"offset": 20, "limit": 10}
    assert records == payload["records"]
    assert page_info == payload["pageInfo"]
