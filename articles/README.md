# Newsletter articles

Two standalone newsletter pieces drawn from *The Missing Package Manager — Managing AI
Agent Context with APM* (this repo's book). Both are getting-started level and follow a
**problem → solution** arc in the essayistic, de-hyped voice of
[agentengineering.co](https://www.agentengineering.co) — written for practitioners who are
past the release-and-model hype and care about the engineering underneath.

They tell the **same story from two angles**. Pick the one that fits the issue, or run them
as a two-part series (developer pain first, then the governance response).

| File | Angle | Lead property | Reader |
|---|---|---|---|
| [`the-undeclared-dependency.md`](./the-undeclared-dependency.md) | **Developer efficiency** — agent-context drift, the "works on my machine" tax, onboarding, and the daily `apm install` loop | Portability + reproducibility | Individual devs and team leads |
| [`the-agent-supply-chain.md`](./the-agent-supply-chain.md) | **Enterprise governance** — prompts as supply-chain surface, install-time policy, `warn → block` rollout, and fleet scale | Provenance/security + governance | Platform, security, and eng leaders |

Both are ~780–800 words, sit inside the requested 500–800 range, and ground every claim in
the book and the official APM docs (`microsoft.github.io/apm`). The shared spine — *agent
context is where application code was before npm, pip, and Cargo* — is deliberate; the two
pieces diverge on which of APM's promises they emphasize.
