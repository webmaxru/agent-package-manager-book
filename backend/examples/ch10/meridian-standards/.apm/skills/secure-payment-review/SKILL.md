---
name: secure-payment-review
description: Reviews payment and checkout code for PCI-sensitive data handling, idempotency, and Meridian Money-type usage. Use when reviewing changes to payment routing, checkout, or fraud-review code.
---

# Secure payment review

When reviewing payment or checkout code:

1. **Money type** — confirm all currency math uses the Meridian `Money` value
   object; flag raw float/decimal arithmetic on monetary values.
2. **Idempotency** — confirm retries are keyed by `paymentAttemptId`.
3. **Data handling** — flag any log, trace, or persistence of PAN/CVV/track data.
4. **Tool trust** — confirm external calls use declared MCP servers only.

Output a table of findings with severity and a `file:line` reference.
