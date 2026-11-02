#!/usr/bin/env python3
"""
Awesome Bot Teams - Team Initiation CLI
Zero-dependency CLI tool to inspect, export, validate, and bootstrap multi-agent bot teams.

Usage:
  python3 init-team.py --list
  python3 init-team.py --template software-engineering-squad
  python3 init-team.py --template software-engineering-squad --export crewai
  python3 init-team.py --template software-engineering-squad --export autogen
  python3 init-team.py --template software-engineering-squad --export langgraph
  python3 init-team.py --template software-engineering-squad --export json
  python3 init-team.py --validate
"""

import argparse
import json
import os
import sys

# Directory containing schema YAMLs
SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "templates", "schemas")


def parse_simple_yaml(filepath):
    """
    Lightweight YAML reader for team definition schemas without third-party dependencies.
    """
    data = {"team": {"roles": []}}
    current_role = None
    in_prompt = False
    prompt_lines = []
    in_tools = False

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                continue

            if in_prompt:
                if stripped.startswith("tools:") or stripped.startswith("model_preference:") or stripped.startswith("- id:"):
                    if current_role is not None:
                        current_role["system_prompt"] = " ".join(prompt_lines).strip()
                    in_prompt = False
                    prompt_lines = []
                elif line.startswith("        ") or line.startswith("      "):
                    prompt_lines.append(stripped)
                    continue
                else:
                    if current_role is not None:
                        current_role["system_prompt"] = " ".join(prompt_lines).strip()
                    in_prompt = False
                    prompt_lines = []

            if stripped.startswith("- id:"):
                if in_prompt and current_role:
                    current_role["system_prompt"] = " ".join(prompt_lines).strip()
                    in_prompt = False
                    prompt_lines = []
                current_role = {
                    "id": stripped.split(":", 1)[1].strip().strip('"'),
                    "tools": []
                }
                data["team"]["roles"].append(current_role)
                in_tools = False
            elif current_role is None:
                # Top-level team metadata
                if stripped.startswith("id:"):
                    data["team"]["id"] = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("name:"):
                    data["team"]["name"] = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("version:"):
                    data["team"]["version"] = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("description:"):
                    data["team"]["description"] = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("topology:"):
                    data["team"]["topology"] = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("leader:"):
                    data["team"]["leader"] = stripped.split(":", 1)[1].strip().strip('"')
            else:
                # Inside a role definition
                if stripped.startswith("title:"):
                    current_role["title"] = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("goal:"):
                    current_role["goal"] = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("model_preference:"):
                    current_role["model_preference"] = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("system_prompt: |"):
                    in_prompt = True
                    prompt_lines = []
                elif stripped.startswith("tools:"):
                    in_tools = True
                elif in_tools and stripped.startswith("- "):
                    tool_name = stripped.split("- ", 1)[1].strip()
                    current_role["tools"].append(tool_name)

    if in_prompt and current_role:
        current_role["system_prompt"] = " ".join(prompt_lines).strip()

    return data


def load_all_teams():
    teams = {}
    if not os.path.exists(SCHEMAS_DIR):
        return teams
    for fname in sorted(os.listdir(SCHEMAS_DIR)):
        if fname.endswith(".yaml") or fname.endswith(".yml"):
            team_path = os.path.join(SCHEMAS_DIR, fname)
            parsed = parse_simple_yaml(team_path)
            team_id = parsed.get("team", {}).get("id") or fname.rsplit(".", 1)[0]
            teams[team_id] = parsed["team"]
    return teams


