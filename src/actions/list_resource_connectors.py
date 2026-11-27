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
from ..constants import MAX_LIMIT_RESOURCE_CONNECTORS
from ..input_helpers import _clamp_offset_limit, _parse_optional_filters
from ..response_handling import require_mapping
from ..sse_api_client import GET, _encode_filters, deployments


class ListResourceConnectorsParams(Params):
    """Parameters for List Resource Connectors. GET deployments/v2/connectorAgents. Requires deployments.resourceconnectors:read."""

    offset: int = Param(
        required=False,
        default=0,
        description="Index to start reading the collection (0-based). Default 0.",
    )
    limit: int = Param(
        required=False,
        default=10,
        description="Maximum number of items to return. Default 10.",
    )
    filters: str = Param(
        required=False,
        description="Optional JSON object to filter by groupId, instanceId, status, confirmed, hasSynced, hasLatestVersion. See API docs.",
    )
    sort_by: str = Param(
        required=False,
        default="originIpAddress",
        description="Sort field: instanceId, originIpAddress, createdAt, modifiedAt.",
        value_list=["instanceId", "originIpAddress", "createdAt", "modifiedAt"],
    )
    sort_order: str = Param(
        required=False,
        default="asc",
        description="Sort order: asc or desc.",
        value_list=["asc", "desc"],
    )


class ResourceConnector(ActionOutput):
    """Resource Connector from List Connectors API (deployments/v2/connectorAgents)."""

    id: int | None = None
    groupId: int | None = None
    instanceId: str | None = None
    confirmed: bool | None = None
    enabled: bool | None = None
    version: str | None = None
    sha1: str | None = None
    hostname: str | None = None
    originIpAddress: str | None = None
    baseVersion: str | None = None
    isLatestBaseVersion: bool | None = None
    upgradeStatus: str | None = None
    status: str | None = None
    statusUpdatedAt: str | None = None
    controlStatusUpdatedAt: str | None = None
    revoked_at: str | None = None
    createdAt: str | None = None
    modifiedAt: str | None = None


class ListResourceConnectorsOutput(ActionOutput):
    data: list[ResourceConnector] | None = None
    offset: int | None = None
    limit: int | None = None
    total: int | None = None


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
