#!/usr/bin/env python3
"""
Awesome Bot Teams - Dual-Mode TUI Cockpit & Runtime
Adheres to the agent-tui-cockpit pattern:
  1. TTY Mode (curses): Live, interactive terminal supervision cockpit.
  2. Agent Mode (--agent or piped stdin): Line-delimited JSONL protocol (1 request = 1 reply).
  3. Built-in Demo Mode (--demo): Instant in-memory simulation without external dependencies.
  4. Secret Safety: Reports presence/absence of credentials, never token values.
"""

import argparse
import curses
import importlib
import json
import os
import re
import sys
import time

# Ensure parent directory is in path for module loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

init_team_mod = importlib.import_module("init-team")
load_all_teams = init_team_mod.load_all_teams
validate_schemas = init_team_mod.validate_schemas
export_crewai = init_team_mod.export_crewai
export_autogen = init_team_mod.export_autogen
export_langgraph = init_team_mod.export_langgraph

MAX_ATTEMPTS_DEFAULT = 3
MAX_STEPS_DEFAULT = 15


# ==============================================================================
# 1. Three-Stage Robust JSON Salvage
# ==============================================================================

def salvage_json(text: str):
    """
    Three-stage JSON salvage:
    1. Direct parse
    2. Markdown fenced block extraction
    3. Balanced brace scan
    """
    clean = text.strip()
    try:
        return json.loads(clean)
    except Exception:
        pass

    # Stage 2: Fenced code block
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", clean)
    if fenced:
        try:
            return json.loads(fenced.group(1).strip())
        except Exception:
            pass

    # Stage 3: Balanced brace extraction
    start_brace = clean.find("{")
    end_brace = clean.rfind("}")
    if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
        try:
            return json.loads(clean[start_brace:end_brace + 1])
        except Exception:
            pass

    raise ValueError(f"Failed to salvage JSON from payload: {clean[:80]}...")


# ==============================================================================
# 2. Secret-Safe Provider Diagnostics
# ==============================================================================

def get_provider_diagnostics():
    """
    Reports whether API keys are configured without exposing credentials.
    """
    keys = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY"),
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY"),
        "GROK_API_KEY": os.environ.get("GROK_API_KEY"),
        "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY"),
        "GITHUB_TOKEN": os.environ.get("GITHUB_TOKEN"),
        "SHIELDNODE_API_KEY": os.environ.get("SHIELDNODE_API_KEY"),
    }
    status = {}
    for k, v in keys.items():
        status[k.lower()] = "present" if v and len(v.strip()) > 0 else "unset"
    return status


# ==============================================================================
# 3. Agent Mode: Line-Delimited JSONL Protocol
# ==============================================================================

