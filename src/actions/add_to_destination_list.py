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
from ..destination_helpers import flatten_field
from ..sse_api_client import GET, POST, policies
from .list_destination_lists import DestinationList


class AddToDestinationListParams(Params):
    destination_list_id: int = Param(
        required=False,
        description="Destination List ID. If not provided, the default destination list ID will be used.",
    )
    destination: str = Param(
        required=True, description="Destination URL, domain, or IP address"
    )
    comment: str = Param(required=False, description="Comment for the destination")


class AddToDestinationListOutput(ActionOutput):
    addedDestinationId: str | None = None
    destinationList: DestinationList


def _normalize_destination_for_match(value: str) -> str:
    """Normalize a destination value for case-insensitive matching."""
    return (value or "").strip().lower()


def _find_added_destination_row(
    rows: list,
    *,
    destination: str,
    comment: str | None,
) -> dict | None:
    """Find the newly added destination row by destination and optional comment."""
    if not isinstance(rows, list) or not rows:
        return None
    want = _normalize_destination_for_match(destination)
    matches_dest: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if _normalize_destination_for_match(str(row.get("destination") or "")) != want:
            continue
        matches_dest.append(row)
    if not matches_dest:
        return None
    if comment is not None:
        with_comment = [r for r in matches_dest if (r.get("comment") or "") == comment]
        if with_comment:
            matches_dest = with_comment

    return sorted(
        matches_dest, key=lambda row: str(row.get("createdAt") or ""), reverse=True
    )[0]


def add_to_destination_list(
    params: AddToDestinationListParams, asset: Asset
) -> AddToDestinationListOutput:
    """
    Add to Destination List (one destination and optional comment per run).
    https://developer.cisco.com/docs/cloud-security/add-destinations-to-destination-list/
    """
    client = asset.get_client()
    destination_list_id = (
        params.destination_list_id
        if params.destination_list_id
        else asset.default_destination_list_id
    )
    if not destination_list_id:
        raise ValueError("Destination list ID is required")
    obj = {"destination": params.destination}
    if params.comment is not None:
        obj["comment"] = params.comment
    destination_list_response = client.request_json(
        scope=policies,
        end_point=f"destinationlists/{destination_list_id}/destinations",
        operation=POST,
        request_data=[obj],
    )
    destination_list = destination_list_response["data"]
    if isinstance(destination_list, dict) and destination_list.get("meta") is not None:
        destination_list = flatten_field([destination_list], "meta")[0]
    added_id = None
    destinations_response = client.query_all_pages(
        scope=policies,
        end_point=f"destinationlists/{destination_list_id}/destinations",
        operation=GET,
    )
    raw_destinations = destinations_response["data"]
    dest_rows = raw_destinations if isinstance(raw_destinations, list) else []
    added_row = _find_added_destination_row(
        dest_rows,
        destination=params.destination,
        comment=params.comment,
    )
    if added_row and added_row.get("id") is not None:
        added_id = str(added_row["id"])
        destination_list = {**destination_list, "destinations": [added_row]}
    return AddToDestinationListOutput(
        addedDestinationId=added_id, destinationList=destination_list
    )
