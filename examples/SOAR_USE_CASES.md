# Cisco Secure Access – Splunk SOAR Use Cases for SOC Analysts

Three short, actionable use cases for SOC analysts to implement in Splunk SOAR using the **Cisco Secure Access** app. Each uses 2–4 app actions and stays simple for quick deployment.

______________________________________________________________________

## Use Case 1: Block Malicious or Phishing Domain

**Triggering event / scenario**\
A SIEM or email security alert indicates a user clicked a link to a malicious or phishing domain (e.g., from a reported email or a threat intel feed). The SOC wants to block the domain organization-wide in Cisco Secure Access (SSE) so no other user can reach it.

**Splunk SOAR playbook (actions and order)**

1. **get_domain_status** – Input: domain from the alert. Use the result to confirm the domain is seen by SSE and check status/categorization.
1. **get_domain_risk_score** – Input: same domain. Use risk score to decide whether to block (e.g., block if high risk or malicious).
1. **add_to_destination_list** – Input: destination list ID (or asset default), destination = domain, comment = e.g. “SOAR block – phishing alert ”.

**Resolution**\
The domain is added to the chosen destination list (block list) in Cisco SSE. Policy can then deny access to that domain for all users behind SSE, reducing further exposure while the incident is investigated.

______________________________________________________________________

## Use Case 2: Terminate Suspicious VPN Session

**Triggering event / scenario**\
A detection (e.g., impossible travel, credential stuffing, or anomalous login) indicates a VPN session is suspicious or compromised. The SOC wants to disconnect that session immediately so the user must re-authenticate (or an attacker loses access).

**Splunk SOAR playbook (actions and order)**

1. **list_vpn_sessions** – Retrieve current VPN sessions.
1. **terminate_vpn_session** – Input: profile name and region from asset/playbook config; usernames and/or session IDs from the alert (or from step 1 filtered by username/IP). Disconnect the identified session(s).

**Resolution**\
The targeted VPN session is terminated in Cisco Secure Access. The user (or attacker) loses VPN access and must reconnect; with MFA and monitoring, this limits misuse and forces re-verification.

______________________________________________________________________

## Use Case 3: Revoke ZTNA Access for Compromised or Offboarded Device

**Triggering event / scenario**\
A device is flagged as compromised (e.g., EDR alert, lost/stolen, or offboarding). The device has ZTNA (zero trust) access via Cisco SSE. The SOC wants to revoke that device’s certificates and remove it from ZTNA so it can no longer access internal applications.

**How to get `user_id`**\
`revoke_certificates_for_device` requires both `user_id` and `device_id`. The Cisco Secure Access app does **not** expose an action that returns `user_id` from a `device_id` (the ZTNA APIs are user-scoped: you list/revoke by user and device).

- **From the event (recommended):** Use the alert payload. Many sources already provide the user identity (e.g. EDR “affected user”, IAM “username”, offboarding “email”). Map that to the identity your organization uses for ZTNA—often the same as the IdP (e.g. email, UPN, or Okta/Entra user ID). Configure the playbook to take `user_id` from the event (e.g. `artifact.user` or a normalized field) and `device_id` from the event (e.g. `artifact.device_id` or hostname lookup).
- **From another system:** If the event has only `device_id`, use a SOAR lookup to another app (e.g. CMDB, directory, or EDR) that maps device → user, then pass that user identifier as `user_id`.
- **From SSE via the app:** There is no “get user by device” action. `list_identities(type="device")` returns device registrations (key, label, authName), not ZTNA user–device links. `get_roaming_computer` / `list_roaming_computers` return device posture only (no `user_id`). So you cannot resolve `user_id` from `device_id` using this app alone; the event or another data source must supply `user_id`.

**Splunk SOAR playbook (actions and order)**

1. **get_roaming_computer** – Input: device_id from the alert. Optionally used to confirm the device is known to SSE and get current posture/status.
1. **revoke_certificates_for_device** – Input: user_id (from event or lookup) and device_id (from event). Revoke active ZTNA certificates and remove the device.

**Resolution**\
The device’s ZTNA certificates are revoked and the device is removed from the zero trust user’s devices in Cisco SSE. The device can no longer access ZTNA-protected applications until re-enrolled through a controlled process.

______________________________________________________________________

## Summary Table

| Use case | Trigger | Actions (in order) | Outcome |
| -------------------------------- | ------------------------------- | ------------------------------------------------------------------- | ------------------------------- |
| Block malicious/phishing domain | Alert on malicious/phishing URL | get_domain_status → get_domain_risk_score → add_to_destination_list | Domain blocked in SSE |
| Terminate suspicious VPN session | Suspicious VPN session alert | list_vpn_sessions → terminate_vpn_session | VPN session disconnected |
| Revoke ZTNA for bad device | Compromised/offboarded device | get_roaming_computer → revoke_certificates_for_device | Device removed from ZTNA access |

All playbooks use only actions implemented in the Cisco Secure Access app. Enrichment (e.g., domain risk) can drive conditional branching (e.g., only add to block list if risk score exceeds a threshold) when building the playbooks in the SOAR editor.
