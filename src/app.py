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

import json
from soar_sdk.app import App
from soar_sdk.asset import BaseAsset
from soar_sdk.asset import AssetField
from soar_sdk.params import Params
from soar_sdk.logging import getLogger

from .params import (
    AddToDestinationListParams,
    CreateDestinationListParams,
    CreateRuleParams,
    DeleteManagedDeviceParams,
    DeleteSWGOverrideDeviceSettingsParams,
    GetNetworkDeviceParams,
    ListDestinationListsParams,
    ListIdentitiesParams,
    ListCertificatesForDeviceParams,
    ListCertificatesForUserParams,
    ListSWGOverrideDeviceSettingsParams,
    RevokeCertificatesForDeviceParams,
    GetRoamingComputerParams,
    RemoveDestinationsFromListParams,
    GetDomainParams,
    SetSWGOverrideDeviceSettingsParams,
    TerminateVPNSessionParams,
    UpdateIdentitiesParams,
    ListFirewallRulesParams,
    ListNetworkTunnelGroupsParams,
    GetNetworkTunnelGroupParams,
    ListResourceConnectorsParams,
)
from .sse_api_client import SSE_API

from .outputs import (
    ListIdentitiesOutput,
    ListCertificatesForDeviceOutput,
    ListCertificatesForUserOutput,
    RevokeCertificatesForDeviceOutput,
    GetRoamingComputerOutput,
    ListRoamingComputersOutput,
    ListManagedDevicesOutput,
    GetNetworkDeviceOutput,
    DeleteManagedDeviceOutput,
    ListAPIKeysOutput,
    ListVPNSessionsOutput,
    ListVirtualAppliancesOutput,
    ListSitesOutput,
    ListDestinationListsOutput,
    AddToDestinationListOutput,
    CreateDestinationListOutput,
    RemoveDestinationsFromListOutput,
    GetDomainStatusOutput,
    GetDomainRiskScoreOutput,
    GetPassiveDNSOutput,
    TerminateVPNSessionOutput,
    UpdateIdentitiesOutput,
    ListFirewallRulesOutput,
    CreateRuleOutput,
    ListNetworkTunnelGroupsOutput,
    GetNetworkTunnelGroupOutput,
    ListResourceConnectorsOutput,
    RefreshS3KeyOutput,
    ListSWGOverrideDeviceSettingsOutput,
    SetSWGOverrideDeviceSettingsOutput,
    DeleteSWGOverrideDeviceSettingsOutput,
)

logger = getLogger()

# Pagination / validation limits
MAX_LIMIT_NETWORK_TUNNEL_GROUPS = 200
MAX_LIMIT_FIREWALL_RULES = 1000
MAX_LIMIT_RESOURCE_CONNECTORS = 100
MAX_IDENTITIES_UPDATE = 250
MAX_SWG_ORIGIN_IDS = 100
MAX_DESTINATIONS_CREATE_DESTINATION_LIST = 500
_DESTINATION_CREATE_TYPES = frozenset({"domain", "url", "ipv4"})

# Domain status code -> human-readable description
DOMAIN_STATUS_DESCRIPTIONS = {-1: "Malicious", 1: "Benign", 0: "Unclassified"}


def _parse_json_param(value: str, param_name: str, *, allow_list: bool = False):
    """Parse a JSON string; raise ValueError with param_name in message. If allow_list, require a list."""
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as e:
        raise ValueError(f"{param_name} must be valid JSON: {e}") from e
    if allow_list and not isinstance(parsed, list):
        raise ValueError(f"{param_name} must be a JSON array")
    return parsed


def _parse_optional_filters(params) -> dict | None:
    """Return parsed filters dict from params.filters, or None if missing/empty."""
    raw = getattr(params, "filters", None)
    if not raw or not str(raw).strip():
        return None
    return _parse_json_param(str(raw).strip(), "filters")


def _clamp_offset_limit(params, max_limit: int) -> tuple[int, int]:
    """Return (offset, limit) clamped to valid range; limit capped by max_limit."""
    offset = max(0, params.offset)
    limit = min(max(1, params.limit), max_limit)
    return offset, limit


def _output_from_api_data(OutputModel, data: dict):
    """Build OutputModel instance from API dict, keeping only keys that exist on the model."""
    fields = getattr(OutputModel, "model_fields", None) or getattr(
        OutputModel, "__fields__", {}
    )
    return OutputModel(**{k: data[k] for k in data if k in fields})


