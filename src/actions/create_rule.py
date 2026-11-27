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
from soar_sdk.action_results import ActionOutput
from soar_sdk.exceptions import ActionFailure
from soar_sdk.params import Param, Params

from ..asset import Asset
from ..error_handling import format_action_error
from ..input_helpers import _parse_json_param
from ..response_handling import require_mapping
from ..sse_api_client import POST, policies

RULE_ACTION_VALUES = ["allow", "block"]


class CreateRuleParams(Params):
    """Parameters for Create Rule. POST policies/v2/rules. Requires policies.rules:write."""

    rule_name: str = Param(
        required=True,
        description="Rule name (2-50 alphanumeric, hyphen, underscore, space). Unique across access rules.",
    )
    rule_action: str = Param(
        required=True,
        description="Action for the rule.",
        value_list=RULE_ACTION_VALUES,
    )
    rule_conditions_json: str = Param(
        required=True,
        description='JSON array of conditions, e.g. [{"attributeName":"umbrella.destination.all","attributeValue":true,"attributeOperator":"="},{"attributeName":"umbrella.source.all","attributeValue":true,"attributeOperator":"="}]',
    )
    rule_settings_json: str = Param(
        required=True,
        description='JSON array of settings, e.g. [{"settingName":"umbrella.default.traffic","settingValue":"PUBLIC_INTERNET"}]',
    )
    rule_description: str = Param(
        required=False,
        description="Optional description (max 256 characters).",
    )
    rule_priority: int = Param(
        required=False,
        description="Optional priority (positive integer, unique across rules).",
    )
    rule_is_enabled: bool = Param(
        required=False,
        default=True,
        description="Whether the rule is enabled. Default true.",
    )


class RuleConditionItem(ActionOutput):
    """Single rule condition (SDK requires typed output, not raw list)."""

    attributeName: str | None = None
    # API returns strings, booleans, or numbers; SOAR manifest only allows Optional[T].
    attributeValue: str | None = None
    attributeOperator: str | None = None


class RuleSettingItem(ActionOutput):
    """Single rule setting (SDK requires typed output, not raw list)."""

    settingName: str | None = None
    settingValue: str | None = None


class CreateRuleOutput(ActionOutput):
    """Response from Create Rule API (POST policies/v2/rules)."""

    organizationId: int | None = None
    ruleId: int | None = None
    ruleName: str | None = None
    ruleDescription: str | None = None
    ruleAction: str | None = None
    rulePriority: int | None = None
    ruleIsDefault: bool | None = None
    ruleIsEnabled: bool | None = None
    ruleConditions: list[RuleConditionItem] | None = None
    ruleSettings: list[RuleSettingItem] | None = None
    modifiedBy: str | None = None
    modifiedAt: str | None = None
    createdAt: str | None = None


def _stringify_item_values(items, value_keys: tuple[str, ...]):
    """Convert selected rule values to strings for typed SOAR outputs."""
    if not isinstance(items, list):
        return items
    normalized = []
    for item in items:
        if isinstance(item, dict):
            normalized_item = dict(item)
            for key in value_keys:
                value = normalized_item.get(key)
                if value is not None and not isinstance(value, str):
                    if isinstance(value, bool):
                        normalized_item[key] = "true" if value else "false"
                    else:
                        normalized_item[key] = str(value)
            normalized.append(normalized_item)
        else:
            normalized.append(item)
    return normalized


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
        data = client.request_json(
            scope=policies,
            end_point="rules",
            operation=POST,
            request_data=body,
        )
    except requests.exceptions.RequestException as exc:
        raise ActionFailure(format_action_error("Failed to create rule", exc)) from exc
    if isinstance(data, dict):
        if "ruleConditions" in data:
            data["ruleConditions"] = _stringify_item_values(
                data["ruleConditions"], ("attributeValue",)
            )
        if "ruleSettings" in data:
            data["ruleSettings"] = _stringify_item_values(
                data["ruleSettings"], ("settingValue",)
            )
    data = require_mapping(data, "CreateRuleOutput output")
    return CreateRuleOutput(**data)
