---
description: Meridian shared engineering rules for AI agents
applyTo: "**/*.{ts,tsx,js,jsx,md}"
---

# Meridian engineering standards

- Use the Meridian `Money` value object for all currency math; never use raw
  floats or decimals for monetary amounts.
- Treat checkout and payment retries as idempotent operations keyed by
  `paymentAttemptId`.
- Never store, log, or echo full card numbers, CVVs, or unmasked PANs.
- Prefer explicit, typed errors over a generic `Error` in payment-routing code.
