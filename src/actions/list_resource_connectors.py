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
    MAX_LIMIT_RESOURCE_CONNECTORS,
    _clamp_offset_limit,
    _parse_optional_filters,
)
from ..outputs import ListResourceConnectorsOutput
from ..params import ListResourceConnectorsParams


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
    data = client.ListResourceConnectors(
        offset=offset,
        limit=limit,
        filters=filters_obj,
        sort_by=getattr(params, "sort_by", "originIpAddress"),
        sort_order=getattr(params, "sort_order", "asc"),
    )
    return ListResourceConnectorsOutput(
        data=data.get("data"),
        offset=data.get("offset"),
        limit=data.get("limit"),
        total=data.get("total"),
    )
