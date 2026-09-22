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

import pytest

from src.response_handling import (
    UnexpectedAPIResponse,
    require_list,
    require_mapping,
)


def test_require_mapping_rejects_non_object_with_context():
    """Reject non-object values with a contextual response-shape error."""
    with pytest.raises(
        UnexpectedAPIResponse,
        match="Unexpected API response for list sites: expected an object",
    ):
        require_mapping([], "list sites")


def test_require_list_accepts_json_array():
    """Accept a valid JSON array as a response list."""
    assert require_list([{"id": 1}], "sites") == [{"id": 1}]


def test_require_list_rejects_non_array_with_context():
    """Reject non-array values with a contextual response-shape error."""
    with pytest.raises(
        UnexpectedAPIResponse,
        match="Unexpected API response for sites: expected an array",
    ):
        require_list({"id": 1}, "sites")
