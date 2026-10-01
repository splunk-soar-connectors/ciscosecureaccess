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
from ..input_helpers import _parse_origin_ids
from ..outputs import SetSWGOverrideDeviceSettingsOutput
from ..params import SetSWGOverrideDeviceSettingsParams
from ..output_helpers import _output_from_api_data
from ..sse_api_client import POST, deployments


def set_swg_override_device_settings(
    params: SetSWGOverrideDeviceSettingsParams, asset: Asset
) -> SetSWGOverrideDeviceSettingsOutput:
    """
    Set SWG Override Device Settings.
    POST deployments/v2/deviceSettings/SWGEnabled/set. Override SWG enable/disable for devices by origin ID (1-100).
    Requires deployments.devices.swg:write. Devices must be registered as roaming computers.
    https://developer.cisco.com/docs/cloud-security/set-swg-override-device-settings/
    """
    origin_ids = _parse_origin_ids(params.origin_ids)
    client = asset.get_client()
    data = client.request_json(
        scope=deployments,
        end_point="deviceSettings/SWGEnabled/set",
        operation=POST,
        request_data={"value": params.value, "originIds": origin_ids},
    )
    return _output_from_api_data(SetSWGOverrideDeviceSettingsOutput, data)