def _parse_comma_list(s: str) -> list[str]:
    """Split comma-separated string into non-empty stripped strings."""
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def _destinations_for_create_destination_list(
    destinations_json: str | None,
) -> list[dict] | None:
    """
    Parse and validate destinations_json for POST /destinationlists.
    Returns a list suitable for the API body, or None if omitted/blank.
    """
    if destinations_json is None or not str(destinations_json).strip():
        return None
    parsed = _parse_json_param(
        str(destinations_json).strip(), "destinations_json", allow_list=True
    )
    if len(parsed) > MAX_DESTINATIONS_CREATE_DESTINATION_LIST:
        raise ValueError(
            f"destinations_json must contain at most "
            f"{MAX_DESTINATIONS_CREATE_DESTINATION_LIST} destinations"
        )
    out: list[dict] = []
    for i, item in enumerate(parsed):
        if not isinstance(item, dict):
            raise ValueError(f"destinations_json[{i}] must be a JSON object")
        dest = item.get("destination")
        typ = item.get("type")
        if dest is None or typ is None:
            raise ValueError(
                f"destinations_json[{i}] must include destination and type fields"
            )
        dest_s = str(dest).strip()
        typ_s = str(typ).strip()
        if not dest_s:
            raise ValueError(f"destinations_json[{i}] destination must be non-empty")
        if typ_s not in _DESTINATION_CREATE_TYPES:
            raise ValueError(
                f"destinations_json[{i}] type must be one of: "
                f"{', '.join(sorted(_DESTINATION_CREATE_TYPES))}"
            )
        row: dict = {"destination": dest_s, "type": typ_s}
        if item.get("comment") is not None:
            row["comment"] = str(item["comment"])
        out.append(row)
    return out


def _normalize_destination_for_match(value: str) -> str:
    return (value or "").strip().lower()


def _find_added_destination_row(
    rows: list,
    *,
    destination: str,
    comment: str | None,
) -> dict | None:
    """
    After POST add, the API returns only list metadata. Match the new row from
    GET destinations by destination string (and comment when unique).
    """
    if not isinstance(rows, list) or not rows:
        return None
    want = _normalize_destination_for_match(destination)
    matches_dest: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if _normalize_destination_for_match(str(row.get("destination") or "")) != want:
            continue
        matches_dest.append(row)
    if not matches_dest:
        return None
    if comment is not None:
        with_comment = [r for r in matches_dest if (r.get("comment") or "") == comment]
        if with_comment:
            matches_dest = with_comment

    def created_at_key(r: dict) -> str:
        return str(r.get("createdAt") or "")

    return sorted(matches_dest, key=created_at_key, reverse=True)[0]


def _parse_origin_ids(s: str, max_count: int = MAX_SWG_ORIGIN_IDS) -> list[int]:
    """Parse comma-separated origin IDs; validate count 1..max_count and that each is an integer."""
    parts = _parse_comma_list(s)
    if len(parts) < 1:
        raise ValueError("origin_ids must contain at least one origin ID")
    if len(parts) > max_count:
        raise ValueError(f"origin_ids must contain at most {max_count} origin IDs")
    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            raise ValueError(
                f"origin_ids must be comma-separated integers; invalid: {p!r}"
            ) from None
    return result


def flatten_field(obj_list, field_name, separator="."):
    """
    Flatten a nested dict field into top-level keys on each object in the list.
    Modifies obj_list in place. Skips objects that lack field_name or where value is not a dict.
    """
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
                logger.warning(
                    "can't flatten_field %s because object already has key", key
                )
                continue
            obj[key] = value
    return obj_list


class Asset(BaseAsset):
    base_url: str = AssetField(default="https://api.sse.cisco.com")
    client_id: str = AssetField(
        sensitive=False, description="Client ID for authentication"
    )
    client_secret: str = AssetField(
        sensitive=True, description="Client Secret key for authentication"
    )
    auth_header_name: str = AssetField(
        default="Authorization",
        description="HTTP header name for the Bearer token (value is always sent as 'Bearer {token}')",
    )
    default_destination_list_id: str = AssetField(
        description="Default destination list ID to use for automated domain/URL blocking",
        required=False,
    )

    def get_client(self) -> SSE_API:
        return SSE_API(
            self.base_url,
            self.client_id,
            self.client_secret,
            auth_header_name=self.auth_header_name,
        )


app = App(
    name="Cisco Secure Access",
    app_type="corrective",
    logo="logo_cisco.svg",
    logo_dark="logo_cisco_dark.svg",
    product_vendor="Cisco",
    product_name="Cisco Secure Access",
    publisher="Splunk Inc.",
    appid="48ce45b2-0de5-474f-be52-8266350325cd",
    fips_compliant=False,
    asset_cls=Asset,
)


