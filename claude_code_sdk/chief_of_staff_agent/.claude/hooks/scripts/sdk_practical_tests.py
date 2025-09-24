#!/usr/bin/env python3
"""
SDK Practical Tests - Testes práticos para validar conhecimento real do Claude Code SDK
Desafios progressivos usando query(), ClaudeCodeOptions, MCP Tools e Hooks
"""

import asyncio
from typing import Dict, List, Optional, Callable
import json

class SDKPracticalTests:
    """Bateria de testes práticos do Claude Code SDK"""

    def __init__(self):
        self.tests = []
        self.results = {}

    # ============ TESTE 1: Query Básica ============
    def test_1_basic_query(self) -> Dict:
        """Teste 1: Implementar query básica"""
        challenge = {
            "id": "test_1",
            "level": "BÁSICO",
            "points": 10,
            "description": "Implemente uma função que usa query() para perguntar ao Claude",
            "requirements": [
                "Usar async/await corretamente",
                "Importar query do claude_code_sdk",
                "Processar resposta AssistantMessage",
                "Extrair texto de TextBlock"
            ],
            "template": """
# Complete o código:
from claude_code_sdk import ___

async def perguntar_claude(pergunta: str):
    # TODO: Implementar query assíncrona
    # TODO: Processar resposta
    # TODO: Retornar texto
    pass
            """,
            "solution": """
from claude_code_sdk import query

async def perguntar_claude(pergunta: str):
    resposta = ""
    async for msg in query(pergunta):
        if hasattr(msg, 'content'):
            for block in msg.content:
                if hasattr(block, 'text'):
                    resposta += block.text
    return resposta
            """,
            "validation": lambda code: all([
                "from claude_code_sdk import query" in code,
                "async for" in code,
                "query(" in code,
                "async def" in code
            ])
        }
        return challenge

    # ============ TESTE 2: ClaudeCodeOptions ============
    def test_2_options_configuration(self) -> Dict:
        """Teste 2: Configurar ClaudeCodeOptions"""
        challenge = {
            "id": "test_2",
            "level": "BÁSICO",
            "points": 10,
            "description": "Configure options para código preciso com ferramentas",
            "requirements": [
                "Temperature baixa (0.1-0.3)",
                "Permitir Read e Write",
                "System prompt customizado",
                "Max turns definido"
            ],
            "template": """
# Configure para gerar código Python preciso:
from claude_code_sdk import ClaudeCodeOptions

options = ClaudeCodeOptions(
    # TODO: Temperature para código
    # TODO: Ferramentas Read e Write
    # TODO: System prompt
    # TODO: Máximo 5 turnos
)
            """,
            "solution": """
from claude_code_sdk import ClaudeCodeOptions

options = ClaudeCodeOptions(
    temperature=0.2,
    allowed_tools=["Read", "Write"],
    system_prompt="Você é um expert em Python que sempre adiciona type hints",
    max_turns=5
)
            """,
            "validation": lambda code: all([
                "temperature=" in code and any(f"0.{i}" in code for i in range(4)),
                '["Read", "Write"]' in code or "['Read', 'Write']" in code,
                "system_prompt=" in code,
                "max_turns=" in code
            ])
        }
        return challenge

    # ============ TESTE 3: Pipeline de Ferramentas ============
    def test_3_tools_pipeline(self) -> Dict:
        """Teste 3: Criar pipeline Read → Process → Write"""
        challenge = {
            "id": "test_3",
            "level": "INTERMEDIÁRIO",
            "points": 15,
            "description": "Crie pipeline que lê arquivo, processa e salva resultado",
            "requirements": [
                "Permitir Read, Write e Edit",
                "Prompt claro com 3 etapas",
                "Usar options corretamente",
                "Pipeline completo"
            ],
            "template": """
# Crie pipeline: Ler README.md → Adicionar timestamp → Salvar como README_backup.md
from claude_code_sdk import query, ClaudeCodeOptions

async def pipeline_backup():
    options = ClaudeCodeOptions(
        # TODO: Permitir ferramentas necessárias
    )

    prompt = '''
    # TODO: Escrever prompt com 3 etapas:
    # 1. Ler README.md
    # 2. Adicionar timestamp no início
    # 3. Salvar como README_backup.md
    '''

    # TODO: Executar query
            """,
            "solution": """
from claude_code_sdk import query, ClaudeCodeOptions
from datetime import datetime

async def pipeline_backup():
    options = ClaudeCodeOptions(
        allowed_tools=["Read", "Write", "Edit"]
    )

    prompt = '''
    Execute este pipeline:
    1. Leia o arquivo README.md
    2. Adicione no início: "# Backup criado em: {datetime.now()}"
    3. Salve o conteúdo modificado como README_backup.md
    '''

    async for msg in query(prompt, options=options):
        if hasattr(msg, 'content'):
            print("Pipeline em execução...")
            """,
            "validation": lambda code: all([
                "allowed_tools" in code,
                "Read" in code and "Write" in code,
                "query(" in code,
                "options=" in code
            ])
        }
        return challenge

    # ============ TESTE 4: MCP Tools (CRÍTICO!) ============
    def test_4_mcp_tools_critical(self) -> Dict:
        """Teste 4: Implementar ferramenta MCP customizada"""
        challenge = {
            "id": "test_4",
            "level": "🔴 CRÍTICO",
            "points": 25,
            "description": "Crie ferramenta MCP para análise de código Python",
            "requirements": [
                "Usar @tool decorator",
                "Input schema correto",
                "Retornar content com type text",
                "Criar servidor MCP",
                "Configurar em options"
            ],
            "template": """
# DESAFIO CRÍTICO: Crie ferramenta que conta linhas de código Python
from claude_code_sdk import tool, create_sdk_mcp_server, ClaudeCodeOptions

# TODO: Criar ferramenta com @tool
@tool(
    name=___,
    description=___,
    input_schema=___
)
async def contar_linhas_python(args: dict) -> dict:
    # TODO: Implementar contagem
    # TODO: Retornar formato correto
    pass

# TODO: Criar servidor MCP
servidor = ___

# TODO: Configurar options
options = ClaudeCodeOptions(
    mcp_servers=___,
    allowed_tools=___
)
            """,
            "solution": """
from claude_code_sdk import tool, create_sdk_mcp_server, ClaudeCodeOptions

@tool(
    name="python_analyzer",
    description="Analisa e conta linhas de código Python",
    input_schema={"code": str}
)
async def contar_linhas_python(args: dict) -> dict:
    code = args.get("code", "")
    lines = code.split('\\n')
    non_empty = [l for l in lines if l.strip()]

    return {
        "content": [{
            "type": "text",
            "text": f"Total: {len(lines)} linhas, {len(non_empty)} não-vazias"
        }]
    }

servidor = create_sdk_mcp_server(
    name="code_tools",
    version="1.0.0",
    tools=[contar_linhas_python]
)

options = ClaudeCodeOptions(
    mcp_servers={"analyzer": servidor},
    allowed_tools=["mcp__analyzer__python_analyzer"]
)
            """,
            "validation": lambda code: all([
                "@tool(" in code,
                "input_schema=" in code,
                '"content":' in code or "'content':" in code,
                "create_sdk_mcp_server(" in code,
                "mcp_servers=" in code
            ])
        }
        return challenge

    # ============ TESTE 5: Hooks System (CRÍTICO!) ============
    def test_5_hooks_critical(self) -> Dict:
        """Teste 5: Implementar sistema de hooks para segurança"""
        challenge = {
            "id": "test_5",
            "level": "🔴 CRÍTICO",
            "points": 25,
            "description": "Crie hooks para validar e modificar execução de ferramentas",
            "requirements": [
                "Hook PreToolUse para validação",
                "Hook PostToolUse para logging",
                "Bloquear comandos perigosos",
                "Modificar entrada quando necessário",
                "Configurar HookMatcher corretamente"
            ],
            "template": """
# DESAFIO CRÍTICO: Sistema de segurança com hooks
from claude_code_sdk import HookMatcher, ClaudeCodeOptions

# TODO: Hook de validação PRÉ execução
async def validar_seguranca(data: dict, tool_id: str, ctx: dict) -> dict:
    # TODO: Bloquear rm -rf
    # TODO: Bloquear comandos sudo
    # TODO: Retornar deny ou None
    pass

# TODO: Hook PÓS execução para log
async def log_execucao(data: dict, tool_id: str, ctx: dict) -> dict:
    # TODO: Registrar execução
    pass

# TODO: Configurar hooks
options = ClaudeCodeOptions(
    hooks=[
        # TODO: HookMatcher para PreToolUse
        # TODO: HookMatcher para PostToolUse
    ]
)
            """,
            "solution": """
from claude_code_sdk import HookMatcher, ClaudeCodeOptions

async def validar_seguranca(data: dict, tool_id: str, ctx: dict) -> dict:
    command = str(data.get("input", {}).get("command", ""))

    # Bloquear comandos perigosos
    dangerous = ["rm -rf", "sudo", "chmod 777", "curl | bash"]
    for danger in dangerous:
        if danger in command:
            return {
                "behavior": "deny",
                "message": f"Comando bloqueado: {danger}"
            }

    return None  # Permitir

async def log_execucao(data: dict, tool_id: str, ctx: dict) -> dict:
    tool_name = data.get("name", "unknown")
    print(f"[LOG] Ferramenta {tool_name} executada com sucesso")
    return None

options = ClaudeCodeOptions(
    hooks=[
        HookMatcher(
            matcher="PreToolUse",
            hooks=[validar_seguranca]
        ),
        HookMatcher(
            matcher="PostToolUse",
            hooks=[log_execucao]
        )
    ]
)
            """,
            "validation": lambda code: all([
                "HookMatcher(" in code,
                "PreToolUse" in code,
                "PostToolUse" in code,
                '"behavior": "deny"' in code or "'behavior': 'deny'" in code,
                "return None" in code
            ])
        }
        return challenge

    # ============ TESTE 6: Streaming ============
    def test_6_streaming_client(self) -> Dict:
        """Teste 6: Usar ClaudeSDKClient com streaming"""
        challenge = {
            "id": "test_6",
            "level": "AVANÇADO",
            "points": 15,
            "description": "Implemente chat interativo com streaming",
            "requirements": [
                "Usar ClaudeSDKClient",
                "Context manager (async with)",
                "receive_response() para streaming",
                "Interrupção após N mensagens"
            ],
            "template": """
# Chat com streaming e interrupção
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def chat_interativo():
    options = ClaudeCodeOptions(
        # TODO: Configurar options
    )

    # TODO: Usar async with para cliente
    # TODO: Fazer query inicial
    # TODO: Receber resposta com streaming
    # TODO: Interromper após 3 chunks
            """,
            "solution": """
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

async def chat_interativo():
    options = ClaudeCodeOptions(
        system_prompt="Assistente conciso"
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Explique Python em detalhes")

        chunk_count = 0
        async for message in client.receive_response():
            chunk_count += 1
            if chunk_count > 3:
                await client.interrupt()
                break
            print(f"Chunk {chunk_count} recebido")
            """,
            "validation": lambda code: all([
                "ClaudeSDKClient" in code,
                "async with" in code,
                "receive_response()" in code,
                "interrupt()" in code
            ])
        }
        return challenge

    def run_all_tests(self, candidate_code: Dict[str, str]) -> Dict:
        """Executa todos os testes e calcula score"""
        all_tests = [
            self.test_1_basic_query(),
            self.test_2_options_configuration(),
            self.test_3_tools_pipeline(),
            self.test_4_mcp_tools_critical(),
            self.test_5_hooks_critical(),
            self.test_6_streaming_client()
        ]

        total_score = 0
        passed_tests = []
        failed_tests = []
        critical_gaps = []

        for test in all_tests:
            test_id = test["id"]
            code = candidate_code.get(test_id, "")

            if test["validation"](code):
                total_score += test["points"]
                passed_tests.append(test_id)
            else:
                failed_tests.append(test_id)
                if "CRÍTICO" in test["level"]:
                    critical_gaps.append(f"🔴 {test['description']}")

        return {
            "total_score": total_score,
            "max_score": 100,
            "passed": passed_tests,
            "failed": failed_tests,
            "critical_gaps": critical_gaps,
            "recommendation": self.get_recommendation(total_score, critical_gaps)
        }

    def get_recommendation(self, score: int, gaps: List[str]) -> str:
        """Recomendação baseada no score"""
        if score >= 90:
            return "🏆 EXPERT! Pronto para contribuir com o SDK"
        elif score >= 75:
            return "📚 Avançado - Focar nos gaps críticos"
        elif score >= 50:
            return "⚠️ Intermediário - MCP Tools e Hooks são prioridade!"
        else:
            return "🔴 Iniciante - Começar com exercícios básicos"

    def generate_test_file(self, test_id: str) -> str:
        """Gera arquivo de teste para candidato"""
        tests = {
            "test_1": self.test_1_basic_query(),
            "test_2": self.test_2_options_configuration(),
            "test_3": self.test_3_tools_pipeline(),
            "test_4": self.test_4_mcp_tools_critical(),
            "test_5": self.test_5_hooks_critical(),
            "test_6": self.test_6_streaming_client()
        }

        test = tests.get(test_id)
        if not test:
            return "Teste não encontrado"

        return f"""
#!/usr/bin/env python3
'''
{test['description']}
Nível: {test['level']}
Pontos: {test['points']}

Requisitos:
{chr(10).join(f"- {req}" for req in test['requirements'])}
'''

{test['template']}

# Para validar sua solução:
# python validate_test.py {test_id}
"""

