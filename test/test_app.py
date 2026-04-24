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
"""
Run all launch-config actions with mocked API client and ensure success.
Uses test/test_asset.json and test/test_params*.json; no real network calls.
"""

import json
from pathlib import Path

import pytest
from unittest.mock import MagicMock, patch

# Resolve paths relative to this file (test/test_app.py)
TEST_DIR = Path(__file__).resolve().parent
ASSET_PATH = TEST_DIR / "test_asset.json"
PARAMS_PATH = TEST_DIR / "test_params.json"
UPDATE_IDENTITIES_PARAMS_PATH = TEST_DIR / "test_params_update_identities.json"
CREATE_RULE_PARAMS_PATH = TEST_DIR / "test_params_create_rule.json"
SET_SWG_OVERRIDE_PARAMS_PATH = (
    TEST_DIR / "test_params_set_swg_override_device_settings.json"
)


def _load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _asset_fallback() -> dict:
    """Minimal asset for CI when test_asset.json is gitignored."""
    example = TEST_DIR / "test_asset.json.example"
    if example.exists():
        return _load_json(example)
    return {"client_id": "test-client-id", "client_secret": "test-client-secret"}


def _params_fallback() -> dict:
    """Minimal params for CI when test_params.json is gitignored."""
    return {
        "destination_list_id": 18620840,
        "destination": "https://www.test.com/test",
        "comment": "test comment",
        "list_destinations": True,
        "destination_ids": "60582,60583",
        "domain": "www.test.com",
        "profile_name": "test_profile",
        "region": "us",
        "sessions": ["1234567890"],
        "usernames": ["test_user"],
        "type": "securityGroupTag",
        "user_id": "1251001730",
        "device_id": "0101a128dc5b84e2",
        "origin_id": 618400931,
        "policy_type": "dns",
    }


@pytest.fixture
def asset_data():
    if ASSET_PATH.exists():
        return _load_json(ASSET_PATH)
    return _asset_fallback()


@pytest.fixture
def params_data():
    if PARAMS_PATH.exists():
        return _load_json(PARAMS_PATH)
    return _params_fallback()


@pytest.fixture
def update_identities_params_data():
    return _load_json(UPDATE_IDENTITIES_PARAMS_PATH)


@pytest.fixture
def create_rule_params_data():
    return _load_json(CREATE_RULE_PARAMS_PATH)


@pytest.fixture
def set_swg_override_params_data():
    if SET_SWG_OVERRIDE_PARAMS_PATH.exists():
        return _load_json(SET_SWG_OVERRIDE_PARAMS_PATH)
    return {"value": "1", "origin_ids": "12321231,123134314"}


