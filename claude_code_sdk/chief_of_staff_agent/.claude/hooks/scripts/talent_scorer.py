#!/usr/bin/env python3
"""
Ferramenta Pontuadora de Talentos - Avalia e classifica candidatos baseado em múltiplos critérios
Ferramenta Python customizada para o subagente Recrutador
"""

import argparse
import json


def score_candidate(candidate: dict) -> dict:
    """Pontua um candidato baseado em critérios ponderados"""

    weights = {
        "technical_skills": 0.30,
        "experience_years": 0.20,
        "startup_experience": 0.15,
        "education": 0.10,
        "culture_fit": 0.15,
        "salary_fit": 0.10,
    }

    scores = {}

    # Habilidades técnicas (0-100)
    tech_match = candidate.get("tech_skills_match", 70)
    scores["technical_skills"] = min(100, tech_match)

    # Experiência (0-100, pico aos 8 anos)
    years = candidate.get("years_experience", 5)
    if years <= 2:
        scores["experience_years"] = 40
    elif years <= 5:
        scores["experience_years"] = 70
    elif years <= 8:
        scores["experience_years"] = 90
    else:
        scores["experience_years"] = 85  # Leve declínio para superqualificados

    # Experiência em startup (0-100)
    scores["startup_experience"] = 100 if candidate.get("has_startup_exp", False) else 50

    # Educação (0-100)
    education = candidate.get("education", "bachelors")
    edu_scores = {"high_school": 40, "bachelors": 70, "masters": 85, "phd": 90}
    scores["education"] = edu_scores.get(education, 70)

    # Ajuste cultural (0-100)
    scores["culture_fit"] = candidate.get("culture_score", 75)

    # Ajuste salarial (0-100, penaliza se muito alto ou baixo)
    salary = candidate.get("salary_expectation", 150000)
    target = candidate.get("target_salary", 160000)
    diff_pct = abs(salary - target) / target
    scores["salary_fit"] = max(0, 100 - (diff_pct * 200))

    # Calcula total ponderado
    total = sum(scores[k] * weights[k] for k in weights)

    return {
        "name": candidate.get("name", "Unknown"),
        "total_score": round(total, 1),
        "scores": scores,
        "recommendation": get_recommendation(total),
        "risk_factors": identify_risks(candidate, scores),
    }


def get_recommendation(score: float) -> str:
    """Gera recomendação de contratação baseada na pontuação"""
    if score >= 85:
        return "CONTRATAÇÃO FORTE - Estender oferta imediatamente"
    elif score >= 75:
        return "CONTRATAR - Bom candidato, proceder com oferta"
    elif score >= 65:
        return "TALVEZ - Considerar se não houver melhores opções"
    elif score >= 50:
        return "FRACO - Preocupações significativas, provavelmente dispensar"
    else:
        return "NÃO CONTRATAR - Não atende aos requisitos"


def identify_risks(candidate: dict, scores: dict) -> list[str]:
    """Identifica fatores de risco potenciais"""
    risks = []

    if scores["technical_skills"] < 60:
        risks.append("Habilidades técnicas abaixo dos requisitos")

    if candidate.get("years_experience", 0) < 2:
        risks.append("Experiência limitada, precisará de mentoria")

    if not candidate.get("has_startup_exp", False):
        risks.append("Sem experiência em startup, pode ter dificuldades com ambiguidade")

    if scores["salary_fit"] < 50:
        risks.append("Expectativas salariais desalinhadas")

    if candidate.get("notice_period_days", 14) > 30:
        risks.append(f"Período de aviso longo: {candidate.get('notice_period_days')} dias")

    return risks


def rank_candidates(candidates: list[dict]) -> list[dict]:
    """Classifica múltiplos candidatos"""
    scored = [score_candidate(c) for c in candidates]
    return sorted(scored, key=lambda x: x["total_score"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Ferramenta de pontuação de candidatos")
    parser.add_argument("--input", type=str, help="Arquivo JSON com dados do candidato")
    parser.add_argument("--name", type=str, help="Nome do candidato")
    parser.add_argument("--years", type=int, default=5, help="Anos de experiência")
    parser.add_argument("--tech-match", type=int, default=70, help="Correspondência de habilidades técnicas (0-100)")
    parser.add_argument("--salary", type=int, default=150000, help="Expectativa salarial")
    parser.add_argument("--startup", action="store_true", help="Tem experiência em startup")
    parser.add_argument("--format", choices=["json", "text"], default="text")

    args = parser.parse_args()

    if args.input:
        # Pontua múltiplos candidatos do arquivo
        with open(args.input) as f:
            candidates = json.load(f)
        results = rank_candidates(candidates)
    else:
        # Pontua candidato único dos argumentos
        candidate = {
            "name": args.name or "Candidate",
            "years_experience": args.years,
            "tech_skills_match": args.tech_match,
            "salary_expectation": args.salary,
            "has_startup_exp": args.startup,
            "target_salary": 160000,
            "culture_score": 75,
            "education": "bachelors",
        }
        results = [score_candidate(candidate)]

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        # Saída de texto
        print("🎯 AVALIAÇÃO DE CANDIDATO")
        print("=" * 50)

        for i, result in enumerate(results, 1):
            print(f"\n#{i}. {result['name']}")
            print("-" * 30)
            print(f"Pontuação Geral: {result['total_score']}/100")
            print(f"Recomendação: {result['recommendation']}")

            print("\nPontuações por Categoria:")
            for category, score in result["scores"].items():
                print(f"  {category.replace('_', ' ').title()}: {score:.0f}/100")

            if result["risk_factors"]:
                print("\n⚠️  Fatores de Risco:")
                for risk in result["risk_factors"]:
                    print(f"  - {risk}")

        if len(results) > 1:
            print("\n" + "=" * 50)
            print("RESUMO DO RANKING:")
            for i, r in enumerate(results[:3], 1):
                print(
                    f"{i}. {r['name']}: {r['total_score']:.1f} - {r['recommendation'].split(' - ')[0]}"
                )


if __name__ == "__main__":
    main()
