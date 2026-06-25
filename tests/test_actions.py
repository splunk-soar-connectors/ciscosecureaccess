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

from src.actions.domains import get_passive_dns
from src.actions.make_request import make_request
from src.actions.rules import create_rule
from src.params import (
    CiscoSecureAccessMakeRequestParams,
    CreateRuleParams,
    GetPassiveDNSParams,
)


def test_get_passive_dns_maps_pagination_output():
    client = MagicMock()
    client.GetPassiveDNS.return_value = (
        [{"name": "example.com", "type": "A", "rr": "192.0.2.1"}],
        {
            "offset": 10,
            "limit": 1,
            "totalNumRecords": 12,
            "hasMoreRecords": True,
        },
    )
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
    asset = MagicMock()
    params = CiscoSecureAccessMakeRequestParams(http_method="GET", endpoint=endpoint)

    with pytest.raises(ActionFailure):
        make_request(params, asset)

    asset.get_client.assert_not_called()


def test_make_request_wraps_client_errors():
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
    response = requests.Response()
    response.status_code = 400
    response.url = "https://api.sse.cisco.com/policies/v2/rules"
    response._content = b'{"message":"Rule name must not exceed 50 characters"}'
    client = MagicMock()
    client.CreateRule.side_effect = requests.HTTPError(
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
