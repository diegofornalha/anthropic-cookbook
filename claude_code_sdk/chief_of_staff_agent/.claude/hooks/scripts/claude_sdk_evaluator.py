#!/usr/bin/env python3
"""
Claude Code SDK Evaluator - Avaliação específica de conhecimento do SDK
Score de 0-100 baseado em domínio real do Claude Code SDK
Criado para o bootcamp de Diego Fornalha
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime

class ClaudeSDKEvaluator:
    """Avaliador específico para Claude Code SDK"""

    def __init__(self, candidate_name: str):
        self.candidate = candidate_name
        self.score = 0
        self.gaps = []
        self.strengths = []

    def evaluate_fundamentals(self, answers: Dict) -> int:
        """Avalia conhecimento dos fundamentos do SDK (0-20 pontos)"""
        score = 0
        questions = {
            "query_async": "Sabe que query() é assíncrona?",
            "no_api_key": "Entende que não usa API key?",
            "claude_login": "Sabe usar claude login?",
            "import_correct": "Importa corretamente do SDK?"
        }

        for key, question in questions.items():
            if answers.get(key, False):
                score += 5
                self.strengths.append(question)
            else:
                self.gaps.append(f"Gap: {question}")

        return score

    def evaluate_query_function(self, code_sample: str) -> int:
        """Avalia uso correto de query() (0-15 pontos)"""
        score = 0
        checks = [
            ("async for" in code_sample, "Usa async for", 5),
            ("query(" in code_sample, "Chama query()", 5),
            ("import claude_code_sdk" in code_sample or "from claude_code_sdk" in code_sample, "Import correto", 5)
        ]

        for check, desc, points in checks:
            if check:
                score += points
                self.strengths.append(f"✓ {desc}")
            else:
                self.gaps.append(f"✗ Não {desc}")

        return score

    def evaluate_options(self, options_code: str) -> int:
        """Avalia uso de ClaudeCodeOptions (0-15 pontos)"""
        score = 0
        features = [
            ("ClaudeCodeOptions", "Usa ClaudeCodeOptions", 3),
            ("temperature", "Configura temperature", 3),
            ("allowed_tools", "Define ferramentas", 3),
            ("system_prompt", "Customiza prompt", 3),
            ("max_turns", "Controla turnos", 3)
        ]

        for feature, desc, points in features:
            if feature in options_code:
                score += points
                self.strengths.append(f"✓ {desc}")
            else:
                self.gaps.append(f"✗ Não {desc}")

        return score

    def evaluate_mcp_tools(self, mcp_code: str) -> int:
        """Avalia conhecimento de MCP Tools (0-20 pontos) - GAP CRÍTICO!"""
        score = 0
        critical_features = [
            ("@tool", "Usa @tool decorator", 5),
            ("create_sdk_mcp_server", "Cria servidor MCP", 5),
            ('"content":', "Retorna formato correto", 5),
            ("mcp_servers=", "Configura em options", 5)
        ]

        has_mcp = False
        for feature, desc, points in critical_features:
            if feature in mcp_code:
                score += points
                self.strengths.append(f"✓ MCP: {desc}")
                has_mcp = True
            else:
                self.gaps.append(f"🔴 MCP Gap: {desc}")

        if not has_mcp:
            self.gaps.append("🔴 GAP CRÍTICO: Não domina MCP Tools!")

        return score

    def evaluate_hooks(self, hooks_code: str) -> int:
        """Avalia conhecimento de Hooks (0-20 pontos) - GAP CRÍTICO!"""
        score = 0
        critical_features = [
            ("HookMatcher", "Usa HookMatcher", 5),
            ("PreToolUse", "Hook pré-execução", 5),
            ("PostToolUse", "Hook pós-execução", 5),
            ("return None", "Retorno correto", 5)
        ]

        has_hooks = False
        for feature, desc, points in critical_features:
            if feature in hooks_code:
                score += points
                self.strengths.append(f"✓ Hooks: {desc}")
                has_hooks = True
            else:
                self.gaps.append(f"🔴 Hooks Gap: {desc}")

        if not has_hooks:
            self.gaps.append("🔴 GAP CRÍTICO: Não domina Hooks System!")

        return score

    def evaluate_practical_exercises(self, exercises_completed: List[int]) -> int:
        """Avalia exercícios práticos completados (0-10 pontos)"""
        exercise_values = {
            1: 1,  # Query básica
            2: 1,  # Options
            3: 1,  # Pipeline
            4: 3,  # MCP Tools (crítico!)
            5: 3,  # Hooks (crítico!)
            6: 1,  # Streaming
            7: 0   # Multi-agente (bônus)
        }

        score = sum(exercise_values.get(ex, 0) for ex in exercises_completed)

        if 4 not in exercises_completed:
            self.gaps.append("⚠️ Não completou exercício 4 (MCP Tools)")
        if 5 not in exercises_completed:
            self.gaps.append("⚠️ Não completou exercício 5 (Hooks)")

        return score

    def run_full_evaluation(self, test_data: Dict) -> Dict:
        """Executa avaliação completa"""

        # Calcular scores parciais
        scores = {
            "fundamentals": self.evaluate_fundamentals(test_data.get("fundamentals", {})),
            "query": self.evaluate_query_function(test_data.get("query_code", "")),
            "options": self.evaluate_options(test_data.get("options_code", "")),
            "mcp_tools": self.evaluate_mcp_tools(test_data.get("mcp_code", "")),
            "hooks": self.evaluate_hooks(test_data.get("hooks_code", "")),
            "exercises": self.evaluate_practical_exercises(test_data.get("exercises_done", []))
        }

        # Score total
        self.score = sum(scores.values())

        # Classificação
        if self.score >= 90:
            level = "EXPERT"
            recommendation = "Pronto para contribuir com o SDK!"
        elif self.score >= 75:
            level = "AVANÇADO"
            recommendation = "Focar em MCP Tools e Hooks"
        elif self.score >= 60:
            level = "INTERMEDIÁRIO"
            recommendation = "Completar exercícios 4 e 5"
        elif self.score >= 45:
            level = "INICIANTE"
            recommendation = "Começar com 01_hello_claude.py"
        else:
            level = "BÁSICO"
            recommendation = "Iniciar bootcamp do zero"

        return {
            "candidate": self.candidate,
            "total_score": self.score,
            "level": level,
            "breakdown": scores,
            "strengths": self.strengths[:5],  # Top 5
            "critical_gaps": [g for g in self.gaps if "🔴" in g],
            "all_gaps": self.gaps,
            "recommendation": recommendation,
            "next_steps": self.generate_next_steps(),
            "estimated_weeks_to_95": self.estimate_time_to_expert(),
            "timestamp": datetime.now().isoformat()
        }

    def generate_next_steps(self) -> List[str]:
        """Gera próximos passos baseados nos gaps"""
        steps = []

        if self.score < 45:
            steps.append("python examples/01_hello_claude.py")
            steps.append("python examples/exercicios_praticos_pt_br.py 1")

        if any("MCP" in g for g in self.gaps):
            steps.append("🔴 FOCO CRÍTICO: exercicios_praticos_pt_br.py 4")
            steps.append("Dedicar 3 semanas para MCP Tools")

        if any("Hooks" in g for g in self.gaps):
            steps.append("🔴 FOCO CRÍTICO: exercicios_praticos_pt_br.py 5")
            steps.append("Dedicar 3 semanas para Hooks System")

        if self.score >= 75:
            steps.append("Contribuir com PR no repositório")

        return steps

    def estimate_time_to_expert(self) -> int:
        """Estima semanas para chegar a score 95"""
        if self.score >= 90:
            return 1
        elif self.score >= 75:
            return 3
        elif self.score >= 60:
            return 6
        elif self.score >= 45:
            return 12
        else:
            return 16

# Função principal para teste
def test_candidate(name: str, sample_data: Dict) -> Dict:
    """Testa um candidato com dados de amostra"""
    evaluator = ClaudeSDKEvaluator(name)
    return evaluator.run_full_evaluation(sample_data)

if __name__ == "__main__":
    # Teste com Diego Fornalha
    diego_data = {
        "fundamentals": {
            "query_async": True,
            "no_api_key": True,
            "claude_login": True,
            "import_correct": True
        },
        "query_code": """
