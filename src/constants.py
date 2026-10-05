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

# Pagination and validation limits.
MAX_LIMIT_NETWORK_TUNNEL_GROUPS = 200
MAX_LIMIT_FIREWALL_RULES = 1000
MAX_LIMIT_RESOURCE_CONNECTORS = 100
MAX_IDENTITIES_UPDATE = 250
MAX_SWG_ORIGIN_IDS = 100
MAX_DESTINATIONS_CREATE_DESTINATION_LIST = 500

_DESTINATION_CREATE_TYPES = frozenset({"domain", "url", "ipv4"})

# Domain status code to human-readable description.
DOMAIN_STATUS_DESCRIPTIONS = {-1: "Malicious", 1: "Benign", 0: "Unclassified"}
