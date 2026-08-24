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

from ..core import Asset, _destinations_for_create_destination_list, flatten_field
from ..outputs import CreateDestinationListOutput
from ..params import CreateDestinationListParams
from ..sse_api_client import POST, policies


def create_destination_list(
    params: CreateDestinationListParams, asset: Asset
) -> CreateDestinationListOutput:
    """
    Create a destination list in the organization (optional initial destinations).
    POST policies/v2/destinationlists. Requires policies.destinationLists:write.
    Secure Access does not support global destination lists on create; the request always sets isGlobal to false.
    https://developer.cisco.com/docs/cloud-security/create-destination-list/
    """
    name = params.name.strip()
    if not name:
        raise ValueError("name must be a non-empty string")

    destinations = _destinations_for_create_destination_list(params.destinations_json)
    body: dict = {
        "access": params.access,
        "isGlobal": False,
        "name": name,
        "bundleTypeId": 2,
    }
    if destinations:
        body["destinations"] = destinations

    client = asset.get_client()
    raw = client.request_json(
        scope=policies,
        end_point="destinationlists",
        operation=POST,
        request_data=body,
    )
    if not isinstance(raw, dict):
        raise ValueError("Unexpected API response for create destination list")
    data = raw.get("data", raw)
    if not isinstance(data, dict):
        raise ValueError("Unexpected API response data for create destination list")
    if data.get("meta") is not None:
        data = flatten_field([data], "meta")[0]
    return CreateDestinationListOutput(destinationList=data)
