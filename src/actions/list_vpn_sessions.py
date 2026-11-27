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
from ..sse_api_client import GET, admin


class VPNSession(ActionOutput):
    username: str | None = None
    deviceName: str | None = None
    assignedIp: str | None = None  # RFC 1918 IPv4 assigned to the VPN connection
    assignedIpv6: str | None = None  # IPv6 assigned to the VPN session
    publicIp: str | None = None
    sessionId: str | None = None
    loginTime: str | None = None
    profileName: str | None = None


class ListVPNSessionsOutput(ActionOutput):
    vpn_sessions: list[VPNSession]


def list_vpn_sessions(params: Params, asset: Asset) -> ListVPNSessionsOutput:
    """
    List VPN Sessions.
    https://developer.cisco.com/docs/cloud-security/list-vpn-connections/
    """
    client = asset.get_client()
    result = client.query_all_pages_offset(
        scope=admin,
        end_point="vpn/userConnections",
        operation=GET,
        limit=1000,
    )
    vpn_sessions = result["data"]
    return ListVPNSessionsOutput(vpn_sessions=vpn_sessions)
