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
| [`the-undeclared-dependency.md`](./the-undeclared-dependency.md) | **Developer efficiency** — agent-context drift, the "works on my machine" tax, onboarding, and a runnable `apm install` quick-start | Portability + reproducibility | Individual devs and team leads |
| [`the-agent-supply-chain.md`](./the-agent-supply-chain.md) | **Enterprise governance** — prompts as supply-chain surface, install-time policy, `warn → block` rollout, and fleet scale | Provenance/security + governance | Platform, security, and eng leaders |

The governance piece is ~800 words. The developer piece runs a little longer (~890) because it
carries a hands-on quick-start that installs a real skill
([webmaxru/web-ai-agent-skills](https://github.com/webmaxru/web-ai-agent-skills#install-individual-skills))
via APM and closes on the [Agent Package Manager skill](https://github.com/webmaxru/ai-native-dev#agent-package-manager);
trim the quick-start commentary to land it back under 800 if an issue needs it. Both ground
every claim in the book and the official [APM docs](https://microsoft.github.io/apm/), and link
out to [APM on GitHub](https://github.com/microsoft/apm) and the
[live book](https://apm.isainative.dev/). The shared spine — *agent context is where application
code was before npm, pip, and Cargo* — is deliberate; the two pieces diverge on which of APM's
promises they emphasize.
