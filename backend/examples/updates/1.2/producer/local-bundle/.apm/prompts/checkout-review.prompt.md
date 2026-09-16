---
description: Secure checkout code review checklist for Meridian services
---

# Checkout review

Review the target changes against Meridian standards and report each item as
PASS or FAIL with a `file:line` reference:

1. Currency math uses the `Money` value object (no raw floats or decimals).
2. Payment retries are idempotent (keyed by `paymentAttemptId`).
3. No card data (PAN/CVV/track) is logged or persisted outside the vault.
4. External tool calls go through declared, governed MCP servers only.
