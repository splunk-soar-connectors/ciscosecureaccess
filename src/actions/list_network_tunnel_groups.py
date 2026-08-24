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
from ..sse_api_client import GET, _encode_filters, deployments


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
    request_params = {
        "offset": offset,
        "limit": limit,
        "sortBy": getattr(params, "sort_by", "name"),
        "sortOrder": getattr(params, "sort_order", "asc"),
        "includeStatuses": "true"
        if getattr(params, "include_statuses", False)
        else "false",
    }
    if filters_obj is not None:
        request_params["filters"] = _encode_filters(filters_obj)
    data = client.request_json(
        scope=deployments,
        end_point="networktunnelgroups",
        operation=GET,
        params=request_params,
    )
    return ListNetworkTunnelGroupsOutput(
        data=data.get("data"),
        offset=data.get("offset"),
        limit=data.get("limit"),
        total=data.get("total"),
    )
