#!/usr/bin/env python3
"""
PostToolUse hook: Tracks ALL file writes and edits
Maintains history of all document changes for compliance in both JSON and Markdown formats
"""

import json
import os
import sys
from datetime import datetime


def track_report(tool_name, tool_input, tool_response):
    """Log ALL file creation/modification for audit trail in JSON and Markdown"""

    # Debug: Log that hook was called
    print(f"🔍 Hook called for tool: {tool_name}", file=sys.stderr)

    # Get file path from tool input
    file_path = tool_input.get("file_path", "")

    if not file_path:
        print("⚠️ No file_path in tool_input", file=sys.stderr)
        return

    print(f"📝 Tracking file: {file_path}", file=sys.stderr)

    # Prepare file paths
    audit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../audit")
    history_json = os.path.join(audit_dir, "report_history.json")
    history_md = os.path.join(audit_dir, "report_history.md")

    try:
        # Load existing JSON history or create new
        if os.path.exists(history_json):
            with open(history_json) as f:
                history = json.load(f)
        else:
            history = {"reports": []}

        # Determine action type
        action = "created" if tool_name == "Write" else "modified"

        # Calculate word count if content available
        content = tool_input.get("content", "") or tool_input.get("new_string", "")
        word_count = len(content.split()) if content else 0

        # Get first line of content as preview
        preview = content.split('\n')[0][:100] + "..." if content and len(content) > 100 else content.split('\n')[0] if content else "N/A"

        # Create history entry
        timestamp = datetime.now()
        entry = {
            "timestamp": timestamp.isoformat(),
            "file": os.path.basename(file_path),
            "path": file_path,
            "action": action,
            "word_count": word_count,
            "tool": tool_name,
            "preview": preview
        }

        # Add to JSON history
        history["reports"].append(entry)
        history["reports"] = history["reports"][-50:]  # Keep last 50

        # Save updated JSON history
        os.makedirs(audit_dir, exist_ok=True)
        with open(history_json, "w") as f:
            json.dump(history, f, indent=2)

        # Update Markdown audit log
        update_markdown_audit(history_md, entry, timestamp)

        print(f"📊 File tracked: {os.path.basename(file_path)} ({action})")

    except Exception as e:
        print(f"Report tracking error: {e}", file=sys.stderr)


def update_markdown_audit(md_path, entry, timestamp):
    """Create or update the Markdown audit log"""

    # Format the date for section headers
    date_header = timestamp.strftime("## 📅 %d/%m/%Y")
    time_str = timestamp.strftime("%H:%M:%S")

    # Create the new entry in Markdown format
    md_entry = f"""
### ⏰ {time_str} - {entry['action'].upper()}: {entry['file']}

| Campo | Valor |
|-------|-------|
| **Arquivo** | `{entry['file']}` |
| **Caminho** | `{entry['path']}` |
| **Ação** | {entry['action']} |
| **Ferramenta** | {entry['tool']} |
| **Palavras** | {entry['word_count']} |
| **Preview** | {entry['preview'][:80]}... |
"""

    # Read existing content or create new
    if os.path.exists(md_path):
        with open(md_path, 'r') as f:
            content = f.read()

        # Check if today's section exists
        if date_header not in content:
            # Add new date section at the top (after title)
            lines = content.split('\n')
            if lines[0].startswith('# '):
                # Insert after title
                lines.insert(2, f"\n{date_header}")
                lines.insert(3, md_entry)
            else:
                # Insert at beginning
                lines.insert(0, date_header)
                lines.insert(1, md_entry)
            content = '\n'.join(lines)
        else:
            # Add entry under existing date section
            date_index = content.index(date_header)
            next_section = content.find('\n## ', date_index + 1)
            if next_section == -1:
                # Add at the end
                content += md_entry
            else:
                # Insert before next section
                content = content[:next_section] + md_entry + content[next_section:]
    else:
        # Create new file
        content = f"""# 📚 Audit Trail - Histórico de Arquivos

> Sistema automatizado de tracking de modificações de arquivos

---

{date_header}
{md_entry}

---

*Gerado automaticamente pelo hook report-tracker.py*
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

        # Track the report
        track_report(tool_name, tool_input, tool_response)

        # Always exit successfully
        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)