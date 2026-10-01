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

from ..asset import Asset
from ..constants import MAX_IDENTITIES_UPDATE
from ..input_helpers import _parse_json_param
from ..outputs import UpdateIdentitiesOutput
from ..params import UpdateIdentitiesParams
from ..response_handling import require_mapping
from ..sse_api_client import PUT, deployments


def update_identities(
    params: UpdateIdentitiesParams, asset: Asset
) -> UpdateIdentitiesOutput:
    """
    Update Identities (devices or security group tags).
    PUT /identities/registrations/{type}. Pass 1-250 identity objects as JSON array in identities_json.
    https://developer.cisco.com/docs/cloud-security/update-identities/
    """
    client = asset.get_client()
    identity_type = params.type.strip().lower()
    if identity_type not in ("device", "securitygrouptag"):
        raise ValueError("type must be 'device' or 'securityGroupTag'")
    if identity_type == "securitygrouptag":
        identity_type = "securityGroupTag"
    identities_list = _parse_json_param(
        params.identities_json, "identities_json", allow_list=True
    )
    if len(identities_list) < 1 or len(identities_list) > MAX_IDENTITIES_UPDATE:
        raise ValueError("identities_json must contain 1-250 items")
    data = client.request_json(
        scope=deployments,
        end_point=f"identities/registrations/{identity_type}",
        operation=PUT,
        request_data=identities_list,
    )
    return UpdateIdentitiesOutput(
        success=require_mapping(data, "update identities response").get("success")
    )
