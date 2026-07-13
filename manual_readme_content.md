This connector uses the Cisco Secure Access API with OAuth 2.0 client credentials.
Create an API key in Cisco Secure Access and configure the Splunk SOAR asset with
the generated client ID and client secret.

## Prerequisites

- A Cisco Secure Access tenant with access to the APIs used by the connector.
- A Cisco Secure Access API key that includes the OAuth scopes required for the
  actions you plan to run.
- Network connectivity from Splunk SOAR to the configured Cisco Secure Access API
  base URL. The default base URL is `https://api.sse.cisco.com`.
- The SOAR asset must be configured with the API key's client ID and client
  secret.

## Asset Configuration

The following asset fields are used for Cisco Secure Access authentication and
action behavior:

- **Base URL** - Cisco Secure Access API base URL. The default value is
  `https://api.sse.cisco.com`.
- **Client ID** - Client ID from the Cisco Secure Access API key.
- **Client Secret** - Client secret from the Cisco Secure Access API key.
- **Auth Header Name** - HTTP header used for the bearer token. The default
  value is `Authorization`. The connector always sends the value as
  `Bearer <token>`.
- **Default Destination List ID** - Optional destination list ID used by the
  destination list add and remove actions when an action parameter value is not
  provided.

## Cisco API Scopes

Cisco documents the required OAuth scopes in the Secure Access API reference for
each endpoint. Test Connectivity only verifies that the connector can request an
OAuth token from `/auth/v2/token`. A successful Test Connectivity result does not
guarantee that the API key has permission to run every action. If an action fails
with `401 Unauthorized` or `403 Forbidden`, verify that the API key is valid and
contains the scope listed for that action below.

### Action-Specific Scope Reference

| Action | Required Cisco OAuth Scope |
| --- | --- |
| `test connectivity` | No action API scope. Requires valid client credentials for `/auth/v2/token`. |
| `list destination lists` | `policies.destinationLists:read` |
| `list destination lists` with **list_destinations** enabled | `policies.destinationLists:read` and `policies.destinations:read` |
| `create destination list` | `policies.destinationLists:write` |
| `add to destination list` | `policies.destinations:write` |
| `remove destinations from list` | `policies.destinations:write` |
| `list managed devices` | `deployments.networkdevices:read` |
| `get network device` | `deployments.networkdevices:read` |
| `delete managed device` | `deployments.networkdevices:write` |
| `list virtual appliances` | `deployments.virtualappliances:read` |
| `list sites` | `deployments.sites:read` |
| `list roaming computers` | `deployments.roamingcomputers:read` |
| `get roaming computer` | `deployments.roamingcomputers:read` |
| `list network tunnel groups` | `deployments.networktunnelgroups:read` |
| `get network tunnel group` | `deployments.networktunnelgroups:read` |
| `list resource connectors` | `deployments.resourceconnectors:read` |
| `get domain status` | `investigate.investigate:read` |
| `get domain risk score` | `investigate.investigate:read` |
| `get passive dns` | `investigate.investigate:read` |
| `list identities` | `deployments.identities:read` |
| `update identities` | `deployments.identities:write` |
| `list certificates for device` | `admin.ztna.devices:read` |
| `list certificates for user` | `admin.ztna.users:read` |
| `make request` | Depends on the Cisco Secure Access endpoint being called. |
| `create rule` | `policies.rules:write` |
| `list firewall rules` | `policies.rules:read` |
| `list swg override device settings` | `deployments.devices.swg:read` |
| `set swg override device settings` | `deployments.devices.swg:write` |
| `delete swg override device settings` | `deployments.devices.swg:write` |
| `list vpn sessions` | `admin.vpn:read` |

## Scope Troubleshooting

- If Test Connectivity passes but a later action returns `403 Forbidden`, the
  most common cause is that the API key does not include the required action
  scope.
- If an action returns `401 Unauthorized`, verify that the client ID and client
  secret are current, copied without extra whitespace, and belong to the Cisco
  Secure Access tenant configured in the asset.
- If only write actions fail, verify that the API key includes the corresponding
  `:write` scope. A `:read` scope is not sufficient for create, update, delete,
  or remove actions.
- If `make request` fails with an authorization error, check the Cisco API
  reference for the endpoint passed in the **endpoint** parameter and add the
  scope required by that endpoint.
- If `list destination lists` succeeds but enabling **list_destinations** fails,
  verify that the API key also includes `policies.destinations:read`.

## Useful Cisco Documentation

- [Cisco Secure Access API Authentication](https://developer.cisco.com/docs/cloud-security/secure-access-api-authentication/)
- [Cisco Secure Access API Getting Started](https://developer.cisco.com/docs/cloud-security/secure-access-api-getting-started/)
- [Create Authorization Token](https://developer.cisco.com/docs/cloud-security/create-authorization-token/)
- [Destination Lists API](https://developer.cisco.com/docs/cloud-security/get-destination-lists/)
- [Network Devices API](https://developer.cisco.com/docs/cloud-security/list-network-devices/)
- [Investigate API](https://developer.cisco.com/docs/cloud-security/get-domain-status-and-categorization/)
- [Policy Rules API](https://developer.cisco.com/docs/cloud-security/list-rules/)
- [SWG Device Settings API](https://developer.cisco.com/docs/cloud-security/list-swg-override-device-settings/)
- [VPN Connections API](https://developer.cisco.com/docs/cloud-security/list-vpn-connections/)