if __name__ == "__main__":
    # Exemplo de uso
    tester = SDKPracticalTests()

    # Simular código do candidato
    diego_solutions = {
        "test_1": """
from claude_code_sdk import query

async def perguntar_claude(pergunta: str):
    async for msg in query(pergunta):
        if hasattr(msg, 'content'):
            return msg
        """,
        "test_2": """
from claude_code_sdk import ClaudeCodeOptions

options = ClaudeCodeOptions(
    temperature=0.2,
    allowed_tools=["Read", "Write"],
    system_prompt="Expert em Python",
    max_turns=5
)
        """,
        "test_3": "",  # Não resolvido
        "test_4": "",  # Gap crítico!
        "test_5": "",  # Gap crítico!
        "test_6": ""   # Não resolvido
    }

    result = tester.run_all_tests(diego_solutions)

    print("\n" + "="*60)
    print("📝 TESTES PRÁTICOS CLAUDE CODE SDK")
    print("="*60)
    print(f"Score: {result['total_score']}/{result['max_score']}")
    print(f"\n✅ Testes Aprovados: {', '.join(result['passed'])}")
    print(f"\n❌ Testes Reprovados: {', '.join(result['failed'])}")
    print(f"\n🔴 Gaps Críticos:")
    for gap in result['critical_gaps']:
        print(f"  {gap}")
    print(f"\n📊 Recomendação: {result['recommendation']}")
    print("="*60)