@pytest.fixture
def mock_client():
    """Mock SSE_API with safe return values for every action."""
    client = MagicMock()
    client.GetToken.return_value = True
    client.ListNetworkDevices.return_value = []
    client.DeleteNetworkDevice.return_value = {
        "success": True,
        "message": "Network device removed",
    }
    client.ListApiKeys.return_value = {"name": "test-key"}
    client.ListVirtualAppliances.return_value = []
    client.ListSites.return_value = []
    client.ListDestinationLists.return_value = []
    _destination_list_data = {
        "id": 1234567,
        "organizationId": 2345678,
        "access": "allow",
        "isGlobal": False,
        "name": "Global Allow List",
        "thirdpartyCategoryId": 0,
        "createdAt": 1490206249,
        "modifiedAt": 1520476127,
        "isMspDefault": False,
        "markedForDeletion": False,
    }
    _created_destination_list_data = {
        "id": 2477857,
        "organizationId": 22429759,
        "access": "none",
        "isGlobal": False,
        "name": "New Destination List",
        "thirdpartyCategoryId": 0,
        "createdAt": 1532628019,
        "modifiedAt": 1532628019,
        "isMspDefault": False,
        "markedForDeletion": False,
        "bundleTypeId": 2,
        "meta": {
            "destinationCount": 1,
            "domainCount": 1,
            "urlCount": 0,
            "ipv4Count": 0,
            "ipv6Count": 0,
            "applicationCount": 0,
        },
    }
    client.CreateDestinationList.return_value = {
        "status": {"code": 200, "text": "OK"},
        "data": _created_destination_list_data,
    }
    client.AddToDestinationList.return_value = {"data": _destination_list_data}
    client.RemoveDestinationsFromList.return_value = _destination_list_data
    client.GetDomainStatus.return_value = {
        "www.test.com": {
            "status": 0,
            "security_categories": [],
            "content_categories": [],
        }
    }
    client.GetDomainRiskScore.return_value = {"risk_score": 0, "indicators": []}
    client.GetPassiveDNS.return_value = []
    client.ListVPNSessions.return_value = []
    client.TerminateVPNSession.return_value = {"statusCode": 200, "message": "OK"}
    client.ListIdentities.return_value = []
    client.UpdateIdentities.return_value = {"success": True}
    client.ListCertificatesForDevice.return_value = {
        "deviceId": "0ace1b5f6104a466",  # pragma: allowlist secret
        "certificates": [
            {
                "certificateId": "54321",
                "status": "active",
                "createdAt": "2024-05-15T21:36:32Z",
                "expiresAt": "2024-07-15T21:36:32Z",
            }
        ],
    }
    client.ListCertificatesForUser.return_value = {
        "userId": "1251001730",
        "devices": [
            {
                "deviceId": "0ace1b5f6104a466",  # pragma: allowlist secret
                "certificates": [
                    {
                        "certificateId": "54321",
                        "status": "active",
                        "createdAt": "2024-05-15T21:36:32Z",
                        "expiresAt": "2024-07-15T21:36:32Z",
                    }
                ],
            },
        ],
    }
    client.RevokeCertificatesForDevice.return_value = {
        "success": True,
        "message": "Certificates revoked and device removed",
    }
    client.GetRoamingComputer.return_value = {
        "originId": 618400931,
        "deviceId": "AB000C044C87A4F0",
        "type": "anyconnect",
        "status": "Encrypted",
        "swgStatus": "Protected",
        "lastSyncStatus": "Encrypted",
        "lastSyncSwgStatus": "Protected",
        "lastSync": "2024-09-19T10:34:30.000Z",
        "version": "5.2.3",
        "name": "wkst2",
        "hasIpBlocking": False,
        "appliedBundle": 2,
        "osVersion": "Microsoft Windows NT 10.0.19045.0",
        "osVersionName": "Windows 10",
        "anyconnectDeviceId": "9e963836fef9429b66c3e47b58e496efce2b5003",  # pragma: allowlist secret
    }
    client.ListRoamingComputers.return_value = []
    client.ListSWGOverrideDeviceSettings.return_value = [
        {
            "originId": 124131441,
            "name": "SWGEnabled",
            "value": "1",
            "modifiedAt": "2021-04-26 13:12:11",
        },
        {
            "originId": 124131442,
            "name": "SWG-not-enabled",
            "value": "0",
            "modifiedAt": "2023-04-26 13:12:11",
        },
    ]
    client.SetSWGOverrideDeviceSettings.return_value = {
        "totalCount": 2,
        "successCount": 1,
        "failCount": 1,
        "items": [
            {"originId": 12321231, "code": 200, "message": "success"},
            {
                "originId": 123134314,
                "code": 404,
                "message": "The origin ID does not exist.",
            },
        ],
        "value": "1",
    }
    client.DeleteSWGOverrideDeviceSettings.return_value = {"status": "No content"}
    client.ListFirewallRules.return_value = {"count": 0, "results": []}
    client.CreateRule.return_value = {
        "organizationId": 8094936,
        "ruleId": 591710,
        "ruleName": "Test_Rule-1",
        "ruleDescription": "Test rule created by SOAR",
        "ruleAction": "allow",
        "rulePriority": 9,
        "ruleIsDefault": False,
        "ruleIsEnabled": True,
        "ruleConditions": [
            {
                "attributeName": "umbrella.destination.all",
                "attributeValue": "true",
                "attributeOperator": "=",
            },
            {
                "attributeName": "umbrella.source.all",
                "attributeValue": "true",
                "attributeOperator": "=",
            },
        ],
        "ruleSettings": [
            {
                "settingName": "umbrella.default.traffic",
                "settingValue": "PUBLIC_INTERNET",
            }
        ],
        "modifiedBy": "org/1234/user/1",
        "modifiedAt": "2024-04-01T19:42:38",
        "createdAt": "2024-03-28T18:17:36",
    }
    client.ListNetworkTunnelGroups.return_value = {
        "data": [],
        "offset": 0,
        "limit": 10,
        "total": 0,
    }
    client.GetNetworkTunnelGroup.return_value = {
        "id": 456123789,
        "name": "New York Branch Tunnels",
        "organizationId": 123456,
        "deviceType": "ASA",
        "region": "us-east-1",
        "status": "connected",
        "hubs": [],
        "routing": {"type": "static", "data": {"networkCIDRs": ["123.111.222.25/24"]}},
        "createdAt": "2024-06-12T18:04:23Z",
        "modifiedAt": "2024-06-25T15:21:32Z",
    }
    client.ListResourceConnectors.return_value = {
        "data": [],
        "offset": 0,
        "limit": 10,
        "total": 0,
    }
    client.RefreshS3BucketKey.return_value = {
        "oldKeyId": "test-old-key-id",
        "currentKeyId": "test-current-key-id",
        "secretAccessKey": "test-secret-access-key-not-logged",  # pragma: allowlist secret
        "keyCreationDate": "2025-02-19T12:00:00Z",
    }
    return client


