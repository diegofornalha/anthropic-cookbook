#!/usr/bin/env python3
"""
SDK Technical Interview - Processo de entrevista técnica específico para Claude Code SDK
Sistema de pontuação focado no SDK com desafio prático em tempo real
"""

import asyncio
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

class ClaudeSDKTechnicalInterview:
    """Sistema completo de entrevista técnica para Claude Code SDK"""

    def __init__(self, candidate_name: str, interviewer: str = "CTO"):
        self.candidate = candidate_name
        self.interviewer = interviewer
        self.start_time = time.time()
        self.responses = []
        self.score = 0
        self.max_score = 100

    # ================== PARTE 1: SCREENING (20 pontos) ==================
    def screening_questions(self) -> List[Dict]:
        """Perguntas de screening inicial"""
        questions = [
            {
                "id": "q1",
                "question": "Qual a diferença entre usar Claude com API key vs Claude Code SDK?",
                "expected_keywords": ["claude login", "sem api key", "autenticação local"],
                "points": 5,
                "time_limit": 60
            },
            {
                "id": "q2",
                "question": "Por que query() é assíncrona? Como você a executa?",
                "expected_keywords": ["async for", "asyncio.run", "await"],
                "points": 5,
                "time_limit": 60
            },
            {
                "id": "q3",
                "question": "Cite 3 parâmetros importantes de ClaudeCodeOptions",
                "expected_keywords": ["temperature", "allowed_tools", "system_prompt", "max_turns"],
                "points": 5,
                "time_limit": 60
            },
            {
                "id": "q4",
                "question": "Quais ferramentas o Claude pode usar através do SDK?",
                "expected_keywords": ["Read", "Write", "Edit", "Bash", "Grep"],
                "points": 5,
                "time_limit": 60
            }
        ]
        return questions

    # ================== PARTE 2: CONCEITOS AVANÇADOS (30 pontos) ==================
    def advanced_concepts(self) -> List[Dict]:
        """Perguntas sobre conceitos avançados"""
        questions = [
            {
                "id": "a1",
                "question": "Explique como criar uma ferramenta MCP customizada",
                "expected_keywords": ["@tool", "create_sdk_mcp_server", "content", "return"],
                "points": 10,
                "critical": True,
                "time_limit": 120
            },
            {
                "id": "a2",
                "question": "Como funcionam os Hooks? Dê exemplo de PreToolUse",
                "expected_keywords": ["HookMatcher", "PreToolUse", "return None", "behavior deny"],
                "points": 10,
                "critical": True,
                "time_limit": 120
            },
            {
                "id": "a3",
                "question": "Qual a estrutura de retorno de uma MCP Tool?",
                "expected_keywords": ["content", "type text", "dict"],
                "points": 5,
                "time_limit": 60
            },
            {
                "id": "a4",
                "question": "Como implementar streaming com ClaudeSDKClient?",
                "expected_keywords": ["async with", "receive_response", "interrupt"],
                "points": 5,
                "time_limit": 90
            }
        ]
        return questions

    # ================== PARTE 3: DESAFIO PRÁTICO (50 pontos) ==================
    def practical_challenge(self) -> Dict:
        """Desafio prático em tempo real"""
        return {
            "title": "DESAFIO: Criar Sistema de Análise de Código com Claude Code SDK",
            "time_limit": 1200,  # 20 minutos
            "requirements": [
                "1. Criar função que usa query() para analisar código Python",
                "2. Configurar ClaudeCodeOptions com temperature baixa e ferramentas",
                "3. Implementar MCP Tool para contar linhas de código",
                "4. Adicionar Hook de segurança para bloquear comandos perigosos",
                "5. Criar pipeline que lê arquivo → analisa → salva resultado"
            ],
            "starter_code": """
# Complete o código abaixo para criar o sistema

import asyncio
from claude_code_sdk import (
    query,
    ClaudeCodeOptions,
    tool,
    create_sdk_mcp_server,
    HookMatcher
)

# TODO: 1. Função de análise com query()
async def analisar_codigo(arquivo: str):
    # Implementar análise
    pass

# TODO: 2. MCP Tool para contar linhas
@tool(
    name=___,
    description=___,
    input_schema=___
)
async def contar_linhas_tool(args: dict) -> dict:
    # Implementar contagem
    pass

# TODO: 3. Hook de segurança
async def validar_seguranca(data: dict, tool_id: str, ctx: dict) -> dict:
    # Implementar validação
    pass

# TODO: 4. Pipeline completo
async def pipeline_analise():
    # Configurar options
    # Criar servidor MCP
    # Executar análise
    pass

# TODO: 5. Main
if __name__ == "__main__":
    asyncio.run(pipeline_analise())
            """,
            "evaluation_criteria": {
                "query_usage": 10,      # Usa query() corretamente
                "options_config": 10,   # Configura ClaudeCodeOptions
                "mcp_tool": 15,        # MCP Tool funcional
                "hooks": 10,           # Hook de segurança implementado
                "pipeline": 5          # Pipeline completo funciona
            }
        }

    def evaluate_code_submission(self, submitted_code: str) -> Dict:
        """Avalia código submetido no desafio"""
        score = 0
        feedback = []

        # Verificar query() usage
        if "async for" in submitted_code and "query(" in submitted_code:
            score += 10
            feedback.append("✅ query() usado corretamente")
        else:
            feedback.append("❌ query() não implementado corretamente")

        # Verificar ClaudeCodeOptions
        if "ClaudeCodeOptions(" in submitted_code and "temperature=" in submitted_code:
            score += 10
            feedback.append("✅ ClaudeCodeOptions configurado")
        else:
            feedback.append("❌ ClaudeCodeOptions não configurado")

        # Verificar MCP Tool
        if "@tool(" in submitted_code and '"content":' in submitted_code:
            score += 15
            feedback.append("✅ MCP Tool implementada corretamente")
        else:
            feedback.append("❌ MCP Tool com problemas")

        # Verificar Hooks
        if "HookMatcher(" in submitted_code and "PreToolUse" in submitted_code:
            score += 10
            feedback.append("✅ Hook de segurança implementado")
        else:
            feedback.append("❌ Hook não implementado")

        # Verificar Pipeline
        if "async def pipeline" in submitted_code:
            score += 5
            feedback.append("✅ Pipeline estruturado")
        else:
            feedback.append("❌ Pipeline incompleto")

        return {
            "score": score,
            "max_score": 50,
            "feedback": feedback
        }

    # ================== SISTEMA DE PONTUAÇÃO ==================
    def calculate_final_score(self, screening: int, advanced: int, practical: int) -> Dict:
        """Calcula score final e nível"""
        total = screening + advanced + practical

        if total >= 90:
            level = "EXPERT"
            recommendation = "✅ APROVADO - Expert em Claude Code SDK!"
            salary_range = "R$ 20k-25k"
        elif total >= 75:
            level = "SENIOR"
            recommendation = "✅ APROVADO - Senior, precisa reforçar gaps"
            salary_range = "R$ 15k-20k"
        elif total >= 60:
            level = "PLENO"
            recommendation = "⚠️ APROVADO CONDICIONAL - Requer mentoria"
            salary_range = "R$ 12k-15k"
        elif total >= 45:
            level = "JUNIOR"
            recommendation = "⚠️ CONSIDERAR - Potencial com bootcamp"
            salary_range = "R$ 8k-12k"
        else:
            level = "TRAINEE"
            recommendation = "❌ REPROVADO - Não pronto para SDK"
            salary_range = "N/A"

        return {
            "candidate": self.candidate,
            "total_score": total,
            "breakdown": {
                "screening": screening,
                "advanced": advanced,
                "practical": practical
            },
            "level": level,
            "recommendation": recommendation,
            "salary_range": salary_range,
            "gaps": self.identify_gaps(screening, advanced, practical),
            "next_steps": self.generate_next_steps(total, level),
            "interview_duration": time.time() - self.start_time
        }

    def identify_gaps(self, screening: int, advanced: int, practical: int) -> List[str]:
        """Identifica gaps específicos"""
        gaps = []

        if screening < 15:
            gaps.append("Fundamentos do SDK")

        if advanced < 20:
            gaps.append("🔴 MCP Tools (crítico!)")
            gaps.append("🔴 Hooks System (crítico!)")

        if practical < 30:
            gaps.append("Implementação prática")
            gaps.append("Pipeline integration")

        return gaps

    def generate_next_steps(self, score: int, level: str) -> List[str]:
        """Gera próximos passos baseados no resultado"""
        steps = []

        if level == "EXPERT":
            steps.append("Oferta imediata")
            steps.append("Designar para projetos críticos")
        elif level == "SENIOR":
            steps.append("Segunda entrevista com arquiteto")
            steps.append("Teste de 1 semana pago")
        elif level == "PLENO":
            steps.append("Bootcamp intensivo de 2 semanas")
            steps.append("Pair programming com senior")
        elif level in ["JUNIOR", "TRAINEE"]:
            steps.append("Encaminhar para bootcamp completo")
            steps.append("Reavaliar em 4 semanas")

        return steps

    # ================== EXECUÇÃO DA ENTREVISTA ==================
    async def run_interview(self, mock_responses: Optional[Dict] = None) -> Dict:
        """Executa entrevista completa"""
        print("\n" + "="*60)
        print("🎯 ENTREVISTA TÉCNICA - CLAUDE CODE SDK")
        print("="*60)
        print(f"Candidato: {self.candidate}")
        print(f"Entrevistador: {self.interviewer}")
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*60)

        # Parte 1: Screening
        print("\n📝 PARTE 1: SCREENING (20 pontos)")
        screening_score = 0
        for q in self.screening_questions():
            print(f"\n{q['question']}")
            if mock_responses:
                response = mock_responses.get(q['id'], "")
                keywords_found = sum(1 for kw in q['expected_keywords'] if kw in response.lower())
                points = (keywords_found / len(q['expected_keywords'])) * q['points']
                screening_score += points
                print(f"→ Pontos: {points:.1f}/{q['points']}")

        # Parte 2: Conceitos Avançados
        print("\n🔬 PARTE 2: CONCEITOS AVANÇADOS (30 pontos)")
        advanced_score = 0
        for q in self.advanced_concepts():
            print(f"\n{q['question']}")
            if q.get('critical'):
                print("⚠️ QUESTÃO CRÍTICA!")
            if mock_responses:
                response = mock_responses.get(q['id'], "")
                keywords_found = sum(1 for kw in q['expected_keywords'] if kw in response.lower())
                points = (keywords_found / len(q['expected_keywords'])) * q['points']
                advanced_score += points
                print(f"→ Pontos: {points:.1f}/{q['points']}")

        # Parte 3: Desafio Prático
        print("\n💻 PARTE 3: DESAFIO PRÁTICO (50 pontos)")
        challenge = self.practical_challenge()
        print(f"Título: {challenge['title']}")
        print(f"Tempo limite: {challenge['time_limit']//60} minutos")
        print("\nRequisitos:")
        for req in challenge['requirements']:
            print(f"  {req}")

        practical_score = 0
        if mock_responses and 'code_submission' in mock_responses:
            result = self.evaluate_code_submission(mock_responses['code_submission'])
            practical_score = result['score']
            print("\n📊 Avaliação do código:")
            for feedback in result['feedback']:
                print(f"  {feedback}")

        # Score Final
        final = self.calculate_final_score(screening_score, advanced_score, practical_score)

        print("\n" + "="*60)
        print("📊 RESULTADO FINAL")
        print("="*60)
        print(f"Score Total: {final['total_score']:.1f}/100")
        print(f"Nível: {final['level']}")
        print(f"Recomendação: {final['recommendation']}")
        print(f"Faixa Salarial: {final['salary_range']}")
        print(f"\n🔴 Gaps Identificados:")
        for gap in final['gaps']:
            print(f"  - {gap}")
        print(f"\n📋 Próximos Passos:")
        for step in final['next_steps']:
            print(f"  → {step}")
        print("="*60)

        # Salvar resultado
        self.save_to_neo4j(final)

        return final

    def save_to_neo4j(self, result: Dict):
        """Salva resultado da entrevista no Neo4j"""
        query = f"""
        CREATE (i:Interview {{
            candidate: '{result['candidate']}',
            score: {result['total_score']},
            level: '{result['level']}',
            timestamp: datetime(),
            recommendation: '{result['recommendation']}'
        }})
        """
        print(f"\n💾 Salvando no Neo4j: Interview node criado")

