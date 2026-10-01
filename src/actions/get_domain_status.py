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
from ..constants import DOMAIN_STATUS_DESCRIPTIONS
from ..outputs import GetDomainStatusOutput
from ..params import GetDomainParams
from ..sse_api_client import GET, investigate


def get_domain_status(params: GetDomainParams, asset: Asset) -> GetDomainStatusOutput:
    """
    Get Domain Status.
    https://developer.cisco.com/docs/cloud-security/get-domain-status-and-categorization/
    """
    client = asset.get_client()
    domain = params.domain
    domain_status_response = client.request_json(
        scope=investigate,
        end_point=f"domains/categorization/{domain}?showLabels",
        operation=GET,
    )
    domain_status_object = domain_status_response[domain]
    domain_status_object["domain"] = domain
    domain_status_object["status_description"] = DOMAIN_STATUS_DESCRIPTIONS.get(
        domain_status_object.get("status"), "Unknown"
    )
    return GetDomainStatusOutput(**domain_status_object)
