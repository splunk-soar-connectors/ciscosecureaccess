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

from ..core import (
    Asset,
    MAX_LIMIT_NETWORK_TUNNEL_GROUPS,
    MAX_LIMIT_RESOURCE_CONNECTORS,
    _clamp_offset_limit,
    _output_from_api_data,
    _parse_optional_filters,
    app,
)
from ..outputs import (
    DeleteManagedDeviceOutput,
    GetNetworkDeviceOutput,
    GetNetworkTunnelGroupOutput,
    GetRoamingComputerOutput,
    ListManagedDevicesOutput,
    ListNetworkTunnelGroupsOutput,
    ListResourceConnectorsOutput,
    ListRoamingComputersOutput,
    ListSitesOutput,
    ListVirtualAppliancesOutput,
)
from ..params import (
    DeleteManagedDeviceParams,
    GetNetworkDeviceParams,
    GetNetworkTunnelGroupParams,
    GetRoamingComputerParams,
    ListNetworkTunnelGroupsParams,
    ListResourceConnectorsParams,
)


@app.action()
def list_managed_devices(params: Params, asset: Asset) -> ListManagedDevicesOutput:
    """
    List all valid IOA platforms.
    https://developer.cisco.com/docs/cloud-security/list-network-devices/
    """
    client = asset.get_client()
    devices = client.ListNetworkDevices()
    return ListManagedDevicesOutput(devices=devices)


@app.action(read_only=False)
def delete_managed_device(
    params: DeleteManagedDeviceParams, asset: Asset
) -> DeleteManagedDeviceOutput:
    """
    Remove a network device by origin ID.
    DELETE deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:write.
    https://developer.cisco.com/docs/cloud-security/delete-network-device/
    """
    client = asset.get_client()
    data = client.DeleteNetworkDevice(params.origin_id)
    return DeleteManagedDeviceOutput(
        success=data.get("success", True), message=data.get("message")
    )


@app.action()
def get_network_device(
    params: GetNetworkDeviceParams, asset: Asset
) -> GetNetworkDeviceOutput:
    """
    Get a network device by origin ID.
    GET deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:read.
    https://developer.cisco.com/docs/cloud-security/get-network-device/
    """
    client = asset.get_client()
    data = client.GetNetworkDevice(params.origin_id)
    return _output_from_api_data(GetNetworkDeviceOutput, data)


@app.action()
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


@app.action()
def list_sites(params: Params, asset: Asset) -> ListSitesOutput:
    """
    List all Sites in the organization.
    GET deployments/v2/sites. Requires deployments.sites:read.
    https://developer.cisco.com/docs/cloud-security/list-sites/
    """
    client = asset.get_client()
    sites = client.ListSites()
    if not isinstance(sites, list):
        sites = [sites] if sites is not None else []
    return ListSitesOutput(sites=sites)


@app.action()
def get_roaming_computer(
    params: GetRoamingComputerParams, asset: Asset
) -> GetRoamingComputerOutput:
    """
    Get Roaming Computer (posture/security status for a device).
    GET /roamingcomputers/{deviceId}. Returns status, swgStatus, lastSync, appliedBundle, version, OS info, etc.
    https://developer.cisco.com/docs/cloud-security/get-roaming-computer/
    """
    client = asset.get_client()
    data = client.GetRoamingComputer(params.device_id)
    return _output_from_api_data(GetRoamingComputerOutput, data)


@app.action()
def list_roaming_computers(params: Params, asset: Asset) -> ListRoamingComputersOutput:
    """
    List all roaming computers.
    GET /roamingcomputers. Returns roaming computers (posture/security status) in the organization.
    https://developer.cisco.com/docs/cloud-security/list-roaming-computers/
    """
    client = asset.get_client()
    data = client.ListRoamingComputers()
    if not isinstance(data, list):
        data = []
    return ListRoamingComputersOutput(roamingComputers=data)


@app.action()
def list_network_tunnel_groups(
    params: ListNetworkTunnelGroupsParams, asset: Asset
) -> ListNetworkTunnelGroupsOutput:
    """
    List Network Tunnel Groups in the organization.
    GET deployments/v2/networktunnelgroups. Requires deployments.networktunnelgroups:read.
    https://developer.cisco.com/docs/cloud-security/list-network-tunnel-groups/
    """
    client = asset.get_client()
    filters_obj = _parse_optional_filters(params)
    offset, limit = _clamp_offset_limit(params, MAX_LIMIT_NETWORK_TUNNEL_GROUPS)
    data = client.ListNetworkTunnelGroups(
        offset=offset,
        limit=limit,
        filters=filters_obj,
        sort_by=getattr(params, "sort_by", "name"),
        sort_order=getattr(params, "sort_order", "asc"),
        include_statuses=getattr(params, "include_statuses", False),
    )
    return ListNetworkTunnelGroupsOutput(
        data=data.get("data"),
        offset=data.get("offset"),
        limit=data.get("limit"),
        total=data.get("total"),
    )


@app.action()
def get_network_tunnel_group(
    params: GetNetworkTunnelGroupParams, asset: Asset
) -> GetNetworkTunnelGroupOutput:
    """
    Get a Network Tunnel Group by ID.
    GET deployments/v2/networktunnelgroups/{id}. Requires deployments.networktunnelgroups:read.
    https://developer.cisco.com/docs/cloud-security/get-network-tunnel-group/
    """
    client = asset.get_client()
    data = client.GetNetworkTunnelGroup(params.id)
    return _output_from_api_data(GetNetworkTunnelGroupOutput, data)


@app.action()
def list_resource_connectors(
    params: ListResourceConnectorsParams, asset: Asset
) -> ListResourceConnectorsOutput:
    """
    List Resource Connectors for the organization.
    GET deployments/v2/connectorAgents. Requires deployments.resourceconnectors:read.
    https://developer.cisco.com/docs/cloud-security/list-connectors/
    """
    client = asset.get_client()
    filters_obj = _parse_optional_filters(params)
    offset, limit = _clamp_offset_limit(params, MAX_LIMIT_RESOURCE_CONNECTORS)
    data = client.ListResourceConnectors(
        offset=offset,
        limit=limit,
        filters=filters_obj,
        sort_by=getattr(params, "sort_by", "originIpAddress"),
        sort_order=getattr(params, "sort_order", "asc"),
    )
    return ListResourceConnectorsOutput(
        data=data.get("data"),
        offset=data.get("offset"),
        limit=data.get("limit"),
        total=data.get("total"),
    )
