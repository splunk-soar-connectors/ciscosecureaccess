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

from unittest.mock import MagicMock

import pytest
import requests
from soar_sdk.exceptions import ActionFailure
from soar_sdk.params import Params

from src.actions.create_destination_list import create_destination_list
from src.actions.domains import get_passive_dns
from src.actions.list_firewall_rules import list_firewall_rules
from src.actions.list_sites import list_sites
from src.actions.list_vpn_sessions import list_vpn_sessions
from src.actions.make_request import make_request
from src.actions.rules import create_rule
from src.params import (
    CiscoSecureAccessMakeRequestParams,
    CreateDestinationListParams,
    CreateRuleParams,
    GetPassiveDNSParams,
    ListFirewallRulesParams,
)


def test_get_passive_dns_maps_pagination_output():
    """Map passive-DNS pagination metadata into the action output."""
    client = MagicMock()
    client.request_json.return_value = {
        "records": [{"name": "example.com", "type": "A", "rr": "192.0.2.1"}],
        "pageInfo": {
            "offset": 10,
            "limit": 1,
            "totalNumRecords": 12,
            "hasMoreRecords": True,
        },
    }
    asset = MagicMock()
    asset.get_client.return_value = client

    output = get_passive_dns(
        GetPassiveDNSParams(domain="example.com", offset=10, limit=1), asset
    )

    assert output.total_records == 12
    assert output.returned_records == 1
    assert output.offset == 10
    assert output.limit == 1
    assert output.has_more_records is True
    assert output.next_offset == 11
    client.request_json.assert_called_once_with(
        scope="investigate",
        end_point="pdns/name/example.com",
        operation="get",
        params={"offset": 10, "limit": 1},
    )


def test_list_sites_uses_paginated_transport():
    """Use page-numbered transport when listing sites."""
    client = MagicMock()
    client.QueryAllPages.return_value = {
        "data": [
            {
                "originId": 1,
                "name": "site",
                "siteId": 10,
                "isDefault": False,
                "modifiedAt": "2026-01-01T00:00:00Z",
                "createdAt": "2026-01-01T00:00:00Z",
            }
        ]
    }
    asset = MagicMock()
    asset.get_client.return_value = client

    output = list_sites(Params(), asset)

    assert output.sites[0].name == "site"
    client.QueryAllPages.assert_called_once_with(
        scope="deployments",
        end_point="sites",
        operation="get",
        limit=100,
        response_is_array=True,
    )


def test_list_vpn_sessions_uses_offset_paginated_transport():
    """Use offset pagination when listing VPN sessions."""
    client = MagicMock()
    client.QueryAllPagesOffset.return_value = {"data": [{"username": "user"}]}
    asset = MagicMock()
    asset.get_client.return_value = client

    output = list_vpn_sessions(Params(), asset)

    assert output.vpn_sessions[0].username == "user"
    client.QueryAllPagesOffset.assert_called_once_with(
        scope="admin",
        end_point="vpn/userConnections",
        operation="get",
        limit=1000,
    )


def test_create_destination_list_builds_request_body():
    """Build the expected destination-list creation request body."""
    client = MagicMock()
    client.request_json.return_value = {
        "data": {
            "id": 123,
            "organizationId": 456,
            "access": "allow",
            "isGlobal": False,
            "name": "Block Test",
            "thirdpartyCategoryId": None,
            "createdAt": 1,
            "modifiedAt": 1,
            "isMspDefault": False,
            "markedForDeletion": False,
            "bundleTypeId": 2,
        }
    }
    asset = MagicMock()
    asset.get_client.return_value = client
    params = CreateDestinationListParams(
        name=" Block Test ",
        access="allow",
        destinations_json='[{"destination":"example.com","type":"domain"}]',
    )

    output = create_destination_list(params, asset)

    assert output.destinationList.name == "Block Test"
    client.request_json.assert_called_once_with(
        scope="policies",
        end_point="destinationlists",
        operation="post",
        request_data={
            "access": "allow",
            "isGlobal": False,
            "name": "Block Test",
            "bundleTypeId": 2,
            "destinations": [{"destination": "example.com", "type": "domain"}],
        },
    )