@app.test_connectivity()
def test_connectivity(asset: Asset) -> None:
    """
    Test connectivity against the Cisco Secure Access API.
    Get a token to ensure connectivity, and valid configuration.
    https://developer.cisco.com/docs/cloud-security/create-authorization-token/
    """
    logger.info(f"testing connectivity against {asset.base_url}")
    client = asset.get_client()
    logger.info("created SSE API client successfully")
    logger.info("querying valid ioa platforms to ensure connectivity")
    if client.GetToken():
        logger.info("Connection success")
    else:
        raise Exception("Unable to get auth token")


@app.action()
def list_managed_devices(params: Params, asset: Asset) -> ListManagedDevicesOutput:
    """
    List all valid IOA platforms.
    https://developer.cisco.com/docs/cloud-security/list-network-devices/
    """
    logger.info("listing valid IOA platforms")
    client = asset.get_client()
    devices = client.ListNetworkDevices()
    logger.info(f"got devices {devices}")
    # Parse the devices list
    return ListManagedDevicesOutput(devices=devices)


@app.action()
def delete_managed_device(
    params: DeleteManagedDeviceParams, asset: Asset
) -> DeleteManagedDeviceOutput:
    """
    Remove a network device by origin ID.
    DELETE deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:write.
    https://developer.cisco.com/docs/cloud-security/delete-network-device/
    """
    logger.info("deleting network device by origin_id=%s", params.origin_id)
    client = asset.get_client()
    data = client.DeleteNetworkDevice(params.origin_id)
    logger.info("delete_managed_device result %s", data)
    return DeleteManagedDeviceOutput(
        success=data.get("success", True), message=data.get("message")
    )


@app.action()
def get_network_device(
    params: GetNetworkDeviceParams, asset: Asset
) -> GetNetworkDeviceOutput:
    """
    Get a network device by origin ID.
    GET deployments/v2/networkdevices/{originId}. Requires deployments.networkdevices:read.
    https://developer.cisco.com/docs/cloud-security/get-network-device/
    """
    logger.info("Getting network device origin_id=%s", params.origin_id)
    client = asset.get_client()
    data = client.GetNetworkDevice(params.origin_id)
    logger.info("get_network_device result originId=%s", data.get("originId"))
    return _output_from_api_data(GetNetworkDeviceOutput, data)


@app.action()
def list_api_keys(params: Params, asset: Asset) -> ListAPIKeysOutput:
    """
    List SSE API Keys
    https://developer.cisco.com/docs/cloud-security/list-api-keys/
    """
    logger.info("Listing API Keys")
    client = asset.get_client()
    api_keys = client.ListApiKeys()
    logger.info(f"got API Keys {api_keys}")
    # TODO Parse API Keys list
    if isinstance(api_keys, dict) and "keys" in api_keys:
        return ListAPIKeysOutput(
            keys=api_keys.get("keys", []),
            message=api_keys.get("message"),
            offset=api_keys.get("offset"),
            limit=api_keys.get("limit"),
            total=api_keys.get("total"),
        )
    return ListAPIKeysOutput(keys=[])


@app.action()
def list_virtual_appliances(
    params: Params, asset: Asset
) -> ListVirtualAppliancesOutput:
    """
    List SSE Virtual Appliances
    https://developer.cisco.com/docs/cloud-security/list-virtual-appliances/
    """
    logger.info("Listing Virtual Appliances")
    client = asset.get_client()
    virtual_appliances = client.ListVirtualAppliances()
    # Flatten `state` and `settings` dicts into scalar/list fields for SOAR outputs
    for va in virtual_appliances or []:
        state = va.get("state")
        if isinstance(state, dict):
            va["state_syncing"] = state.get("syncing")
            # remove nested object to avoid schema/type issues
            va.pop("state", None)

        settings = va.get("settings")
        if isinstance(settings, dict):
            va["internalIPs"] = settings.get("internalIPs")
            va["externalIP"] = settings.get("externalIP")
            va["hostType"] = settings.get("hostType")
            va["uptime"] = settings.get("uptime")
            va["version"] = settings.get("version")
            va["domains"] = settings.get("domains")
            va["lastSyncTime"] = settings.get("lastSyncTime")
            # remove nested object to avoid schema/type issues
            va.pop("settings", None)
    logger.info(f"got Virtual Appliances {virtual_appliances}")
    output = ListVirtualAppliancesOutput(virtualAppliances=virtual_appliances)
    return output