@pytest.fixture
def asset(asset_data):
    from src.app import Asset

    return Asset(**asset_data)


@pytest.fixture(autouse=True)
def patch_sse_api(mock_client):
    """Patch SSE_API so asset.get_client() returns mock_client (no real API calls)."""
    with patch("src.app.SSE_API", MagicMock(return_value=mock_client)):
        yield


def _params(cls, data: dict):
    """Build param instance from class and dict (only keys the model knows)."""
    fields = getattr(cls, "model_fields", None) or getattr(cls, "__fields__", {})
    allowed = {k: data[k] for k in fields if k in data}
    return cls(**allowed)


def _action(fn):
    """Call the underlying action function, bypassing the SOAR decorator (no get_message/get_summary)."""
    return getattr(fn, "__wrapped__", fn)


def test_connectivity(asset):
    from src.app import test_connectivity

    _action(test_connectivity)(asset)


def test_list_managed_devices(asset):
    from soar_sdk.params import Params
    from src.app import list_managed_devices

    result = _action(list_managed_devices)(Params(), asset)
    assert result is not None
    assert hasattr(result, "devices")


def test_delete_managed_device(asset, params_data):
    from src.params import DeleteManagedDeviceParams
    from src.app import delete_managed_device

    params = _params(DeleteManagedDeviceParams, params_data)
    result = _action(delete_managed_device)(params, asset)
    assert result is not None
    assert hasattr(result, "success")
    assert result.success is True


def test_list_api_keys(asset):
    from soar_sdk.params import Params
    from src.app import list_api_keys

    result = _action(list_api_keys)(Params(), asset)
    assert result is not None


def test_list_virtual_appliances(asset):
    from soar_sdk.params import Params
    from src.app import list_virtual_appliances

    result = _action(list_virtual_appliances)(Params(), asset)
    assert result is not None
    assert hasattr(result, "virtualAppliances")


def test_list_sites(asset):
    from soar_sdk.params import Params
    from src.app import list_sites

    result = _action(list_sites)(Params(), asset)
    assert result is not None
    assert hasattr(result, "sites")


def test_list_destination_lists(asset, params_data):
    from src.params import ListDestinationListsParams
    from src.app import list_destination_lists

    params = _params(ListDestinationListsParams, params_data)
    result = _action(list_destination_lists)(params, asset)
    assert result is not None
    assert hasattr(result, "destinationLists")


