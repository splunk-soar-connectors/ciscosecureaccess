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

from .add_to_destination_list import add_to_destination_list
from .create_destination_list import create_destination_list
from .list_destination_lists import list_destination_lists
from .remove_destinations_from_list import remove_destinations_from_list

__all__ = [
    "add_to_destination_list",
    "create_destination_list",
    "list_destination_lists",
    "remove_destinations_from_list",
]
