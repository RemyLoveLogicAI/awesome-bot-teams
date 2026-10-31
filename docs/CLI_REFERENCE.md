# CLI Reference (`init-team.py`)

> Zero-dependency command-line interface for inspecting, validating, and bootstrapping multi-agent bot teams.

---

## 1. Overview

`init-team.py` is a lightweight Python utility included in the root of the repository. It requires no third-party libraries (runs directly on Python 3.8+ standard library) and converts declarative team schemas into production-ready scaffolds for major multi-agent frameworks.

```bash
python3 init-team.py [OPTIONS]
```

---

## 2. Options & Flags

| Flag | Argument | Description |
|:---|:---|:---|
| `--list` | *None* | Lists all registered bot teams, topologies, and descriptions in a formatted table. |
| `--template` | `<team-id>` | Selects a specific squad template by its unique identifier (e.g., `software-engineering-squad`). |
| `--export` | `crewai`, `autogen`, `langgraph`, `json`, `yaml`, `markdown` | Specifies the output format or target orchestrator framework. Default: `markdown`. |
| `--output` | `<file-path>` | Writes the generated code or schema directly to the specified file path. |
| `--validate` | *None* | Validates all YAML schema files in `templates/schemas/` against structural integrity rules. |
| `--cockpit`, `--tui` | *None* | Launches the interactive curses dual-mode terminal cockpit for human navigation. |
| `--agent` | *None* | Launches the pipeable line-delimited JSONL protocol (1 request = 1 reply). |
| `-h`, `--help` | *None* | Displays the CLI help message and exits. |

---

## 3. Dual-Mode Terminal Cockpit (`cockpit.py`)

Adhering to the **agent-tui-cockpit** architectural pattern, the cockpit provides two synchronized interfaces:
1. **Interactive TTY Mode**: Split-pane curses terminal interface for human navigation, code export, and live schema validation.
2. **Piped Agent Mode**: Deterministic JSONL protocol on stdin/stdout for autonomous agents, sub-shells, and Charm/Bubble Tea clients.

```bash
# Launch interactive curses cockpit
python3 cockpit.py

# Or launch via init-team CLI
python3 init-team.py --cockpit

# Test JSONL agent protocol via pipe
echo "list" | python3 cockpit.py
echo "validate" | python3 cockpit.py
echo "doctor" | python3 cockpit.py
```

### JSONL Protocol Specification
- **Greeting Envelope**:
  ```json
  {"ok": true, "engine": "awesome-bot-teams-cockpit", "protocol": 1, "status": "ready", "teams_count": 8, "safety_brakes": {"max_steps": 15, "max_retry_attempts": 3}}
  ```
- **Supported Verbs**:
  - `list` - Returns array of available teams and role counts.
  - `get <template_id>` - Returns full team schema.
  - `export <template_id> <framework>` - Exports framework code scaffold.
  - `validate` - Validates all repository schemas.
  - `doctor` / `providers` - Reports presence of provider API keys (zero secret leakage).
  - `status` - Returns engine telemetry and model routing tier assignments.
  - `quit` / `exit` - Cleanly closes the stream.

---

## 3. Usage Examples

### 3.1. List Available Squads
```bash
python3 init-team.py --list
```
**Output:**
```
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

### 3.2. Export to CrewAI
Generates runnable Python code defining `Agent` and `Crew` objects:
```bash
python3 init-team.py --template software-engineering-squad --export crewai --output my_crew.py
```

### 3.3. Export to AutoGen
Generates executable AutoGen code defining `AssistantAgent`, `UserProxyAgent`, and `GroupChatManager`:
```bash
python3 init-team.py --template multi-model-debate-pod --export autogen --output my_autogen.py
```

### 3.4. Export to LangGraph
Generates state graph node functions, routing edges, and conditional gates:
```bash
python3 init-team.py --template solo-founder-cockpit --export langgraph --output my_graph.py
```

### 3.5. Export JSON Schema for Custom Parsers
Outputs machine-readable JSON structure for ingestion by custom LLM routers or microservices:
```bash
python3 init-team.py --template cyber-security-redteam --export json
```

### 3.6. Run Schema Validation Gate
Ensures every YAML schema in `templates/schemas/` satisfies required fields (`id`, `name`, `topology`, `leader`, `roles`, `system_prompt`):
```bash
python3 init-team.py --validate
```
**Exit Codes:**
- `0`: All schemas are valid.
- `1`: Validation failed or missing template error.

---

## 4. Programmatic YAML Schema Specification

Every team template in `templates/schemas/<id>.yaml` follows this specification:

```yaml
team:
  id: string              # Unique hyphenated identifier
  name: string            # Human-readable team name
  version: string         # Semantic version string (e.g. "1.0.0")
  description: string     # High-level summary of the squad's objective
  topology: string        # One of: hierarchical_gate, pipeline, consensus_debate,
                          # fan_out_synthesis, sandbox_pipeline, triage_pod, stream_circuit_breaker
  leader: string          # Role ID of the coordinating agent or arbiter
  roles:
    - id: string          # Unique role identifier (e.g. "architect")
      title: string       # Professional title
      model_preference: string # Optional preferred model (e.g. "deepseek-r1", "gpt-4o")
      goal: string        # Specific role goal
      system_prompt: |    # Seed system instructions
        ...
      tools:              # Array of tool identifiers
        - tool_a
        - tool_b
```