def validate_schemas():
    """
    Validates all schema files against required fields and consistency rules.
    """
    if not os.path.exists(SCHEMAS_DIR):
        print(f"Error: Schemas directory '{SCHEMAS_DIR}' does not exist.", file=sys.stderr)
        return False

    errors = []
    teams = {}
    files = [f for f in sorted(os.listdir(SCHEMAS_DIR)) if f.endswith(".yaml") or f.endswith(".yml")]

    if not files:
        errors.append("No schema files found in templates/schemas/")

    for fname in files:
        path = os.path.join(SCHEMAS_DIR, fname)
        base_name = fname.rsplit(".", 1)[0]
        parsed = parse_simple_yaml(path)
        team = parsed.get("team", {})

        # Check required team fields
        for field in ["id", "name", "description", "topology", "leader", "roles"]:
            if field not in team or not team[field]:
                errors.append(f"[{fname}] Missing required team field: '{field}'")

        if team.get("id") and team.get("id") != base_name:
            errors.append(f"[{fname}] Team id '{team.get('id')}' does not match filename '{base_name}'")

        roles = team.get("roles", [])
        if not roles:
            errors.append(f"[{fname}] Team defines no roles")

        role_ids = set()
        for r in roles:
            rid = r.get("id")
            if not rid:
                errors.append(f"[{fname}] Role missing id")
            elif rid in role_ids:
                errors.append(f"[{fname}] Duplicate role id '{rid}'")
            else:
                role_ids.add(rid)

            for rfield in ["title", "goal", "system_prompt"]:
                if rfield not in r or not r[rfield]:
                    errors.append(f"[{fname}] Role '{rid}' missing required field: '{rfield}'")

        if team.get("leader") and team.get("leader") not in role_ids:
            errors.append(f"[{fname}] Leader '{team.get('leader')}' is not in roles roster: {list(role_ids)}")

        teams[base_name] = team

    if errors:
        print("\n❌ Schema Validation Failed:")
        for err in errors:
            print(f"  • {err}")
        return False
    else:
        print(f"\n✅ All {len(files)} team schemas passed validation successfully!")
        return True


def export_crewai(team):
    code = f'''# Auto-generated CrewAI Scaffold for {team.get("name", "Bot Team")}
from crewai import Agent, Crew, Process, Task

# --- Agents Definition ---
'''
    agents = []
    for r in team.get("roles", []):
        agent_var = f"{r['id']}_agent"
        agents.append(agent_var)
        code += f'''{agent_var} = Agent(
    role="{r.get('title', r['id'])}",
    goal="{r.get('goal', '')}",
    backstory="{r.get('system_prompt', '')[:160]}...",
    verbose=True,
    allow_delegation={str(r['id'] == team.get('leader', '')).lower()}
)

'''
    code += f'''# --- Crew Orchestration ---
squad_crew = Crew(
    agents=[{", ".join(agents)}],
    tasks=[], # Attach tasks matching team topology: {team.get("topology", "sequential")}
    process=Process.hierarchical if "{team.get("topology")}" in ["hierarchical_gate", "hierarchical_proxy_gate"] else Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("Initiating {team.get('name')}...")
    # result = squad_crew.kickoff(inputs={{"objective": "YOUR_GOAL_HERE"}})
'''
    return code


def export_autogen(team):
    code = f'''# Auto-generated AutoGen Scaffold for {team.get("name", "Bot Team")}
import autogen

config_list = [{{"model": "gpt-4o", "api_key": "YOUR_API_KEY"}}]
llm_config = {{"config_list": config_list, "cache_seed": 42}}

# --- Agent Personas ---
'''
    agents = []
    for r in team.get("roles", []):
        agent_var = f"{r['id']}_bot"
        agents.append(agent_var)
        code += f'''{agent_var} = autogen.AssistantAgent(
    name="{r['id']}",
    system_message="""{r.get('system_prompt', r.get('goal', ''))}""",
    llm_config=llm_config,
)

'''
    code += f'''# --- Group Chat Topology ({team.get("topology", "round_robin")}) ---
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    human_input_mode="TERMINATE",
    code_execution_config={{"work_dir": "workspace", "use_docker": False}}
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, {", ".join(agents)}],
    messages=[],
    max_round=15
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

if __name__ == "__main__":
    user_proxy.initiate_chat(manager, message="Execute team objective: [STATE_TASK_HERE]")
'''
    return code


