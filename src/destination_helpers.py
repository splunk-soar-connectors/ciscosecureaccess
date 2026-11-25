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
