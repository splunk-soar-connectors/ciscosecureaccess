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
from soar_sdk.params import Params

from ..asset import Asset
from ..sse_api_client import GET, deployments


class RoamingComputer(ActionOutput):
    """Roaming computer from Get/List Roaming Computers. Required per schema: originId, name, deviceId, type, status, swgStatus, lastSyncStatus, lastSyncSwgStatus, lastSync, appliedBundle, hasIpBlocking, version, osVersion, osVersionName."""

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


class ListRoamingComputersOutput(ActionOutput):
    roamingComputers: list[RoamingComputer]


def list_roaming_computers(params: Params, asset: Asset) -> ListRoamingComputersOutput:
    """
    List all roaming computers.
    GET /roamingcomputers. Returns roaming computers (posture/security status) in the organization.
    https://developer.cisco.com/docs/cloud-security/list-roaming-computers/
    """
    client = asset.get_client()
    result = client.query_all_pages(
        scope=deployments,
        end_point="roamingcomputers",
        operation=GET,
        limit=100,
        response_is_array=True,
    )
    data = result["data"]
    if not isinstance(data, list):
        data = []
    return ListRoamingComputersOutput(roamingComputers=data)
