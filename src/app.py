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

from .actions.destination_lists import (
    add_to_destination_list,
    create_destination_list,
    list_destination_lists,
    remove_destinations_from_list,
)
from .actions.devices import (
    delete_managed_device,
    get_network_device,
    get_network_tunnel_group,
    get_roaming_computer,
    list_managed_devices,
    list_network_tunnel_groups,
    list_resource_connectors,
    list_roaming_computers,
    list_sites,
    list_virtual_appliances,
)
from .actions.domains import get_domain_risk_score, get_domain_status, get_passive_dns
from .actions.identities import (
    list_certificates_for_device,
    list_certificates_for_user,
    list_identities,
    update_identities,
)
from .actions.make_request import make_request
from .actions.rules import create_rule, list_firewall_rules
from .actions.swg import (
    delete_swg_override_device_settings,
    list_swg_override_device_settings,
    set_swg_override_device_settings,
)
from .actions.vpn import list_vpn_sessions
from .core import app, test_connectivity


app.test_connectivity()(test_connectivity)

app.register_action(
    list_destination_lists,
    description="List destination lists configured for the organization",
)
app.register_action(
    create_destination_list,
    description="Create a destination list in the organization",
    read_only=False,
)
app.register_action(
    add_to_destination_list,
    description="Add a destination to a destination list",
    read_only=False,
)
app.register_action(
    remove_destinations_from_list,
    description="Remove destinations from a destination list",
    read_only=False,
)

app.register_action(
    list_managed_devices,
    description="List managed network devices in the organization",
)
app.register_action(
    delete_managed_device,
    description="Delete a managed network device by origin ID",
    read_only=False,
)
app.register_action(
    get_network_device,
    description="Get a managed network device by origin ID",
)
app.register_action(
    list_virtual_appliances,
    description="List virtual appliances in the organization",
)
app.register_action(
    list_sites,
    description="List sites in the organization",
)
app.register_action(
    get_roaming_computer,
    description="Get posture and security details for a roaming computer",
)
app.register_action(
    list_roaming_computers,
    description="List roaming computers in the organization",
)
app.register_action(
    list_network_tunnel_groups,
    description="List network tunnel groups in the organization",
)
app.register_action(
    get_network_tunnel_group,
    description="Get a network tunnel group by ID",
)
app.register_action(
    list_resource_connectors,
    description="List resource connectors in the organization",
)

app.register_action(
    get_domain_status,
    description="Get the status and categorization of a domain",
)
app.register_action(
    get_domain_risk_score,
    description="Get the risk score for a domain",
)
app.register_action(
    get_passive_dns,
    description="Get passive DNS records for a domain",
)

app.register_action(
    list_identities,
    description="List device or security group tag identities",
)
app.register_action(
    update_identities,
    description="Create or update device or security group tag identities",
    read_only=False,
)
app.register_action(
    list_certificates_for_device,
    description="List ZTNA certificates for a user device",
)
app.register_action(
    list_certificates_for_user,
    description="List ZTNA device certificates for a user",
)

app.make_request()(make_request)

app.register_action(
    create_rule,
    description="Create an access rule in the organization's Access policy",
    read_only=False,
)
app.register_action(
    list_firewall_rules,
    description="List access rules in the organization's Access policy",
)

app.register_action(
    list_swg_override_device_settings,
    description="List SWG override settings for managed devices",
)
app.register_action(
    set_swg_override_device_settings,
    description="Set SWG override settings for managed devices",
    read_only=False,
)
app.register_action(
    delete_swg_override_device_settings,
    description="Delete SWG override settings for managed devices",
    read_only=False,
)

app.register_action(
    list_vpn_sessions,
    description="List active VPN sessions",
)


if __name__ == "__main__":
    app.cli()
