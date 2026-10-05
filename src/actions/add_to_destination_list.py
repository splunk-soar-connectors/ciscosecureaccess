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
from ..destination_helpers import _find_added_destination_row, flatten_field
from ..outputs import AddToDestinationListOutput
from ..params import AddToDestinationListParams
from ..sse_api_client import GET, POST, policies


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
    destinations_response = client.QueryAllPages(
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
