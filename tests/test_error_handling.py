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

from src.actions.make_request import make_request
from src.asset import test_connectivity as run_connectivity_test
from src.error_handling import format_action_error, format_api_error
from src.params import CiscoSecureAccessMakeRequestParams


def test_format_api_error_uses_api_message():
    """Prefer a structured API message when formatting an HTTP error."""
    response = requests.Response()
    response.status_code = 400
    response._content = b'{"message":"Invalid rule"}'
    error = requests.HTTPError("400 Client Error", response=response)

    assert format_api_error(error) == "Invalid rule"
    assert (
        format_action_error("Request failed", error) == "Request failed: Invalid rule"
    )


def test_format_api_error_preserves_generic_message():
    """Preserve a generic exception message when no API detail exists."""
    error = ValueError("connection failed")

    message = format_api_error(error)

    assert message == "connection failed"


def test_connectivity_converts_client_errors_to_action_failure():
    """Convert connectivity client errors into action failures."""
    client = MagicMock()
    client.GetToken.side_effect = RuntimeError("authentication failed")
    asset = MagicMock()
    asset.get_client.return_value = client

    with pytest.raises(
        ActionFailure, match="Connectivity test failed: authentication failed"
    ):
        run_connectivity_test(asset)


def test_connectivity_rejects_empty_token():
    """Reject connectivity checks that return an empty token."""
    client = MagicMock()
    client.GetToken.return_value = None
    asset = MagicMock()
    asset.get_client.return_value = client

    with pytest.raises(ActionFailure, match="Unable to get auth token"):
        run_connectivity_test(asset)


def test_make_request_does_not_echo_invalid_body():
    """Avoid exposing invalid request-body contents in the error message."""
    params = CiscoSecureAccessMakeRequestParams(
        http_method="POST",
        endpoint="policies/v2/rules",
        body='{"client_secret":',
    )

    with pytest.raises(
        ActionFailure, match="Invalid JSON in the body parameter"
    ) as error:
        make_request(params, MagicMock())

    assert "client_secret" not in str(error.value)
