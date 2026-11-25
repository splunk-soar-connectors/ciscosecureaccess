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
from ..response_handling import require_mapping
from ..sse_api_client import DELETE, deployments


class DeleteManagedDeviceParams(Params):
    origin_id: int = Param(
        required=True,
        description="Origin ID of the network device to remove (obtain from the List Managed Devices action).",
    )


class DeleteManagedDeviceOutput(ActionOutput):
    success: bool = True
    message: str | None = None


def delete_managed_device(
    params: DeleteManagedDeviceParams, asset: Asset
) -> DeleteManagedDeviceOutput:
    """
    Remove a network device by origin ID.
    DELETE deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:write.
    https://developer.cisco.com/docs/cloud-security/delete-network-device/
    """
    client = asset.get_client()
    response = client.query(
        scope=deployments,
        end_point=f"networkdevices/{params.origin_id}",
        operation=DELETE,
    )
    if response.status_code in (200, 204) and not response.text.strip():
        data = {"success": True, "message": "Network device removed"}
    else:
        data = require_mapping(response.json(), "delete network device response")
    return DeleteManagedDeviceOutput(
        success=data.get("success", True), message=data.get("message")
    )
