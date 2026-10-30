#!/usr/bin/env python3
"""
Awesome Bot Teams - Team Initiation CLI
Zero-dependency CLI tool to inspect, export, and bootstrap multi-agent bot teams.

Usage:
  python3 init-team.py --list
  python3 init-team.py --template software-engineering-squad
  python3 init-team.py --template software-engineering-squad --export crewai
  python3 init-team.py --template software-engineering-squad --export autogen
  python3 init-team.py --template software-engineering-squad --export json
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
            raw_line = line.rstrip()

            if not stripped or stripped.startswith("#"):
                continue

            if in_prompt:
                if line.startswith("      ") or (line.startswith("        ") and in_prompt):
                    prompt_lines.append(stripped)
                    continue
                else:
                    if current_role is not None:
                        current_role["system_prompt"] = " ".join(prompt_lines).strip()
                    in_prompt = False
                    prompt_lines = []

            if stripped.startswith("id:") and "roles" not in data["team"]:
                data["team"]["id"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("name:"):
                data["team"]["name"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("description:"):
                data["team"]["description"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("topology:"):
                data["team"]["topology"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("leader:"):
                data["team"]["leader"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("- id:"):
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
            elif current_role is not None:
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
    process=Process.hierarchical if "{team.get("topology")}" == "hierarchical_gate" else Process.sequential,
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


def main():
    parser = argparse.ArgumentParser(description="Awesome Bot Teams - Initiation CLI")
    parser.add_argument("--list", action="store_true", help="List all available bot team templates")
    parser.add_argument("--template", type=str, help="Specific template ID to inspect or export")
    parser.add_argument("--export", choices=["json", "yaml", "crewai", "autogen", "markdown"],
                        default="markdown", help="Format to output the team configuration in")

    args = parser.parse_args()
    teams = load_all_teams()

    if args.list or not args.template:
        print("\n🤖 Available Awesome Bot Teams:\n")
        print(f"  {'ID':<30} {'Topology':<22} {'Description'}")
        print("  " + "-" * 85)
        for tid, t in teams.items():
            print(f"  {tid:<30} {t.get('topology', 'standard'):<22} {t.get('name')}")
        print("\nTip: Run `python3 init-team.py --template <id> --export crewai|autogen|json` to generate code.\n")
        return

    if args.template not in teams:
        print(f"Error: Template '{args.template}' not found. Use --list to see available templates.", file=sys.stderr)
        sys.exit(1)

    selected = teams[args.template]

    if args.export == "json":
        print(json.dumps(selected, indent=2))
    elif args.export == "crewai":
        print(export_crewai(selected))
    elif args.export == "autogen":
        print(export_autogen(selected))
    else:
        # Default Markdown summary
        print(f"\n# {selected.get('name')}")
        print(f"**Topology**: `{selected.get('topology')}` | **Leader**: `{selected.get('leader')}`\n")
        print(f"{selected.get('description')}\n")
        print("### Roles Roster:")
        for r in selected.get("roles", []):
            print(f"- **{r.get('title', r['id'])}** (`{r['id']}`)")
            print(f"  - Goal: {r.get('goal')}")
            if r.get("tools"):
                print(f"  - Tools: {', '.join(r['tools'])}")
            print(f"  - System Seed: {r.get('system_prompt', '')[:120]}...\n")


if __name__ == "__main__":
    main()
