# Awesome Bot Teams [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

<div align="center">

[![CI](https://github.com/RemyLoveLogicAI/awesome-bot-teams/actions/workflows/lint.yml/badge.svg)](https://github.com/RemyLoveLogicAI/awesome-bot-teams/actions)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Frameworks](https://img.shields.io/badge/export-CrewAI%20%7C%20AutoGen%20%7C%20LangGraph-orange.svg)](#instant-team-initiation-cli)
[![Docs](https://img.shields.io/badge/docs-specifications-blueviolet.svg)](docs/ARCHITECTURE.md)

<p align="center">
  <b>A curated list of awesome bot teams, multi-agent frameworks, collaborative AI bot stacks, role templates, and operational setups for autonomous and human-in-the-loop workflows.</b>
</p>

<sub>Built for engineers and operators coordinating agent swarms, software squads, autonomous research cells, and bot clusters like Grok bot, Mausbot, OpenMausbot, and OpenClaw.</sub>

</div>

---

## Quickstart in 30 Seconds

This repository includes a zero-dependency CLI tool ([`init-team.py`](init-team.py)) that validates and exports production-grade scaffolds for any bot team directly to **CrewAI**, **AutoGen**, or **LangGraph**:

```bash
# 1. Clone the repository
git clone https://github.com/RemyLoveLogicAI/awesome-bot-teams.git
cd awesome-bot-teams

# 2. List all available team blueprints
python3 init-team.py --list

# 3. Launch the Dual-Mode Terminal Cockpit (Curses TUI)
python3 cockpit.py
# Or launch via: python3 init-team.py --cockpit

# 4. Export an instant runnable scaffold (CrewAI, AutoGen, or LangGraph)
python3 init-team.py --template software-engineering-squad --export crewai
python3 init-team.py --template multi-model-debate-pod --export autogen
python3 init-team.py --template solo-founder-cockpit --export langgraph

# 5. Pipe commands through the JSONL Agent Protocol
echo "list" | python3 cockpit.py
echo "validate" | python3 cockpit.py
```

---

## Contents

- [Platforms & Bot Runtimes](#platforms--bot-runtimes)
- [Bot Teams & Noteworthy Swarms](#bot-teams--noteworthy-swarms)
- [Instant Team Initiation CLI](#instant-team-initiation-cli)
- [Ready-to-Initiate Team Templates](#ready-to-initiate-team-templates)
  - [1. Software Engineering Squad](#1-software-engineering-squad)
  - [2. Multi-Model Consensus & Debate Pod](#2-multi-model-consensus--debate-pod)
  - [3. Solo Founder & Executive Cockpit](#3-solo-founder--executive-cockpit)
  - [4. Growth & Content Studio Swarm](#4-growth--content-studio-swarm)
  - [5. Deep Research & Intelligence Cell](#5-deep-research--intelligence-cell)
  - [6. Cyber Security & Red Team](#6-cyber-security--red-team)
  - [7. Community & Support Guild](#7-community--support-guild)
  - [8. Autonomous Web3 & Risk Sentinel](#8-autonomous-web3--risk-sentinel)
- [Team Topologies & Comparison Matrix](#team-topologies--comparison-matrix)
- [Communication & Coordination Protocols](#communication--coordination-protocols)
- [Memory, State & Context Engines](#memory-state--context-engines)
- [Observability, Cockpits & TUIs](#observability-cockpits--tuis)
- [Safety Brakes, Cost Governors & Human-in-the-Loop](#safety-brakes-cost-governors--human-in-the-loop)
- [Documentation Hub](#documentation-hub)
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
- [Smolagents](https://github.com/huggingface/smolagents) - Lightweight library by Hugging Face where agents write Python code actions instead of JSON tool calls.
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel) - Enterprise SDK by Microsoft integrating LLMs with conventional programming languages and agent routing.

---

## Bot Teams & Noteworthy Swarms

- [Grok Bot](https://x.ai) - Real-time conversational and search-augmented bot ecosystem with native vision, live X feed awareness, and multimodal function execution.
- [Mausbot](https://github.com) - Modular autonomous assistant bot specialized in task routing, system telemetry monitoring, and local-first automation.
- [OpenMausbot](https://github.com) - Open-source variant of Mausbot providing decentralized agent tooling, customizable skills, and peer-to-peer bot handoffs.
- [OpenClaw](https://github.com) - Sovereign personal agent framework and memory runtime designed for continuous operation and secure tool mesh integration.
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) - Open-source software development agent platform (formerly OpenDevin) capable of modifying code, running bash commands, and opening PRs.
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) - Autonomous software engineering agent by Princeton University that turns GitHub issues into resolved pull requests.
- [Devv.ai](https://devv.ai) - AI-powered search engine and autonomous developer research assistant integrating repository-wide contextual grounding.

---

## Instant Team Initiation CLI

The repository includes [`init-team.py`](init-team.py), a zero-dependency CLI tool to inspect, validate, and bootstrap multi-agent bot teams:

```
$ python3 init-team.py --list

🤖 Available Awesome Bot Teams:

  ID                             Topology               Description
  -------------------------------------------------------------------------------------
  community-support-guild        triage_pod             Community & Support Operations Guild
  cyber-security-redteam         sandbox_pipeline       Cyber Security & Smart Contract Red Team
  deep-research-cell             fan_out_synthesis      Deep Research & Intelligence Cell
  growth-content-studio          pipeline               Growth & Content Studio Swarm
  multi-model-debate-pod         consensus_debate       Multi-Model Consensus & Debate Pod
  software-engineering-squad     hierarchical_gate      Autonomous Software Engineering Squad
  solo-founder-cockpit           hub_and_spoke          Solo Founder & Executive Cockpit
  web3-risk-sentinel             stream_circuit_breaker Autonomous Web3 & Risk Sentinel
```

### CLI Feature Matrix
- **Schema Validation**: Run `python3 init-team.py --validate` to verify all YAML schemas against strict structural criteria.
- **Direct Output to File**: Use `--output <path>` (e.g. `python3 init-team.py --template software-engineering-squad --export langgraph --output team.py`).
- **Zero Third-Party Dependencies**: Runs strictly on standard library Python 3.8+.

Read the complete [CLI Reference Manual](docs/CLI_REFERENCE.md) for advanced options.

---

## Ready-to-Initiate Team Templates

Pre-configured role rosters, system prompt blueprints, handoff triggers, and input/output contracts. Each template comes with detailed Markdown specifications and programmatic YAML schemas in [`templates/schemas/`](templates/schemas/):

| Template | Primary Topology | Target Use Case | Specs & Prompts | Executable Schema |
|:---|:---|:---|:---:|:---:|
| **1. Software Engineering Squad** | Hierarchical + QA Gate | Architecture, implementation, adversarial testing, release PRs. | [`Spec`](templates/software-engineering-squad.md) | [`YAML`](templates/schemas/software-engineering-squad.yaml) |
| **2. Multi-Model Debate Pod** | Consensus & Cross-Critique | Unbiasing complex decisions, theorem proving, hallucination pruning. | [`Spec`](templates/multi-model-debate-pod.md) | [`YAML`](templates/schemas/multi-model-debate-pod.yaml) |
| **3. Solo Founder Cockpit** | Hub-and-Spoke (Chief of Staff) | Strategic triage, revenue & burn monitoring, product roadmaps, support. | [`Spec`](templates/solo-founder-cockpit.md) | [`YAML`](templates/schemas/solo-founder-cockpit.yaml) |
| **4. Growth & Content Studio** | Pipeline + Feedback Loop | Social listening, thread/newsletter ghostwriting, visual cards, scheduling. | [`Spec`](templates/growth-content-studio.md) | [`YAML`](templates/schemas/growth-content-studio.yaml) |
| **5. Deep Research Cell** | Parallel Fan-out + Fact Check | Market intelligence, academic literature surveys, citation verification. | [`Spec`](templates/deep-research-cell.md) | [`YAML`](templates/schemas/deep-research-cell.yaml) |
| **6. Cyber Security Red Team** | Sandbox Pipeline | Attack surface recon, automated fuzzing, exploit simulation, patching. | [`Spec`](templates/cyber-security-redteam.md) | [`YAML`](templates/schemas/cyber-security-redteam.yaml) |
| **7. Community Support Guild** | Frontline Triage + Tier Pods | Community greeting, docs FAQ resolution, moderation safety, escalation. | [`Spec`](templates/community-support-guild.md) | [`YAML`](templates/schemas/community-support-guild.yaml) |
| **8. Web3 & Risk Sentinel** | Stream Circuit Breaker | On-chain event monitoring, mempool exploit detection, treasury protection. | [`Spec`](templates/web3-risk-sentinel.md) | [`YAML`](templates/schemas/web3-risk-sentinel.yaml) |

### 1. Software Engineering Squad
- **Roles**: Squad Architect, Implementer / Coder, Adversarial QA, DevOps & Release Bot.
- **Protocol**: Spec-driven development with mandatory test suite execution before code lands on main.
- **Links**: [Specification](templates/software-engineering-squad.md) · [YAML Schema](templates/schemas/software-engineering-squad.yaml)

### 2. Multi-Model Consensus & Debate Pod
- **Roles**: Debater Alpha (DeepSeek R1), Debater Beta (Claude 3.7 Sonnet), Debater Gamma (Grok 3), Consensus Arbiter (GPT-4o).
- **Protocol**: Independent parallel solution generation followed by round-robin cross-critique and arbiter synthesis.
- **Links**: [Specification](templates/multi-model-debate-pod.md) · [YAML Schema](templates/schemas/multi-model-debate-pod.yaml)

### 3. Solo Founder & Executive Cockpit
- **Roles**: Chief of Staff, Product Strategist, Revenue Sentinel, Customer Concierge.
- **Protocol**: Asynchronous briefing digest with priority triage and cost/leak alerts.
- **Links**: [Specification](templates/solo-founder-cockpit.md) · [YAML Schema](templates/schemas/solo-founder-cockpit.yaml)

### 4. Growth & Content Studio Swarm
- **Roles**: Trend & Signal Scout, Editorial Director, Ghostwriter, Media Generator, Distribution Scheduler.
- **Protocol**: Trend-to-draft pipeline with human sign-off checkpoint for brand safety.
- **Links**: [Specification](templates/growth-content-studio.md) · [YAML Schema](templates/schemas/growth-content-studio.yaml)

### 5. Deep Research & Intelligence Cell
- **Roles**: Research Director, Parallel Harvesters, Adversarial Fact-Checker, Synthesis Author.
- **Protocol**: Multi-vector querying followed by strict source verification and hallucination pruning.
- **Links**: [Specification](templates/deep-research-cell.md) · [YAML Schema](templates/schemas/deep-research-cell.yaml)

### 6. Cyber Security & Red Team
- **Roles**: Recon & Threat Modeler, Exploit & Fuzzing Specialist, Remediation Engineer, Audit Lead.
- **Protocol**: Isolated sandbox testing and patch verification against CVSS/OWASP criteria.
- **Links**: [Specification](templates/cyber-security-redteam.md) · [YAML Schema](templates/schemas/cyber-security-redteam.yaml)

### 7. Community & Support Operations Guild
- **Roles**: Triage & Greeting Bot, Docs Concierge, Sentiment & Safety Guardian, Escalation Liaison.
- **Protocol**: Immediate automated first response with structured handoff cards to human staff when confidence drops below 85%.
- **Links**: [Specification](templates/community-support-guild.md) · [YAML Schema](templates/schemas/community-support-guild.yaml)

### 8. Autonomous Web3 & Risk Sentinel
- **Roles**: Mempool & Event Scout, Attack Vector Classifier, Risk & Treasury Arbiter, Emergency Guard Bot.
- **Protocol**: Stream monitoring with EVM fork exploit simulation and pre-authorized circuit breaker triggers.
- **Links**: [Specification](templates/web3-risk-sentinel.md) · [YAML Schema](templates/schemas/web3-risk-sentinel.yaml)

---

## Team Topologies & Comparison Matrix

Choosing the right coordination topology prevents recursive tool loops, deadlocks, and token waste:

| Topology Pattern | Control Flow | Best Use Case | Primary Bottleneck | Recommended Engine |
|:---|:---|:---|:---|:---|
| **Hierarchical Gate** | Supervisor $\to$ Worker $\to$ QA | Software Engineering, Formal RFCs | Supervisor latency | LangGraph / CrewAI |
| **Sequential Pipeline** | Step $A \to$ Step $B \to$ Step $C$ | Content Creation, ETL Pipelines | Cascading errors | LangGraph / Swarms |
| **Consensus Debate** | Cross-Critique $\to$ Arbiter | Algorithmic Decisions, Truth Auditing | Token consumption | AutoGen / CrewAI |
| **Blackboard Workspace** | Shared Central State Store | Open-Ended Research, Memory Ops | State conflicts | Letta / Redis |
| **Stream Circuit Breaker** | Ingest $\to$ Classify $\to$ Pause | DeFi Telemetry, Cloud Security | False positives | Custom Webhooks / SSE |
| **Triage Pod** | Intake $\to$ Domain Routing $\to$ Staff | Support Desks, Discord Guilds | Unmatched intents | ElizaOS / LangGraph |

Read the full [Architecture & Topologies Deep Dive](docs/ARCHITECTURE.md) for technical specifications.

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
- [Graphiti](https://github.com) - Knowledge graph framework designed for dynamic, temporal multi-agent memory retrieval.
- [Chroma](https://github.com/chroma-core/chroma) - Open-source embedding vector database for agent episodic and semantic document memory.
- [Cognee](https://github.com/topoteretes/cognee) - Memory management engine for AI applications using graph-native chunking.

---

## Observability, Cockpits & TUIs

- [Langfuse](https://github.com/langfuse/langfuse) - Open source LLM engineering platform for tracing multi-agent execution graphs, latency, and cost.
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - AI observability and evaluation platform with native trace visualizations for complex agent graphs.
- [Helicone](https://github.com/Helicone/helicone) - Lightweight LLM proxy and caching gateway providing real-time cost, token tracking, and rate limiting.
- [AgentOps](https://github.com/AgentOps-AI/agentops) - Operational observability suite for autonomous agents with replay tracking and compliance logging.
- [Charm CLI (Bubble Tea / Lip Gloss)](https://github.com/charmbracelet/bubbletea) - Golang TUI framework for building decoupled, high-performance terminal cockpits for live bot operations.

---

## Safety Brakes, Cost Governors & Human-in-the-Loop

Operating autonomous bot teams in production requires rigorous safety mechanisms:

1. **Hard Turn Governors**: Enforce strict execution ceilings (e.g. maximum 15–20 turns per task) to prevent runaway recursive calls.
2. **Financial Token Circuit Breakers**: Set dollar-based and token-based budget caps ($0.50 / task) with automatic halting.
3. **Human Confirmation Gates**: Require explicit approval before mutating critical resources (`rm -rf`, `DROP TABLE`, fund transfers, external emails).
4. **Isolated Sandboxes**: Execute untrusted code inside ephemeral Docker containers or microVMs with restricted network egress.
5. **Dead Man's Switches**: Automated heartbeat loops that safely pause swarms if human operators disconnect.

Read our complete [Safety & Governance Rules](docs/SAFETY_AND_GOVERNANCE.md) for implementation patterns.

---

## Documentation Hub

Explore the modular technical documentation:

- 🏛️ [Architecture & Topologies Deep Dive](docs/ARCHITECTURE.md) - Communication patterns, message envelopes, and loop prevention.
- 💻 [CLI Reference Manual](docs/CLI_REFERENCE.md) - Complete flags and export guide for `init-team.py`.
- 📋 [Template Authoring Guidelines](docs/TEMPLATE_GUIDELINES.md) - Specification standards for adding new squad blueprints.
- 🛡️ [Safety & Governance Guide](docs/SAFETY_AND_GOVERNANCE.md) - Turn governors, budget circuit breakers, and sandbox isolation.
- 📐 [Production Quality Standard](docs/PRODUCTION_STANDARD.md) - The authoritative standard for repository scaffolding and release gates.

---

## Contributing

Contributions are welcome! Please read the [Contribution Guidelines](CONTRIBUTING.md) and review the [Code of Conduct](CODE_OF_CONDUCT.md) first.

```bash
git clone https://github.com/RemyLoveLogicAI/awesome-bot-teams.git
cd awesome-bot-teams
python3 init-team.py --validate
```

---

## Code of Conduct

This project is governed by the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

---

## Citation

If you use these bot team templates, schemas, or orchestration patterns in your research or project, please cite:

```bibtex
@misc{awesome_bot_teams_2026,
  author = {Jones, Jeremy},
  title = {Awesome Bot Teams: Curated Multi-Agent Squads, Topologies, and Executable Schemas},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/RemyLoveLogicAI/awesome-bot-teams}}
}
```

---

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](LICENSE)

To the extent possible under law, the authors waive all copyright and related or neighboring rights to this work under [CC0 1.0 Universal](LICENSE).
