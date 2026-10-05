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

from .constants import (
    MAX_DESTINATIONS_CREATE_DESTINATION_LIST,
    _DESTINATION_CREATE_TYPES,
)
from .input_helpers import _parse_json_param


def _destinations_for_create_destination_list(
    destinations_json: str | None,
) -> list[dict] | None:
    """Parse and validate optional destination-list entries for an API request."""
    if destinations_json is None or not str(destinations_json).strip():
        return None
    parsed = _parse_json_param(
        str(destinations_json).strip(), "destinations_json", allow_list=True
    )
    if len(parsed) > MAX_DESTINATIONS_CREATE_DESTINATION_LIST:
        raise ValueError(
            f"destinations_json must contain at most "
            f"{MAX_DESTINATIONS_CREATE_DESTINATION_LIST} destinations"
        )
    out: list[dict] = []
    for i, item in enumerate(parsed):
        if not isinstance(item, dict):
            raise ValueError(f"destinations_json[{i}] must be a JSON object")
        dest = item.get("destination")
        typ = item.get("type")
        if dest is None or typ is None:
            raise ValueError(
                f"destinations_json[{i}] must include destination and type fields"
            )
        dest_s = str(dest).strip()
        typ_s = str(typ).strip()
        if not dest_s:
            raise ValueError(f"destinations_json[{i}] destination must be non-empty")
        if typ_s not in _DESTINATION_CREATE_TYPES:
            raise ValueError(
                f"destinations_json[{i}] type must be one of: "
                f"{', '.join(sorted(_DESTINATION_CREATE_TYPES))}"
            )
        row: dict = {"destination": dest_s, "type": typ_s}
        if item.get("comment") is not None:
            row["comment"] = str(item["comment"])
        out.append(row)
    return out


def _normalize_destination_for_match(value: str) -> str:
    """Normalize a destination value for case-insensitive matching."""
    return (value or "").strip().lower()


def _find_added_destination_row(
    rows: list,
    *,
    destination: str,
    comment: str | None,
) -> dict | None:
    """Find the newly added destination row by destination and optional comment."""
    if not isinstance(rows, list) or not rows:
        return None
    want = _normalize_destination_for_match(destination)
    matches_dest: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if _normalize_destination_for_match(str(row.get("destination") or "")) != want:
            continue
        matches_dest.append(row)
    if not matches_dest:
        return None
    if comment is not None:
        with_comment = [r for r in matches_dest if (r.get("comment") or "") == comment]
        if with_comment:
            matches_dest = with_comment

    return sorted(
        matches_dest, key=lambda row: str(row.get("createdAt") or ""), reverse=True
    )[0]


def flatten_field(obj_list, field_name, separator="."):
    """Flatten a nested dictionary field into top-level keys in-place."""
    if not isinstance(obj_list, list):
        return obj_list
    for obj in obj_list:
        if field_name not in obj:
            continue
        if not isinstance(obj[field_name], dict):
            continue
        nested_dict = obj.pop(field_name)
        for key, value in nested_dict.items():
            if key in obj:
                continue
            obj[key] = value
    return obj_list
