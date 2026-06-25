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

import requests
from soar_sdk.exceptions import ActionFailure

from ..core import (
    Asset,
    MAX_LIMIT_FIREWALL_RULES,
    _clamp_offset_limit,
    _output_from_api_data,
    _parse_json_param,
    _parse_optional_filters,
    _stringify_item_values,
)
from ..outputs import CreateRuleOutput, ListFirewallRulesOutput
from ..params import CreateRuleParams, ListFirewallRulesParams


def create_rule(params: CreateRuleParams, asset: Asset) -> CreateRuleOutput:
    """
    Create an access rule on the organization's Access policy.
    POST policies/v2/rules. Requires policies.rules:write.
    https://developer.cisco.com/docs/cloud-security/create-rule/
    """
    rule_conditions = _parse_json_param(
        params.rule_conditions_json, "rule_conditions_json", allow_list=True
    )
    rule_settings = _parse_json_param(
        params.rule_settings_json, "rule_settings_json", allow_list=True
    )
    body = {
        "ruleName": params.rule_name,
        "ruleAction": params.rule_action,
        "ruleConditions": rule_conditions,
        "ruleSettings": rule_settings,
    }
    if (
        getattr(params, "rule_description", None)
        and str(params.rule_description).strip()
    ):
        body["ruleDescription"] = params.rule_description.strip()
    if getattr(params, "rule_priority", None) is not None:
        body["rulePriority"] = params.rule_priority
    if getattr(params, "rule_is_enabled", None) is not None:
        body["ruleIsEnabled"] = params.rule_is_enabled
    client = asset.get_client()
    try:
        data = client.CreateRule(body)
    except requests.exceptions.RequestException as exc:
        message = str(exc)
        if exc.response is not None:
            try:
                response_data = exc.response.json()
            except requests.exceptions.JSONDecodeError:
                response_data = None
            if isinstance(response_data, dict):
                message = str(
                    response_data.get("message")
                    or response_data.get("error")
                    or message
                )
        raise ActionFailure(f"Failed to create rule: {message}") from exc
    if isinstance(data, dict):
        if "ruleConditions" in data:
            data["ruleConditions"] = _stringify_item_values(
                data["ruleConditions"], ("attributeValue",)
            )
        if "ruleSettings" in data:
            data["ruleSettings"] = _stringify_item_values(
                data["ruleSettings"], ("settingValue",)
            )
    return _output_from_api_data(CreateRuleOutput, data)


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
    data = client.ListFirewallRules(
        offset=offset,
        limit=limit,
        rule_name=rule_name,
        filters=filters_obj,
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
