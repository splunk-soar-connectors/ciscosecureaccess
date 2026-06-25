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

from soar_sdk.params import Params

from ..core import Asset, app
from ..outputs import ListAPIKeysOutput, RefreshS3KeyOutput


@app.action()
def list_api_keys(params: Params, asset: Asset) -> ListAPIKeysOutput:
    """
    List all API keys.
    https://developer.cisco.com/docs/cloud-security/list-api-keys/
    """
    client = asset.get_client()
    api_keys = client.ListApiKeys()
    if isinstance(api_keys, dict) and "keys" in api_keys:
        return ListAPIKeysOutput(
            keys=api_keys.get("keys", []),
            message=api_keys.get("message"),
            offset=api_keys.get("offset"),
            limit=api_keys.get("limit"),
            total=api_keys.get("total"),
        )
    return ListAPIKeysOutput(keys=[])


@app.action(read_only=False)
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
