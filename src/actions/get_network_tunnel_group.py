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
from .list_network_tunnel_groups import NetworkTunnelGroupHub, NetworkTunnelGroupRouting


class GetNetworkTunnelGroupParams(Params):
    """Parameters for Get Network Tunnel Group. GET deployments/v2/networktunnelgroups/{id}. Requires deployments.networktunnelgroups:read."""

    id: int = Param(
        required=True,
        description="ID of the network tunnel group (obtain from the List Network Tunnel Groups action).",
    )


class GetNetworkTunnelGroupOutput(ActionOutput):
    """Response from Get Network Tunnel Group API (GET deployments/v2/networktunnelgroups/{id}). Same shape as NetworkTunnelGroup."""

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


def get_network_tunnel_group(
    params: GetNetworkTunnelGroupParams, asset: Asset
) -> GetNetworkTunnelGroupOutput:
    """
    Get a Network Tunnel Group by ID.
    GET deployments/v2/networktunnelgroups/{id}. Requires deployments.networktunnelgroups:read.
    https://developer.cisco.com/docs/cloud-security/get-network-tunnel-group/
    """
    client = asset.get_client()
    data = client.request_json(
        scope=deployments,
        end_point=f"networktunnelgroups/{params.id}",
        operation=GET,
    )
    data = require_mapping(data, "GetNetworkTunnelGroupOutput output")
    return GetNetworkTunnelGroupOutput(**data)
