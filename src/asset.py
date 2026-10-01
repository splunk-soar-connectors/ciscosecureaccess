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

from soar_sdk.asset import AssetField
from soar_sdk.asset import BaseAsset
from soar_sdk.exceptions import ActionFailure

from .error_handling import format_action_error
from .sse_api_client import SSE_API


class Asset(BaseAsset):
    """Represent a Cisco Secure Access asset and its authentication settings."""

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
        """Create an API client using this asset's configured credentials."""
        return SSE_API(
            self.base_url,
            self.client_id,
            self.client_secret,
            auth_header_name=self.auth_header_name,
        )


def test_connectivity(asset: Asset) -> None:
    """Test OAuth connectivity against the Cisco Secure Access API."""
    client = asset.get_client()
    try:
        token = client.GetToken()
    except Exception as exc:
        raise ActionFailure(
            format_action_error("Connectivity test failed", exc)
        ) from exc
    if not token:
        raise ActionFailure("Unable to get auth token")
