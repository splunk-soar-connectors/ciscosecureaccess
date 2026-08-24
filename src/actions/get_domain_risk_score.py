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

from ..core import Asset
from ..outputs import GetDomainRiskScoreOutput
from ..params import GetDomainParams
from ..sse_api_client import GET, investigate


def get_domain_risk_score(
    params: GetDomainParams, asset: Asset
) -> GetDomainRiskScoreOutput:
    """
    Get Domain Risk Score.
    https://developer.cisco.com/docs/cloud-security/get-risk-score-for-domain/
    """
    client = asset.get_client()
    domain_risk_score_response = client.request_json(
        scope=investigate,
        end_point=f"domains/risk-score/{params.domain}",
        operation=GET,
    )
    return GetDomainRiskScoreOutput(**domain_risk_score_response)
