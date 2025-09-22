#!/usr/bin/env python3
"""
PostToolUse hook: Logs when Python scripts are executed via the Bash tool
Maintains both JSON and Markdown audit logs
"""

import json
import os
import sys
from datetime import datetime


def log_script_usage(tool_name, tool_input, tool_response):
    """Log execution of Python scripts via Bash tool in JSON and Markdown"""

    # Only track Bash tool (which is used to execute scripts)
    if tool_name != "Bash":
        return

    # Get the command from tool input
    command = tool_input.get("command", "")

    # Check if it's executing a Python script from scripts/ directory
    # Support both: "python scripts/file.py" and "./scripts/file.py"
    import re

    # Try to match either pattern: python scripts/... or ./scripts/... or scripts/...
    script_match = re.search(r"(?:python\s+)?(?:\./)?scripts/(\w+\.py)", command)
    if not script_match:
        return

    # Only proceed if it's a scripts/ directory execution
    if "scripts/" not in command:
        return

    script_file = script_match.group(1)

    # Prepare file paths
    audit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../audit")
    log_json = os.path.join(audit_dir, "script_usage_log.json")
    log_md = os.path.join(audit_dir, "script_usage_log.md")

    try:
        # Load existing JSON log or create new
        if os.path.exists(log_json):
            with open(log_json) as f:
                log_data = json.load(f)
        else:
            log_data = {"script_executions": []}

        # Create log entry
        timestamp = datetime.now()
        entry = {
            "timestamp": timestamp.isoformat(),
            "script": script_file,
            "command": command,
            "description": tool_input.get("description", "No description"),
            "tool_used": "Bash",
            "success": tool_response.get("success", True) if tool_response else True,
        }

        # Add to JSON log
        log_data["script_executions"].append(entry)
        log_data["script_executions"] = log_data["script_executions"][-100:]  # Keep last 100

        # Save updated JSON log
        os.makedirs(audit_dir, exist_ok=True)
        with open(log_json, "w") as f:
            json.dump(log_data, f, indent=2)

        # Update Markdown log
        update_markdown_log(log_md, entry, timestamp)

        print(f"📜 Script executed: {script_file}")

    except Exception as e:
        print(f"Script logging error: {e}", file=sys.stderr)


def update_markdown_log(md_path, entry, timestamp):
    """Create or update the Markdown script execution log"""

    # Format the date for section headers
    date_header = timestamp.strftime("## 📅 %d/%m/%Y")
    time_str = timestamp.strftime("%H:%M:%S")

    # Determine status emoji
    status_emoji = "✅" if entry["success"] else "❌"

    # Create the new entry in Markdown format
    md_entry = f"""
### ⚡ {time_str} - {entry['script']} {status_emoji}

| Campo | Valor |
|-------|---------|
| **Script** | `{entry['script']}` |
| **Comando** | `{entry['command']}` |
| **Descrição** | {entry['description']} |
| **Status** | {'Sucesso' if entry['success'] else 'Falha'} |
"""

    # Script documentation
    script_docs = {
        "ai_expertise_evaluator.py": "🤖 Avalia expertise técnica em IA/ML",
        "talent_scorer.py": "👥 Pontua candidatos com múltiplos critérios",
        "simple_calculation.py": "🧮 Cálculos financeiros básicos"
    }

    if entry['script'] in script_docs:
        md_entry += f"\n> **Função**: {script_docs[entry['script']]}\n"

    # Read existing content or create new
    if os.path.exists(md_path):
        with open(md_path, 'r') as f:
            content = f.read()

        # Check if today's section exists
        if date_header not in content:
            # Add new date section
            lines = content.split('\n')
            insert_pos = 2
            for i, line in enumerate(lines):
                if line.startswith('## 📅'):
                    insert_pos = i
                    break
            lines.insert(insert_pos, f"\n{date_header}")
            lines.insert(insert_pos + 1, md_entry)
            content = '\n'.join(lines)
        else:
            # Add entry under existing date
            date_index = content.index(date_header)
            next_section = content.find('\n## ', date_index + 1)
            if next_section == -1:
                content += md_entry
            else:
                content = content[:next_section] + md_entry + content[next_section:]
    else:
        # Create new file
        content = f"""# 🔧 Script Execution Log

> Registro automatizado de scripts Python executados

---

{date_header}
{md_entry}

---

*Gerado por script-usage-logger.py*
"""

    # Save the updated Markdown
    with open(md_path, 'w') as f:
        f.write(content)


# Main execution
if __name__ == "__main__":
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        tool_response = input_data.get("tool_response", {})

        # Log the script usage
        log_script_usage(tool_name, tool_input, tool_response)

        # Always exit successfully
        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)
