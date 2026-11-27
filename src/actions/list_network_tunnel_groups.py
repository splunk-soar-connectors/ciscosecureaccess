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
from ..constants import MAX_LIMIT_NETWORK_TUNNEL_GROUPS
from ..input_helpers import _clamp_offset_limit, _parse_optional_filters
from ..response_handling import require_mapping
from ..sse_api_client import GET, _encode_filters, deployments


class ListNetworkTunnelGroupsParams(Params):
    """Parameters for List Network Tunnel Groups. GET deployments/v2/networktunnelgroups. Requires deployments.networktunnelgroups:read."""

    offset: int = Param(
        required=False,
        default=0,
        description="Index to start reading the collection (0-based). Default 0.",
    )
    limit: int = Param(
        required=False,
        default=10,
        description="Number of records per page (1-200). Default 10.",
    )
    filters: str = Param(
        required=False,
        description="Optional JSON object to filter by name, exactName, region, networkTunnelGroupIds, exactAuthIdPrefix, status, or duplicateCIDRs. See API docs.",
    )
    sort_by: str = Param(
        required=False,
        default="name",
        description="Sort field: name, status, createdAt, modifiedAt.",
        value_list=["name", "status", "createdAt", "modifiedAt"],
    )
    sort_order: str = Param(
        required=False,
        default="asc",
        description="Sort order: asc or desc.",
        value_list=["asc", "desc"],
    )
    include_statuses: bool = Param(
        required=False,
        default=False,
        description="Include tunnelsStatus for each hub (max 10 tunnel states per hub).",
    )


class NetworkTunnelGroupHubStatus(ActionOutput):
    """Hub status from API. Required per schema: time, status."""

    time: str
    status: str


class NetworkTunnelGroupHub(ActionOutput):
    """Single hub entry in a network tunnel group (SDK requires typed output, not raw list)."""

    id: int | None = None
    name: str | None = None
    status: NetworkTunnelGroupHubStatus | None = None  # API returns object, not string


class NetworkTunnelGroupRouting(ActionOutput):
    """Routing config for a network tunnel group (SDK requires typed output, not raw dict)."""

    type: str | None = None


class NetworkTunnelGroup(ActionOutput):
    """Network Tunnel Group from List Network Tunnel Groups API (deployments/v2/networktunnelgroups)."""

    id: int | None = None
    name: str | None = None
    organizationId: int | None = None
    deviceType: str | None = None
    region: str | None = None
    status: str | None = None
    hubs: list[NetworkTunnelGroupHub] | None = None
    routing: NetworkTunnelGroupRouting | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None


class ListNetworkTunnelGroupsOutput(ActionOutput):
    data: list[NetworkTunnelGroup] | None = None
    offset: int | None = None
    limit: int | None = None
    total: int | None = None


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
    data = require_mapping(data, "list network tunnel groups response")
    return ListNetworkTunnelGroupsOutput(
        data=data.get("data"),
        offset=data.get("offset"),
        limit=data.get("limit"),
        total=data.get("total"),
    )
