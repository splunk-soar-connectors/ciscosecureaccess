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

from ..core import Asset
from ..outputs import ListIdentitiesOutput
from ..params import ListIdentitiesParams
from ..sse_api_client import GET, deployments


def list_identities(params: ListIdentitiesParams, asset: Asset) -> ListIdentitiesOutput:
    """
    List Identities.
    https://developer.cisco.com/docs/cloud-security/list-identities/
    """
    client = asset.get_client()
    result = client.request_all_offset_pages(
        scope=deployments,
        end_point=f"identities/registrations/{params.type}",
        operation=GET,
        limit=250,
    )
    identities = result["data"]
    return ListIdentitiesOutput(identities=identities)