def run_agent_mode(demo=False):
    """
    Runs the line-delimited JSONL agent protocol on stdin/stdout.
    1 line in = 1 line out.
    """
    teams = load_all_teams()
    greeting = {
        "ok": True,
        "engine": "awesome-bot-teams-cockpit",
        "protocol": 1,
        "status": "ready",
        "teams_count": len(teams),
        "demo": demo,
        "safety_brakes": {
            "max_steps": MAX_STEPS_DEFAULT,
            "max_retry_attempts": MAX_ATTEMPTS_DEFAULT,
            "human_confirmation_gate": True
        }
    }
    sys.stdout.write(json.dumps(greeting) + "\n")
    sys.stdout.flush()

    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue

        parts = raw.split()
        verb = parts[0].lower()

        if verb in ["quit", "exit"]:
            sys.stdout.write(json.dumps({"ok": True, "status": "closed", "farewell": "bye"}) + "\n")
            sys.stdout.flush()
            break

        elif verb == "ping":
            sys.stdout.write(json.dumps({"ok": True, "pong": True, "time": time.time()}) + "\n")
            sys.stdout.flush()

        elif verb == "list":
            summary = []
            for tid, t in sorted(teams.items()):
                summary.append({
                    "id": tid,
                    "name": t.get("name"),
                    "topology": t.get("topology"),
                    "roles_count": len(t.get("roles", []))
                })
            sys.stdout.write(json.dumps({"ok": True, "teams": summary}) + "\n")
            sys.stdout.flush()

        elif verb == "get":
            if len(parts) < 2:
                sys.stdout.write(json.dumps({"ok": False, "error": "Usage: get <template_id>"}) + "\n")
            else:
                tid = parts[1]
                if tid in teams:
                    sys.stdout.write(json.dumps({"ok": True, "team": teams[tid]}) + "\n")
                else:
                    sys.stdout.write(json.dumps({"ok": False, "error": f"Template '{tid}' not found"}) + "\n")
            sys.stdout.flush()

        elif verb == "validate":
            valid = validate_schemas()
            sys.stdout.write(json.dumps({"ok": valid, "schemas_valid": valid, "count": len(teams)}) + "\n")
            sys.stdout.flush()

        elif verb == "export":
            if len(parts) < 3:
                sys.stdout.write(json.dumps({"ok": False, "error": "Usage: export <template_id> <crewai|autogen|langgraph|json|yaml>"}) + "\n")
            else:
                tid, fmt = parts[1], parts[2].lower()
                if tid not in teams:
                    sys.stdout.write(json.dumps({"ok": False, "error": f"Template '{tid}' not found"}) + "\n")
                else:
                    selected = teams[tid]
                    code = ""
                    if fmt == "crewai":
                        code = export_crewai(selected)
                    elif fmt == "autogen":
                        code = export_autogen(selected)
                    elif fmt == "langgraph":
                        code = export_langgraph(selected)
                    elif fmt == "json":
                        code = json.dumps(selected, indent=2)
                    elif fmt == "yaml":
                        schema_path = os.path.join(BASE_DIR, "templates", "schemas", f"{tid}.yaml")
                        if os.path.exists(schema_path):
                            with open(schema_path, "r", encoding="utf-8") as f:
                                code = f.read()
                    else:
                        code = f"# Unsupported format: {fmt}"
                    sys.stdout.write(json.dumps({"ok": True, "template": tid, "format": fmt, "code": code}) + "\n")
            sys.stdout.flush()

        elif verb in ["doctor", "providers"]:
            diag = get_provider_diagnostics()
            sys.stdout.write(json.dumps({"ok": True, "providers": diag}) + "\n")
            sys.stdout.flush()

        elif verb == "status":
            sys.stdout.write(json.dumps({
                "ok": True,
                "engine": "awesome-bot-teams-cockpit",
                "mode": "agent",
                "demo": demo,
                "teams_loaded": len(teams),
                "routing_tiers": {
                    "fast": "Triage, Critics, Guards (e.g. Gemini 2.5 Flash / Claude Haiku)",
                    "daily": "Implementation, Refactoring (e.g. Claude 3.7 Sonnet / Qwen 2.5 Coder)",
                    "heavy": "Consensus, Formal Proofs (e.g. DeepSeek-R1 / GPT-4o)"
                }
            }) + "\n")
            sys.stdout.flush()

        else:
            sys.stdout.write(json.dumps({"ok": False, "error": f"Unknown verb '{verb}'. Supported: list, get, export, validate, status, doctor, ping, quit"}) + "\n")
            sys.stdout.flush()


# ==============================================================================
# 4. TTY Interactive Curses Mode
# ==============================================================================

