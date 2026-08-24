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

from ..core import Asset, _output_from_api_data, _parse_origin_ids
from ..outputs import DeleteSWGOverrideDeviceSettingsOutput
from ..params import DeleteSWGOverrideDeviceSettingsParams


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
    data = client.DeleteSWGOverrideDeviceSettings(origin_ids)
    return _output_from_api_data(DeleteSWGOverrideDeviceSettingsOutput, data)
