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

from ..core import Asset
from ..outputs import GetPassiveDNSOutput
from ..params import GetPassiveDNSParams


def get_passive_dns(params: GetPassiveDNSParams, asset: Asset) -> GetPassiveDNSOutput:
    """
    Get Passive DNS.
    https://developer.cisco.com/docs/cloud-security/get-resource-records-for-name/
    """
    client = asset.get_client()
    records, page_info = client.GetPassiveDNS(
        params.domain, offset=params.offset, limit=params.limit
    )
    offset = page_info.get("offset", params.offset)
    total = page_info.get("totalNumRecords")
    has_more = page_info.get("hasMoreRecords")
    if has_more is None and total is not None:
        has_more = (offset + len(records)) < total
    next_offset = offset + len(records) if has_more else None
    return GetPassiveDNSOutput(
        passive_dns_records=records,
        total_records=total,
        returned_records=len(records),
        offset=offset,
        limit=page_info.get("limit", params.limit),
        has_more_records=has_more,
        next_offset=next_offset,
    )
