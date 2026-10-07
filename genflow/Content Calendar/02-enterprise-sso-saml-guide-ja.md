---
title: "【日本語】 SSO and SAML Integration ガイド for Enterprise Teams Using Lovart"
date: 2027-06-03
category: Enterprise
tags: [lovart sso, saml integration, enterprise design, single sign-on, identity management, security]
keywords: [lovart sso, saml integration, enterprise design tool sso, single sign-on design, identity provider integration]
description: "A comprehensive technical guide to configuring SSO and SAML authentication for Lovart enterprise accounts — covering identity provider setup, user provisioning, role mapping, security policies, and common troubleshooting scenarios."
slug: sso-saml-integration-guide-enterprise-2027
featured_image: /images/lovart-sso-saml-guide.jpg
canonical_url: https://lovart.ai/blog/sso-saml-integration-guide-enterprise
language: ja
---

# SSO and SAML Integration Guide for Enterprise Teams Using Lovart

[IMAGE 1 PLACEHOLDER — Persona Scenario]

Enterprise adoption of creative tools hits a hard wall when those tools cannot integrate with the organization's identity and access management infrastructure. IT security teams do not negotiate on this: if a SaaS tool cannot authenticate through the company's single sign-on (SSO) provider, it does not get deployed. No matter how compelling the product is. No matter how enthusiastic the design team is. No SSO, no deal.

Lovart's Enterprise plan ($149/month per seat) includes full SSO support via SAML 2.0 and OpenID Connect (OIDC), with Just-in-Time (JIT) user provisioning, role-based access control mapping, and session management policies. This guide covers the complete integration process — from identity provider configuration to user lifecycle management to common troubleshooting scenarios.

## Supported Identity Providers

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

Lovart supports SAML 2.0 integration with any identity provider (IdP) that implements the standard. We have validated integrations with:

| Identity Provider | Configuration Complexity | Notes |
|-------------------|-------------------------|-------|
| **Okta** | Low | Pre-built Lovart app in Okta Integration Network |
| **Microsoft Entra ID (Azure AD)** | Low | Pre-built Lovart gallery app |
| **Google Workspace** | Low | SAML app configuration, documented below |
| **OneLogin** | Low | Pre-built app catalog entry |
| **Ping Identity / PingOne** | Medium | Manual SAML configuration required |
| **JumpCloud** | Medium | Manual SAML configuration required |
| **Auth0** | Low | Flexible SAML/OIDC, well-documented |
| **Any SAML 2.0 compliant IdP** | Medium | Generic SAML configuration documented below |

## SAML Configuration Overview

The integration follows the standard SAML 2.0 Service Provider (SP) initiated flow:

1. User navigates to Lovart (app.lovart.ai) or clicks a Lovart tile in their IdP dashboard.
2. Lovart redirects unauthenticated users to the configured IdP.
3. The IdP authenticates the user (or recognizes an existing session) and generates a SAML assertion.
4. The assertion is POSTed back to Lovart's Assertion Consumer Service (ACS) endpoint.
5. Lovart validates the assertion, maps SAML attributes to Lovart user properties, and creates or updates the user account (JIT provisioning).
6. User is redirected to the Lovart dashboard with an active session.

### Required SAML Configuration Parameters

When configuring Lovart as a Service Provider in your IdP, use these values:

| Parameter | Value |
|-----------|-------|
| **Entity ID / Issuer** | `https://app.lovart.ai/saml/metadata` |
| **ACS URL** | `https://app.lovart.ai/saml/acs` |
| **Single Logout URL** | `https://app.lovart.ai/saml/slo` |
| **Name ID Format** | `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` |
| **Signature Algorithm** | RSA-SHA256 |
| **Sign Assertion** | Required |
| **Sign Response** | Recommended |
| **Encrypt Assertion** | Optional (supported) |

### Required SAML Attributes

Lovart expects the following attributes in the SAML assertion. Attributes marked with (*) are required for JIT provisioning:

| SAML Attribute Name | Lovart Property | Required | Notes |
|---------------------|-----------------|----------|-------|
| `email` | User email | * | Must match a domain claimed by your Enterprise account |
| `firstName` | First name | * | Displayed in the Lovart UI |
| `lastName` | Last name | * | Displayed in the Lovart UI |
| `role` | Lovart role | | Maps to Lovart roles (admin, manager, designer, viewer) |
| `department` | Team/department | | Used for automatic team assignment |
| `title` | Job title | | Displayed on user profile |

