# meridian-standards

Shared Meridian engineering context, packaged for APM. Install it to get the
same always-on instruction, checkout review prompt, and secure-payment-review
skill that the `meridian-checkout` service uses — through the normal
`apm install` loop.

```bash
# Primary (git) distribution — SKIPPED-needs-network in the book:
apm install meridian-finance/meridian-standards#v1.0.0

# Offline (development) — install from a local path:
apm install ./meridian-standards
```

## Primitives

- `.apm/instructions/meridian-engineering.instructions.md` — always-on rules
  (currency `Money` type, idempotent retries, no card data in logs).
- `.apm/prompts/checkout-review.prompt.md` — a runnable review checklist,
  invoked via `apm run`.
- `.apm/skills/secure-payment-review/SKILL.md` — a reusable review capability.

## Packaging

This package sets `targets:` but declares no `dependencies:`, so `apm pack`
runs in **plugin.json mode**: it writes `.github/plugin/plugin.json` (Copilot)
and `.claude-plugin/plugin.json` (Claude) in-tree. It does **not** produce a
`build/` bundle or a `--archive` `.zip` — that path requires a `dependencies:`
closure. See [../README.md](../README.md) and the
[Chapter 10 reference](../../../content/research/10-becoming-a-producer-reference.md).
