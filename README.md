# Cisco Secure Access

Publisher: Splunk <br>
Connector Version: 1.0.0 <br>
Product Vendor: Cisco <br>
Product Name: Cisco Secure Access <br>
Minimum Product Version: 7.0.0

Cisco Secure Access API actions for Splunk SOAR

### Configuration variables

This table lists the configuration variables required to operate Cisco Secure Access. These variables are specified when configuring a Cisco Secure Access asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** | required | string | Base Url |
**client_id** | required | string | Client ID for authentication |
**client_secret** | required | password | Client Secret key for authentication |
**auth_header_name** | required | string | HTTP header name for the Bearer token (value is always sent as 'Bearer {token}') |
**default_destination_list_id** | optional | string | Default destination list ID to use for automated domain/URL blocking |

### Supported Actions

[test connectivity](#action-test-connectivity) - Test connectivity against the Cisco Secure Access API.
Get a token to ensure connectivity, and valid configuration.
https://developer.cisco.com/docs/cloud-security/create-authorization-token/ <br>
[list managed devices](#action-list-managed-devices) - List all valid IOA platforms.
https://developer.cisco.com/docs/cloud-security/list-network-devices/ <br>
[delete managed device](#action-delete-managed-device) - Remove a network device by origin ID.
DELETE deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:write.
https://developer.cisco.com/docs/cloud-security/delete-network-device/ <br>
[get network device](#action-get-network-device) - Get a network device by origin ID.
GET deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:read.
https://developer.cisco.com/docs/cloud-security/get-network-device/ <br>
[list api keys](#action-list-api-keys) - List all API keys
https://developer.cisco.com/docs/cloud-security/list-api-keys/ <br>
[list virtual appliances](#action-list-virtual-appliances) - List all virtual appliances
https://developer.cisco.com/docs/cloud-security/list-virtual-appliances/ <br>
[list sites](#action-list-sites) - List all Sites in the organization.
GET deployments/v2/sites. Requires deployments.sites:read.
https://developer.cisco.com/docs/cloud-security/list-sites/ <br>
[list destination lists](#action-list-destination-lists) - List Destination Lists
https://developer.cisco.com/docs/cloud-security/get-destination-lists/ <br>
[create destination list](#action-create-destination-list) - Create a destination list in the organization (optional initial destinations).
POST policies/v2/destinationlists. Requires policies.destinationLists:write.
Secure Access does not support global destination lists on create; the request always sets isGlobal to false.
https://developer.cisco.com/docs/cloud-security/create-destination-list/ <br>
[add to destination list](#action-add-to-destination-list) - Add to Destination List (one destination and optional comment per run).
https://developer.cisco.com/docs/cloud-security/add-destinations-to-destination-list/ <br>
[remove destinations from list](#action-remove-destinations-from-list) - Remove from Destination List
https://developer.cisco.com/docs/cloud-security/delete-destinations-from-destination-list/ <br>
[get domain status](#action-get-domain-status) - Get Domain Status
https://developer.cisco.com/docs/cloud-security/get-domain-status-and-categorization/ <br>
[get domain risk score](#action-get-domain-risk-score) - Get Domain Risk Score
https://developer.cisco.com/docs/cloud-security/get-risk-score-for-domain/ <br>
[get passive dns](#action-get-passive-dns) - Get Passive DNS
https://developer.cisco.com/docs/cloud-security/get-resource-records-for-name/ <br>
[list vpn sessions](#action-list-vpn-sessions) - List VPN Sessions
https://developer.cisco.com/docs/cloud-security/list-vpn-connections/ <br>
[terminate vpn session](#action-terminate-vpn-session) - Terminate VPN Session
https://developer.cisco.com/docs/cloud-security/disconnect-vpn-users/ <br>
[list identities](#action-list-identities) - List Identities
https://developer.cisco.com/docs/cloud-security/list-identities/ <br>
[update identities](#action-update-identities) - Update Identities (devices or security group tags).
PUT /identities/registrations/{type}. Pass 1-250 identity objects as JSON array in identities_json.
https://developer.cisco.com/docs/cloud-security/update-identities/ <br>
[list certificates for device](#action-list-certificates-for-device) - List Certificates for Device (ZTNA).
GET /ztna/users/{userId}/devices/{deviceId}/certificates. Returns ACME-issued certificate info for the user device.
https://developer.cisco.com/docs/cloud-security/list-certificates-for-device/ <br>
[list certificates for user](#action-list-certificates-for-user) - List Certificates for User (ZTNA).
GET /ztna/users/{userId}/deviceCertificates. Returns all device certificates for the zero trust user.
https://developer.cisco.com/docs/cloud-security/list-certificates-for-user/ <br>
[revoke certificates for device](#action-revoke-certificates-for-device) - Revoke Certificates for Device (ZTNA).
DELETE /ztna/users/{userId}/devices/{deviceId}. Revokes active ACME-issued certificates and removes the zero trust user device.
https://developer.cisco.com/docs/cloud-security/revoke-certificates-for-device/ <br>
[get roaming computer](#action-get-roaming-computer) - Get Roaming Computer (posture/security status for a device).
GET /roamingcomputers/{deviceId}. Returns status, swgStatus, lastSync, appliedBundle, version, OS info, etc.
https://developer.cisco.com/docs/cloud-security/get-roaming-computer/ <br>
[list roaming computers](#action-list-roaming-computers) - List all roaming computers
GET /roamingcomputers. Returns roaming computers (posture/security status) in the organization.
https://developer.cisco.com/docs/cloud-security/list-roaming-computers/ <br>
[list swg override device settings](#action-list-swg-override-device-settings) - List SWG Override Device Settings.
POST deployments/v2/deviceSettings/SWGEnabled/list. Returns SWG override setting (originId, name, value, modifiedAt) for each given origin ID (1-100).
Requires deployments.devices.swg:read.
https://developer.cisco.com/docs/cloud-security/list-swg-override-device-settings/ <br>
[set swg override device settings](#action-set-swg-override-device-settings) - Set SWG Override Device Settings.
POST deployments/v2/deviceSettings/SWGEnabled/set. Override SWG enable/disable for devices by origin ID (1-100).
Requires deployments.devices.swg:write. Devices must be registered as roaming computers.
https://developer.cisco.com/docs/cloud-security/set-swg-override-device-settings/ <br>
[delete swg override device settings](#action-delete-swg-override-device-settings) - Delete SWG Override Device Settings.
POST deployments/v2/deviceSettings/SWGEnabled/remove. Removes the SWG override for the given devices (1-100);
organization SWG setting will apply after removal. Requires deployments.devices.swg:write.
https://developer.cisco.com/docs/cloud-security/delete-swg-override-device-settings/ <br>
[list network tunnel groups](#action-list-network-tunnel-groups) - List Network Tunnel Groups in the organization.
GET deployments/v2/networktunnelgroups. Requires deployments.networktunnelgroups:read.
https://developer.cisco.com/docs/cloud-security/list-network-tunnel-groups/ <br>
[get network tunnel group](#action-get-network-tunnel-group) - Get a Network Tunnel Group by ID.
GET deployments/v2/networktunnelgroups/{id}. Requires deployments.networktunnelgroups:read.
https://developer.cisco.com/docs/cloud-security/get-network-tunnel-group/ <br>
[create rule](#action-create-rule) - Create an access rule on the organization's Access policy.
POST policies/v2/rules. Requires policies.rules:write.
https://developer.cisco.com/docs/cloud-security/create-rule/ <br>
[list firewall rules](#action-list-firewall-rules) - List access rules in the organization's Access policy.
GET policies/v2/rules. Requires policies.rules:read.
https://developer.cisco.com/docs/cloud-security/list-rules/ <br>
[list resource connectors](#action-list-resource-connectors) - List Resource Connectors for the organization.
GET deployments/v2/connectorAgents. Requires deployments.resourceconnectors:read.
https://developer.cisco.com/docs/cloud-security/list-connectors/ <br>
[refresh s3 key](#action-refresh-s3-key) - Rotate the Cisco-managed S3 bucket key for the organization.
POST admin/v2/iam/rotateKey. Requires admin.iam:write.
https://developer.cisco.com/docs/cloud-security/refresh-s3-bucket-key/

## action: 'test connectivity'

Test connectivity against the Cisco Secure Access API.
Get a token to ensure connectivity, and valid configuration.
https://developer.cisco.com/docs/cloud-security/create-authorization-token/

Type: **test** <br>
Read only: **True**

Basic test for app.

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list managed devices'

List all valid IOA platforms.
https://developer.cisco.com/docs/cloud-security/list-network-devices/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.data.\*.devices.\*.originId | numeric | | |
action_result.data.\*.devices.\*.deviceId | string | | |
action_result.data.\*.devices.\*.deviceKey | string | | |
action_result.data.\*.devices.\*.name | string | | |
action_result.data.\*.devices.\*.serialNumber | string | | |
action_result.data.\*.devices.\*.createdAt | string | | |
action_result.data.\*.devices.\*.organizationId | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'delete managed device'

Remove a network device by origin ID.
DELETE deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:write.
https://developer.cisco.com/docs/cloud-security/delete-network-device/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**origin_id** | required | Origin ID of the network device to remove (obtain from the List Managed Devices action). | numeric | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.origin_id | numeric | | |
action_result.data.\*.success | boolean | | True False |
action_result.data.\*.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get network device'

Get a network device by origin ID.
GET deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:read.
https://developer.cisco.com/docs/cloud-security/get-network-device/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**origin_id** | required | Origin ID of the network device (obtain from the List Managed Devices action). | numeric | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.origin_id | numeric | | |
action_result.data.\*.originId | numeric | | |
action_result.data.\*.deviceId | string | | |
action_result.data.\*.deviceKey | string | | |
action_result.data.\*.name | string | | |
action_result.data.\*.serialNumber | string | | |
action_result.data.\*.createdAt | string | | |
action_result.data.\*.organizationId | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list api keys'

List all API keys
https://developer.cisco.com/docs/cloud-security/list-api-keys/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.data.\*.keys.\*.id | string | | |
action_result.data.\*.keys.\*.creatorName | string | | |
action_result.data.\*.keys.\*.creatorEmail | string | | |
action_result.data.\*.keys.\*.createdAt | string | | |
action_result.data.\*.keys.\*.expireAt | string | | |
action_result.data.\*.keys.\*.modifiedAt | string | | |
action_result.data.\*.keys.\*.lastUsedAt | string | | |
action_result.data.\*.keys.\*.lastRefreshedAt | string | | |
action_result.data.\*.keys.\*.scopes.\* | string | | |
action_result.data.\*.keys.\*.name | string | | |
action_result.data.\*.keys.\*.clientId | string | | |
action_result.data.\*.keys.\*.creatorKeyId | string | | |
action_result.data.\*.keys.\*.description | string | | |
action_result.data.\*.message | string | | |
action_result.data.\*.offset | numeric | | |
action_result.data.\*.limit | numeric | | |
action_result.data.\*.total | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list virtual appliances'

List all virtual appliances
https://developer.cisco.com/docs/cloud-security/list-virtual-appliances/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.data.\*.virtualAppliances.\*.originId | numeric | | |
action_result.data.\*.virtualAppliances.\*.name | string | | |
action_result.data.\*.virtualAppliances.\*.isUpgradable | boolean | | True False |
action_result.data.\*.virtualAppliances.\*.health | string | | |
action_result.data.\*.virtualAppliances.\*.type | string | | |
action_result.data.\*.virtualAppliances.\*.stateUpdatedAt | string | | |
action_result.data.\*.virtualAppliances.\*.siteId | numeric | | |
action_result.data.\*.virtualAppliances.\*.createdAt | string | | |
action_result.data.\*.virtualAppliances.\*.modifiedAt | string | | |
action_result.data.\*.virtualAppliances.\*.state_syncing | string | | |
action_result.data.\*.virtualAppliances.\*.internalIPs.\* | string | | |
action_result.data.\*.virtualAppliances.\*.externalIP | string | | |
action_result.data.\*.virtualAppliances.\*.hostType | string | | |
action_result.data.\*.virtualAppliances.\*.uptime | numeric | | |
action_result.data.\*.virtualAppliances.\*.version | string | | |
action_result.data.\*.virtualAppliances.\*.domains.\* | string | | |
action_result.data.\*.virtualAppliances.\*.lastSyncTime | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list sites'

List all Sites in the organization.
GET deployments/v2/sites. Requires deployments.sites:read.
https://developer.cisco.com/docs/cloud-security/list-sites/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.data.\*.sites.\*.originId | numeric | | |
action_result.data.\*.sites.\*.name | string | | |
action_result.data.\*.sites.\*.siteId | numeric | | |
action_result.data.\*.sites.\*.isDefault | boolean | | True False |
action_result.data.\*.sites.\*.modifiedAt | string | | |
action_result.data.\*.sites.\*.createdAt | string | | |
action_result.data.\*.sites.\*.type | string | | |
action_result.data.\*.sites.\*.internalNetworkCount | numeric | | |
action_result.data.\*.sites.\*.vaCount | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list destination lists'

List Destination Lists
https://developer.cisco.com/docs/cloud-security/get-destination-lists/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**list_destinations** | optional | If true, also fetch and embed each list's destination entries. Default false (returns list metadata only). | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.list_destinations | boolean | | |
action_result.data.\*.destinationLists.\*.id | numeric | | |
action_result.data.\*.destinationLists.\*.organizationId | numeric | | |
action_result.data.\*.destinationLists.\*.access | string | | |
action_result.data.\*.destinationLists.\*.isGlobal | boolean | | True False |
action_result.data.\*.destinationLists.\*.name | string | | |
action_result.data.\*.destinationLists.\*.thirdpartyCategoryId | numeric | | |
action_result.data.\*.destinationLists.\*.createdAt | numeric | | |
action_result.data.\*.destinationLists.\*.modifiedAt | numeric | | |
action_result.data.\*.destinationLists.\*.isMspDefault | boolean | | True False |
action_result.data.\*.destinationLists.\*.markedForDeletion | boolean | | True False |
action_result.data.\*.destinationLists.\*.bundleTypeId | numeric | | |
action_result.data.\*.destinationLists.\*.destinationCount | numeric | | |
action_result.data.\*.destinationLists.\*.domainCount | numeric | | |
action_result.data.\*.destinationLists.\*.urlCount | numeric | | |
action_result.data.\*.destinationLists.\*.ipv4Count | numeric | | |
action_result.data.\*.destinationLists.\*.ipv6Count | numeric | | |
action_result.data.\*.destinationLists.\*.applicationCount | numeric | | |
action_result.data.\*.destinationLists.\*.destinations.\*.id | string | | |
action_result.data.\*.destinationLists.\*.destinations.\*.type | string | | |
action_result.data.\*.destinationLists.\*.destinations.\*.createdAt | string | | |
action_result.data.\*.destinationLists.\*.destinations.\*.destination | string | | |
action_result.data.\*.destinationLists.\*.destinations.\*.comment | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'create destination list'

Create a destination list in the organization (optional initial destinations).
POST policies/v2/destinationlists. Requires policies.destinationLists:write.
Secure Access does not support global destination lists on create; the request always sets isGlobal to false.
https://developer.cisco.com/docs/cloud-security/create-destination-list/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** | required | Name of the destination list. | string | |
**access** | required | Access classification for the list (used with access rules). Cannot create lists with access type thirdparty_block via this API. | string | |
**destinations_json** | optional | Optional JSON array of up to 500 destinations, e.g. [{"destination":"cisco.com","type":"domain","comment":"optional"}]. type: domain, url, or ipv4. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.name | string | | |
action_result.parameter.access | string | | |
action_result.parameter.destinations_json | string | | |
action_result.data.\*.destinationList.id | numeric | | |
action_result.data.\*.destinationList.organizationId | numeric | | |
action_result.data.\*.destinationList.access | string | | |
action_result.data.\*.destinationList.isGlobal | boolean | | True False |
action_result.data.\*.destinationList.name | string | | |
action_result.data.\*.destinationList.thirdpartyCategoryId | numeric | | |
action_result.data.\*.destinationList.createdAt | numeric | | |
action_result.data.\*.destinationList.modifiedAt | numeric | | |
action_result.data.\*.destinationList.isMspDefault | boolean | | True False |
action_result.data.\*.destinationList.markedForDeletion | boolean | | True False |
action_result.data.\*.destinationList.bundleTypeId | numeric | | |
action_result.data.\*.destinationList.destinationCount | numeric | | |
action_result.data.\*.destinationList.domainCount | numeric | | |
action_result.data.\*.destinationList.urlCount | numeric | | |
action_result.data.\*.destinationList.ipv4Count | numeric | | |
action_result.data.\*.destinationList.ipv6Count | numeric | | |
action_result.data.\*.destinationList.applicationCount | numeric | | |
action_result.data.\*.destinationList.destinations.\*.id | string | | |
action_result.data.\*.destinationList.destinations.\*.type | string | | |
action_result.data.\*.destinationList.destinations.\*.createdAt | string | | |
action_result.data.\*.destinationList.destinations.\*.destination | string | | |
action_result.data.\*.destinationList.destinations.\*.comment | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'add to destination list'

Add to Destination List (one destination and optional comment per run).
https://developer.cisco.com/docs/cloud-security/add-destinations-to-destination-list/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**destination_list_id** | optional | Destination List ID. If not provided, the default destination list ID will be used. | numeric | |
**destination** | required | Destination URL, domain, or IP address | string | |
**comment** | optional | Comment for the destination | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.destination_list_id | numeric | | |
action_result.parameter.destination | string | | |
action_result.parameter.comment | string | | |
action_result.data.\*.addedDestinationId | string | | |
action_result.data.\*.destinationList.id | numeric | | |
action_result.data.\*.destinationList.organizationId | numeric | | |
action_result.data.\*.destinationList.access | string | | |
action_result.data.\*.destinationList.isGlobal | boolean | | True False |
action_result.data.\*.destinationList.name | string | | |
action_result.data.\*.destinationList.thirdpartyCategoryId | numeric | | |
action_result.data.\*.destinationList.createdAt | numeric | | |
action_result.data.\*.destinationList.modifiedAt | numeric | | |
action_result.data.\*.destinationList.isMspDefault | boolean | | True False |
action_result.data.\*.destinationList.markedForDeletion | boolean | | True False |
action_result.data.\*.destinationList.bundleTypeId | numeric | | |
action_result.data.\*.destinationList.destinationCount | numeric | | |
action_result.data.\*.destinationList.domainCount | numeric | | |
action_result.data.\*.destinationList.urlCount | numeric | | |
action_result.data.\*.destinationList.ipv4Count | numeric | | |
action_result.data.\*.destinationList.ipv6Count | numeric | | |
action_result.data.\*.destinationList.applicationCount | numeric | | |
action_result.data.\*.destinationList.destinations.\*.id | string | | |
action_result.data.\*.destinationList.destinations.\*.type | string | | |
action_result.data.\*.destinationList.destinations.\*.createdAt | string | | |
action_result.data.\*.destinationList.destinations.\*.destination | string | | |
action_result.data.\*.destinationList.destinations.\*.comment | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'remove destinations from list'

Remove from Destination List
https://developer.cisco.com/docs/cloud-security/delete-destinations-from-destination-list/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**destination_list_id** | optional | The ID of the Destination List to remove destinations from. If not provided, the default destination list ID will be used. | numeric | |
**destination_ids** | required | Comma-separated destination IDs to remove (e.g. 60582,60583). | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.destination_list_id | numeric | | |
action_result.parameter.destination_ids | string | | |
action_result.data.\*.destinationList.id | numeric | | |
action_result.data.\*.destinationList.organizationId | numeric | | |
action_result.data.\*.destinationList.access | string | | |
action_result.data.\*.destinationList.isGlobal | boolean | | True False |
action_result.data.\*.destinationList.name | string | | |
action_result.data.\*.destinationList.thirdpartyCategoryId | numeric | | |
action_result.data.\*.destinationList.createdAt | numeric | | |
action_result.data.\*.destinationList.modifiedAt | numeric | | |
action_result.data.\*.destinationList.isMspDefault | boolean | | True False |
action_result.data.\*.destinationList.markedForDeletion | boolean | | True False |
action_result.data.\*.destinationList.bundleTypeId | numeric | | |
action_result.data.\*.destinationList.destinationCount | numeric | | |
action_result.data.\*.destinationList.domainCount | numeric | | |
action_result.data.\*.destinationList.urlCount | numeric | | |
action_result.data.\*.destinationList.ipv4Count | numeric | | |
action_result.data.\*.destinationList.ipv6Count | numeric | | |
action_result.data.\*.destinationList.applicationCount | numeric | | |
action_result.data.\*.destinationList.destinations.\*.id | string | | |
action_result.data.\*.destinationList.destinations.\*.type | string | | |
action_result.data.\*.destinationList.destinations.\*.createdAt | string | | |
action_result.data.\*.destinationList.destinations.\*.destination | string | | |
action_result.data.\*.destinationList.destinations.\*.comment | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get domain status'

Get Domain Status
https://developer.cisco.com/docs/cloud-security/get-domain-status-and-categorization/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | Domain name to look up (e.g. cisco.com). | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.domain | string | | |
action_result.data.\*.domain | string | | |
action_result.data.\*.status | numeric | | |
action_result.data.\*.status_description | string | | |
action_result.data.\*.security_categories.\* | string | | |
action_result.data.\*.content_categories.\* | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get domain risk score'

Get Domain Risk Score
https://developer.cisco.com/docs/cloud-security/get-risk-score-for-domain/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | Domain name to look up (e.g. cisco.com). | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.domain | string | | |
action_result.data.\*.risk_score | numeric | | |
action_result.data.\*.indicators.\*.indicator | string | | |
action_result.data.\*.indicators.\*.normalized_score | numeric | | |
action_result.data.\*.indicators.\*.score | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get passive dns'

Get Passive DNS
https://developer.cisco.com/docs/cloud-security/get-resource-records-for-name/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | The domain to get passive DNS records for. | string | |
**offset** | optional | Index to start reading the collection (0-based). Default 0. | numeric | |
**limit** | optional | Maximum records to return in one call (1-9999). Default 1000. Use 9999 to retrieve the full set in a single call; the API caps total retrievable records at 10000 per domain. | numeric | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.domain | string | | |
action_result.parameter.offset | numeric | | |
action_result.parameter.limit | numeric | | |
action_result.data.\*.passive_dns_records.\*.minTtl | numeric | | |
action_result.data.\*.passive_dns_records.\*.maxTtl | numeric | | |
action_result.data.\*.passive_dns_records.\*.firstSeen | numeric | | |
action_result.data.\*.passive_dns_records.\*.lastSeen | numeric | | |
action_result.data.\*.passive_dns_records.\*.name | string | | |
action_result.data.\*.passive_dns_records.\*.type | string | | |
action_result.data.\*.passive_dns_records.\*.rr | string | | |
action_result.data.\*.passive_dns_records.\*.securityCategories.\* | string | | |
action_result.data.\*.passive_dns_records.\*.contentCategories.\* | string | | |
action_result.data.\*.passive_dns_records.\*.firstSeenISO | string | | |
action_result.data.\*.passive_dns_records.\*.lastSeenISO | string | | |
action_result.data.\*.total_records | numeric | | |
action_result.data.\*.returned_records | numeric | | |
action_result.data.\*.offset | numeric | | |
action_result.data.\*.limit | numeric | | |
action_result.data.\*.has_more_records | boolean | | True False |
action_result.data.\*.next_offset | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list vpn sessions'

List VPN Sessions
https://developer.cisco.com/docs/cloud-security/list-vpn-connections/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.data.\*.vpn_sessions.\*.username | string | | |
action_result.data.\*.vpn_sessions.\*.deviceName | string | | |
action_result.data.\*.vpn_sessions.\*.assignedIp | string | | |
action_result.data.\*.vpn_sessions.\*.assignedIpv6 | string | | |
action_result.data.\*.vpn_sessions.\*.publicIp | string | | |
action_result.data.\*.vpn_sessions.\*.sessionId | string | | |
action_result.data.\*.vpn_sessions.\*.loginTime | string | | |
action_result.data.\*.vpn_sessions.\*.profileName | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'terminate vpn session'

Terminate VPN Session
https://developer.cisco.com/docs/cloud-security/disconnect-vpn-users/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**profile_name** | optional | VPN profile name identifying the user connections to disconnect. | string | |
**region** | optional | Data center region identifying the VPN connections to disconnect. | string | |
**sessions** | optional | VPN session ID(s) to disconnect. | string | |
**usernames** | optional | Username(s) whose VPN connections should be disconnected. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.profile_name | string | | |
action_result.parameter.region | string | | |
action_result.parameter.sessions | string | | |
action_result.parameter.usernames | string | | |
action_result.data.\*.statusCode | numeric | | |
action_result.data.\*.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list identities'

List Identities
https://developer.cisco.com/docs/cloud-security/list-identities/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**type** | required | Identity type to list: 'device' for device registrations, 'securityGroupTag' for security group tags (SGTs). | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.type | string | | |
action_result.data.\*.identities.\*.key | string | | |
action_result.data.\*.identities.\*.label | string | | |
action_result.data.\*.identities.\*.status | string | | |
action_result.data.\*.identities.\*.createdAt | numeric | | |
action_result.data.\*.identities.\*.modifiedAt | numeric | | |
action_result.data.\*.identities.\*.authName | string | | |
action_result.data.\*.identities.\*.tagId | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'update identities'

Update Identities (devices or security group tags).
PUT /identities/registrations/{type}. Pass 1-250 identity objects as JSON array in identities_json.
https://developer.cisco.com/docs/cloud-security/update-identities/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**type** | required | Identity type: 'device' for identity endpoints, 'securityGroupTag' for SGTs. | string | |
**identities_json** | required | JSON array of identity objects (1-250). Devices: {"key","label","status","authName"}. SGTs: {"key","label","status","tagId"}. status: "active"|"inactive". | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.type | string | | |
action_result.parameter.identities_json | string | | |
action_result.data.\*.success | boolean | | True False |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list certificates for device'

List Certificates for Device (ZTNA).
GET /ztna/users/{userId}/devices/{deviceId}/certificates. Returns ACME-issued certificate info for the user device.
https://developer.cisco.com/docs/cloud-security/list-certificates-for-device/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_id** | required | The ID of the user (ZTNA). | string | |
**device_id** | required | The ID of the user device. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.user_id | string | | |
action_result.parameter.device_id | string | | |
action_result.data.\*.deviceId | string | | |
action_result.data.\*.certificates.\*.certificateId | string | | |
action_result.data.\*.certificates.\*.status | string | | |
action_result.data.\*.certificates.\*.createdAt | string | | |
action_result.data.\*.certificates.\*.expiresAt | string | | |
action_result.data.\*.certificates.\*.revokedAt | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list certificates for user'

List Certificates for User (ZTNA).
GET /ztna/users/{userId}/deviceCertificates. Returns all device certificates for the zero trust user.
https://developer.cisco.com/docs/cloud-security/list-certificates-for-user/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_id** | required | The ID of the user (ZTNA). Get all device certificates for this user. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.user_id | string | | |
action_result.data.\*.userId | string | | |
action_result.data.\*.devices.\*.deviceId | string | | |
action_result.data.\*.devices.\*.certificates.\*.certificateId | string | | |
action_result.data.\*.devices.\*.certificates.\*.status | string | | |
action_result.data.\*.devices.\*.certificates.\*.createdAt | string | | |
action_result.data.\*.devices.\*.certificates.\*.expiresAt | string | | |
action_result.data.\*.devices.\*.certificates.\*.revokedAt | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'revoke certificates for device'

Revoke Certificates for Device (ZTNA).
DELETE /ztna/users/{userId}/devices/{deviceId}. Revokes active ACME-issued certificates and removes the zero trust user device.
https://developer.cisco.com/docs/cloud-security/revoke-certificates-for-device/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_id** | required | The ID of the user (ZTNA). | string | |
**device_id** | required | The ID of the user device. Revokes active certificates and removes the device. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.user_id | string | | |
action_result.parameter.device_id | string | | |
action_result.data.\*.success | boolean | | True False |
action_result.data.\*.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get roaming computer'

Get Roaming Computer (posture/security status for a device).
GET /roamingcomputers/{deviceId}. Returns status, swgStatus, lastSync, appliedBundle, version, OS info, etc.
https://developer.cisco.com/docs/cloud-security/get-roaming-computer/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** | required | The device ID (deviceId) of the roaming computer, e.g. AB00C7DCEC99D211. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.device_id | string | | |
action_result.data.\*.originId | numeric | | |
action_result.data.\*.name | string | | |
action_result.data.\*.deviceId | string | | |
action_result.data.\*.type | string | | |
action_result.data.\*.status | string | | |
action_result.data.\*.swgStatus | string | | |
action_result.data.\*.lastSyncStatus | string | | |
action_result.data.\*.lastSyncSwgStatus | string | | |
action_result.data.\*.lastSync | string | | |
action_result.data.\*.appliedBundle | numeric | | |
action_result.data.\*.hasIpBlocking | boolean | | True False |
action_result.data.\*.version | string | | |
action_result.data.\*.osVersion | string | | |
action_result.data.\*.osVersionName | string | | |
action_result.data.\*.anyconnectDeviceId | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list roaming computers'

List all roaming computers
GET /roamingcomputers. Returns roaming computers (posture/security status) in the organization.
https://developer.cisco.com/docs/cloud-security/list-roaming-computers/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.data.\*.roamingComputers.\*.originId | numeric | | |
action_result.data.\*.roamingComputers.\*.name | string | | |
action_result.data.\*.roamingComputers.\*.deviceId | string | | |
action_result.data.\*.roamingComputers.\*.type | string | | |
action_result.data.\*.roamingComputers.\*.status | string | | |
action_result.data.\*.roamingComputers.\*.swgStatus | string | | |
action_result.data.\*.roamingComputers.\*.lastSyncStatus | string | | |
action_result.data.\*.roamingComputers.\*.lastSyncSwgStatus | string | | |
action_result.data.\*.roamingComputers.\*.lastSync | string | | |
action_result.data.\*.roamingComputers.\*.appliedBundle | numeric | | |
action_result.data.\*.roamingComputers.\*.hasIpBlocking | boolean | | True False |
action_result.data.\*.roamingComputers.\*.version | string | | |
action_result.data.\*.roamingComputers.\*.osVersion | string | | |
action_result.data.\*.roamingComputers.\*.osVersionName | string | | |
action_result.data.\*.roamingComputers.\*.anyconnectDeviceId | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list swg override device settings'

List SWG Override Device Settings.
POST deployments/v2/deviceSettings/SWGEnabled/list. Returns SWG override setting (originId, name, value, modifiedAt) for each given origin ID (1-100).
Requires deployments.devices.swg:read.
https://developer.cisco.com/docs/cloud-security/list-swg-override-device-settings/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**origin_ids** | required | Comma-separated origin IDs of devices (1-100) to list SWG override settings for. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.origin_ids | string | | |
action_result.data.\*.settings.\*.originId | numeric | | |
action_result.data.\*.settings.\*.name | string | | |
action_result.data.\*.settings.\*.value | string | | |
action_result.data.\*.settings.\*.modifiedAt | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'set swg override device settings'

Set SWG Override Device Settings.
POST deployments/v2/deviceSettings/SWGEnabled/set. Override SWG enable/disable for devices by origin ID (1-100).
Requires deployments.devices.swg:write. Devices must be registered as roaming computers.
https://developer.cisco.com/docs/cloud-security/set-swg-override-device-settings/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**value** | required | Enable (1) or disable (0) Secure Web Gateway for the devices. | string | |
**origin_ids** | required | Comma-separated origin IDs of devices (1-100). Devices must be registered as roaming computers. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.value | string | | |
action_result.parameter.origin_ids | string | | |
action_result.data.\*.totalCount | numeric | | |
action_result.data.\*.successCount | numeric | | |
action_result.data.\*.failCount | numeric | | |
action_result.data.\*.items.\*.originId | numeric | | |
action_result.data.\*.items.\*.code | numeric | | |
action_result.data.\*.items.\*.message | string | | |
action_result.data.\*.value | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'delete swg override device settings'

Delete SWG Override Device Settings.
POST deployments/v2/deviceSettings/SWGEnabled/remove. Removes the SWG override for the given devices (1-100);
organization SWG setting will apply after removal. Requires deployments.devices.swg:write.
https://developer.cisco.com/docs/cloud-security/delete-swg-override-device-settings/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**origin_ids** | required | Comma-separated origin IDs of devices (1-100) to remove SWG override setting from. Organization SWG setting will apply after removal. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.origin_ids | string | | |
action_result.data.\*.status | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list network tunnel groups'

List Network Tunnel Groups in the organization.
GET deployments/v2/networktunnelgroups. Requires deployments.networktunnelgroups:read.
https://developer.cisco.com/docs/cloud-security/list-network-tunnel-groups/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**offset** | optional | Index to start reading the collection (0-based). Default 0. | numeric | |
**limit** | optional | Number of records per page (1-200). Default 10. | numeric | |
**filters** | optional | Optional JSON object to filter by name, exactName, region, networkTunnelGroupIds, exactAuthIdPrefix, status, or duplicateCIDRs. See API docs. | string | |
**sort_by** | optional | Sort field: name, status, createdAt, modifiedAt. | string | |
**sort_order** | optional | Sort order: asc or desc. | string | |
**include_statuses** | optional | Include tunnelsStatus for each hub (max 10 tunnel states per hub). | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.offset | numeric | | |
action_result.parameter.limit | numeric | | |
action_result.parameter.filters | string | | |
action_result.parameter.sort_by | string | | |
action_result.parameter.sort_order | string | | |
action_result.parameter.include_statuses | boolean | | |
action_result.data.\*.data.\*.id | numeric | | |
action_result.data.\*.data.\*.name | string | | |
action_result.data.\*.data.\*.organizationId | numeric | | |
action_result.data.\*.data.\*.deviceType | string | | |
action_result.data.\*.data.\*.region | string | | |
action_result.data.\*.data.\*.status | string | | |
action_result.data.\*.data.\*.hubs.\*.id | numeric | | |
action_result.data.\*.data.\*.hubs.\*.name | string | | |
action_result.data.\*.data.\*.hubs.\*.status.time | string | | |
action_result.data.\*.data.\*.hubs.\*.status.status | string | | |
action_result.data.\*.data.\*.routing.type | string | | |
action_result.data.\*.data.\*.createdAt | string | | |
action_result.data.\*.data.\*.modifiedAt | string | | |
action_result.data.\*.offset | numeric | | |
action_result.data.\*.limit | numeric | | |
action_result.data.\*.total | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get network tunnel group'

Get a Network Tunnel Group by ID.
GET deployments/v2/networktunnelgroups/{id}. Requires deployments.networktunnelgroups:read.
https://developer.cisco.com/docs/cloud-security/get-network-tunnel-group/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the network tunnel group (obtain from the List Network Tunnel Groups action). | numeric | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.id | numeric | | |
action_result.data.\*.id | numeric | | |
action_result.data.\*.name | string | | |
action_result.data.\*.organizationId | numeric | | |
action_result.data.\*.deviceType | string | | |
action_result.data.\*.region | string | | |
action_result.data.\*.status | string | | |
action_result.data.\*.hubs.\*.id | numeric | | |
action_result.data.\*.hubs.\*.name | string | | |
action_result.data.\*.hubs.\*.status.time | string | | |
action_result.data.\*.hubs.\*.status.status | string | | |
action_result.data.\*.routing.type | string | | |
action_result.data.\*.createdAt | string | | |
action_result.data.\*.modifiedAt | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'create rule'

Create an access rule on the organization's Access policy.
POST policies/v2/rules. Requires policies.rules:write.
https://developer.cisco.com/docs/cloud-security/create-rule/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**rule_name** | required | Rule name (2-50 alphanumeric, hyphen, underscore, space). Unique across access rules. | string | |
**rule_action** | required | Action for the rule. | string | |
**rule_conditions_json** | required | JSON array of conditions, e.g. [{"attributeName":"umbrella.destination.all","attributeValue":true,"attributeOperator":"="},{"attributeName":"umbrella.source.all","attributeValue":true,"attributeOperator":"="}] | string | |
**rule_settings_json** | required | JSON array of settings, e.g. [{"settingName":"umbrella.default.traffic","settingValue":"PUBLIC_INTERNET"}] | string | |
**rule_description** | optional | Optional description (max 256 characters). | string | |
**rule_priority** | optional | Optional priority (positive integer, unique across rules). | numeric | |
**rule_is_enabled** | optional | Whether the rule is enabled. Default true. | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.rule_name | string | | |
action_result.parameter.rule_action | string | | |
action_result.parameter.rule_conditions_json | string | | |
action_result.parameter.rule_settings_json | string | | |
action_result.parameter.rule_description | string | | |
action_result.parameter.rule_priority | numeric | | |
action_result.parameter.rule_is_enabled | boolean | | |
action_result.data.\*.organizationId | numeric | | |
action_result.data.\*.ruleId | numeric | | |
action_result.data.\*.ruleName | string | | |
action_result.data.\*.ruleDescription | string | | |
action_result.data.\*.ruleAction | string | | |
action_result.data.\*.rulePriority | numeric | | |
action_result.data.\*.ruleIsDefault | boolean | | True False |
action_result.data.\*.ruleIsEnabled | boolean | | True False |
action_result.data.\*.ruleConditions.\*.attributeName | string | | |
action_result.data.\*.ruleConditions.\*.attributeValue | string | | |
action_result.data.\*.ruleConditions.\*.attributeOperator | string | | |
action_result.data.\*.ruleSettings.\*.settingName | string | | |
action_result.data.\*.ruleSettings.\*.settingValue | string | | |
action_result.data.\*.modifiedBy | string | | |
action_result.data.\*.modifiedAt | string | | |
action_result.data.\*.createdAt | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list firewall rules'

List access rules in the organization's Access policy.
GET policies/v2/rules. Requires policies.rules:read.
https://developer.cisco.com/docs/cloud-security/list-rules/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**offset** | optional | Index to start reading the collection (0-based). Default 0. | numeric | |
**limit** | optional | Number of rules per page. Max 1000. Default 10. | numeric | |
**rule_name** | optional | Filter by rule name or substring (e.g. 'Allow all rule'). | string | |
**filters** | optional | Optional JSON object to filter rules by properties (ruleName, ruleDescription, ruleIsEnabled, ruleAction, ruleConditions, sources, destinations, etc.). Cannot combine ruleConditions with sources/destinations. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.offset | numeric | | |
action_result.parameter.limit | numeric | | |
action_result.parameter.rule_name | string | | |
action_result.parameter.filters | string | | |
action_result.data.\*.count | numeric | | |
action_result.data.\*.firewall_rules.\*.ruleId | numeric | | |
action_result.data.\*.firewall_rules.\*.organizationId | numeric | | |
action_result.data.\*.firewall_rules.\*.ruleName | string | | |
action_result.data.\*.firewall_rules.\*.ruleDescription | string | | |
action_result.data.\*.firewall_rules.\*.ruleAction | string | | |
action_result.data.\*.firewall_rules.\*.rulePriority | numeric | | |
action_result.data.\*.firewall_rules.\*.ruleIsDefault | boolean | | True False |
action_result.data.\*.firewall_rules.\*.ruleIsEnabled | boolean | | True False |
action_result.data.\*.firewall_rules.\*.modifiedBy | string | | |
action_result.data.\*.firewall_rules.\*.modifiedAt | string | | |
action_result.data.\*.firewall_rules.\*.createdAt | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list resource connectors'

List Resource Connectors for the organization.
GET deployments/v2/connectorAgents. Requires deployments.resourceconnectors:read.
https://developer.cisco.com/docs/cloud-security/list-connectors/

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**offset** | optional | Index to start reading the collection (0-based). Default 0. | numeric | |
**limit** | optional | Maximum number of items to return. Default 10. | numeric | |
**filters** | optional | Optional JSON object to filter by groupId, instanceId, status, confirmed, hasSynced, hasLatestVersion. See API docs. | string | |
**sort_by** | optional | Sort field: instanceId, originIpAddress, createdAt, modifiedAt. | string | |
**sort_order** | optional | Sort order: asc or desc. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.offset | numeric | | |
action_result.parameter.limit | numeric | | |
action_result.parameter.filters | string | | |
action_result.parameter.sort_by | string | | |
action_result.parameter.sort_order | string | | |
action_result.data.\*.data.\*.id | numeric | | |
action_result.data.\*.data.\*.groupId | numeric | | |
action_result.data.\*.data.\*.instanceId | string | | |
action_result.data.\*.data.\*.confirmed | boolean | | True False |
action_result.data.\*.data.\*.enabled | boolean | | True False |
action_result.data.\*.data.\*.version | string | | |
action_result.data.\*.data.\*.sha1 | string | | |
action_result.data.\*.data.\*.hostname | string | | |
action_result.data.\*.data.\*.originIpAddress | string | | |
action_result.data.\*.data.\*.baseVersion | string | | |
action_result.data.\*.data.\*.isLatestBaseVersion | boolean | | True False |
action_result.data.\*.data.\*.upgradeStatus | string | | |
action_result.data.\*.data.\*.status | string | | |
action_result.data.\*.data.\*.statusUpdatedAt | string | | |
action_result.data.\*.data.\*.controlStatusUpdatedAt | string | | |
action_result.data.\*.data.\*.revoked_at | string | | |
action_result.data.\*.data.\*.createdAt | string | | |
action_result.data.\*.data.\*.modifiedAt | string | | |
action_result.data.\*.offset | numeric | | |
action_result.data.\*.limit | numeric | | |
action_result.data.\*.total | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'refresh s3 key'

Rotate the Cisco-managed S3 bucket key for the organization.
POST admin/v2/iam/rotateKey. Requires admin.iam:write.
https://developer.cisco.com/docs/cloud-security/refresh-s3-bucket-key/

Type: **generic** <br>
Read only: **False**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.data.\*.oldKeyId | string | | |
action_result.data.\*.currentKeyId | string | | |
action_result.data.\*.secretAccessKey | string | | |
action_result.data.\*.keyCreationDate | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2026 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
