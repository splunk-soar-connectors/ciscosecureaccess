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

import json

from .constants import MAX_SWG_ORIGIN_IDS


def _parse_json_param(value: str, param_name: str, *, allow_list: bool = False):
    """Parse a JSON string and validate whether an array is required."""
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as e:
        raise ValueError(f"{param_name} must be valid JSON: {e}") from e
    if allow_list and not isinstance(parsed, list):
        raise ValueError(f"{param_name} must be a JSON array")
    return parsed


def _parse_optional_filters(params) -> dict | None:
    """Return parsed filters from params, or None when filters are absent."""
    raw = getattr(params, "filters", None)
    if not raw or not str(raw).strip():
        return None
    return _parse_json_param(str(raw).strip(), "filters")


def _clamp_offset_limit(params, max_limit: int) -> tuple[int, int]:
    """Clamp pagination offset and limit to their supported ranges."""
    offset = max(0, params.offset)
    limit = min(max(1, params.limit), max_limit)
    return offset, limit


def _parse_comma_list(s: str) -> list[str]:
    """Split a comma-separated string into stripped, non-empty values."""
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def _parse_origin_ids(s: str, max_count: int = MAX_SWG_ORIGIN_IDS) -> list[int]:
    """Parse and validate comma-separated numeric origin IDs."""
    parts = _parse_comma_list(s)
    if len(parts) < 1:
        raise ValueError("origin_ids must contain at least one origin ID")
    if len(parts) > max_count:
        raise ValueError(f"origin_ids must contain at most {max_count} origin IDs")
    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            raise ValueError(
                f"origin_ids must be comma-separated integers; invalid: {p!r}"
            ) from None
    return result
