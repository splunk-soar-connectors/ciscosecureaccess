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

from ..core import Asset, flatten_field
from ..outputs import ListDestinationListsOutput
from ..params import ListDestinationListsParams
from ..sse_api_client import GET, policies


def list_destination_lists(
    params: ListDestinationListsParams, asset: Asset
) -> ListDestinationListsOutput:
    """
    List Destination Lists.
    https://developer.cisco.com/docs/cloud-security/get-destination-lists/
    """
    client = asset.get_client()
    destination_list_response = client.request_all_pages(
        scope=policies, end_point="destinationlists", operation=GET
    )
    destination_lists = destination_list_response["data"]
    destination_lists = flatten_field(destination_lists, "meta")
    if params.list_destinations:
        destination_lists_output = []
        for destination_list in destination_lists:
            destinations_response = client.request_all_pages(
                scope=policies,
                end_point=f"destinationlists/{destination_list['id']}/destinations",
                operation=GET,
            )
            destinations = destinations_response["data"]
            destination_list["destinations"] = destinations
            destination_lists_output.append(destination_list)
    else:
        destination_lists_output = destination_lists
    return ListDestinationListsOutput(destinationLists=destination_lists_output)
