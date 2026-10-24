# Awesome Bot Teams [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of awesome bot teams, multi-agent frameworks, collaborative AI bot stacks, role templates, and operational setups for autonomous and human-in-the-loop workflows.

Whether you are coordinating multi-agent software engineering squads, running autonomous content studios, orchestrating customer ops, or deploying specialized bot clusters like Grok bot, Mausbot, and OpenMausbot, this repository provides frameworks, protocols, and ready-to-initiate team templates.

---

## Contents

- [Platforms & Bot Runtimes](#platforms--bot-runtimes)
- [Bot Teams & Noteworthy Swarms](#bot-teams--noteworthy-swarms)
- [Ready-to-Initiate Team Templates](#ready-to-initiate-team-templates)
  - [Software Engineering Squad](#1-software-engineering-squad)
  - [Solo Founder & Executive Cockpit](#2-solo-founder--executive-cockpit)
  - [Growth & Content Studio Swarm](#3-growth--content-studio-swarm)
  - [Deep Research & Intelligence Cell](#4-deep-research--intelligence-cell)
  - [Cyber Security & Red Team](#5-cyber-security--red-team)
  - [Community & Support Guild](#6-community--support-guild)
- [Team Topologies & Orchestration](#team-topologies--orchestration)
- [Communication & Coordination Protocols](#communication--coordination-protocols)
- [Memory, State & Context Engines](#memory-state--context-engines)
- [Observability, Cockpits & TUIs](#observability-cockpits--tuis)
- [Safety Brakes, Cost Governors & Human-in-the-Loop](#safety-brakes-cost-governors--human-in-the-loop)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)

---

## Platforms & Bot Runtimes

- [AutoGen](https://github.com/microsoft/autogen) - Microsoft's multi-agent conversation framework enabling multi-role collaboration and customizable tool use.
- [CrewAI](https://github.com/crewAIInc/crewAI) - Framework for orchestrating role-playing autonomous AI agents that work together to accomplish complex tasks.
- [LangGraph](https://github.com/langchain-ai/langgraph) - Cyclic state-machine framework for multi-actor LLM applications with human-in-the-loop controls.
- [MetaGPT](https://github.com/geekan/MetaGPT) - Multi-agent framework that assigns distinct software company roles (Product Manager, Architect, Project Manager, Engineer, QA) to LLMs via standard operating procedures (SOPs).
- [ChatDev](https://github.com/OpenBMB/ChatDev) - Virtual software company runtime where specialized agent bots communicate through simulated waterfall development phases.
- [ElizaOS](https://github.com/elizaOS/eliza) - Flexible multi-agent simulation framework with modular connectors (Discord, Twitter/X, Telegram) and character cards.
- [Swarms](https://github.com/kyegomez/swarms) - Enterprise-grade production framework for orchestrating reliable swarms of diverse AI models and specialized bots.
- [Camel-AI](https://github.com/camel-ai/camel) - Communicative agent framework demonstrating cooperative autonomous role-playing via inception prompting.
- [AgentVerse](https://github.com/OpenBMB/AgentVerse) - Modular platform for simulating autonomous agent environments, social dynamics, and task-solving teams.

---

## Bot Teams & Noteworthy Swarms

- [Grok Bot](https://x.ai) - Real-time conversational and search-augmented bot ecosystem with native vision, live X feed awareness, and multimodal function execution.
- [Mausbot](https://github.com) - Modular autonomous assistant bot specialized in task routing, system telemetry monitoring, and local-first automation.
- [OpenMausbot](https://github.com) - Open-source variant of Mausbot providing decentralized agent tooling, customizable skills, and peer-to-peer bot handoffs.
- [OpenClaw](https://github.com) - Sovereign personal agent framework and memory runtime designed for continuous operation and secure tool mesh integration.
- [Smolagents](https://github.com/huggingface/smolagents) - Lightweight library by Hugging Face where agents write Python code actions instead of JSON tool calls.

---

## Ready-to-Initiate Team Templates

Pre-configured role rosters, system prompt blueprints, handoff triggers, and input/output contracts. Each template is ready to deploy directly in your multi-agent orchestrator:

| Template | Primary Topology | Target Use Case | Specs & Prompts |
|:---|:---|:---|:---:|
| **1. Software Engineering Squad** | Hierarchical + QA Gate | Architecture, implementation, adversarial testing, and release PRs. | [`View Template`](templates/software-engineering-squad.md) |
| **2. Solo Founder Cockpit** | Hub-and-Spoke (Chief of Staff) | Strategic triage, revenue & burn monitoring, product roadmaps, customer support. | [`View Template`](templates/solo-founder-cockpit.md) |
| **3. Growth & Content Studio** | Pipeline + Feedback Loop | Social media listening, thread/newsletter ghostwriting, visual cards, scheduling. | [`View Template`](templates/growth-content-studio.md) |
| **4. Deep Research Cell** | Parallel Fan-out + Fact Check | Market intelligence, academic literature surveys, citation cross-examination. | [`View Template`](templates/deep-research-cell.md) |
| **5. Cyber Security Red Team** | Sandbox Pipeline | Attack surface recon, automated fuzzing, exploit simulation, verified patching. | [`View Template`](templates/cyber-security-redteam.md) |
| **6. Community Support Guild** | Frontline Triage + Tier Pods | Community greeting, docs FAQ resolution, moderation safety, human escalation. | [`View Template`](templates/community-support-guild.md) |

### 1. Software Engineering Squad
- **Roles**: Squad Architect, Implementer / Coder, Adversarial QA, DevOps & Release Bot.
- **Protocol**: Spec-driven development with mandatory test suite execution before code lands on main.
- **Link**: [templates/software-engineering-squad.md](templates/software-engineering-squad.md)

### 2. Solo Founder & Executive Cockpit
- **Roles**: Chief of Staff, Product Strategist, Revenue Sentinel, Customer Concierge.
- **Protocol**: Asynchronous briefing digest with priority triage and cost/leak alerts.
- **Link**: [templates/solo-founder-cockpit.md](templates/solo-founder-cockpit.md)

### 3. Growth & Content Studio Swarm
- **Roles**: Trend & Signal Scout, Editorial Director, Ghostwriter, Media Generator, Distribution Scheduler.
- **Protocol**: Trend-to-draft pipeline with human sign-off checkpoint for brand safety.
- **Link**: [templates/growth-content-studio.md](templates/growth-content-studio.md)

### 4. Deep Research & Intelligence Cell
- **Roles**: Research Director, Parallel Harvesters, Adversarial Fact-Checker, Synthesis Author.
- **Protocol**: Multi-vector querying followed by strict source verification and hallucination pruning.
- **Link**: [templates/deep-research-cell.md](templates/deep-research-cell.md)

### 5. Cyber Security & Red Team
- **Roles**: Recon & Threat Modeler, Exploit & Fuzzing Specialist, Remediation Engineer, Audit Lead.
- **Protocol**: Isolated sandbox testing and patch verification against CVSS/OWASP criteria.
- **Link**: [templates/cyber-security-redteam.md](templates/cyber-security-redteam.md)

### 6. Community & Support Operations Guild
- **Roles**: Triage & Greeting Bot, Docs Concierge, Sentiment & Safety Guardian, Escalation Liaison.
- **Protocol**: Immediate automated first response with structured handoff cards to human staff when confidence drops below 85%.
- **Link**: [templates/community-support-guild.md](templates/community-support-guild.md)

---

## Team Topologies & Orchestration

Choosing the right communication topology prevents infinite loops and coordination deadlocks:

1. **Hierarchical / Supervisor (Hub-and-Spoke)**: A lead router bot breaks down problems and delegates tasks to domain specialists. Best for well-defined workflows where quality checks are required.
2. **Sequential Pipeline (Assembly Line)**: Agent A produces an output consumed by Agent B, which passes to Agent C. Best for content creation, ETL pipelines, and document drafting.
3. **Blackboard Architecture (Shared Memory Workspace)**: Agents read from and write to a common shared state/database independently. Best for complex problem-solving and open-ended research.
4. **Peer-to-Peer Consensus Swarm**: Agents negotiate, critique, and vote on proposals until consensus is achieved. Best for decision analysis and adversarial code reviews.

---

## Communication & Coordination Protocols

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - Open standard for connecting AI agents and bots to databases, APIs, dev tools, and external services.
- [A2A (Agent-to-Agent Protocol)](https://github.com) - Structured JSON/JSONL protocol for exchanging tasks, context, and capabilities between decentralized agents.
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification) - Lightweight remote procedure call standard commonly used for decoupled bot IPC.
- [Server-Sent Events (SSE) & WebSockets](https://developer.mozilla.org) - Real-time bidirectional streaming protocols for multi-agent chatter and live user observability.

---

## Memory, State & Context Engines

- [Letta (formerly MemGPT)](https://github.com/letta-ai/letta) - State management and memory runtime that provides persistent OS-like memory tiers for LLM agents.
- [Mem.ai](https://mem.ai) - Self-organizing personal and team knowledge graph with semantic search and automatic context injection.
- [Supermemory](https://supermemory.ai) - Durable bookmarking and context repository for AI agents and knowledge workers.
- [Graphiti](https://github.com/getzep/graphiti) - Knowledge graph framework designed for dynamic, temporal multi-agent memory retrieval.
- [Chroma](https://github.com/chroma-core/chroma) - Open-source embedding vector database for agent episodic and semantic document memory.

---

## Observability, Cockpits & TUIs

- [Langfuse](https://github.com/langfuse/langfuse) - Open source LLM engineering platform for tracing multi-agent execution graphs, latency, and cost.
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - AI observability and evaluation platform with native trace visualizations for complex agent graphs.
- [Helicone](https://github.com/Helicone/helicone) - Lightweight LLM proxy and caching gateway providing real-time cost, token tracking, and rate limiting.
- [Charm CLI (Bubble Tea / Lip Gloss)](https://github.com/charmbracelet/bubbletea) - Golang TUI framework for building decoupled, high-performance terminal cockpits for live bot operations.

---

## Safety Brakes, Cost Governors & Human-in-the-Loop

- **Max Step Governors**: Enforce hard execution ceilings (e.g., maximum 15 turns per task) to prevent runaway recursive tool calls.
- **Token & Dollar Budgets**: Pin strict monetary caps ($0.50 / task) with circuit breakers that halt execution if breached.
- **Destructive Action Confirmation Gates**: Require cryptographic or human confirmation before executing `rm -rf`, `DROP TABLE`, public social posts, or fund transfers.
- **Dead Man's Switches**: Automated heartbeat monitors that pause bot execution if the human operator disconnects or fails a verification challenge.

---

## Contributing

Contributions are welcome! Please read the [Contribution Guidelines](CONTRIBUTING.md) and review the [Code of Conduct](CODE_OF_CONDUCT.md) first.

```bash
git clone https://github.com/RemyLoveLogicAI/awesome-bot-teams.git
cd awesome-bot-teams
```

---

## Code of Conduct

This project is governed by the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

---

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](LICENSE)

To the extent possible under law, the authors waive all copyright and related or neighboring rights to this work under [CC0 1.0 Universal](LICENSE).
