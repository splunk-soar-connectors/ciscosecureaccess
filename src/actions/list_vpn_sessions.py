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
from ..outputs import ListVPNSessionsOutput


def list_vpn_sessions(params: Params, asset: Asset) -> ListVPNSessionsOutput:
    """
    List VPN Sessions.
    https://developer.cisco.com/docs/cloud-security/list-vpn-connections/
    """
    client = asset.get_client()
    vpn_sessions = client.ListVPNSessions()
    return ListVPNSessionsOutput(vpn_sessions=vpn_sessions)
