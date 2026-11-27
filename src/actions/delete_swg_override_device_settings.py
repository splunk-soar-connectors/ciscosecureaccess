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
from ..input_helpers import _parse_origin_ids
from ..response_handling import require_mapping
from ..sse_api_client import POST, deployments


class DeleteSWGOverrideDeviceSettingsParams(Params):
    """Parameters for Delete SWG Override Device Settings. POST deployments/v2/deviceSettings/SWGEnabled/remove. Requires deployments.devices.swg:write."""

    origin_ids: str = Param(
        required=True,
        description="Comma-separated origin IDs of devices (1-100) to remove SWG override setting from. Organization SWG setting will apply after removal.",
    )


class DeleteSWGOverrideDeviceSettingsOutput(ActionOutput):
    """Response from Delete SWG Override Device Settings (POST deployments/v2/deviceSettings/SWGEnabled/remove)."""

    status: str | None = None


def delete_swg_override_device_settings(
    params: DeleteSWGOverrideDeviceSettingsParams, asset: Asset
) -> DeleteSWGOverrideDeviceSettingsOutput:
    """
    Delete SWG Override Device Settings.
    POST deployments/v2/deviceSettings/SWGEnabled/remove. Removes the SWG override for the given devices (1-100);
    organization SWG setting will apply after removal. Requires deployments.devices.swg:write.
    https://developer.cisco.com/docs/cloud-security/delete-swg-override-device-settings/
    """
    origin_ids = _parse_origin_ids(params.origin_ids)
    client = asset.get_client()
    data = client.request_json(
        scope=deployments,
        end_point="deviceSettings/SWGEnabled/remove",
        operation=POST,
        request_data={"originIds": origin_ids},
    )
    data = require_mapping(data, "DeleteSWGOverrideDeviceSettingsOutput output")
    return DeleteSWGOverrideDeviceSettingsOutput(**data)
