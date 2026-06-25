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
    MAX_IDENTITIES_UPDATE,
    _parse_json_param,
    app,
)
from ..outputs import (
    ListCertificatesForDeviceOutput,
    ListCertificatesForUserOutput,
    ListIdentitiesOutput,
    RevokeCertificatesForDeviceOutput,
    UpdateIdentitiesOutput,
)
from ..params import (
    ListCertificatesForDeviceParams,
    ListCertificatesForUserParams,
    ListIdentitiesParams,
    RevokeCertificatesForDeviceParams,
    UpdateIdentitiesParams,
)


@app.action()
def list_identities(params: ListIdentitiesParams, asset: Asset) -> ListIdentitiesOutput:
    """
    List Identities.
    https://developer.cisco.com/docs/cloud-security/list-identities/
    """
    client = asset.get_client()
    identities = client.ListIdentities(params.type)
    return ListIdentitiesOutput(identities=identities)


@app.action(read_only=False)
def update_identities(
    params: UpdateIdentitiesParams, asset: Asset
) -> UpdateIdentitiesOutput:
    """
    Update Identities (devices or security group tags).
    PUT /identities/registrations/{type}. Pass 1-250 identity objects as JSON array in identities_json.
    https://developer.cisco.com/docs/cloud-security/update-identities/
    """
    client = asset.get_client()
    identity_type = params.type.strip().lower()
    if identity_type not in ("device", "securitygrouptag"):
        raise ValueError("type must be 'device' or 'securityGroupTag'")
    if identity_type == "securitygrouptag":
        identity_type = "securityGroupTag"
    identities_list = _parse_json_param(
        params.identities_json, "identities_json", allow_list=True
    )
    if len(identities_list) < 1 or len(identities_list) > MAX_IDENTITIES_UPDATE:
        raise ValueError("identities_json must contain 1-250 items")
    data = client.UpdateIdentities(identity_type, identities_list)
    return UpdateIdentitiesOutput(success=data.get("success"))


@app.action()
def list_certificates_for_device(
    params: ListCertificatesForDeviceParams, asset: Asset
) -> ListCertificatesForDeviceOutput:
    """
    List Certificates for Device (ZTNA).
    GET /ztna/users/{userId}/devices/{deviceId}/certificates. Returns ACME-issued certificate info for the user device.
    https://developer.cisco.com/docs/cloud-security/list-certificates-for-device/
    """
    client = asset.get_client()
    data = client.ListCertificatesForDevice(params.user_id, params.device_id)
    return ListCertificatesForDeviceOutput(
        deviceId=data.get("deviceId"),
        certificates=data.get("certificates"),
    )


@app.action()
def list_certificates_for_user(
    params: ListCertificatesForUserParams, asset: Asset
) -> ListCertificatesForUserOutput:
    """
    List Certificates for User (ZTNA).
    GET /ztna/users/{userId}/deviceCertificates. Returns all device certificates for the zero trust user.
    https://developer.cisco.com/docs/cloud-security/list-certificates-for-user/
    """
    client = asset.get_client()
    data = client.ListCertificatesForUser(params.user_id)
    return ListCertificatesForUserOutput(
        userId=data.get("userId"),
        devices=data.get("devices"),
    )


@app.action(read_only=False)
def revoke_certificates_for_device(
    params: RevokeCertificatesForDeviceParams, asset: Asset
) -> RevokeCertificatesForDeviceOutput:
    """
    Revoke Certificates for Device (ZTNA).
    DELETE /ztna/users/{userId}/devices/{deviceId}. Revokes active ACME-issued certificates and removes the zero trust user device.
    https://developer.cisco.com/docs/cloud-security/revoke-certificates-for-device/
    """
    client = asset.get_client()
    data = client.RevokeCertificatesForDevice(params.user_id, params.device_id)
    return RevokeCertificatesForDeviceOutput(
        success=data.get("success"),
        message=data.get("message"),
    )
