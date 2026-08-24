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

from ..core import Asset, _parse_origin_ids
from ..outputs import ListSWGOverrideDeviceSettingsOutput
from ..params import ListSWGOverrideDeviceSettingsParams
from ..sse_api_client import POST, deployments


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
    if not isinstance(data, list):
        data = []
    return ListSWGOverrideDeviceSettingsOutput(settings=data)
