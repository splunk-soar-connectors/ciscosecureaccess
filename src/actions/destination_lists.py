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
    _destinations_for_create_destination_list,
    _find_added_destination_row,
    _parse_comma_list,
    flatten_field,
)
from ..outputs import (
    AddToDestinationListOutput,
    CreateDestinationListOutput,
    ListDestinationListsOutput,
    RemoveDestinationsFromListOutput,
)
from ..params import (
    AddToDestinationListParams,
    CreateDestinationListParams,
    ListDestinationListsParams,
    RemoveDestinationsFromListParams,
)


def list_destination_lists(
    params: ListDestinationListsParams, asset: Asset
) -> ListDestinationListsOutput:
    """
    List Destination Lists.
    https://developer.cisco.com/docs/cloud-security/get-destination-lists/
    """
    client = asset.get_client()
    destination_lists = client.ListDestinationLists()
    destination_lists = flatten_field(destination_lists, "meta")
    if params.list_destinations:
        destination_lists_output = []
        for destination_list in destination_lists:
            destinations = client.GetDestinationsFromListById(destination_list["id"])
            destination_list["destinations"] = destinations
            destination_lists_output.append(destination_list)
    else:
        destination_lists_output = destination_lists
    return ListDestinationListsOutput(destinationLists=destination_lists_output)


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
    raw = client.CreateDestinationList(body)
    if not isinstance(raw, dict):
        raise ValueError("Unexpected API response for create destination list")
    data = raw.get("data", raw)
    if not isinstance(data, dict):
        raise ValueError("Unexpected API response data for create destination list")
    if data.get("meta") is not None:
        data = flatten_field([data], "meta")[0]
    return CreateDestinationListOutput(destinationList=data)


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
    destination_list_response = client.AddToDestinationList(
        destination_list_id, params.destination, params.comment
    )
    destination_list = destination_list_response["data"]
    if isinstance(destination_list, dict) and destination_list.get("meta") is not None:
        destination_list = flatten_field([destination_list], "meta")[0]
    added_id = None
    raw_destinations = client.GetDestinationsFromListById(destination_list_id)
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


def remove_destinations_from_list(
    params: RemoveDestinationsFromListParams, asset: Asset
) -> RemoveDestinationsFromListOutput:
    """
    Remove from Destination List.
    https://developer.cisco.com/docs/cloud-security/delete-destinations-from-destination-list/
    """
    client = asset.get_client()
    destination_list_id = (
        params.destination_list_id
        if params.destination_list_id
        else asset.default_destination_list_id
    )
    if not destination_list_id:
        raise ValueError("Destination list ID is required")
    destination_ids = _parse_comma_list(params.destination_ids)
    destination_list_response = client.RemoveDestinationsFromList(
        destination_list_id, destination_ids
    )
    return RemoveDestinationsFromListOutput(destinationList=destination_list_response)
