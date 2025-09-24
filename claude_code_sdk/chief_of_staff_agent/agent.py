"""
Assistente Pessoal de IA - Diego Fornalha
"""

import asyncio
import json
import os
from collections.abc import Callable
from typing import Any, Literal

from dotenv import load_dotenv

from claude_code_sdk import ClaudeCodeOptions, ClaudeSDKClient

load_dotenv()


def get_activity_text(msg) -> str | None:
    """Extrai texto de atividade de uma mensagem"""
    try:
        if "Assistant" in msg.__class__.__name__:
            if hasattr(msg, "content") and msg.content:
                first_content = msg.content[0] if isinstance(msg.content, list) else msg.content
                if hasattr(first_content, "name"):
                    return f"🤖 Usando: {first_content.name}()"
            return "🤖 Pensando..."
        elif "User" in msg.__class__.__name__:
            return "✓ Ferramenta concluída"
    except (AttributeError, IndexError):
        pass
    return None


def print_activity(msg) -> None:
    """Imprime atividade no console"""
    activity = get_activity_text(msg)
    if activity:
        print(activity)


async def send_query(
    prompt: str,
    continue_conversation: bool = False,
    permission_mode: Literal["default", "plan", "acceptEdits"] = "default",
    output_style: str | None = None,
    activity_handler: Callable[[Any], None | Any] = print_activity,
) -> tuple[str | None, list]:
    """
    Envia uma consulta ao Assistente Pessoal de IA do Diego Fornalha com todas as funcionalidades integradas.

    Args:
        prompt: A consulta a enviar (pode incluir comandos slash como /budget-impact)
        activity_handler: Callback para atualizações de atividade (padrão: print_activity)
        continue_conversation: Continuar a conversa anterior se True
        permission_mode: "default" (executar), "plan" (apenas pensar), ou "acceptEdits"
        output_style: Substituir estilo de saída (ex: "executive", "technical", "board-report")

    Returns:
        Tupla de (result, messages) - result é o texto final, messages é a conversa completa

    Funcionalidades automaticamente incluídas/utilizadas:
        - Memória: Contexto CLAUDE.md carregado de chief_of_staff/CLAUDE.md
        - Subagentes: cto e recrutador via ferramenta Task (definidos em .claude/agents)
        - Scripts customizados: Scripts Python em tools/ via Bash
        - Comandos slash: Expandidos de .claude/commands/
        - Estilos de saída: Estilos de saída customizados definidos em .claude/output-styles
        - Hooks: Acionados baseados em settings.local.json, definidos em .claude/hooks
        - Neo4j Memory: Acesso ao progresso de aprendizado do Diego
    """

    system_prompt = """Você é o Assistente Pessoal de IA do Diego Fornalha, um desenvolvedor em transição de blockchain para especialista em Claude Code SDK.

        Além das suas ferramentas e dois subagentes (cto e recrutador), você também tem scripts Python customizados no diretório scripts/ que pode executar com Bash:
        - python scripts/ai_expertise_evaluator.py: Avaliação técnica de expertise em IA/ML
        - python scripts/talent_scorer.py: Algoritmo de pontuação de candidatos
        - python scripts/decision_matrix.py: Framework de decisão estratégica

        Você tem acesso aos dados do bootcamp no diretório financial_data/ e ao progresso de aprendizado no Neo4j Memory.
        
        Contexto do Diego:
        - Score atual: 45/100
        - Meta: 100/100 em 12 semanas
        - Fase atual: Fundamentos (Semana 1)
        - Objetivo: Dominar Claude Code SDK completamente
        """

    # construir opções com estilo de saída opcional
    options_dict = {
        "model": "claude-sonnet-4-20250514",
        "allowed_tools": [
            "Task",  # habilita delegação de subagentes
            "Read",
            "Write",
            "Edit",
            "Bash",
            "WebSearch",
        ],
        "continue_conversation": continue_conversation,
        "system_prompt": system_prompt,
        "permission_mode": permission_mode,
        "cwd": os.path.dirname(os.path.abspath(__file__)),
    }

    # adicionar estilo de saída se especificado
    if output_style:
        options_dict["settings"] = json.dumps({"outputStyle": output_style})

    options = ClaudeCodeOptions(**options_dict)

    result = None
    messages = []  # isto é para anexar as mensagens APENAS para esta vez do agente

    try:
        async with ClaudeSDKClient(options=options) as agent:
            await agent.query(prompt=prompt)
            async for msg in agent.receive_response():
                messages.append(msg)
                if asyncio.iscoroutinefunction(activity_handler):
                    await activity_handler(msg)
                else:
                    activity_handler(msg)

                if hasattr(msg, "result"):
                    result = msg.result
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")
        raise

    return result, messages
