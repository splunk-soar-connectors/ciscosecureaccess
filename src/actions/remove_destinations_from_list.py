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

from ..core import Asset, _parse_comma_list
from ..outputs import RemoveDestinationsFromListOutput
from ..params import RemoveDestinationsFromListParams
from ..sse_api_client import DELETE, policies


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
    destination_list_response = client.request_json(
        scope=policies,
        end_point=f"destinationlists/{destination_list_id}/destinations/remove",
        operation=DELETE,
        request_data=destination_ids,
    )
    destination_list_response = destination_list_response["data"]
    return RemoveDestinationsFromListOutput(destinationList=destination_list_response)