@app.action()
def list_sites(params: Params, asset: Asset) -> ListSitesOutput:
    """
    List all Sites in the organization (fetches all pages).
    GET deployments/v2/sites. Requires deployments.sites:read.
    https://developer.cisco.com/docs/cloud-security/list-sites/
    """
    logger.info("Listing sites (all pages)")
    client = asset.get_client()
    sites = client.ListSites()
    if not isinstance(sites, list):
        sites = [sites] if sites is not None else []
    logger.info("got sites count=%s", len(sites))
    return ListSitesOutput(sites=sites)


@app.action()
def list_destination_lists(
    params: ListDestinationListsParams, asset: Asset
) -> ListDestinationListsOutput:
    """
    List Destination Lists
    https://developer.cisco.com/docs/cloud-security/get-destination-lists/
    """
    logger.info("Listing Destination Lists")
    client = asset.get_client()
    destination_lists = client.ListDestinationLists()
    logger.info(f"got Destination Lists {destination_lists}")
    destination_lists = flatten_field(
        destination_lists, "meta"
    )  # flatten meta field into meta.* fields
    destination_lists_output = []
    if params.list_destinations:
        for destination_list in destination_lists:
            destinations = client.GetDestinationsFromListById(destination_list["id"])
            destination_list["destinations"] = destinations
            destination_lists_output.append(destination_list)
    else:
        destination_lists_output = destination_lists
    return ListDestinationListsOutput(destinationLists=destination_lists_output)


@app.action()
def create_destination_list(
    params: CreateDestinationListParams, asset: Asset
) -> CreateDestinationListOutput:
    """
    Create a destination list in the organization (optional initial destinations).
    POST policies/v2/destinationlists. Requires policies.destinationLists:write.
    Secure Access does not support global destination lists on create; the request always sets isGlobal to false.
    https://developer.cisco.com/docs/cloud-security/create-destination-list/
    """
    name = params.name.strip()
    if not name:
        raise ValueError("name must be a non-empty string")

    destinations = _destinations_for_create_destination_list(params.destinations_json)
    body: dict = {
        "access": params.access,
        "isGlobal": False,
        "name": name,
        "bundleTypeId": 2,
    }
    if destinations:
        body["destinations"] = destinations

    logger.info("Creating destination list name=%r access=%s", name, params.access)
    client = asset.get_client()
    raw = client.CreateDestinationList(body)
    if not isinstance(raw, dict):
        raise ValueError("Unexpected API response for create destination list")
    data = raw.get("data", raw)
    if not isinstance(data, dict):
        raise ValueError("Unexpected API response data for create destination list")
    if data.get("meta") is not None:
        data = flatten_field([data], "meta")[0]
    logger.info("Created destination list id=%s", data.get("id"))
    return CreateDestinationListOutput(destinationList=data)


@app.action()
def add_to_destination_list(
    params: AddToDestinationListParams, asset: Asset
) -> AddToDestinationListOutput:
    """
    Add to Destination List (one destination and optional comment per run).
    https://developer.cisco.com/docs/cloud-security/add-destinations-to-destination-list/
    """
    logger.info("Adding to Destination List")
    client = asset.get_client()
    destination_list_id = (
        params.destination_list_id
        if params.destination_list_id
        else asset.default_destination_list_id
    )
    if not destination_list_id:
        raise ValueError("Destination list ID is required")
    destination_list_response = client.AddToDestinationList(
        destination_list_id, params.destination, params.comment
    )
    destination_list = destination_list_response["data"]
    if isinstance(destination_list, dict) and destination_list.get("meta") is not None:
        destination_list = flatten_field([destination_list], "meta")[0]
    added_row: dict | None = None
    added_id: str | None = None
    raw_destinations = client.GetDestinationsFromListById(destination_list_id)
    dest_rows = raw_destinations if isinstance(raw_destinations, list) else []
    added_row = _find_added_destination_row(
        dest_rows,
        destination=params.destination,
        comment=params.comment,
    )
    if added_row and added_row.get("id") is not None:
        added_id = str(added_row["id"])
        destination_list = {**destination_list, "destinations": [added_row]}
    else:
        logger.warning(
            "Could not resolve added destination entry id for list %s; "
            "use list_destination_lists with list_destinations=true to inspect rows",
            destination_list_id,
        )
    logger.info(f"added to Destination List {destination_list}")
    return AddToDestinationListOutput(
        destinationList=destination_list, addedDestinationId=added_id
    )


