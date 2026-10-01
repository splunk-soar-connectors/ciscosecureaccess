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
import requests

from src.response_handling import UnexpectedAPIResponse
from src.sse_api_client import SSE_API


def _json_response(payload):
    """Create a successful mocked HTTP response containing JSON payload."""
    response = MagicMock()
    response.json.return_value = payload
    response.raise_for_status.return_value = None
    return response


@pytest.fixture
def client():
    """Return an authenticated SSE API client for unit tests."""
    api = SSE_API("https://api.sse.cisco.com", "client-id", "client-secret")
    api.token = "test-token"
    return api


def test_query_normalizes_method_url_and_forwards_request_options():
    """Normalize request inputs and forward them to requests."""
    api = SSE_API("https://api.sse.cisco.com/", "client-id", "client-secret")
    api.token = "test-token"
    response = _json_response({"ok": True})

    with patch("src.sse_api_client.requests.request", return_value=response) as request:
        result = api.Query(
            scope="deployments",
            end_point="/networkdevices",
            operation="post",
            request_data={"name": "device"},
            params={"limit": 10},
        )

    assert result is response
    request.assert_called_once_with(
        method="POST",
        url="https://api.sse.cisco.com/deployments/v2/networkdevices",
        headers={
            "Authorization": "Bearer test-token",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        params={"limit": 10},
        json={"name": "device"},
        timeout=60,
    )
    response.raise_for_status.assert_called_once_with()


def test_request_json_returns_parsed_json(client):
    """Return decoded JSON from the canonical query method."""
    with patch.object(client, "Query", return_value=_json_response({"ok": True})):
        assert client.request_json(
            scope="deployments", end_point="networkdevices", operation="GET"
        ) == {"ok": True}


@pytest.mark.parametrize(
    ("method_name", "item_key"),
    [
        ("ListVirtualAppliances", "originId"),
        ("ListRoamingComputers", "deviceId"),
    ],
)
def test_array_list_actions_fetch_all_numbered_pages(client, method_name, item_key):
    """Fetch and combine all numbered pages for array-based list actions."""
    page_one = [{item_key: index} for index in range(100)]
    page_two = [{item_key: index} for index in range(100, 125)]

    with patch.object(
        client,
        "request_json",
        side_effect=[page_one, page_two],
    ) as request_json:
        result = getattr(client, method_name)()

    assert [call.kwargs["params"] for call in request_json.call_args_list] == [
        {"page": 1, "limit": 100},
        {"page": 2, "limit": 100},
    ]
    assert len(result) == 125
    assert result[0][item_key] == 0
    assert result[-1][item_key] == 124


def test_query_all_pages_stops_when_total_reached(client):
    """Stop page-numbered requests after the reported total is reached."""
    with patch.object(
        client,
        "request_json",
        side_effect=[
            {"status": "ok", "meta": {"limit": 1, "total": 2}, "data": [{"id": 1}]},
            {"status": "ok", "meta": {"limit": 1, "total": 2}, "data": [{"id": 2}]},
        ],
    ) as request_json:
        result = client.QueryAllPages(
            scope="policies", end_point="destinationlists", limit=1
        )

    assert [call.kwargs["params"] for call in request_json.call_args_list] == [
        {"page": 1, "limit": 1},
        {"page": 2, "limit": 1},
    ]
    assert result["data"] == [{"id": 1}, {"id": 2}]
    assert result["meta"]["total"] == 2


def test_query_all_pages_stops_when_has_more_records_false(client):
    """Stop page-numbered requests when the API reports no more records."""
    with patch.object(
        client,
        "request_json",
        return_value={
            "status": "ok",
            "pageInfo": {
                "limit": 1,
                "totalNumRecords": 10,
                "hasMoreRecords": False,
            },
            "records": [{"id": 1}],
        },
    ) as request_json:
        result = client.QueryAllPages(
            scope="investigate", end_point="pdns/name/example.com", limit=1
        )

    request_json.assert_called_once()
    assert result["data"] == [{"id": 1}]
    assert result["meta"]["total"] == 10


def test_query_all_pages_handles_raw_array_short_page(client):
    """Stop raw-array pagination when a page contains fewer records than requested."""
    with patch.object(client, "request_json", return_value=[{"id": 1}]):
        result = client.QueryAllPages(
            scope="deployments",
            end_point="sites",
            limit=100,
            response_is_array=True,
        )

    assert result["data"] == [{"id": 1}]
    assert result["meta"]["limit"] == 1


def test_query_all_pages_rejects_invalid_response_shapes(client):
    """Reject raw-array and envelope responses with invalid JSON shapes."""
    with (
        patch.object(client, "request_json", return_value={"id": 1}),
        pytest.raises(UnexpectedAPIResponse, match="expected an array"),
    ):
        client.QueryAllPages(
            scope="deployments",
            end_point="sites",
            limit=100,
            response_is_array=True,
        )

    with (
        patch.object(client, "request_json", return_value=[]),
        pytest.raises(UnexpectedAPIResponse, match="expected an object"),
    ):
        client.QueryAllPages(
            scope="policies",
            end_point="destinationlists",
            limit=100,
        )


def test_query_all_pages_offset_rejects_non_object_response(client):
    """Reject a non-object response from offset-based pagination."""
    with (
        patch.object(client, "request_json", return_value=[]),
        pytest.raises(UnexpectedAPIResponse, match="expected an object"),
    ):
        client.QueryAllPagesOffset(
            scope="admin",
            end_point="vpn/userConnections",
            limit=100,
        )


def test_query_all_pages_offset_advances_offset_and_coerces_non_list(client):
    """Advance offsets and preserve singleton response coercion."""
    with patch.object(
        client,
        "request_json",
        side_effect=[
            {"data": [{"id": 1}], "total": 2},
            {"data": {"id": 2}, "total": 2},
        ],
    ) as request_json:
        result = client.QueryAllPagesOffset(
            scope="admin", end_point="vpn/userConnections", limit=1
        )

    assert [call.kwargs["params"] for call in request_json.call_args_list] == [
        {"offset": 0, "limit": 1},
        {"offset": 1, "limit": 1},
    ]
    assert result["data"] == [{"id": 1}, {"id": 2}]
    assert result["offset"] == 0
    assert result["limit"] == 1
    assert result["total"] == 2


def test_query_refreshes_token_once_on_401(client):
    """Refresh the token once and retry after an unauthorized response."""
    unauthorized = requests.Response()
    unauthorized.status_code = 401
    unauthorized.url = "https://api.sse.cisco.com/deployments/v2/networkdevices"
    unauthorized._content = b"unauthorized"
    unauthorized_error = requests.HTTPError("401 Client Error", response=unauthorized)

    first_response = MagicMock()
    first_response.raise_for_status.side_effect = unauthorized_error
    second_response = _json_response({"ok": True})

    def refresh_token():
        """Set the refreshed token used by the retry assertion."""
        client.token = "refreshed-token"
        return client.token

    with (
        patch("src.sse_api_client.requests.request") as request,
        patch.object(client, "GetToken", side_effect=refresh_token) as get_token,
    ):
        request.side_effect = [first_response, second_response]
        result = client.Query("deployments", "networkdevices", "GET")

    assert result is second_response
    assert get_token.call_count == 1
    assert [
        call.kwargs["headers"]["Authorization"] for call in request.call_args_list
    ] == ["Bearer test-token", "Bearer refreshed-token"]


def test_passive_dns_forwards_pagination_and_returns_page_info(client):
    """Forward passive-DNS pagination parameters and return page metadata."""
    payload = {
        "records": [{"name": "example.com", "type": "A", "rr": "192.0.2.1"}],
        "pageInfo": {
            "offset": 20,
            "limit": 10,
            "totalNumRecords": 31,
            "hasMoreRecords": True,
        },
    }

    with patch.object(client, "request_json", return_value=payload) as request_json:
        records, page_info = client.GetPassiveDNS("example.com", offset=20, limit=10)

    assert request_json.call_args.kwargs["params"] == {"offset": 20, "limit": 10}
    assert records == payload["records"]
    assert page_info == payload["pageInfo"]


def test_make_request_verifies_tls_by_default(client):
    """Enable TLS certificate verification by default for arbitrary requests."""
    with patch("src.sse_api_client.requests.request") as request:
        client.MakeRequest(method="get", endpoint="deployments/v2/networkdevices")

    assert request.call_args.kwargs["verify"] is True


def test_query_uses_requests_tls_verification_default(client):
    """Use requests' default TLS behavior for standard queries."""
    response = MagicMock()
    response.raise_for_status.return_value = None

    with patch("src.sse_api_client.requests.request", return_value=response) as request:
        client.Query("deployments", "networkdevices", "GET")

    assert "verify" not in request.call_args.kwargs
    assert request.call_args.kwargs["method"] == "GET"
    assert (
        request.call_args.kwargs["url"]
        == "https://api.sse.cisco.com/deployments/v2/networkdevices"
    )


def test_query_rejects_unsupported_operation(client):
    """Reject HTTP operations outside the supported operation set."""
    with pytest.raises(ValueError, match="Unsupported operation: trace"):
        client.Query("deployments", "networkdevices", "TRACE")


def test_query_returns_raw_response(client):
    """Return the raw response from the canonical query method."""
    response = _json_response({"ok": True})
    with patch("src.sse_api_client.requests.request", return_value=response) as request:
        result = client.Query("deployments", "networkdevices", "GET")

    assert result is response
    request.assert_called_once()
