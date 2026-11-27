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
from ..constants import (
    _DESTINATION_CREATE_TYPES,
    MAX_DESTINATIONS_CREATE_DESTINATION_LIST,
)
from ..destination_helpers import flatten_field
from ..input_helpers import _parse_json_param
from ..sse_api_client import POST, policies
from .list_destination_lists import DestinationList

DESTINATION_LIST_ACCESS_VALUES = [
    "allow",
    "block",
    "url_proxy",
    "no_decrypt",
    "warn",
    "none",
    "thirdparty_block",
]


class CreateDestinationListParams(Params):
    """Parameters for Create Destination List. POST policies/v2/destinationlists. Requires policies.destinationLists:write."""

    name: str = Param(
        required=True,
        description="Name of the destination list.",
    )
    access: str = Param(
        required=True,
        description="Access classification for the list (used with access rules). Cannot create lists with access type thirdparty_block via this API.",
        value_list=DESTINATION_LIST_ACCESS_VALUES,
    )
    destinations_json: str = Param(
        required=False,
        description='Optional JSON array of up to 500 destinations, e.g. [{"destination":"cisco.com","type":"domain","comment":"optional"}]. type: domain, url, or ipv4.',
    )


class CreateDestinationListOutput(ActionOutput):
    """Response data from Create Destination List (POST policies/v2/destinationlists)."""

    destinationList: DestinationList


def _destinations_for_create_destination_list(
    destinations_json: str | None,
) -> list[dict] | None:
    """Parse and validate optional destination-list entries for an API request."""
    if destinations_json is None or not str(destinations_json).strip():
        return None
    parsed = _parse_json_param(
        str(destinations_json).strip(), "destinations_json", allow_list=True
    )
    if len(parsed) > MAX_DESTINATIONS_CREATE_DESTINATION_LIST:
        raise ValueError(
            f"destinations_json must contain at most "
            f"{MAX_DESTINATIONS_CREATE_DESTINATION_LIST} destinations"
        )
    out: list[dict] = []
    for i, item in enumerate(parsed):
        if not isinstance(item, dict):
            raise ValueError(f"destinations_json[{i}] must be a JSON object")
        dest = item.get("destination")
        typ = item.get("type")
        if dest is None or typ is None:
            raise ValueError(
                f"destinations_json[{i}] must include destination and type fields"
            )
        dest_s = str(dest).strip()
        typ_s = str(typ).strip()
        if not dest_s:
            raise ValueError(f"destinations_json[{i}] destination must be non-empty")
        if typ_s not in _DESTINATION_CREATE_TYPES:
            raise ValueError(
                f"destinations_json[{i}] type must be one of: "
                f"{', '.join(sorted(_DESTINATION_CREATE_TYPES))}"
            )
        row: dict = {"destination": dest_s, "type": typ_s}
        if item.get("comment") is not None:
            row["comment"] = str(item["comment"])
        out.append(row)
    return out


def create_destination_list(
    params: CreateDestinationListParams, asset: Asset
) -> CreateDestinationListOutput:
    """
    Create a destination list in the organization (optional initial destinations).
    POST policies/v2/destinationlists. Requires policies.destinationLists:write.
    Secure Access does not support global destination lists on create; the request always sets isGlobal to false.
    https://developer.cisco.com/docs/cloud-security/create-destination-list/
    """
    name = params.name.strip()
    if not name:
        raise ValueError("name must be a non-empty string")

    destinations = _destinations_for_create_destination_list(params.destinations_json)
    body: dict = {
        "access": params.access,
        "isGlobal": False,
        "name": name,
        "bundleTypeId": 2,
    }
    if destinations:
        body["destinations"] = destinations

    client = asset.get_client()
    raw = client.request_json(
        scope=policies,
        end_point="destinationlists",
        operation=POST,
        request_data=body,
    )
    if not isinstance(raw, dict):
        raise ValueError("Unexpected API response for create destination list")
    data = raw.get("data", raw)
    if not isinstance(data, dict):
        raise ValueError("Unexpected API response data for create destination list")
    if data.get("meta") is not None:
        data = flatten_field([data], "meta")[0]
    return CreateDestinationListOutput(destinationList=data)