def test_list_firewall_rules_builds_filtered_request():
    """Serialize firewall-rule filters and clamp the request limit."""
    client = MagicMock()
    client.request_json.return_value = {
        "count": 1,
        "results": [{"ruleId": 99, "ruleName": "Allow Test"}],
    }
    asset = MagicMock()
    asset.get_client.return_value = client
    params = ListFirewallRulesParams(
        offset=5,
        limit=2000,
        rule_name="Allow",
        filters='{"ruleAction":"allow"}',
    )

    output = list_firewall_rules(params, asset)

    assert output.count == 1
    assert output.firewall_rules[0].ruleId == 99
    client.request_json.assert_called_once_with(
        scope="policies",
        end_point="rules",
        operation="get",
        params={
            "offset": 5,
            "limit": 1000,
            "ruleName": "Allow",
            "filters": '{"ruleAction": "allow"}',
        },
    )


@pytest.mark.parametrize(
    ("http_method", "endpoint", "body", "parsed_body"),
    [
        ("GET", "deployments/v2/sites", None, None),
        (
            "POST",
            "deployments/v2/networkdevices",
            '{"name": "test-device"}',
            {"name": "test-device"},
        ),
        (
            "PUT",
            "admin/v2/identities",
            '[{"key": "test-device", "status": "active"}]',
            [{"key": "test-device", "status": "active"}],
        ),
    ],
)
def test_make_request_passes_supported_methods_to_client(
    http_method, endpoint, body, parsed_body
):
    """Forward supported arbitrary-request parameters to the API client."""
    response = MagicMock(status_code=200, text='{"ok": true}')
    client = MagicMock()
    client.MakeRequest.return_value = response
    asset = MagicMock()
    asset.get_client.return_value = client
    params = CiscoSecureAccessMakeRequestParams(
        http_method=http_method,
        endpoint=endpoint,
        headers='{"X-Test": "value"}',
        query_parameters='{"limit": 10}',
        timeout=15,
        verify_ssl=True,
        **({"body": body} if body is not None else {}),
    )

    output = make_request(params, asset)

    client.MakeRequest.assert_called_once_with(
        method=http_method,
        endpoint=endpoint,
        headers={"X-Test": "value"},
        query_parameters={"limit": 10},
        query_string=None,
        body=parsed_body,
        timeout=15,
        verify_ssl=True,
    )
    assert output.status_code == 200
    assert output.response_body == '{"ok": true}'


@pytest.mark.parametrize("endpoint", ["", "/", "https://example.com/path"])
def test_make_request_rejects_invalid_endpoint(endpoint):
    """Reject empty, root, and absolute endpoints before making a request."""
    asset = MagicMock()
    params = CiscoSecureAccessMakeRequestParams(http_method="GET", endpoint=endpoint)

    with pytest.raises(ActionFailure):
        make_request(params, asset)

    asset.get_client.assert_not_called()


def test_make_request_wraps_client_errors():
    """Convert client exceptions into an action failure."""
    client = MagicMock()
    client.MakeRequest.side_effect = RuntimeError("request failed")
    asset = MagicMock()
    asset.get_client.return_value = client
    params = CiscoSecureAccessMakeRequestParams(
        http_method="GET", endpoint="deployments/v2/sites"
    )

    with pytest.raises(ActionFailure, match="Request failed: request failed"):
        make_request(params, asset)


def test_create_rule_wraps_api_errors_with_readable_message():
    """Expose a structured API error message when rule creation fails."""
    response = requests.Response()
    response.status_code = 400
    response.url = "https://api.sse.cisco.com/policies/v2/rules"
    response._content = b'{"message":"Rule name must not exceed 50 characters"}'
    client = MagicMock()
    client.request_json.side_effect = requests.HTTPError(
        "400 Client Error", response=response
    )
    asset = MagicMock()
    asset.get_client.return_value = client
    params = CreateRuleParams(
        rule_name="a" * 51,
        rule_action="allow",
        rule_conditions_json="[]",
        rule_settings_json="[]",
    )

    with pytest.raises(
        ActionFailure,
        match="Failed to create rule: Rule name must not exceed 50 characters",
    ):
        create_rule(params, asset)
