# Cisco Secure Access

Publisher: Splunk <br>
Connector Version: 1.0.0 <br>
Product Vendor: Cisco <br>
Product Name: Cisco Secure Access <br>
Minimum Product Version: 6.3.0

Cisco Secure Access API actions for Splunk SOAR.

### Configuration variables

This table lists the configuration variables required to operate Cisco Secure Access. These variables are specified when configuring a Cisco Secure Access asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** | optional | string | Cisco Secure Access API base URL (default: https://api.sse.cisco.com) |
**client_id** | required | string | Client ID for authentication |
**client_secret** | required | password | Client Secret key for authentication |
**auth_header_name** | optional | string | HTTP header name for the Bearer token (value is always sent as 'Bearer {token}'; default: Authorization) |
**default_destination_list_id** | optional | string | Default destination list ID to use for automated domain/URL blocking |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity <br>
[list managed devices](#action-list-managed-devices) - List registered network devices in the organization (deployments network devices / IOA platforms). <br>
[delete managed device](#action-delete-managed-device) - Remove a network device by origin ID. <br>
[get network device](#action-get-network-device) - Get a network device by origin ID. <br>
[list api keys](#action-list-api-keys) - List SSE API Keys <br>
[list virtual appliances](#action-list-virtual-appliances) - List SSE Virtual Appliances <br>
[list sites](#action-list-sites) - List all Sites in the organization (fetches all pages). <br>
[list destination lists](#action-list-destination-lists) - List Destination Lists <br>
[create destination list](#action-create-destination-list) - Create Destination List (optional initial destinations, up to 500 per request). <br>
[add to destination list](#action-add-to-destination-list) - Add to Destination List (one destination and optional comment per run). <br>
[remove destinations from list](#action-remove-destinations-from-list) - Remove from Destination List <br>
[get domain status](#action-get-domain-status) - Get Domain Status <br>
[get domain risk score](#action-get-domain-risk-score) - Get Domain Risk Score <br>
[get passive dns](#action-get-passive-dns) - Get Passive DNS <br>
[list vpn sessions](#action-list-vpn-sessions) - List VPN Sessions <br>
[terminate vpn session](#action-terminate-vpn-session) - Terminate VPN Session <br>
[list identities](#action-list-identities) - List Identities <br>
[update identities](#action-update-identities) - Update Identities (devices or security group tags). <br>
[list certificates for device](#action-list-certificates-for-device) - List Certificates for Device (ZTNA). <br>
[list certificates for user](#action-list-certificates-for-user) - List Certificates for User (ZTNA). <br>
[revoke certificates for device](#action-revoke-certificates-for-device) - Revoke Certificates for Device (ZTNA). <br>
[get roaming computer](#action-get-roaming-computer) - Get Roaming Computer (posture/security status for a device). <br>
[list roaming computers](#action-list-roaming-computers) - List Roaming Computers. <br>
[list swg override device settings](#action-list-swg-override-device-settings) - List SWG Override Device Settings. <br>
[set swg override device settings](#action-set-swg-override-device-settings) - Set SWG Override Device Settings. <br>
[delete swg override device settings](#action-delete-swg-override-device-settings) - Delete SWG Override Device Settings. <br>
[list network tunnel groups](#action-list-network-tunnel-groups) - List Network Tunnel Groups in the organization. <br>
[get network tunnel group](#action-get-network-tunnel-group) - Get a Network Tunnel Group by ID. <br>
[create rule](#action-create-rule) - Create an access rule on the organization's Access policy. <br>
[list firewall rules](#action-list-firewall-rules) - List access rules in the organization's Access policy. <br>
[list resource connectors](#action-list-resource-connectors) - List Resource Connectors for the organization. <br>
[refresh s3 key](#action-refresh-s3-key) - Rotate the Cisco-managed S3 bucket key for the organization.

## action: 'test connectivity'

Validate the asset configuration for connectivity

Type: **test** <br>
Read only: **True**

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

List registered network devices in the organization (deployments network devices / IOA platforms).

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

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**origin_id** | required | The origin ID of the network device to remove (path parameter from List Managed Devices). | numeric | |

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

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**origin_id** | required | The origin ID of the network device (path parameter from List Managed Devices). | numeric | |

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

List SSE API Keys

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

List SSE Virtual Appliances

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
action_result.data.\*.virtualAppliances.\*.internalIPs.\* | string | `ip` | |
action_result.data.\*.virtualAppliances.\*.externalIP | string | `ip` | |
action_result.data.\*.virtualAppliances.\*.hostType | string | | |
action_result.data.\*.virtualAppliances.\*.uptime | numeric | | |
action_result.data.\*.virtualAppliances.\*.version | string | | |
action_result.data.\*.virtualAppliances.\*.domains.\* | string | `domain` | |
action_result.data.\*.virtualAppliances.\*.lastSyncTime | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list sites'

List all Sites in the organization (fetches all pages).

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

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**list_destinations** | optional | List all destination lists | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.list_destinations | boolean | | True False |
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
action_result.data.\*.destinationLists.\*.destinations.\*.destination | string | `domain` | |
action_result.data.\*.destinationLists.\*.destinations.\*.comment | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'create destination list'

Create a destination list in the organization. Optional `destinations_json` can include up to 500 destination objects per request. Per Cisco Secure Access, there is no support for global destination lists on create: the connector always sends `isGlobal` **false** and `bundleTypeId` **2**; those fields are not playbook parameters. Requires OAuth scope `policies.destinationLists:write`. See [Create Destination List](https://developer.cisco.com/docs/cloud-security/create-destination-list/).

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** | required | Name of the destination list. | string | |
**access** | required | Access classification: allow, block, url_proxy, no_decrypt, warn, none, thirdparty_block. | string | |
**destinations_json** | optional | JSON array of up to 500 objects: destination (domain, URL, or IPv4 string), type (domain, url, or ipv4), optional comment. | string | |

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
action_result.data.\*.destinationList.destinations.\*.destination | string | `domain` | |
action_result.data.\*.destinationList.destinations.\*.comment | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'add to destination list'

Add to Destination List (one destination and optional comment per run).

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
action_result.parameter.destination | string | `domain` | |
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
action_result.data.\*.destinationList.destinations.\*.destination | string | `domain` | |
action_result.data.\*.destinationList.destinations.\*.comment | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'remove destinations from list'

Remove from Destination List

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
action_result.data.\*.destinationList.destinations.\*.destination | string | `domain` | |
action_result.data.\*.destinationList.destinations.\*.comment | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get domain status'

Get Domain Status

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | The domain to get. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.domain | string | `domain` | |
action_result.data.\*.domain | string | `domain` | |
action_result.data.\*.status | numeric | | |
action_result.data.\*.status_description | string | | |
action_result.data.\*.security_categories.\* | string | | |
action_result.data.\*.content_categories.\* | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get domain risk score'

Get Domain Risk Score

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | The domain to get. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.domain | string | `domain` | |
action_result.data.\*.risk_score | numeric | | |
action_result.data.\*.indicators.\*.indicator | string | | |
action_result.data.\*.indicators.\*.normalized_score | numeric | | |
action_result.data.\*.indicators.\*.score | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get passive dns'

Get Passive DNS

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | The domain to get. | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.domain | string | `domain` | |
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
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list vpn sessions'

List VPN Sessions

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
action_result.data.\*.vpn_sessions.\*.assignedIp | string | `ip` | |
action_result.data.\*.vpn_sessions.\*.assignedIpv6 | string | `ip` | |
action_result.data.\*.vpn_sessions.\*.publicIp | string | `ip` | |
action_result.data.\*.vpn_sessions.\*.sessionId | string | | |
action_result.data.\*.vpn_sessions.\*.loginTime | string | | |
action_result.data.\*.vpn_sessions.\*.profileName | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'terminate vpn session'

Terminate VPN Session

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**profile_name** | optional | The profile name to terminate the VPN session for. | string | |
**region** | optional | The region to terminate the VPN session for. | string | |
**sessions** | optional | The sessions to terminate the VPN session for. | string | |
**usernames** | optional | The usernames to terminate the VPN session for. | string | |

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

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**type** | required | The type of identities to list. | string | |

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

List Roaming Computers.

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
action_result.parameter.include_statuses | boolean | | True False |
action_result.data.\*.data.\*.id | numeric | | |
action_result.data.\*.data.\*.name | string | | |
action_result.data.\*.data.\*.organizationId | numeric | | |
action_result.data.\*.data.\*.deviceType | string | | |
action_result.data.\*.data.\*.region | string | | |
action_result.data.\*.data.\*.status | string | | |
action_result.data.\*.data.\*.createdAt | string | | |
action_result.data.\*.data.\*.modifiedAt | string | | |
action_result.data.\*.data.\*.hubs.\*.id | numeric | | |
action_result.data.\*.data.\*.hubs.\*.name | string | | |
action_result.data.\*.data.\*.hubs.\*.status.time | string | | |
action_result.data.\*.data.\*.hubs.\*.status.status | string | | |
action_result.data.\*.data.\*.routing.type | string | | |
action_result.data.\*.offset | numeric | | |
action_result.data.\*.limit | numeric | | |
action_result.data.\*.total | numeric | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get network tunnel group'

Get a Network Tunnel Group by ID.

Type: **generic** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | The ID of the Network Tunnel Group. | numeric | |

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
action_result.data.\*.createdAt | string | | |
action_result.data.\*.modifiedAt | string | | |
action_result.data.\*.hubs.\*.id | numeric | | |
action_result.data.\*.hubs.\*.name | string | | |
action_result.data.\*.hubs.\*.status.time | string | | |
action_result.data.\*.hubs.\*.status.status | string | | |
action_result.data.\*.routing.type | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'create rule'

Create an access rule on the organization's Access policy.

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
action_result.parameter.rule_is_enabled | boolean | | True False |
action_result.data.\*.organizationId | numeric | | |
action_result.data.\*.ruleId | numeric | | |
action_result.data.\*.ruleName | string | | |
action_result.data.\*.ruleDescription | string | | |
action_result.data.\*.ruleAction | string | | |
action_result.data.\*.rulePriority | numeric | | |
action_result.data.\*.ruleIsDefault | boolean | | True False |
action_result.data.\*.ruleIsEnabled | boolean | | True False |
action_result.data.\*.modifiedBy | string | | |
action_result.data.\*.modifiedAt | string | | |
action_result.data.\*.createdAt | string | | |
action_result.data.\*.ruleConditions.\*.attributeName | string | | |
action_result.data.\*.ruleConditions.\*.attributeValue | string | | |
action_result.data.\*.ruleConditions.\*.attributeOperator | string | | |
action_result.data.\*.ruleSettings.\*.settingName | string | | |
action_result.data.\*.ruleSettings.\*.settingValue | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list firewall rules'

List access rules in the organization's Access policy.

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
action_result.data.\*.data.\*.originIpAddress | string | `ip` | |
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