def test_add_to_destination_list(asset, params_data):
    from src.params import AddToDestinationListParams
    from src.app import add_to_destination_list

    params = _params(AddToDestinationListParams, params_data)
    result = _action(add_to_destination_list)(params, asset)
    assert result is not None
    assert hasattr(result, "destinationList")


def _create_destination_list_params():
    from src.params import CreateDestinationListParams

    return CreateDestinationListParams(
        name="SOAR test destination list",
        access="none",
        destinations_json='[{"destination":"example.com","type":"domain"}]',
    )


def test_create_destination_list(asset):
    from src.app import create_destination_list

    params = _create_destination_list_params()
    result = _action(create_destination_list)(params, asset)
    assert result is not None
    assert hasattr(result, "destinationList")
    assert result.destinationList.id == 2477857
    assert result.destinationList.bundleTypeId == 2
    assert result.destinationList.destinationCount == 1


def test_create_destination_list_calls_client(asset, mock_client):
    from src.app import create_destination_list

    params = _create_destination_list_params()
    _action(create_destination_list)(params, asset)
    mock_client.CreateDestinationList.assert_called_once()
    call_body = mock_client.CreateDestinationList.call_args[0][0]
    assert call_body["name"] == "SOAR test destination list"
    assert call_body["access"] == "none"
    assert call_body["isGlobal"] is False
    assert call_body["bundleTypeId"] == 2
    assert call_body["destinations"] == [
        {"destination": "example.com", "type": "domain"}
    ]


def test_add_to_destination_list_calls_client_with_one_destination(
    asset, params_data, mock_client
):
    """Add to destination list calls client with one destination and optional comment."""
    from src.params import AddToDestinationListParams
    from src.app import add_to_destination_list

    params = _params(AddToDestinationListParams, params_data)
    _action(add_to_destination_list)(params, asset)
    mock_client.AddToDestinationList.assert_called_once_with(
        18620840, "https://www.test.com/test", "test comment"
    )


def test_remove_destinations_from_list(asset, params_data):
    from src.params import RemoveDestinationsFromListParams
    from src.app import remove_destinations_from_list

    params = _params(RemoveDestinationsFromListParams, params_data)
    result = _action(remove_destinations_from_list)(params, asset)
    assert result is not None
    assert hasattr(result, "destinationList")


def test_get_domain_status(asset, params_data):
    from src.params import GetDomainParams
    from src.app import get_domain_status

    params = _params(GetDomainParams, params_data)
    result = _action(get_domain_status)(params, asset)
    assert result is not None
    assert hasattr(result, "status")


def test_get_domain_risk_score(asset, params_data):
    from src.params import GetDomainParams
    from src.app import get_domain_risk_score

    params = _params(GetDomainParams, params_data)
    result = _action(get_domain_risk_score)(params, asset)
    assert result is not None
    assert hasattr(result, "risk_score")


def test_get_passive_dns(asset, params_data):
    from src.params import GetDomainParams
    from src.app import get_passive_dns

    params = _params(GetDomainParams, params_data)
    result = _action(get_passive_dns)(params, asset)
    assert result is not None
    assert hasattr(result, "passive_dns_records")


def test_list_vpn_sessions(asset):
    from soar_sdk.params import Params
    from src.app import list_vpn_sessions

    result = _action(list_vpn_sessions)(Params(), asset)
    assert result is not None
    assert hasattr(result, "vpn_sessions")


def test_terminate_vpn_session(asset, params_data):
    from src.params import TerminateVPNSessionParams
    from src.app import terminate_vpn_session

    data = dict(params_data)
    for key in ("sessions", "usernames"):
        if isinstance(data.get(key), list):
            data[key] = ",".join(str(x) for x in data[key])
    params = _params(TerminateVPNSessionParams, data)
    result = _action(terminate_vpn_session)(params, asset)
    assert result is not None
    assert hasattr(result, "statusCode")


def test_list_identities(asset, params_data):
    from src.params import ListIdentitiesParams
    from src.app import list_identities

    params = _params(ListIdentitiesParams, params_data)
    result = _action(list_identities)(params, asset)
    assert result is not None
    assert hasattr(result, "identities")