@app.action()
def remove_destinations_from_list(
    params: RemoveDestinationsFromListParams, asset: Asset
) -> RemoveDestinationsFromListOutput:
    """
    Remove from Destination List
    https://developer.cisco.com/docs/cloud-security/delete-destinations-from-destination-list/
    """
    logger.info("Removing from Destination List")
    client = asset.get_client()
    destination_list_id = (
        params.destination_list_id
        if params.destination_list_id
        else asset.default_destination_list_id
    )
    if not destination_list_id:
        raise ValueError("Destination list ID is required")
    destination_ids = _parse_comma_list(params.destination_ids)
    destination_list_response = client.RemoveDestinationsFromList(
        destination_list_id, destination_ids
    )
    logger.info(f"removed from Destination List {destination_list_response}")
    return RemoveDestinationsFromListOutput(destinationList=destination_list_response)


@app.action()
def get_domain_status(params: GetDomainParams, asset: Asset) -> GetDomainStatusOutput:
    """
    Get Domain Status
    https://developer.cisco.com/docs/cloud-security/get-domain-status-and-categorization/
    """
    logger.info("Getting Domain Status")
    client = asset.get_client()
    domain = params.domain
    domain_status_response = client.GetDomainStatus(domain)
    logger.info(f"got Domain Status {domain_status_response}")
    domain_status_object = domain_status_response[
        domain
    ]  # get the domain status object
    domain_status_object["domain"] = domain  # add domain to object
    domain_status_object["status_description"] = DOMAIN_STATUS_DESCRIPTIONS.get(
        domain_status_object.get("status"), "Unknown"
    )
    return GetDomainStatusOutput(**domain_status_object)


@app.action()
def get_domain_risk_score(
    params: GetDomainParams, asset: Asset
) -> GetDomainRiskScoreOutput:
    """
    Get Domain Risk Score
    https://developer.cisco.com/docs/cloud-security/get-risk-score-for-domain/
    """
    logger.info("Getting Domain Risk Score")
    client = asset.get_client()
    domain = params.domain
    domain_risk_score_response = client.GetDomainRiskScore(domain)
    logger.info(f"got Domain Risk Score {domain_risk_score_response}")
    return GetDomainRiskScoreOutput(**domain_risk_score_response)


@app.action()
def get_passive_dns(params: GetDomainParams, asset: Asset) -> GetPassiveDNSOutput:
    """
    Get Passive DNS
    https://developer.cisco.com/docs/cloud-security/get-resource-records-for-name/
    """
    logger.info("Getting Passive DNS")
    client = asset.get_client()
    domain = params.domain
    passive_dns_response = client.GetPassiveDNS(domain)
    logger.info(f"got Passive DNS {passive_dns_response}")
    return GetPassiveDNSOutput(passive_dns_records=passive_dns_response)


@app.action()
def list_vpn_sessions(params: Params, asset: Asset) -> ListVPNSessionsOutput:
    """
    List VPN Sessions
    https://developer.cisco.com/docs/cloud-security/list-vpn-connections/
    """
    logger.info("Listing VPN Sessions")
    client = asset.get_client()
    vpn_sessions = client.ListVPNSessions()
    logger.info(f"got VPN Sessions {vpn_sessions}")
    return ListVPNSessionsOutput(vpn_sessions=vpn_sessions)


@app.action()
def terminate_vpn_session(
    params: TerminateVPNSessionParams, asset: Asset
) -> TerminateVPNSessionOutput:
    """
    Terminate VPN Session
    https://developer.cisco.com/docs/cloud-security/disconnect-vpn-users/
    """
    logger.info("Terminating VPN Session")
    usernames = _parse_comma_list(params.usernames)
    sessions = _parse_comma_list(params.sessions)
    client = asset.get_client()
    terminate_vpn_session_response = client.TerminateVPNSession(
        params.profile_name, params.region, sessions, usernames
    )
    logger.info(f"terminated VPN Session {terminate_vpn_session_response}")
    return TerminateVPNSessionOutput(**terminate_vpn_session_response)


@app.action()
def list_identities(params: ListIdentitiesParams, asset: Asset) -> ListIdentitiesOutput:
    """
    List Identities
    https://developer.cisco.com/docs/cloud-security/list-identities/
    """
    logger.info("Listing Identities")
    client = asset.get_client()
    identities = client.ListIdentities(params.type)
    logger.info(f"got Identities {identities}")
    return ListIdentitiesOutput(identities=identities)


