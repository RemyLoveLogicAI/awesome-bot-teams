# Template: Community & Support Operations Guild

> **Topology**: Front-line Triage -> Subject Matter Pods -> Human Escalation  
> **Ideal For**: Discord servers, Telegram communities, GitHub Discussions, and customer support queues.

---

## 1. Roster & Roles

| Role | Responsibility | Input | Output | Tools / Permissions |
|------|---------------|-------|--------|---------------------|
| **Triage & Greeting Bot** | Welcomes newcomers, parses inbound inquiries, tags intent, routes to specialist pods. | Raw community message / ticket | Tagged intent & routing event | Community webhook, read-only feed |
| **Knowledge & Docs Concierge** | Answers technical questions by referencing canonical documentation and verified FAQs. | Customer question & query tags | Accurate markdown answer with links | Vector search over docs, embedding retriever |
| **Sentiment & Safety Guardian** | Monitors spam, scam links, toxic behavior, and raid attempts. Applies timeouts/bans. | Real-time chat stream | Warning / Timeout / Flag to mods | Moderation API, ban hammer |
| **Human Escalation Liaison** | Prepares concise escalation context for human staff when bots lack confidence or high-stakes issues arise. | Unresolved thread context | Staff alert card with recommended action | Webhook to staff channel (Slack/Discord) |
