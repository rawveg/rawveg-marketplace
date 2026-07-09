---
name: xquik-api
description: Xquik API Development and Integration
---

# Xquik API Skill

Use this skill when building AI-agent workflows, dashboards, SDKs, automations, or webhooks that interact with Xquik's X/Twitter automation API.

## When to Use This Skill

This skill should be triggered when:
- Integrating Xquik API endpoints into an application or agent workflow
- Building X/Twitter search, profile lookup, follower export, or media workflows
- Connecting Xquik webhooks to product events or automation systems
- Using the Xquik MCP server from an AI agent
- Working with generated Xquik SDKs or REST API clients
- Adding gated posting or write-action controls to an internal tool
- Debugging API authentication, pagination, rate limits, or webhook signatures

## Key Concepts

- **Authentication**: Send an Xquik API key with requests that need account access.
- **Read workflows**: Search, profile lookup, follower export, media, trends, monitors, and radar-style discovery.
- **Write workflows**: Treat posting and account actions as gated operations. Require explicit user intent and environment controls.
- **Webhooks**: Use HMAC verification before trusting incoming webhook payloads.
- **MCP**: Prefer the MCP server when an agent should call Xquik as a tool instead of writing a bespoke client.
- **SDKs**: Use generated SDKs when available so request and response contracts stay typed.

## Quick Reference

### API Key

Keep the API key outside source control:

```bash
export XQUIK_API_KEY="your_api_key"
```

### REST Request Pattern

```bash
curl -sS "https://xquik.com/api/v1/<endpoint>" \
  -H "Authorization: Bearer ${XQUIK_API_KEY}" \
  -H "Accept: application/json"
```

### Agent Tool Pattern

When exposing Xquik to an agent:

1. Register only the read tools needed for the task.
2. Keep write tools disabled unless the user explicitly opts in.
3. Require clear confirmation before posting or modifying accounts.
4. Log request IDs and sanitized error messages for troubleshooting.

### Webhook Verification Pattern

```javascript
import crypto from "node:crypto";

function verifyXquikWebhook(payload, signature, secret) {
  const expected = crypto
    .createHmac("sha256", secret)
    .update(payload)
    .digest("hex");

  return crypto.timingSafeEqual(
    Buffer.from(signature, "hex"),
    Buffer.from(expected, "hex")
  );
}
```

## Best Practices

- Store `XQUIK_API_KEY` in a secret manager or local environment file.
- Do not print API keys, webhook secrets, access tokens, or raw account material.
- Use pagination helpers for list endpoints instead of assuming one page is complete.
- Retry transient `429` and `5xx` responses with capped exponential backoff.
- Keep posting and other write actions behind explicit opt-in controls.
- Validate webhook signatures before parsing event data.
- Use SDK types or generated clients for production integrations.

## Common Tasks

### Add Xquik to a Dashboard

1. Create a server-side API route that owns the Xquik API key.
2. Fetch read-only data from Xquik.
3. Return only the fields the dashboard needs.
4. Render status, pagination, and empty states explicitly.

### Add Xquik to an Agent

1. Start with read-only tools for search and profile lookup.
2. Add webhooks for asynchronous updates.
3. Register posting tools only after adding an explicit action gate.
4. Test with a non-production account before enabling real actions.

### Handle API Errors

- `401`: Check API key presence and rotation status.
- `403`: Confirm the current plan and action gate allow this workflow.
- `404`: Verify the target resource or account identifier.
- `429`: Back off and retry within the documented limit.
- `5xx`: Retry transient failures and surface a concise user-facing message.

## Related Resources

- Xquik repository: https://github.com/Xquik-dev/x-twitter-scraper
- Xquik docs: https://docs.xquik.com