@app.action()
def update_identities(
    params: UpdateIdentitiesParams, asset: Asset
) -> UpdateIdentitiesOutput:
    """
    Update Identities (devices or security group tags).
    PUT /identities/registrations/{type}. Pass 1-250 identity objects as JSON array in identities_json.
    https://developer.cisco.com/docs/cloud-security/update-identities/
    """
    logger.info("Updating Identities")
    client = asset.get_client()
    identity_type = params.type.strip().lower()
    if identity_type not in ("device", "securitygrouptag"):
        raise ValueError("type must be 'device' or 'securityGroupTag'")
    if identity_type == "securitygrouptag":
        identity_type = "securityGroupTag"
    identities_list = _parse_json_param(
        params.identities_json, "identities_json", allow_list=True
    )
    if len(identities_list) < 1 or len(identities_list) > MAX_IDENTITIES_UPDATE:
        raise ValueError("identities_json must contain 1-250 items")
    data = client.UpdateIdentities(identity_type, identities_list)
    logger.info(f"Update Identities result {data}")
    return UpdateIdentitiesOutput(success=data.get("success"))


@app.action()
def list_certificates_for_device(
    params: ListCertificatesForDeviceParams, asset: Asset
) -> ListCertificatesForDeviceOutput:
    """
    List Certificates for Device (ZTNA).
    GET /ztna/users/{userId}/devices/{deviceId}/certificates. Returns ACME-issued certificate info for the user device.
    https://developer.cisco.com/docs/cloud-security/list-certificates-for-device/
    """
    logger.info("Listing certificates for device")
    client = asset.get_client()
    data = client.ListCertificatesForDevice(params.user_id, params.device_id)
    logger.info(f"got certificates for device {data}")
    return ListCertificatesForDeviceOutput(
        deviceId=data.get("deviceId"),
        certificates=data.get("certificates"),
    )


@app.action()
def list_certificates_for_user(
    params: ListCertificatesForUserParams, asset: Asset
) -> ListCertificatesForUserOutput:
    """
    List Certificates for User (ZTNA).
    GET /ztna/users/{userId}/deviceCertificates. Returns all device certificates for the zero trust user.
    https://developer.cisco.com/docs/cloud-security/list-certificates-for-user/
    """
    logger.info("Listing certificates for user")
    client = asset.get_client()
    data = client.ListCertificatesForUser(params.user_id)
    logger.info(f"got certificates for user {data}")
    return ListCertificatesForUserOutput(
        userId=data.get("userId"),
        devices=data.get("devices"),
    )


@app.action()
def revoke_certificates_for_device(
    params: RevokeCertificatesForDeviceParams, asset: Asset
) -> RevokeCertificatesForDeviceOutput:
    """
    Revoke Certificates for Device (ZTNA).
    DELETE /ztna/users/{userId}/devices/{deviceId}. Revokes active ACME-issued certificates and removes the zero trust user device.
    https://developer.cisco.com/docs/cloud-security/revoke-certificates-for-device/
    """
    logger.info("Revoking certificates for device")
    client = asset.get_client()
    data = client.RevokeCertificatesForDevice(params.user_id, params.device_id)
    logger.info(f"revoke result {data}")
    return RevokeCertificatesForDeviceOutput(
        success=data.get("success"),
        message=data.get("message"),
    )


@app.action()
def get_roaming_computer(
    params: GetRoamingComputerParams, asset: Asset
) -> GetRoamingComputerOutput:
    """
    Get Roaming Computer (posture/security status for a device).
    GET /roamingcomputers/{deviceId}. Returns status, swgStatus, lastSync, appliedBundle, version, OS info, etc.
    https://developer.cisco.com/docs/cloud-security/get-roaming-computer/
    """
    logger.info("Getting roaming computer")
    client = asset.get_client()
    data = client.GetRoamingComputer(params.device_id)
    logger.info(f"got roaming computer {data}")
    return _output_from_api_data(GetRoamingComputerOutput, data)


@app.action()
def list_roaming_computers(params: Params, asset: Asset) -> ListRoamingComputersOutput:
    """
    List Roaming Computers.
    GET /roamingcomputers. Returns all roaming computers (posture/security status) in the organization.
    https://developer.cisco.com/docs/cloud-security/list-roaming-computers/
    """
    logger.info("Listing roaming computers")
    client = asset.get_client()
    data = client.ListRoamingComputers()
    if not isinstance(data, list):
        data = []
    logger.info(f"got {len(data)} roaming computers")
    return ListRoamingComputersOutput(roamingComputers=data)


