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

from ..core import (
    Asset,
    MAX_LIMIT_NETWORK_TUNNEL_GROUPS,
    _clamp_offset_limit,
    _parse_optional_filters,
)
from ..outputs import ListNetworkTunnelGroupsOutput
from ..params import ListNetworkTunnelGroupsParams


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
