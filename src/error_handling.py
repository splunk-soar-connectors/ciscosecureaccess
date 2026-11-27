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


def format_api_error(exc: Exception) -> str:
    """Return a useful API error message, preferring structured API details."""
    message = str(exc) or exc.__class__.__name__
    response = getattr(exc, "response", None)
    if response is None:
        return message

    try:
        response_data = response.json()
    except (TypeError, ValueError):
        response_data = None
    if isinstance(response_data, dict):
        return str(
            response_data.get("message") or response_data.get("error") or message
        )
    return message


def format_action_error(prefix: str, exc: Exception) -> str:
    """Prefix a normalized API error for display as an action failure."""
    return f"{prefix}: {format_api_error(exc)}"
