#!/usr/bin/env python3
"""
Hook PostToolUse: Registra quando scripts Python são executados via ferramenta Bash
Mantém logs de auditoria em JSON e Markdown
"""

import json
import os
import sys
from datetime import datetime


def log_script_usage(tool_name, tool_input, tool_response):
    """Registra execução de scripts Python via ferramenta Bash em JSON e Markdown"""

    # Rastreia apenas ferramenta Bash (usada para executar scripts)
    if tool_name != "Bash":
        return

    # Obtém o comando do input da ferramenta
    command = tool_input.get("command", "")

    # Verifica se está executando um script Python do diretório scripts/
    # Suporte para ambos: "python scripts/file.py" e "./scripts/file.py"
    import re

    # Tenta corresponder qualquer padrão: python scripts/... ou ./scripts/... ou scripts/...
    script_match = re.search(r"(?:python\s+)?(?:\./)?scripts/(\w+\.py)", command)
    if not script_match:
        return

    # Continua apenas se for execução do diretório scripts/
    if "scripts/" not in command:
        return

    script_file = script_match.group(1)

    # Prepara caminhos dos arquivos
    audit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../audit")
    log_json = os.path.join(audit_dir, "script_usage_log.json")
    log_md = os.path.join(audit_dir, "script_usage_log.md")

    try:
        # Carrega log JSON existente ou cria novo
        if os.path.exists(log_json):
            with open(log_json) as f:
                log_data = json.load(f)
        else:
            log_data = {"script_executions": []}

        # Cria entrada do log
        timestamp = datetime.now()
        entry = {
            "timestamp": timestamp.isoformat(),
            "script": script_file,
            "command": command,
            "description": tool_input.get("description", "No description"),
            "tool_used": "Bash",
            "success": tool_response.get("success", True) if tool_response else True,
        }

        # Adiciona ao log JSON
        log_data["script_executions"].append(entry)
        log_data["script_executions"] = log_data["script_executions"][-100:]  # Mantém últimas 100

        # Salva log JSON atualizado
        os.makedirs(audit_dir, exist_ok=True)
        with open(log_json, "w") as f:
            json.dump(log_data, f, indent=2)

        # Atualiza log Markdown
        update_markdown_log(log_md, entry, timestamp)

        print(f"📜 Script executado: {script_file}")

    except Exception as e:
        print(f"Erro no log de script: {e}", file=sys.stderr)


def update_markdown_log(md_path, entry, timestamp):
    """Cria ou atualiza o log Markdown de execução de scripts"""

    # Formata a data para cabeçalhos de seção
    date_header = timestamp.strftime("## 📅 %d/%m/%Y")
    time_str = timestamp.strftime("%H:%M:%S")

    # Determina emoji de status
    status_emoji = "✅" if entry["success"] else "❌"

    # Cria nova entrada no formato Markdown
    md_entry = f"""
### ⚡ {time_str} - {entry['script']} {status_emoji}

| Campo | Valor |
|-------|---------|
| **Script** | `{entry['script']}` |
| **Comando** | `{entry['command']}` |
| **Descrição** | {entry['description']} |
| **Status** | {'Sucesso' if entry['success'] else 'Falha'} |
"""

    # Documentação dos scripts
    script_docs = {
        "ai_expertise_evaluator.py": "🤖 Avalia expertise técnica em IA/ML",
        "talent_scorer.py": "👥 Pontua candidatos com múltiplos critérios",
        "simple_calculation.py": "🧮 Cálculos financeiros básicos"
    }

    if entry['script'] in script_docs:
        md_entry += f"\n> **Função**: {script_docs[entry['script']]}\n"

    # Lê conteúdo existente ou cria novo
    if os.path.exists(md_path):
        with open(md_path, 'r') as f:
            content = f.read()

        # Verifica se seção de hoje existe
        if date_header not in content:
            # Adiciona nova seção de data
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
            # Adiciona entrada sob data existente
            date_index = content.index(date_header)
            next_section = content.find('\n## ', date_index + 1)
            if next_section == -1:
                content += md_entry
            else:
                content = content[:next_section] + md_entry + content[next_section:]
    else:
        # Cria novo arquivo
        content = f"""# 🔧 Script Execution Log

> Registro automatizado de scripts Python executados

---

{date_header}
{md_entry}

---

*Gerado por script-usage-logger.py*
"""

    # Salva o Markdown atualizado
    with open(md_path, 'w') as f:
        f.write(content)


# Execução principal
if __name__ == "__main__":
    try:
        # Lê entrada do stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        tool_response = input_data.get("tool_response", {})

        # Registra o uso do script
        log_script_usage(tool_name, tool_input, tool_response)

        # Sempre sai com sucesso
        sys.exit(0)

    except Exception as e:
        print(f"Erro do hook: {e}", file=sys.stderr)
        sys.exit(0)
