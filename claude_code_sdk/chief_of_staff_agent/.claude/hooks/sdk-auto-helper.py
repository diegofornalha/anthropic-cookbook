#!/usr/bin/env python3
"""
SDK Auto Helper - Hook que detecta quando ajuda é necessária sobre Claude Code SDK
Ativa automaticamente quando detecta erros ou imports do SDK
"""

import json
import re
from typing import Dict, Any, Optional

# Padrões que indicam necessidade de ajuda
SDK_PATTERNS = {
    'import_error': r'from\s+claude_code_sdk\s+import\s+(\w+)',
    'query_usage': r'query\s*\(',
    'options_usage': r'ClaudeCodeOptions\s*\(',
    'mcp_tool': r'@tool\s*\(',
    'hook_usage': r'HookMatcher\s*\(',
    'error_sdk': r'ClaudeSDKError|CLIConnectionError',
}

# Mapeamento de conceitos para exercícios
CONCEPT_TO_EXERCISE = {
    'query': 1,
    'ClaudeCodeOptions': 2,
    'tools': 3,
    'mcp': 4,
    'hooks': 5,
    'streaming': 6,
    'multi_agent': 7
}

def detect_sdk_usage(content: str) -> Optional[str]:
    """Detecta uso do SDK e retorna conceito relacionado"""

    for pattern_name, pattern in SDK_PATTERNS.items():
        if re.search(pattern, content, re.IGNORECASE):
            if 'query' in pattern_name:
                return 'query'
            elif 'options' in pattern_name:
                return 'ClaudeCodeOptions'
            elif 'mcp' in pattern_name:
                return 'mcp'
            elif 'hook' in pattern_name:
                return 'hooks'
            elif 'error' in pattern_name:
                return 'error_handling'

    return None

def get_help_suggestion(concept: str) -> str:
    """Retorna sugestão de ajuda baseada no conceito"""

    suggestions = {
        'query': """
💡 Detectei uso de query()!
→ Lembre-se: query() é assíncrona, use 'async for'
→ Pratique: python examples/exercicios_praticos_pt_br.py 1
        """,

        'ClaudeCodeOptions': """
⚙️ Configurando ClaudeCodeOptions!
→ Principais opções: temperature, allowed_tools, max_turns
→ Pratique: python examples/exercicios_praticos_pt_br.py 2
        """,

        'mcp': """
🔴 MCP Tools detectado! (Gap crítico)
→ Use @tool decorator + create_sdk_mcp_server()
→ FOCO: python examples/exercicios_praticos_pt_br.py 4
        """,

        'hooks': """
🔴 Hooks System detectado! (Gap crítico)
→ Use HookMatcher com PreToolUse/PostToolUse
→ FOCO: python examples/exercicios_praticos_pt_br.py 5
        """,

        'error_handling': """
❌ Tratamento de erros SDK
→ ClaudeSDKError é a classe base
→ Use try/except específicos para cada tipo
        """
    }

    return suggestions.get(concept, "")

def save_to_neo4j(concept: str, file_path: str):
    """Salva detecção no Neo4j para tracking"""

    neo4j_query = f"""
    CREATE (d:Learning {{
        type: 'sdk_usage_detected',
        concept: '{concept}',
        file: '{file_path}',
        timestamp: datetime(),
        exercise: {CONCEPT_TO_EXERCISE.get(concept, 0)}
    }})
    """

    # Aqui seria a integração real com Neo4j
    print(f"📊 Salvando no Neo4j: {concept} usado em {file_path}")

def main(hook_input: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Hook principal que processa código e oferece ajuda
    """

    # Extrair informações do input
    tool_name = hook_input.get('name', '')
    tool_input = hook_input.get('input', {})

    # Se for ferramenta de escrita/edição, verificar código
    if tool_name in ['Write', 'Edit', 'MultiEdit']:
        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        file_path = tool_input.get('file_path', '')

        # Detectar uso do SDK
        concept = detect_sdk_usage(content)

        if concept:
            # Obter sugestão
            suggestion = get_help_suggestion(concept)

            # Salvar no Neo4j
            if file_path.endswith('.py'):
                save_to_neo4j(concept, file_path)

            # Adicionar sugestão ao output
            if suggestion:
                print(f"\n{'='*60}")
                print("🤖 SDK AUTO HELPER ATIVADO")
                print(suggestion)
                print(f"{'='*60}\n")

                # Se for gap crítico, enfatizar
                if concept in ['mcp', 'hooks']:
                    print("⚠️ ATENÇÃO: Este é um dos seus GAPS CRÍTICOS!")
                    print(f"📚 Dedique tempo extra ao exercício {CONCEPT_TO_EXERCISE[concept]}")
                    print("")

    # Permitir execução normal
    return None

if __name__ == "__main__":
    # Para teste local
    test_input = {
        'name': 'Write',
        'input': {
            'file_path': 'test.py',
            'content': '''
from claude_code_sdk import query, ClaudeCodeOptions

options = ClaudeCodeOptions(temperature=0.7)

@tool(name="test")
async def test_tool():
    pass
            '''
        }
    }

    main(test_input)