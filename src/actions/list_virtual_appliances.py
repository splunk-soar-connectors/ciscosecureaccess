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


class VirtualAppliance(ActionOutput):
    originId: int
    name: str
    isUpgradable: bool
    health: str
    type: str
    stateUpdatedAt: str
    siteId: int | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None
    # Flattened from API's `state` object
    state_syncing: str | None = None
    # Flattened from API's `settings` object
    internalIPs: list[str] | None = None
    externalIP: str | None = None
    hostType: str | None = None
    uptime: int | None = None
    version: str | None = None
    domains: list[str] | None = None
    lastSyncTime: str | None = None


class ListVirtualAppliancesOutput(ActionOutput):
    virtualAppliances: list[VirtualAppliance]


def list_virtual_appliances(
    params: Params, asset: Asset
) -> ListVirtualAppliancesOutput:
    """
    List all virtual appliances.
    https://developer.cisco.com/docs/cloud-security/list-virtual-appliances/
    """
    client = asset.get_client()
    result = client.query_all_pages(
        scope=deployments,
        end_point="virtualappliances",
        operation=GET,
        limit=100,
        response_is_array=True,
    )
    virtual_appliances = result["data"]
    for appliance in virtual_appliances or []:
        state = appliance.get("state")
        if isinstance(state, dict):
            appliance["state_syncing"] = state.get("syncing")
            appliance.pop("state", None)

        settings = appliance.get("settings")
        if isinstance(settings, dict):
            appliance["internalIPs"] = settings.get("internalIPs")
            appliance["externalIP"] = settings.get("externalIP")
            appliance["hostType"] = settings.get("hostType")
            appliance["uptime"] = settings.get("uptime")
            appliance["version"] = settings.get("version")
            appliance["domains"] = settings.get("domains")
            appliance["lastSyncTime"] = settings.get("lastSyncTime")
            appliance.pop("settings", None)
    return ListVirtualAppliancesOutput(virtualAppliances=virtual_appliances)