def test_update_identities(asset, update_identities_params_data):
    from src.params import UpdateIdentitiesParams
    from src.app import update_identities

    params = _params(UpdateIdentitiesParams, update_identities_params_data)
    result = _action(update_identities)(params, asset)
    assert result is not None
    assert hasattr(result, "success")
    assert result.success is True


def test_list_certificates_for_device(asset, params_data):
    from src.params import ListCertificatesForDeviceParams
    from src.app import list_certificates_for_device

    params = _params(ListCertificatesForDeviceParams, params_data)
    result = _action(list_certificates_for_device)(params, asset)
    assert result is not None
    assert hasattr(result, "deviceId")
    assert hasattr(result, "certificates")
    assert result.certificates is not None
    assert len(result.certificates) >= 1


def test_list_certificates_for_user(asset, params_data):
    from src.params import ListCertificatesForUserParams
    from src.app import list_certificates_for_user

    params = _params(ListCertificatesForUserParams, params_data)
    result = _action(list_certificates_for_user)(params, asset)
    assert result is not None
    assert hasattr(result, "userId")
    assert hasattr(result, "devices")
    assert result.devices is not None
    assert len(result.devices) >= 1


def test_revoke_certificates_for_device(asset, params_data):
    from src.params import RevokeCertificatesForDeviceParams
    from src.app import revoke_certificates_for_device

    params = _params(RevokeCertificatesForDeviceParams, params_data)
    result = _action(revoke_certificates_for_device)(params, asset)
    assert result is not None
    assert hasattr(result, "success")
    assert result.success is True


def test_get_roaming_computer(asset, params_data):
    from src.params import GetRoamingComputerParams
    from src.app import get_roaming_computer

    params = _params(GetRoamingComputerParams, params_data)
    result = _action(get_roaming_computer)(params, asset)
    assert result is not None
    assert hasattr(result, "deviceId")
    assert hasattr(result, "status")
    assert hasattr(result, "swgStatus")
    assert result.status == "Encrypted"
    assert result.swgStatus == "Protected"


def test_list_roaming_computers(asset):
    from soar_sdk.params import Params
    from src.app import list_roaming_computers

    result = _action(list_roaming_computers)(Params(), asset)
    assert result is not None
    assert hasattr(result, "roamingComputers")
    assert result.roamingComputers is not None


def test_list_swg_override_device_settings(asset, set_swg_override_params_data):
    from src.params import ListSWGOverrideDeviceSettingsParams
    from src.app import list_swg_override_device_settings

    params = _params(ListSWGOverrideDeviceSettingsParams, set_swg_override_params_data)
    result = _action(list_swg_override_device_settings)(params, asset)
    assert result is not None
    assert hasattr(result, "settings")
    assert len(result.settings) == 2
    assert result.settings[0].originId == 124131441
    assert result.settings[0].value == "1"
    assert result.settings[1].originId == 124131442
    assert result.settings[1].value == "0"


def test_list_swg_override_device_settings_calls_client(
    asset, set_swg_override_params_data, mock_client
):
    """List SWG override calls client with list of origin IDs."""
    from src.params import ListSWGOverrideDeviceSettingsParams
    from src.app import list_swg_override_device_settings

    params = _params(ListSWGOverrideDeviceSettingsParams, set_swg_override_params_data)
    _action(list_swg_override_device_settings)(params, asset)
    mock_client.ListSWGOverrideDeviceSettings.assert_called_once_with(
        [12321231, 123134314]
    )


def test_set_swg_override_device_settings(asset, set_swg_override_params_data):
    from src.params import SetSWGOverrideDeviceSettingsParams
    from src.app import set_swg_override_device_settings

    params = _params(SetSWGOverrideDeviceSettingsParams, set_swg_override_params_data)
    result = _action(set_swg_override_device_settings)(params, asset)
    assert result is not None
    assert result.totalCount == 2
    assert result.successCount == 1
    assert result.failCount == 1
    assert result.value == "1"
    assert len(result.items) == 2
    assert result.items[0].originId == 12321231
    assert result.items[0].code == 200
    assert result.items[1].originId == 123134314
    assert result.items[1].code == 404


