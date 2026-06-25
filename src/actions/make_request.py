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

from soar_sdk.action_results import MakeRequestOutput
from soar_sdk.exceptions import ActionFailure

from ..core import (
    Asset,
    _parse_make_request_body,
    _parse_make_request_json_object,
    _parse_make_request_query_parameters,
    app,
)
from ..params import CiscoSecureAccessMakeRequestParams


@app.make_request()
def make_request(
    params: CiscoSecureAccessMakeRequestParams, asset: Asset
) -> MakeRequestOutput:
    """Make an HTTP request to any Cisco Secure Access API endpoint using the configured asset credentials."""
    endpoint = params.endpoint.strip()
    if endpoint.lower().startswith(("http://", "https://")):
        raise ActionFailure(
            "Do not include the base URL in the endpoint. "
            "Only the API path is needed, e.g. 'deployments/v2/networkdevices'."
        )
    if not endpoint.strip("/"):
        raise ActionFailure("The endpoint parameter must contain an API path.")

    headers = _parse_make_request_json_object(params.headers, "headers")
    query_parameters, query_string = _parse_make_request_query_parameters(
        params.query_parameters
    )
    body = _parse_make_request_body(params.body)

    client = asset.get_client()
    try:
        response = client.MakeRequest(
            method=params.http_method,
            endpoint=endpoint,
            headers=headers,
            query_parameters=query_parameters,
            query_string=query_string,
            body=body,
            timeout=params.timeout,
            verify_ssl=params.verify_ssl,
        )
    except Exception as exc:
        raise ActionFailure(f"Request failed: {exc}") from exc

    return MakeRequestOutput(
        status_code=response.status_code,
        response_body=response.text,
    )