import asyncio
from claude_code_sdk import query

async def main():
    async for msg in query("Olá Claude!"):
        print(msg)
        """,
        "options_code": """
from claude_code_sdk import ClaudeCodeOptions

options = ClaudeCodeOptions(
    temperature=0.7,
    allowed_tools=["Read", "Write"]
)
        """,
        "mcp_code": "",  # Gap crítico!
        "hooks_code": "",  # Gap crítico!
        "exercises_done": [1, 2]  # Apenas básicos
    }

    result = test_candidate("Diego Fornalha", diego_data)

    print("\n" + "="*60)
    print("🎯 AVALIAÇÃO CLAUDE CODE SDK")
    print("="*60)
    print(f"Candidato: {result['candidate']}")
    print(f"Score Total: {result['total_score']}/100")
    print(f"Nível: {result['level']}")
    print(f"\n📊 Breakdown:")
    for area, score in result['breakdown'].items():
        print(f"  {area}: {score}")
    print(f"\n✅ Pontos Fortes:")
    for strength in result['strengths']:
        print(f"  {strength}")
    print(f"\n🔴 Gaps Críticos:")
    for gap in result['critical_gaps']:
        print(f"  {gap}")
    print(f"\n📋 Próximos Passos:")
    for step in result['next_steps']:
        print(f"  → {step}")
    print(f"\n⏱️ Tempo estimado para expert: {result['estimated_weeks_to_95']} semanas")
    print("="*60)