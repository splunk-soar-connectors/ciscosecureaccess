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

from ..core import Asset, _output_from_api_data
from ..outputs import GetNetworkTunnelGroupOutput
from ..params import GetNetworkTunnelGroupParams


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
