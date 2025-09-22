#!/usr/bin/env python3
"""
AI Expertise Evaluator - Avalia expertise técnica em desenvolvimento de agentes de IA
Ferramenta customizada para o CTO avaliar candidatos técnicos
"""

import argparse
import json
import sys


def evaluate_ai_expertise(candidate: dict) -> dict:
    """Avalia expertise de candidato em desenvolvimento de agentes de IA"""

    # Pesos para diferentes áreas técnicas
    weights = {
        "llm_experience": 0.25,      # Experiência com LLMs
        "agent_frameworks": 0.20,     # Frameworks de agentes
        "system_design": 0.15,        # Design de sistemas
        "code_quality": 0.15,         # Qualidade de código
        "ml_fundamentals": 0.10,      # Fundamentos de ML
        "production_exp": 0.10,       # Experiência em produção
        "innovation": 0.05,           # Potencial de inovação
    }

    scores = {}

    # Experiência com LLMs (0-100)
    llm_apis = candidate.get("llm_apis", [])
    llm_score = 0
    if "openai" in llm_apis: llm_score += 30
    if "anthropic" in llm_apis: llm_score += 35
    if "google" in llm_apis: llm_score += 20
    if len(llm_apis) > 3: llm_score += 15
    scores["llm_experience"] = min(100, llm_score)

    # Frameworks de agentes (0-100)
    frameworks = candidate.get("agent_frameworks", [])
    framework_score = 0
    if "langchain" in frameworks: framework_score += 35
    if "autogen" in frameworks: framework_score += 25
    if "crewai" in frameworks: framework_score += 20
    if "claude_sdk" in frameworks: framework_score += 30
    scores["agent_frameworks"] = min(100, framework_score)

    # Design de sistemas (0-100)
    has_distributed = candidate.get("distributed_systems", False)
    has_microservices = candidate.get("microservices", False)
    has_scalability = candidate.get("scalability_exp", False)
    scores["system_design"] = (
        (40 if has_distributed else 0) +
        (30 if has_microservices else 0) +
        (30 if has_scalability else 0)
    )

    # Qualidade de código (0-100)
    github_stars = candidate.get("github_stars", 0)
    test_coverage = candidate.get("test_coverage", 0)
    scores["code_quality"] = min(100, (
        min(50, github_stars / 2) +  # Max 50 pontos por stars
        (test_coverage / 2)           # Max 50 pontos por cobertura
    ))

    # Fundamentos de ML (0-100)
    ml_knowledge = candidate.get("ml_knowledge", 50)
    has_fine_tuning = candidate.get("fine_tuning_exp", False)
    has_embeddings = candidate.get("embeddings_exp", False)
    scores["ml_fundamentals"] = min(100,
        ml_knowledge +
        (25 if has_fine_tuning else 0) +
        (25 if has_embeddings else 0)
    )

    # Experiência em produção (0-100)
    prod_ai_systems = candidate.get("production_ai_systems", 0)
    scores["production_exp"] = min(100, prod_ai_systems * 25)

    # Potencial de inovação (0-100)
    has_research = candidate.get("ai_research", False)
    has_patents = candidate.get("patents", 0) > 0
    has_contributions = candidate.get("open_source_ai", False)
    scores["innovation"] = (
        (35 if has_research else 0) +
        (35 if has_patents else 0) +
        (30 if has_contributions else 0)
    )

    # Calcular score total ponderado
    total_score = sum(scores[k] * weights[k] for k in scores)

    # Determinar nível
    if total_score >= 85:
        level = "Senior AI Engineer"
        recommendation = "Contratação Forte"
    elif total_score >= 70:
        level = "Mid-Level AI Engineer"
        recommendation = "Contratação Recomendada"
    elif total_score >= 55:
        level = "Junior AI Engineer"
        recommendation = "Considerar com Mentoria"
    else:
        level = "Entry Level"
        recommendation = "Não Recomendado"

    # Red flags específicos de IA
    red_flags = []
    if not llm_apis:
        red_flags.append("Sem experiência com APIs de LLM")
    if not frameworks:
        red_flags.append("Sem experiência com frameworks de agentes")
    if prod_ai_systems == 0:
        red_flags.append("Sem sistemas de IA em produção")
    if not candidate.get("prompt_engineering", False):
        red_flags.append("Sem experiência em engenharia de prompts")

    return {
        "candidate_name": candidate.get("name", "Unknown"),
        "total_score": round(total_score, 2),
        "level": level,
        "recommendation": recommendation,
        "detailed_scores": scores,
        "red_flags": red_flags,
        "strengths": [k for k, v in scores.items() if v >= 80],
        "areas_for_improvement": [k for k, v in scores.items() if v < 60]
    }


def main():
    parser = argparse.ArgumentParser(
        description="Avalia expertise técnica de candidatos em desenvolvimento de agentes de IA"
    )
    parser.add_argument("--candidate-json", type=str, help="JSON com dados do candidato")
    parser.add_argument("--file", type=str, help="Arquivo JSON com dados do candidato")

    args = parser.parse_args()

    # Carregar dados do candidato
    if args.file:
        with open(args.file, 'r') as f:
            candidate = json.load(f)
    elif args.candidate_json:
        candidate = json.loads(args.candidate_json)
    else:
        # Exemplo de candidato para teste
        candidate = {
            "name": "João Silva",
            "llm_apis": ["openai", "anthropic"],
            "agent_frameworks": ["langchain", "claude_sdk"],
            "distributed_systems": True,
            "microservices": True,
            "scalability_exp": False,
            "github_stars": 150,
            "test_coverage": 85,
            "ml_knowledge": 70,
            "fine_tuning_exp": True,
            "embeddings_exp": True,
            "production_ai_systems": 3,
            "ai_research": False,
            "patents": 0,
            "open_source_ai": True,
            "prompt_engineering": True
        }

    # Avaliar candidato
    result = evaluate_ai_expertise(candidate)

    # Output formatado
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())