### Role Mapping

The `role` SAML attribute maps to Lovart's permission levels:

| IdP Role Value | Lovart Role | Permissions |
|----------------|-------------|-------------|
| `admin` | Administrator | Full account control, billing, SSO configuration, user management |
| `manager` | Team Manager | Template publishing, brand kit governance, asset approval, user management for assigned teams |
| `designer` | Designer | Full design capabilities, template customization, brand kit usage |
| `viewer` | Viewer | View and comment on assets, no design capabilities |

If no `role` attribute is provided, users default to `designer`. If an unrecognized role value is sent, the user is provisioned as `viewer` (safe default).

## Step-by-Step Setup: Okta

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

1. **In Okta Admin Console:** Navigate to Applications > Browse App Catalog. Search for "Lovart." Select the Lovart app. Click "Add Integration."
2. **Configure the Lovart app:** On the Sign-On tab, verify that SAML 2.0 is selected. Note the Identity Provider metadata URL or download the metadata XML — you will need this in Lovart.
3. **In Lovart:** Navigate to Account Settings > Security > SSO Configuration. Select "Okta" from the IdP dropdown. Upload the metadata XML or paste the metadata URL. Click "Test Connection." Lovart validates the metadata and reports any configuration issues.
4. **Attribute mapping:** Verify that the default attribute mappings (email, firstName, lastName, role) match your Okta user profile attributes. Adjust if your organization uses different attribute names.
5. **Assign users:** In Okta, assign users or groups to the Lovart application. Users will be provisioned in Lovart on their first login (JIT provisioning).
6. **Test:** Have a test user log in to Lovart via the Okta dashboard or by navigating to app.lovart.ai. The user should be redirected to Okta for authentication, then redirected back to Lovart with an active session and the correct role.

## Step-by-Step Setup: Microsoft Entra ID (Azure AD)

1. **In Azure Portal:** Navigate to Entra ID > Enterprise Applications > New Application > Browse Gallery. Search for "Lovart." Select the Lovart gallery app. Click "Create."
2. **Configure SAML:** In the Lovart application page, navigate to Single Sign-On > SAML. Click "Edit" on Basic SAML Configuration. Verify the Entity ID and Reply URL match the values in the table above.
3. **Download metadata:** On the SAML configuration page, download the Federation Metadata XML.
4. **In Lovart:** Navigate to Account Settings > Security > SSO Configuration. Select "Microsoft Entra ID" from the IdP dropdown. Upload the metadata XML. Click "Test Connection."
5. **Attributes & Claims:** In Azure, configure the required attributes (email, firstName, lastName, role). By default, Azure maps `user.mail` to email, `user.givenname` to firstName, and `user.surname` to lastName. Add a custom claim for `role` if using role-based access control.
6. **Assign users:** Assign users or groups to the Lovart Enterprise Application in Azure.
7. **Test:** Log in with a test user to verify the full flow.

## Step-by-Step Setup: Google Workspace

1. **In Google Admin Console:** Navigate to Apps > Web and Mobile Apps > Add App > Add Custom SAML App.
2. **Configure the custom SAML app:** Enter "Lovart" as the app name. Download the IdP metadata. Enter the ACS URL and Entity ID from the table above. Set Name ID format to EMAIL. Map the required attributes (email → Primary Email, firstName → First Name, lastName → Last Name).
3. **In Lovart:** Navigate to Account Settings > Security > SSO Configuration. Select "Google Workspace" from the IdP dropdown. Upload the IdP metadata. Click "Test Connection."
4. **Enable the app:** In Google Admin, set the Lovart app to "ON for everyone" or "ON for some organizations" (recommended: start with a test group).
5. **Test:** Verify the login flow with a test user.

## Just-in-Time (JIT) Provisioning

Lovart uses JIT provisioning by default for SAML-authenticated users. When a user logs in via SAML for the first time:

1. **Domain verification:** The user's email domain must match a domain claimed by your Lovart Enterprise account. Users with unclaimed domains are rejected (this prevents unauthorized users from being provisioned).
2. **Account creation:** A Lovart user account is created with the attributes from the SAML assertion.
3. **License assignment:** The user consumes one Enterprise seat license. If your account has no available seats, the user receives an error message and is directed to contact their Lovart administrator.
4. **Team assignment:** If the `department` attribute is provided, the user is automatically added to the corresponding team in Lovart. If the team does not exist, it is created.
5. **Welcome:** The user lands on the Lovart dashboard with their provisioned role and permissions.

**Seat management:** Enterprise administrators can monitor seat usage on the Billing page. Users who have not logged in for 90+ days can be deprovisioned (their seat freed) without deleting their assets — their designs remain accessible to their team. Reactivation restores their account and re-consumes a seat.

## Security Policies

SSO is the foundation of enterprise security, but it is not the only layer. Lovart Enterprise supports additional security policies:

- **Session duration:** Configurable from 1 hour to 30 days. Default: 8 hours.
- **IdP-initiated session enforcement:** Require that all sessions originate from the IdP, disabling direct Lovart login for enterprise users. This ensures the IdP's session policies (MFA, device trust, location-based access) are always enforced.
- **IP allowlisting:** Restrict access to specific IP ranges. Users outside allowed ranges are blocked even with valid SAML assertions. Configurable per team or account-wide.
- **Audit logging:** All login events and SSO configuration changes are logged and available to enterprise administrators. Logs are retained for 12 months.

## Common Troubleshooting Scenarios

### "SAML Response Validation Failed — Signature Mismatch"

**Cause:** The certificate in the IdP metadata does not match the certificate used to sign the SAML assertion.
**Resolution:** In your IdP, verify the signing certificate. If it has been rotated, update the metadata in Lovart (Account Settings > Security > SSO Configuration > Update Metadata).

### "User Not Found — Domain Not Claimed"

**Cause:** The email domain in the user's SAML assertion has not been claimed by your Lovart Enterprise account.
**Resolution:** In Lovart, navigate to Account Settings > Domains. Add and verify the domain. DNS TXT record verification is required. Once verified, users with that email domain will be provisioned automatically.

### "No Available Seats"

**Cause:** Your Enterprise plan has reached its licensed seat limit.
**Resolution:** Navigate to Account Settings > Billing to add seats, or deprovision inactive users to free seats. Seat changes take effect immediately.

### "Role Not Recognized"

**Cause:** The `role` attribute in the SAML assertion contains a value that does not match Lovart's expected role values.
**Resolution:** Verify the role mapping in your IdP. Valid values (case-insensitive): admin, manager, designer, viewer. If the issue persists, check for trailing spaces or encoding issues in the SAML assertion.

### "Endless Redirect Loop"

**Cause:** Usually a cookie or session conflict between the IdP and Lovart.
**Resolution:** Clear browser cookies. Verify that your IdP is not configured to require re-authentication for every SAML request (this creates a loop when Lovart redirects to the IdP and the IdP immediately redirects back). Check that the session duration in both the IdP and Lovart are compatible.

## Getting Support

[IMAGE 4 PLACEHOLDER — Brand CTA]

Enterprise customers have access to dedicated SSO integration support:
- **Documentation:** Full technical documentation at docs.lovart.ai/sso
- **Support ticket:**  with "SSO" in the subject line for priority routing
- **Integration call:** Enterprise customers can schedule a 30-minute integration call with a Lovart solutions engineer

---

*Lovart Enterprise SSO features are available on the Enterprise plan ($149/month per seat). SSO configuration requires Administrator role in Lovart and appropriate privileges in your identity provider. Test your SSO configuration with a test user before rolling out to your full organization.*

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
A professional yet approachable person sitting at their desk, looking slightly frustrated at their computer screen while trying to create a design — warm natural lighting, candid documentary style

**Image 2 — The Conceptual Diagram**:
A hand-drawn sketch diagram showing the step-by-step workflow for creating designs with AI — clean line art on grid paper, arrows connecting each step, minimalist style

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart ChatCanvas interface showing the key feature described in this article — clean UI, uncluttered, with a visible result]

**Image 4 — Brand CTA**:
Professional brand visual for Lovart AI Design Agent — showing the final beautiful design result described in SSO and SAML Integration Guide for Enterprise Team — modern, aspirational, cinematic lighting

