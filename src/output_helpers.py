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

from .response_handling import require_mapping


def _output_from_api_data(OutputModel, data: dict):
    """Build an output model using only fields supported by that model."""
    data = require_mapping(data, f"{OutputModel.__name__} output")
    fields = getattr(OutputModel, "model_fields", None) or getattr(
        OutputModel, "__fields__", {}
    )
    return OutputModel(**{k: data[k] for k in data if k in fields})


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