def test_set_swg_override_device_settings_calls_client(
    asset, set_swg_override_params_data, mock_client
):
    """Set SWG override calls client with value and list of origin IDs."""
    from src.params import SetSWGOverrideDeviceSettingsParams
    from src.app import set_swg_override_device_settings

    params = _params(SetSWGOverrideDeviceSettingsParams, set_swg_override_params_data)
    _action(set_swg_override_device_settings)(params, asset)
    mock_client.SetSWGOverrideDeviceSettings.assert_called_once_with(
        "1", [12321231, 123134314]
    )


def test_delete_swg_override_device_settings(asset, set_swg_override_params_data):
    from src.params import DeleteSWGOverrideDeviceSettingsParams
    from src.app import delete_swg_override_device_settings

    params = _params(
        DeleteSWGOverrideDeviceSettingsParams, set_swg_override_params_data
    )
    result = _action(delete_swg_override_device_settings)(params, asset)
    assert result is not None
    assert result.status == "No content"


def test_delete_swg_override_device_settings_calls_client(
    asset, set_swg_override_params_data, mock_client
):
    """Delete SWG override calls client with list of origin IDs."""
    from src.params import DeleteSWGOverrideDeviceSettingsParams
    from src.app import delete_swg_override_device_settings

    params = _params(
        DeleteSWGOverrideDeviceSettingsParams, set_swg_override_params_data
    )
    _action(delete_swg_override_device_settings)(params, asset)
    mock_client.DeleteSWGOverrideDeviceSettings.assert_called_once_with(
        [12321231, 123134314]
    )


def test_create_rule(asset, create_rule_params_data):
    from src.params import CreateRuleParams
    from src.app import create_rule

    params = _params(CreateRuleParams, create_rule_params_data)
    result = _action(create_rule)(params, asset)
    assert result is not None
    assert result.ruleId == 591710
    assert result.ruleName == "Test_Rule-1"
    assert result.ruleAction == "allow"


def test_list_network_tunnel_groups(asset):
    from src.params import ListNetworkTunnelGroupsParams
    from src.app import list_network_tunnel_groups

    params = ListNetworkTunnelGroupsParams(offset=0, limit=10)
    result = _action(list_network_tunnel_groups)(params, asset)
    assert result is not None
    assert hasattr(result, "data")
    assert result.data is not None
    assert result.offset == 0
    assert result.limit == 10
    assert result.total == 0


def test_list_resource_connectors(asset):
    from src.params import ListResourceConnectorsParams
    from src.app import list_resource_connectors

    params = ListResourceConnectorsParams(offset=0, limit=10)
    result = _action(list_resource_connectors)(params, asset)
    assert result is not None
    assert hasattr(result, "data")
    assert result.data is not None
    assert result.offset == 0
    assert result.limit == 10
    assert result.total == 0


def test_refresh_s3_key(asset):
    from src.params import Params
    from src.app import refresh_s3_key

    params = Params()
    result = _action(refresh_s3_key)(params, asset)
    assert result is not None
    assert result.oldKeyId == "test-old-key-id"
    assert result.currentKeyId == "test-current-key-id"
    # fmt: off
    assert result.secretAccessKey == "test-secret-access-key-not-logged"  # pragma: allowlist secret
    # fmt: on
    assert result.keyCreationDate == "2025-02-19T12:00:00Z"


def test_get_network_tunnel_group(asset):
    from src.params import GetNetworkTunnelGroupParams
    from src.app import get_network_tunnel_group

    params = GetNetworkTunnelGroupParams(id=456123789)
    result = _action(get_network_tunnel_group)(params, asset)
    assert result is not None
    assert result.id == 456123789
    assert result.name == "New York Branch Tunnels"
    assert result.region == "us-east-1"
    assert result.status == "connected"
