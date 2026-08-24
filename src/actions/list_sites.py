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
from ..outputs import ListSitesOutput
from ..sse_api_client import GET, deployments


def list_sites(params: Params, asset: Asset) -> ListSitesOutput:
    """
    List all Sites in the organization.
    GET deployments/v2/sites. Requires deployments.sites:read.
    https://developer.cisco.com/docs/cloud-security/list-sites/
    """
    client = asset.get_client()
    result = client.request_all_pages(
        scope=deployments,
        end_point="sites",
        operation=GET,
        limit=100,
        response_is_array=True,
    )
    sites = result["data"]
    if not isinstance(sites, list):
        sites = [sites] if sites is not None else []
    return ListSitesOutput(sites=sites)
