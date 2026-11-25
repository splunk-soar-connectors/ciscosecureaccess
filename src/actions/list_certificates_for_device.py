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
from ..sse_api_client import GET, admin


class ListCertificatesForDeviceParams(Params):
    user_id: str = Param(required=True, description="The ID of the user (ZTNA).")
    device_id: str = Param(required=True, description="The ID of the user device.")


class ZtnaCertificate(ActionOutput):
    """ACME-issued certificate for a ZTNA user device (List Certificates for Device)."""

    certificateId: str | None = None
    status: str | None = None  # active | expired | revoked
    createdAt: str | None = None
    expiresAt: str | None = None
    revokedAt: str | None = None


class ListCertificatesForDeviceOutput(ActionOutput):
    deviceId: str | None = None
    certificates: list[ZtnaCertificate] | None = None


def list_certificates_for_device(
    params: ListCertificatesForDeviceParams, asset: Asset
) -> ListCertificatesForDeviceOutput:
    """
    List Certificates for Device (ZTNA).
    GET /ztna/users/{userId}/devices/{deviceId}/certificates. Returns ACME-issued certificate info for the user device.
    https://developer.cisco.com/docs/cloud-security/list-certificates-for-device/
    """
    client = asset.get_client()
    data = client.request_json(
        scope=admin,
        end_point=f"ztna/users/{params.user_id}/devices/{params.device_id}/certificates",
        operation=GET,
    )
    data = require_mapping(data, "list certificates for device response")
    return ListCertificatesForDeviceOutput(
        deviceId=data.get("deviceId"),
        certificates=data.get("certificates"),
    )