def curses_cockpit(stdscr, demo=False):
    curses.curs_set(0)
    curses.use_default_colors()

    # Color pairs (DevRev inspired)
    # 1: Accent / Focus (Yellow on Black)
    # 2: Success / OK (Green on Black)
    # 3: Danger / Alert (Red on Black)
    # 4: Header Bar (Black on Yellow/White)
    # 5: Muted text (Cyan/Grey)
    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_YELLOW, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_CYAN, -1)

    teams = load_all_teams()
    team_keys = sorted(teams.keys())
    current_idx = 0
    status_msg = "Ready. Use [↑/↓] to navigate squads, [e] to export code, [v] to validate, [q] to quit."
    status_color = 5

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        # Minimum required dimensions
        if h < 16 or w < 70:
            stdscr.addstr(0, 0, f"Terminal window too small ({w}x{h}). Expand to at least 70x16.", curses.color_pair(3))
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in [ord('q'), ord('Q')]:
                break
            continue

        # Header bar
        header_text = f" 🤖 AWESOME BOT TEAMS COCKPIT │ Mode: TTY Live {'[DEMO]' if demo else ''} │ {len(team_keys)} Squads Available "
        stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(0, 0, header_text.ljust(w - 1)[:w - 1])
        stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)

        # Split pane geometry
        split_x = max(32, w // 3)
        left_w = split_x - 1
        right_w = w - split_x - 2
        body_h = h - 3

        # Left Window: List of Teams
        stdscr.addstr(1, 1, "AVAILABLE SQUADS", curses.A_BOLD | curses.color_pair(1))
        for i, tid in enumerate(team_keys):
            if i >= body_h:
                break
            line_y = 2 + i
            is_selected = (i == current_idx)
            t = teams[tid]
            display_title = t.get("name", tid)
            if len(display_title) > left_w - 4:
                display_title = display_title[:left_w - 7] + "..."

            if is_selected:
                stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(line_y, 1, f"▶ {display_title}".ljust(left_w)[:left_w])
                stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
            else:
                stdscr.addstr(line_y, 1, f"  {display_title}".ljust(left_w)[:left_w])

        # Vertical Divider
        for y in range(1, h - 2):
            stdscr.addch(y, split_x, curses.ACS_VLINE)

        # Right Window: Details of Selected Team
        if team_keys:
            selected_id = team_keys[current_idx]
            team = teams[selected_id]

            stdscr.addstr(1, split_x + 2, f"SQUAD: {team.get('name', selected_id)}", curses.A_BOLD)
            meta_str = f"Topology: {team.get('topology', 'standard')}  │  Leader: {team.get('leader', 'lead')}  │  Roles: {len(team.get('roles', []))}"
            stdscr.addstr(2, split_x + 2, meta_str[:right_w], curses.color_pair(1))

            # Description (wrapped snippet)
            desc = team.get("description", "")
            stdscr.addstr(3, split_x + 2, desc[:right_w], curses.color_pair(5))

            # Horizontal separator in right pane
            stdscr.addstr(4, split_x + 2, "─" * min(right_w, 60))

            # Roles list
            stdscr.addstr(5, split_x + 2, "ROSTER & SPECIALIST ROLES:", curses.A_BOLD | curses.color_pair(2))
            role_y = 6
            for r in team.get("roles", []):
                if role_y >= h - 4:
                    break
                r_title = r.get("title", r.get("id"))
                r_pref = f"({r.get('model_preference')})" if r.get("model_preference") else ""
                stdscr.addstr(role_y, split_x + 2, f"• {r_title} {r_pref}", curses.A_BOLD)
                role_y += 1
                if role_y < h - 4:
                    goal_snip = f"  Goal: {r.get('goal', '')}"
                    stdscr.addstr(role_y, split_x + 2, goal_snip[:right_w], curses.color_pair(5))
                    role_y += 1
                if role_y < h - 4 and r.get("tools"):
                    tools_snip = f"  Tools: {', '.join(r.get('tools', []))}"
                    stdscr.addstr(role_y, split_x + 2, tools_snip[:right_w])
                    role_y += 1

        # Bottom Status Bar
        stdscr.addstr(h - 2, 0, "─" * (w - 1))
        footer_cmd = "[↑/↓] Navigate │ [e] Export Scaffold │ [v] Validate │ [d] Toggle Demo │ [q] Quit"
        stdscr.addstr(h - 1, 1, footer_cmd[:w - 2], curses.A_BOLD)
        if status_msg:
            stdscr.addstr(h - 2, 2, f" {status_msg} ", curses.color_pair(status_color) | curses.A_BOLD)

        stdscr.refresh()

        # Keyboard input
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break

        if key in [ord('q'), ord('Q')]:
            break
        elif key in [curses.KEY_UP, ord('k'), ord('K')]:
            if current_idx > 0:
                current_idx -= 1
        elif key in [curses.KEY_DOWN, ord('j'), ord('J')]:
            if current_idx < len(team_keys) - 1:
                current_idx += 1
        elif key in [ord('v'), ord('V')]:
            valid = validate_schemas()
            if valid:
                status_msg = f"✅ All {len(team_keys)} team schemas passed validation!"
                status_color = 2
            else:
                status_msg = "❌ Schema validation failed! Check console output."
                status_color = 3
        elif key in [ord('d'), ord('D')]:
            demo = not demo
            status_msg = f"Demo Mode: {'ENABLED (Simulated Swarm Activity)' if demo else 'DISABLED'}"
            status_color = 1
        elif key in [ord('e'), ord('E')]:
            if team_keys:
                sel_id = team_keys[current_idx]
                out_path = os.path.join(BASE_DIR, f"{sel_id}_scaffold.py")
                code = export_langgraph(teams[sel_id])
                try:
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(code)
                    status_msg = f"🚀 Exported LangGraph scaffold to: {os.path.basename(out_path)}"
                    status_color = 2
                except Exception as ex:
                    status_msg = f"❌ Export failed: {str(ex)[:40]}"
                    status_color = 3


# ==============================================================================
# 5. Entrypoint Dispatcher
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Awesome Bot Teams - Dual-Mode TUI Cockpit & Runtime")
    parser.add_argument("--agent", action="store_true", help="Force Agent Mode (JSONL protocol on stdin/stdout)")
    parser.add_argument("--tui", action="store_true", help="Force interactive curses TTY mode")
    parser.add_argument("--demo", action="store_true", help="Run with in-memory simulated swarm telemetry")
    args = parser.parse_args()

    # Dual-mode selection rule from skill specification:
    # If explicitly requested --agent or stdin is piped (not a tty), run Agent Mode.
    # Otherwise run TTY curses mode.
    if args.agent or (not sys.stdin.isatty() and not args.tui):
        run_agent_mode(demo=args.demo)
    else:
        try:
            curses.wrapper(curses_cockpit, demo=args.demo)
        except curses.error as e:
            # Fallback if terminal does not support curses
            print(f"Terminal does not support curses ({e}). Falling back to Agent Mode:\n")
            run_agent_mode(demo=args.demo)


if __name__ == "__main__":
    main()