def export_langgraph(team):
    roles = team.get("roles", [])
    code = f'''# Auto-generated LangGraph Scaffold for {team.get("name", "Bot Team")}
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END

# --- Shared State ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "Conversation history"]
    active_agent: str
    task_completed: bool

# --- Node Handlers ---
'''
    for r in roles:
        rid = r['id']
        rtitle = r.get('title', rid)
        prompt_snippet = r.get('system_prompt', '')[:100]
        code += f'''def node_{rid}(state: AgentState):
    """Handler for {rtitle}"""
    # System seed: {prompt_snippet}...
    print("Executing {rid} step...")
    return {{"active_agent": "{rid}"}}

'''

    first_role_id = roles[0]['id'] if roles else END
    code += f'''# --- Routing Logic ---
def router(state: AgentState):
    if state.get("task_completed"):
        return END
    return "{first_role_id}"

# --- Build State Graph ---
workflow = StateGraph(AgentState)
'''
    for r in roles:
        rid = r['id']
        code += f'workflow.add_node("{rid}", node_{rid})\n'

    leader_id = team.get('leader') or (roles[0]['id'] if roles else 'start')
    code += f'''
# Entry point: team leader ({leader_id})
workflow.set_entry_point("{leader_id}")

# Wiring edges
'''
    for i in range(len(roles) - 1):
        curr_id = roles[i]['id']
        next_id = roles[i+1]['id']
        code += f'workflow.add_edge("{curr_id}", "{next_id}")\n'
    if roles:
        last_id = roles[-1]['id']
        code += f'workflow.add_edge("{last_id}", END)\n'

    code += '''
app = workflow.compile()

if __name__ == "__main__":
    print("Initiating LangGraph team: ''' + team.get('name', '') + '''...")
    # output = app.invoke({"messages": [], "active_agent": "", "task_completed": False})
'''
    return code


def main():
    parser = argparse.ArgumentParser(description="Awesome Bot Teams - Initiation CLI")
    parser.add_argument("--list", action="store_true", help="List all available bot team templates")
    parser.add_argument("--template", type=str, help="Specific template ID to inspect or export")
    parser.add_argument("--export", choices=["json", "yaml", "crewai", "autogen", "langgraph", "markdown"],
                        default="markdown", help="Format to output the team configuration in")
    parser.add_argument("--output", type=str, help="File path to save output instead of stdout")
    parser.add_argument("--validate", action="store_true", help="Validate all schemas in templates/schemas/")
    parser.add_argument("--cockpit", "--tui", action="store_true", help="Launch interactive dual-mode curses cockpit")
    parser.add_argument("--agent", action="store_true", help="Launch pipeable JSONL agent protocol")

    args = parser.parse_args()

    if args.cockpit or args.agent:
        import cockpit
        if args.agent:
            cockpit.run_agent_mode()
        else:
            curses.wrapper(cockpit.curses_cockpit)
        return

    if args.validate:
        valid = validate_schemas()
        sys.exit(0 if valid else 1)

    teams = load_all_teams()

    if args.list or not args.template:
        print("\n🤖 Available Awesome Bot Teams:\n")
        print(f"  {'ID':<30} {'Topology':<22} {'Description'}")
        print("  " + "-" * 85)
        for tid, t in teams.items():
            print(f"  {tid:<30} {t.get('topology', 'standard'):<22} {t.get('name')}")
        print("\nTip: Run `python3 init-team.py --template <id> --export crewai|autogen|langgraph|json` to generate code.\n")
        return

    if args.template not in teams:
        print(f"Error: Template '{args.template}' not found. Use --list to see available templates.", file=sys.stderr)
        sys.exit(1)

    selected = teams[args.template]
    result_text = ""

    if args.export == "json":
        result_text = json.dumps(selected, indent=2)
    elif args.export == "crewai":
        result_text = export_crewai(selected)
    elif args.export == "autogen":
        result_text = export_autogen(selected)
    elif args.export == "langgraph":
        result_text = export_langgraph(selected)
    elif args.export == "yaml":
        schema_file = os.path.join(SCHEMAS_DIR, f"{args.template}.yaml")
        if os.path.exists(schema_file):
            with open(schema_file, "r", encoding="utf-8") as f:
                result_text = f.read()
        else:
            result_text = f"# Schema file not found for {args.template}"
    else:
        # Default Markdown summary
        md = []
        md.append(f"\n# {selected.get('name')}")
        md.append(f"**Topology**: `{selected.get('topology')}` | **Leader**: `{selected.get('leader')}`\n")
        md.append(f"{selected.get('description')}\n")
        md.append("### Roles Roster:")
        for r in selected.get("roles", []):
            md.append(f"- **{r.get('title', r['id'])}** (`{r['id']}`)")
            md.append(f"  - Goal: {r.get('goal')}")
            if r.get("tools"):
                md.append(f"  - Tools: {', '.join(r['tools'])}")
            md.append(f"  - System Seed: {r.get('system_prompt', '')[:120]}...\n")
        result_text = "\n".join(md)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_text)
        print(f"Successfully wrote output to '{args.output}'")
    else:
        print(result_text)


if __name__ == "__main__":
    main()
