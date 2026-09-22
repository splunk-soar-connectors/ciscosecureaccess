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
from ..outputs import ListCertificatesForUserOutput
from ..params import ListCertificatesForUserParams
from ..response_handling import require_mapping
from ..sse_api_client import GET, admin


def list_certificates_for_user(
    params: ListCertificatesForUserParams, asset: Asset
) -> ListCertificatesForUserOutput:
    """
    List Certificates for User (ZTNA).
    GET /ztna/users/{userId}/deviceCertificates. Returns all device certificates for the zero trust user.
    https://developer.cisco.com/docs/cloud-security/list-certificates-for-user/
    """
    client = asset.get_client()
    data = client.request_json(
        scope=admin,
        end_point=f"ztna/users/{params.user_id}/deviceCertificates",
        operation=GET,
    )
    data = require_mapping(data, "list certificates for user response")
    return ListCertificatesForUserOutput(
        userId=data.get("userId"),
        devices=data.get("devices"),
    )
