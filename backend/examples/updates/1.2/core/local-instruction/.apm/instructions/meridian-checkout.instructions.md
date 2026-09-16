---
description: Meridian checkout service engineering rules
applyTo: "**/*.{ts,tsx,md}"
---

Use the Meridian `Money` value object for currency math. Treat checkout retries as
idempotent operations keyed by `paymentAttemptId`. Never suggest storing card data in
application logs.
