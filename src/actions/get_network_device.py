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

from soar_sdk.action_results import ActionOutput
from soar_sdk.params import Param, Params

from ..asset import Asset
from ..response_handling import require_mapping
from ..sse_api_client import GET, deployments


class GetNetworkDeviceParams(Params):
    """Parameters for Get Network Device. GET deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:read."""

    origin_id: int = Param(
        required=True,
        description="Origin ID of the network device (obtain from the List Managed Devices action).",
    )


class GetNetworkDeviceOutput(ActionOutput):
    """Response from Get Network Device API (GET deployments/v2/networkdevices/{originId}). Same shape as ManagedDevice."""

    originId: int
    deviceId: str
    deviceKey: str
    name: str
    serialNumber: str
    createdAt: str
    organizationId: int


def get_network_device(
    params: GetNetworkDeviceParams, asset: Asset
) -> GetNetworkDeviceOutput:
    """
    Get a network device by origin ID.
    GET deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:read.
    https://developer.cisco.com/docs/cloud-security/get-network-device/
    """
    client = asset.get_client()
    data = client.request_json(
        scope=deployments,
        end_point=f"networkdevices/{params.origin_id}",
        operation=GET,
    )
    data = require_mapping(data, "GetNetworkDeviceOutput output")
    return GetNetworkDeviceOutput(**data)
