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


class GetRoamingComputerParams(Params):
    device_id: str = Param(
        required=True,
        description="The device ID (deviceId) of the roaming computer, e.g. AB00C7DCEC99D211.",
    )


class GetRoamingComputerOutput(ActionOutput):
    """Posture/security status for a roaming computer (Get Roaming Computer API). Same required fields as RoamingComputer."""

    originId: int
    name: str
    deviceId: str
    type: str
    status: str
    swgStatus: str
    lastSyncStatus: str
    lastSyncSwgStatus: str
    lastSync: str
    appliedBundle: int
    hasIpBlocking: bool
    version: str
    osVersion: str
    osVersionName: str
    anyconnectDeviceId: str | None = None


def get_roaming_computer(
    params: GetRoamingComputerParams, asset: Asset
) -> GetRoamingComputerOutput:
    """
    Get Roaming Computer (posture/security status for a device).
    GET /roamingcomputers/{deviceId}. Returns status, swgStatus, lastSync, appliedBundle, version, OS info, etc.
    https://developer.cisco.com/docs/cloud-security/get-roaming-computer/
    """
    client = asset.get_client()
    data = client.request_json(
        scope=deployments,
        end_point=f"roamingcomputers/{params.device_id}",
        operation=GET,
    )
    data = require_mapping(data, "GetRoamingComputerOutput output")
    return GetRoamingComputerOutput(**data)
