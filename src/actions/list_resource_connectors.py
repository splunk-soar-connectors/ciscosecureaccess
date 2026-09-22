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
from ..constants import MAX_LIMIT_RESOURCE_CONNECTORS
from ..input_helpers import _clamp_offset_limit, _parse_optional_filters
from ..outputs import ListResourceConnectorsOutput
from ..params import ListResourceConnectorsParams
from ..response_handling import require_mapping
from ..sse_api_client import GET, _encode_filters, deployments


def list_resource_connectors(
    params: ListResourceConnectorsParams, asset: Asset
) -> ListResourceConnectorsOutput:
    """
    List Resource Connectors for the organization.
    GET deployments/v2/connectorAgents. Requires deployments.resourceconnectors:read.
    https://developer.cisco.com/docs/cloud-security/list-connectors/
    """
    client = asset.get_client()
    filters_obj = _parse_optional_filters(params)
    offset, limit = _clamp_offset_limit(params, MAX_LIMIT_RESOURCE_CONNECTORS)
    request_params = {
        "offset": offset,
        "limit": limit,
        "sortBy": getattr(params, "sort_by", "originIpAddress"),
        "sortOrder": getattr(params, "sort_order", "asc"),
    }
    if filters_obj is not None:
        request_params["filters"] = _encode_filters(filters_obj)
    data = client.request_json(
        scope=deployments,
        end_point="connectorAgents",
        operation=GET,
        params=request_params,
    )
    data = require_mapping(data, "list resource connectors response")
    return ListResourceConnectorsOutput(
        data=data.get("data"),
        offset=data.get("offset"),
        limit=data.get("limit"),
        total=data.get("total"),
    )
