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
from ..response_handling import require_list
from ..sse_api_client import POST, deployments


class ListSWGOverrideDeviceSettingsParams(Params):
    """Parameters for List SWG Override Device Settings. POST deployments/v2/deviceSettings/SWGEnabled/list. Requires deployments.devices.swg:read."""

    origin_ids: str = Param(
        required=True,
        description="Comma-separated origin IDs of devices (1-100) to list SWG override settings for.",
    )


class SWGOverrideSettingItem(ActionOutput):
    """SWG override setting for one device from List SWG Override Device Settings API."""

    originId: int
    name: str
    value: str
    modifiedAt: str


class ListSWGOverrideDeviceSettingsOutput(ActionOutput):
    """Response from List SWG Override Device Settings (POST deployments/v2/deviceSettings/SWGEnabled/list)."""

    settings: list[SWGOverrideSettingItem]


def list_swg_override_device_settings(
    params: ListSWGOverrideDeviceSettingsParams, asset: Asset
) -> ListSWGOverrideDeviceSettingsOutput:
    """
    List SWG Override Device Settings.
    POST deployments/v2/deviceSettings/SWGEnabled/list. Returns SWG override setting (originId, name, value, modifiedAt) for each given origin ID (1-100).
    Requires deployments.devices.swg:read.
    https://developer.cisco.com/docs/cloud-security/list-swg-override-device-settings/
    """
    origin_ids = _parse_origin_ids(params.origin_ids)
    client = asset.get_client()
    data = client.request_json(
        scope=deployments,
        end_point="deviceSettings/SWGEnabled/list",
        operation=POST,
        request_data={"originIds": origin_ids},
    )
    return ListSWGOverrideDeviceSettingsOutput(
        settings=require_list(data, "list SWG override device settings response")
    )