@app.action()
def list_swg_override_device_settings(
    params: ListSWGOverrideDeviceSettingsParams, asset: Asset
) -> ListSWGOverrideDeviceSettingsOutput:
    """
    List SWG Override Device Settings.
    POST deployments/v2/deviceSettings/SWGEnabled/list. Returns SWG override setting (originId, name, value, modifiedAt) for each given origin ID (1-100).
    Requires deployments.devices.swg:read.
    https://developer.cisco.com/docs/cloud-security/list-swg-override-device-settings/
    """
    logger.info("Listing SWG override device settings")
    origin_ids = _parse_origin_ids(params.origin_ids)
    client = asset.get_client()
    data = client.ListSWGOverrideDeviceSettings(origin_ids)
    if not isinstance(data, list):
        data = []
    logger.info("list_swg_override_device_settings returned %s items", len(data))
    return ListSWGOverrideDeviceSettingsOutput(settings=data)


@app.action()
def set_swg_override_device_settings(
    params: SetSWGOverrideDeviceSettingsParams, asset: Asset
) -> SetSWGOverrideDeviceSettingsOutput:
    """
    Set SWG Override Device Settings.
    POST deployments/v2/deviceSettings/SWGEnabled/set. Override SWG enable/disable for devices by origin ID (1-100).
    Requires deployments.devices.swg:write. Devices must be registered as roaming computers.
    https://developer.cisco.com/docs/cloud-security/set-swg-override-device-settings/
    """
    logger.info("Setting SWG override device settings value=%s", params.value)
    origin_ids = _parse_origin_ids(params.origin_ids)
    client = asset.get_client()
    data = client.SetSWGOverrideDeviceSettings(params.value, origin_ids)
    logger.info(
        "set_swg_override_device_settings totalCount=%s successCount=%s failCount=%s",
        data.get("totalCount"),
        data.get("successCount"),
        data.get("failCount"),
    )
    return _output_from_api_data(SetSWGOverrideDeviceSettingsOutput, data)


@app.action()
def delete_swg_override_device_settings(
    params: DeleteSWGOverrideDeviceSettingsParams, asset: Asset
) -> DeleteSWGOverrideDeviceSettingsOutput:
    """
    Delete SWG Override Device Settings.
    POST deployments/v2/deviceSettings/SWGEnabled/remove. Removes the SWG override for the given devices (1-100);
    organization SWG setting will apply after removal. Requires deployments.devices.swg:write.
    https://developer.cisco.com/docs/cloud-security/delete-swg-override-device-settings/
    """
    logger.info("Deleting SWG override device settings")
    origin_ids = _parse_origin_ids(params.origin_ids)
    client = asset.get_client()
    data = client.DeleteSWGOverrideDeviceSettings(origin_ids)
    logger.info(
        "delete_swg_override_device_settings completed status=%s", data.get("status")
    )
    return _output_from_api_data(DeleteSWGOverrideDeviceSettingsOutput, data)


@app.action()
def list_network_tunnel_groups(
    params: ListNetworkTunnelGroupsParams, asset: Asset
) -> ListNetworkTunnelGroupsOutput:
    """
    List Network Tunnel Groups in the organization.
    GET deployments/v2/networktunnelgroups. Requires deployments.networktunnelgroups:read.
    https://developer.cisco.com/docs/cloud-security/list-network-tunnel-groups/
    """
    logger.info(
        "Listing network tunnel groups offset=%s limit=%s",
        params.offset,
        params.limit,
    )
    client = asset.get_client()
    filters_obj = _parse_optional_filters(params)
    offset, limit = _clamp_offset_limit(params, MAX_LIMIT_NETWORK_TUNNEL_GROUPS)
    data = client.ListNetworkTunnelGroups(
        offset=offset,
        limit=limit,
        filters=filters_obj,
        sort_by=getattr(params, "sort_by", "name"),
        sort_order=getattr(params, "sort_order", "asc"),
        include_statuses=getattr(params, "include_statuses", False),
    )
    return ListNetworkTunnelGroupsOutput(
        data=data.get("data"),
        offset=data.get("offset"),
        limit=data.get("limit"),
        total=data.get("total"),
    )


@app.action()
def get_network_tunnel_group(
    params: GetNetworkTunnelGroupParams, asset: Asset
) -> GetNetworkTunnelGroupOutput:
    """
    Get a Network Tunnel Group by ID.
    GET deployments/v2/networktunnelgroups/{id}. Requires deployments.networktunnelgroups:read.
    https://developer.cisco.com/docs/cloud-security/get-network-tunnel-group/
    """
    logger.info("Getting network tunnel group id=%s", params.id)
    client = asset.get_client()
    data = client.GetNetworkTunnelGroup(params.id)
    return _output_from_api_data(GetNetworkTunnelGroupOutput, data)


