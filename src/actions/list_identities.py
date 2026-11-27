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
from ..constants import IDENTITY_TYPE_VALUES
from ..sse_api_client import GET, deployments


class ListIdentitiesParams(Params):
    type: str = Param(
        required=True,
        description="Identity type to list: 'device' for device registrations, "
        "'securityGroupTag' for security group tags (SGTs).",
        value_list=IDENTITY_TYPE_VALUES,
    )


class Identity(ActionOutput):
    key: str
    label: str
    status: str
    createdAt: int
    modifiedAt: int
    authName: str | None = None
    tagId: int | None = None


class ListIdentitiesOutput(ActionOutput):
    """Identities from List Identities. Client returns data array; API schema has total, limit, offset, data."""

    identities: list[Identity]


def list_identities(params: ListIdentitiesParams, asset: Asset) -> ListIdentitiesOutput:
    """
    List Identities.
    https://developer.cisco.com/docs/cloud-security/list-identities/
    """
    client = asset.get_client()
    result = client.query_all_pages_offset(
        scope=deployments,
        end_point=f"identities/registrations/{params.type}",
        operation=GET,
        limit=250,
    )
    identities = result["data"]
    return ListIdentitiesOutput(identities=identities)
