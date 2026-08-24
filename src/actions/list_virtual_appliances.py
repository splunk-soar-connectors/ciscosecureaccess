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

from soar_sdk.params import Params

from ..core import Asset
from ..outputs import ListVirtualAppliancesOutput


def list_virtual_appliances(
    params: Params, asset: Asset
) -> ListVirtualAppliancesOutput:
    """
    List all virtual appliances.
    https://developer.cisco.com/docs/cloud-security/list-virtual-appliances/
    """
    client = asset.get_client()
    virtual_appliances = client.ListVirtualAppliances()
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