# ================== TESTE DO SISTEMA ==================
if __name__ == "__main__":
    # Simular entrevista com Diego Fornalha
    interview = ClaudeSDKTechnicalInterview("Diego Fornalha")

    # Respostas simuladas
    mock_responses = {
        # Screening
        "q1": "Claude Code SDK usa claude login sem api key, autenticação local",
        "q2": "É async para não bloquear, uso com async for e asyncio.run",
        "q3": "temperature para criatividade, allowed_tools para ferramentas, system_prompt",
        "q4": "Read, Write, Edit, Bash, Grep e WebSearch",

        # Avançados
        "a1": "Uso @tool decorator com create_sdk_mcp_server e retorno content",
        "a2": "HookMatcher com PreToolUse, return None permite, behavior deny bloqueia",
        "a3": "Dict com content contendo type text",
        "a4": "async with ClaudeSDKClient, receive_response para streaming",

        # Código submetido (parcial)
        "code_submission": """
import asyncio
from claude_code_sdk import query, ClaudeCodeOptions, tool, create_sdk_mcp_server, HookMatcher

async def analisar_codigo(arquivo: str):
    options = ClaudeCodeOptions(
        temperature=0.2,
        allowed_tools=["Read"]
    )
    async for msg in query(f"Analise o arquivo {arquivo}", options=options):
        return msg

@tool(
    name="line_counter",
    description="Conta linhas",
    input_schema={"file": str}
)
async def contar_linhas_tool(args: dict) -> dict:
    lines = len(open(args["file"]).readlines())
    return {"content": [{"type": "text", "text": f"Total: {lines}"}]}

async def validar_seguranca(data: dict, tool_id: str, ctx: dict) -> dict:
    if "rm -rf" in str(data):
        return {"behavior": "deny", "message": "Bloqueado"}
    return None

async def pipeline_analise():
    # Pipeline parcial
    pass
        """
    }

    # Executar entrevista
    asyncio.run(interview.run_interview(mock_responses))