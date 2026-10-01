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


class UnexpectedAPIResponse(ValueError):
    """Raised when Cisco returns a response with an unexpected JSON shape."""


def require_mapping(value, context: str) -> dict:
    """Require a JSON object and include the API context in the error."""
    if not isinstance(value, dict):
        raise UnexpectedAPIResponse(
            f"Unexpected API response for {context}: expected an object"
        )
    return value


def require_list(value, context: str, *, allow_none: bool = True) -> list:
    """Require a JSON array, optionally treating an explicit null as empty."""
    if value is None and allow_none:
        return []
    if not isinstance(value, list):
        raise UnexpectedAPIResponse(
            f"Unexpected API response for {context}: expected an array"
        )
    return value