@app.action()
def create_rule(params: CreateRuleParams, asset: Asset) -> CreateRuleOutput:
    """
    Create an access rule on the organization's Access policy.
    POST policies/v2/rules. Requires policies.rules:write.
    https://developer.cisco.com/docs/cloud-security/create-rule/
    """
    logger.info("Creating rule name=%s", params.rule_name)
    rule_conditions = _parse_json_param(
        params.rule_conditions_json, "rule_conditions_json", allow_list=True
    )
    rule_settings = _parse_json_param(
        params.rule_settings_json, "rule_settings_json", allow_list=True
    )
    body = {
        "ruleName": params.rule_name,
        "ruleAction": params.rule_action,
        "ruleConditions": rule_conditions,
        "ruleSettings": rule_settings,
    }
    if (
        getattr(params, "rule_description", None)
        and str(params.rule_description).strip()
    ):
        body["ruleDescription"] = params.rule_description.strip()
    if getattr(params, "rule_priority", None) is not None:
        body["rulePriority"] = params.rule_priority
    if getattr(params, "rule_is_enabled", None) is not None:
        body["ruleIsEnabled"] = params.rule_is_enabled
    client = asset.get_client()
    data = client.CreateRule(body)
    logger.info("create_rule result ruleId=%s", data.get("ruleId"))
    return _output_from_api_data(CreateRuleOutput, data)


@app.action()
def list_firewall_rules(
    params: ListFirewallRulesParams, asset: Asset
) -> ListFirewallRulesOutput:
    """
    List access rules in the organization's Access policy.
    GET policies/v2/rules. Requires policies.rules:read.
    https://developer.cisco.com/docs/cloud-security/list-rules/
    """
    logger.info(
        "Listing firewall rules offset=%s limit=%s", params.offset, params.limit
    )
    client = asset.get_client()
    filters_obj = _parse_optional_filters(params)
    rule_name = getattr(params, "rule_name", None) or None
    if rule_name is not None and str(rule_name).strip() == "":
        rule_name = None
    offset, limit = _clamp_offset_limit(params, MAX_LIMIT_FIREWALL_RULES)
    data = client.ListFirewallRules(
        offset=offset,
        limit=limit,
        rule_name=rule_name,
        filters=filters_obj,
    )
    logger.info("got firewall rules count=%s", data.get("count", 0))
    rules = (
        (data.get("results") or data.get("result") or [])
        if isinstance(data, dict)
        else []
    )
    return ListFirewallRulesOutput(
        count=data.get("count") if isinstance(data, dict) else None,
        firewall_rules=rules,
    )


@app.action()
def list_resource_connectors(
    params: ListResourceConnectorsParams, asset: Asset
) -> ListResourceConnectorsOutput:
    """
    List Resource Connectors for the organization.
    GET deployments/v2/connectorAgents. Requires deployments.resourceconnectors:read.
    https://developer.cisco.com/docs/cloud-security/list-connectors/
    """
    logger.info(
        "Listing resource connectors offset=%s limit=%s",
        params.offset,
        params.limit,
    )
    client = asset.get_client()
    filters_obj = _parse_optional_filters(params)
    offset, limit = _clamp_offset_limit(params, MAX_LIMIT_RESOURCE_CONNECTORS)
    data = client.ListResourceConnectors(
        offset=offset,
        limit=limit,
        filters=filters_obj,
        sort_by=getattr(params, "sort_by", "originIpAddress"),
        sort_order=getattr(params, "sort_order", "asc"),
    )
    return ListResourceConnectorsOutput(
        data=data.get("data"),
        offset=data.get("offset"),
        limit=data.get("limit"),
        total=data.get("total"),
    )


@app.action()
def refresh_s3_key(params: Params, asset: Asset) -> RefreshS3KeyOutput:
    """
    Rotate the Cisco-managed S3 bucket key for the organization.
    POST admin/v2/iam/rotateKey. Requires admin.iam:write.
    https://developer.cisco.com/docs/cloud-security/refresh-s3-bucket-key/
    """
    client = asset.get_client()
    data = client.RefreshS3BucketKey()
    return RefreshS3KeyOutput(
        oldKeyId=data.get("oldKeyId"),
        currentKeyId=data.get("currentKeyId"),
        secretAccessKey=data.get("secretAccessKey"),
        keyCreationDate=data.get("keyCreationDate"),
    )


if __name__ == "__main__":
    app.cli()
