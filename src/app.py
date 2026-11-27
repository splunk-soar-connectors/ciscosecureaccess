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

from soar_sdk.app import App
from soar_sdk.exceptions import ActionFailure

from .actions import register_actions
from .asset import Asset
from .error_handling import format_action_error


def create_cisco_secure_access_soar_connector_app() -> App:
    """Create and configure the Cisco Secure Access SOAR connector app."""
    app = App(
        name="Cisco Secure Access",
        app_type="information",
        logo="logo_cisco.svg",
        logo_dark="logo_cisco_dark.svg",
        product_vendor="Cisco",
        product_name="Cisco Secure Access",
        publisher="Splunk",
        appid="48ce45b2-0de5-474f-be52-8266350325cd",
        fips_compliant=False,
        asset_cls=Asset,
    )

    @app.test_connectivity()
    def test_connectivity(asset: Asset) -> None:
        """Test OAuth authentication to Cisco Secure Access."""
        client = asset.get_client()
        try:
            token = client.get_token()
        except Exception as exc:
            raise ActionFailure(
                format_action_error("Connectivity test failed", exc)
            ) from exc
        if not token:
            raise ActionFailure("Unable to get auth token")

    # The SDK hook derives description from the docstring but has no verbose argument.
    test_connectivity.meta.verbose = (
        "Verifies that the configured asset can authenticate to Cisco Secure Access "
        "with OAuth credentials."
    )

    return register_actions(app)


app: App = create_cisco_secure_access_soar_connector_app()


if __name__ == "__main__":
    app.cli()
