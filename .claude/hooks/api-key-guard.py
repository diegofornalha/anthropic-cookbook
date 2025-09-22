#!/usr/bin/env python3
"""
Hook para prevenir uso de API keys e sugerir migração para Claude Code SDK
Versão aprimorada com detecção mais robusta e sugestões automáticas
"""

import json
import sys
import re
from pathlib import Path

def main():
    # Receber dados do hook
    hook_data = json.loads(sys.stdin.read())

    tool_name = hook_data.get("toolName", "")
    tool_input = hook_data.get("toolInput", {})

    # Log para Neo4j Memory
    log_detection(tool_name, tool_input)

    # Verificar se é Write ou Edit
    if tool_name in ["Write", "Edit", "MultiEdit", "NotebookEdit"]:
        content = extract_content(tool_name, tool_input)

        # Detecção aprimorada de patterns
        api_key_patterns = [
            (r"ANTHROPIC_API_KEY", "Variável de ambiente de API key"),
            (r"api_key\s*=\s*['\"][^'\"]+['\"]", "API key hardcoded"),
            (r"api_key\s*=\s*os\.(getenv|environ)", "API key de variável de ambiente"),
            (r"anthropic\.Anthropic\s*\(", "Cliente Anthropic com API key"),
            (r"sk-ant-[a-zA-Z0-9]+", "API key literal detectada"),
            (r"Client\(.*api_key", "Cliente com parâmetro api_key"),
            (r"from\s+anthropic\s+import\s+Anthropic", "Import do cliente legado"),
        ]

        for pattern, description in api_key_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                # Gerar código migrado automaticamente
                migrated_code = auto_migrate_code(content, pattern)

                # Bloquear e sugerir alternativa
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            f"🚫 Detectado: {description}\n\n"
                            "📝 Código correto sugerido:\n"
                            "```python\n"
                            f"{migrated_code[:500]}\n"  # Primeiras 500 chars
                            "```\n\n"
                            "✅ Use sempre:\n"
                            "• ClaudeSDKClient sem API key\n"
                            "• Autenticação via: claude login\n"
                            "• Comando: /migrate-to-sdk <arquivo>\n\n"
                            "📚 Exemplos: claude_code_sdk/*.ipynb"
                        )
                    }
                }))
                return 1

    # Verificar comandos Bash
    if tool_name == "Bash":
        command = tool_input.get("command", "")

        # Patterns de comandos perigosos
        dangerous_commands = [
            (r"export\s+ANTHROPIC_API_KEY", "Export de API key"),
            (r"echo.*ANTHROPIC_API_KEY", "Echo de API key"),
            (r"printenv.*ANTHROPIC", "Print de variáveis Anthropic"),
            (r"pip\s+install\s+anthropic(?!-code-sdk)", "Instalando biblioteca legada"),
        ]

        for pattern, description in dangerous_commands:
            if re.search(pattern, command, re.IGNORECASE):
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            f"🚫 Bloqueado: {description}\n\n"
                            "✅ Alternativas corretas:\n"
                            "• Autenticação: claude login\n"
                            "• Instalação: pip install claude-code-sdk\n"
                            "• Verificação: claude auth status\n\n"
                            "Isso configura autenticação permanentemente."
                        )
                    }
                }))
                return 1

    # Permitir execução
    return 0

def extract_content(tool_name, tool_input):
    """Extrai conteúdo baseado no tipo de ferramenta"""
    if tool_name in ["Write", "NotebookEdit"]:
        return tool_input.get("content", tool_input.get("new_source", ""))
    elif tool_name in ["Edit", "MultiEdit"]:
        if "edits" in tool_input:
            # MultiEdit
            contents = [edit.get("new_string", "") for edit in tool_input.get("edits", [])]
            return " ".join(contents)
        else:
            # Edit simples
            return tool_input.get("new_string", "")
    return ""

def auto_migrate_code(content, pattern):
    """Gera versão migrada do código automaticamente"""
    # Substituições automáticas
    replacements = {
        r"from\s+anthropic\s+import\s+Anthropic": "from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query",
        r"anthropic\.Anthropic\([^)]*\)": "ClaudeSDKClient(options=ClaudeCodeOptions())",
        r"client\.messages\.create": "await query",
        r"api_key\s*=\s*[^,)]+": "",
        r"ANTHROPIC_API_KEY": "# Não necessário com Claude Code SDK",
        r"os\.getenv\(['\"]ANTHROPIC_API_KEY['\"]\)": "# Autenticação via claude login",
    }

    migrated = content
    for old, new in replacements.items():
        migrated = re.sub(old, new, migrated, flags=re.IGNORECASE)

    # Adicionar imports necessários se não existirem
    if "claude_code_sdk" not in migrated and "import" in migrated:
        migrated = "from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query\n" + migrated

    return migrated

def log_detection(tool_name, tool_input):
    """Registra detecções para análise posterior"""
    try:
        log_file = Path("/Users/2a/.claude/anthropic-cookbook/.claude/logs/api_key_detections.json")
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # Adicionar ao log (simplificado para o exemplo)
        # Em produção, isso seria mais robusto
    except:
        pass  # Não falhar o hook por erro de log

if __name__ == "__main__":
    sys.exit(main())