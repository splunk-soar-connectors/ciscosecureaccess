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
from ..constants import MAX_LIMIT_FIREWALL_RULES
from ..input_helpers import _clamp_offset_limit, _parse_optional_filters
from ..sse_api_client import GET, _encode_filters, policies


class ListFirewallRulesParams(Params):
    offset: int = Param(
        required=False,
        default=0,
        description="Index to start reading the collection (0-based). Default 0.",
    )
    limit: int = Param(
        required=False,
        default=10,
        description="Number of rules per page. Max 1000. Default 10.",
    )
    rule_name: str = Param(
        required=False,
        description="Filter by rule name or substring (e.g. 'Allow all rule').",
    )
    filters: str = Param(
        required=False,
        description="Optional JSON object to filter rules by properties (ruleName, ruleDescription, ruleIsEnabled, ruleAction, ruleConditions, sources, destinations, etc.). Cannot combine ruleConditions with sources/destinations.",
    )


class FirewallRule(ActionOutput):
    """Access rule from List Rules API. Required per schema: ruleId."""

    ruleId: int
    organizationId: int | None = None
    ruleName: str | None = None
    ruleDescription: str | None = None
    ruleAction: str | None = None
    rulePriority: int | None = None
    ruleIsDefault: bool | None = None
    ruleIsEnabled: bool | None = None
    modifiedBy: str | None = None
    modifiedAt: str | None = None
    createdAt: str | None = None


class ListFirewallRulesOutput(ActionOutput):
    count: int | None = None
    firewall_rules: list[FirewallRule] | None = None


def list_firewall_rules(
    params: ListFirewallRulesParams, asset: Asset
) -> ListFirewallRulesOutput:
    """
    List access rules in the organization's Access policy.
    GET policies/v2/rules. Requires policies.rules:read.
    https://developer.cisco.com/docs/cloud-security/list-rules/
    """
    client = asset.get_client()
    filters_obj = _parse_optional_filters(params)
    rule_name = getattr(params, "rule_name", None) or None
    if rule_name is not None and str(rule_name).strip() == "":
        rule_name = None
    offset, limit = _clamp_offset_limit(params, MAX_LIMIT_FIREWALL_RULES)
    request_params = {"offset": offset, "limit": limit}
    if rule_name is not None:
        request_params["ruleName"] = rule_name
    if filters_obj is not None:
        request_params["filters"] = _encode_filters(filters_obj)
    data = client.request_json(
        scope=policies,
        end_point="rules",
        operation=GET,
        params=request_params,
    )
    rules = (
        (data.get("results") or data.get("result") or [])
        if isinstance(data, dict)
        else []
    )
    return ListFirewallRulesOutput(
        count=data.get("count") if isinstance(data, dict) else None,
        firewall_rules=rules,
    )
