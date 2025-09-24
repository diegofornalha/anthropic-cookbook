#!/usr/bin/env python3
"""
Bootcamp Tracker Hook - Sistema automatizado de tracking de progresso do bootcamp IA
Monitora evolução do candidato de score 45 para 95 em 12-16 semanas
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

def calculate_velocity(current_score: int, target_score: int, weeks_elapsed: int, total_weeks: int = 12) -> str:
    """Calcula se o candidato está no ritmo esperado"""
    expected_score = 45 + ((target_score - 45) * weeks_elapsed / total_weeks)

    if current_score >= expected_score + 5:
        return "AHEAD"
    elif current_score >= expected_score - 3:
        return "ON_TRACK"
    else:
        return "BEHIND"

def generate_weekly_metrics(candidate: str, week: int) -> Dict[str, Any]:
    """Gera métricas semanais do candidato"""

    # Simulação de dados para Diego Fornalha
    # Em produção, isso viria de APIs reais (GitHub, Slack, etc)

    if candidate == "Diego Fornalha":
        # Progressão realista baseada no perfil
        base_score = 45
        weekly_gain = 4.2  # Velocidade esperada

        current_score = min(base_score + (weekly_gain * week), 95)

        # Métricas por semana
        metrics_by_week = {
            1: {
                "conceitos": ["LLMs basics", "Tokens", "OpenAI API"],
                "projetos": ["Hello World GPT", "Text Classifier"],
                "horas_estudo": 35,
                "horas_mentoria": 5,
                "codigo_loc": 450,
                "bloqueios": ["Ambiente setup inicial"],
                "highlights": ["Rápida absorção de conceitos"],
                "score": 49
            },
            2: {
                "conceitos": ["Embeddings", "Prompt Engineering", "Few-shot"],
                "projetos": ["Prompt Template System"],
                "horas_estudo": 40,
                "horas_mentoria": 4,
                "codigo_loc": 680,
                "bloqueios": [],
                "highlights": ["Excelente em prompt engineering"],
                "score": 53
            },
            3: {
                "conceitos": ["RAG basics", "Vector DBs", "ChromaDB"],
                "projetos": ["Document QA System"],
                "horas_estudo": 42,
                "horas_mentoria": 6,
                "codigo_loc": 920,
                "bloqueios": ["Configuração vector DB"],
                "highlights": ["RAG funcionando com Solidity docs"],
                "score": 57
            },
            4: {
                "conceitos": ["Semantic Search", "Chunking", "Retrieval optimization"],
                "projetos": ["Smart Contract RAG"],
                "horas_estudo": 45,
                "horas_mentoria": 5,
                "codigo_loc": 1200,
                "bloqueios": [],
                "highlights": ["Projeto RAG para contratos aprovado!"],
                "score": 62
            },
            8: {
                "conceitos": ["LangChain", "Agents", "Tools", "Memory"],
                "projetos": ["Solidity Auditor Agent"],
                "horas_estudo": 48,
                "horas_mentoria": 8,
                "codigo_loc": 2800,
                "bloqueios": ["Complexidade de agents"],
                "highlights": ["Agente funcionando com 5 tools"],
                "score": 76
            },
            12: {
                "conceitos": ["Production deployment", "Monitoring", "Cost optimization"],
                "projetos": ["Web3 + AI Platform"],
                "horas_estudo": 50,
                "horas_mentoria": 4,
                "codigo_loc": 4500,
                "bloqueios": [],
                "highlights": ["Deploy em produção com sucesso!"],
                "score": 91
            }
        }

        # Retorna métricas da semana atual ou interpola
        if week in metrics_by_week:
            metrics = metrics_by_week[week]
        else:
            # Interpola para semanas não definidas
            metrics = {
                "conceitos": ["Estudando..."],
                "projetos": ["Em desenvolvimento"],
                "horas_estudo": 40 + week,
                "horas_mentoria": 5,
                "codigo_loc": 300 * week,
                "bloqueios": [],
                "highlights": ["Progresso contínuo"],
                "score": min(45 + (4.2 * week), 95)
            }

        metrics["velocity"] = calculate_velocity(
            metrics["score"],
            95,
            week
        )

        return metrics

    # Default para outros candidatos
    return {
        "conceitos": [],
        "projetos": [],
        "horas_estudo": 0,
        "horas_mentoria": 0,
        "codigo_loc": 0,
        "bloqueios": [],
        "highlights": [],
        "score": 45,
        "velocity": "NOT_MEASURED"
    }

def generate_recommendations(metrics: Dict[str, Any], week: int) -> List[str]:
    """Gera recomendações baseadas no progresso"""
    recommendations = []

    velocity = metrics.get("velocity", "ON_TRACK")
    score = metrics.get("score", 45)

    if velocity == "BEHIND":
        recommendations.append("⚠️ ATENÇÃO: Adicionar sessões extras de mentoria")
        recommendations.append("📚 Sugerir recursos simplificados para gaps identificados")
        recommendations.append("🎯 Considerar ajustar timeline ou reduzir escopo")

    elif velocity == "AHEAD":
        recommendations.append("🚀 Acelerar curriculum - candidato ahead of schedule")
        recommendations.append("💡 Adicionar projetos mais desafiadores")
        recommendations.append("🏆 Considerar promoção antecipada")

    # Recomendações por fase
    if week <= 4:
        if score < 60:
            recommendations.append("📖 Reforçar fundamentos de LLM")
    elif week <= 8:
        if score < 75:
            recommendations.append("🔧 Mais prática com frameworks")
    elif week <= 12:
        if score < 90:
            recommendations.append("🚢 Focar em production readiness")

    return recommendations

def format_progress_report(candidate: str, week: int, metrics: Dict[str, Any]) -> str:
    """Formata relatório de progresso semanal"""

    velocity_emoji = {
        "AHEAD": "🚀",
        "ON_TRACK": "✅",
        "BEHIND": "⚠️"
    }

    report = f"""
# 📊 Relatório de Progresso - Bootcamp IA
## Candidato: {candidate}
## Semana: {week}/12

### 📈 Score Evolution
- **Score Inicial**: 45/100
- **Score Atual**: {metrics['score']}/100
- **Meta**: 95/100
- **Velocity**: {velocity_emoji.get(metrics['velocity'], '❓')} {metrics['velocity']}

### 📚 Conceitos Aprendidos
{chr(10).join(f"- {c}" for c in metrics['conceitos'])}

### 💻 Projetos Completados
{chr(10).join(f"- {p}" for p in metrics['projetos'])}

### ⏱️ Métricas de Dedicação
- **Horas de Estudo**: {metrics['horas_estudo']}h
- **Horas de Mentoria**: {metrics['horas_mentoria']}h
- **Linhas de Código**: {metrics['codigo_loc']}

### 🚧 Bloqueios
{chr(10).join(f"- {b}" for b in metrics['bloqueios']) if metrics['bloqueios'] else "Nenhum bloqueio identificado"}

### ⭐ Highlights
{chr(10).join(f"- {h}" for h in metrics['highlights'])}

### 🎯 Recomendações
{chr(10).join(generate_recommendations(metrics, week))}

### 📅 Próximos Passos
"""

    # Adiciona próximos passos baseados na semana
    if week < 4:
        report += "- Continuar fundamentos de LLM e RAG\n"
        report += "- Preparar para avaliação de Fase 1\n"
    elif week < 8:
        report += "- Aprofundar em LangChain e Claude SDK\n"
        report += "- Iniciar projeto de agente complexo\n"
    elif week < 12:
        report += "- Focar em deployment e produção\n"
        report += "- Otimizar custos e performance\n"
    else:
        report += "- Escolher área de especialização\n"
        report += "- Preparar apresentação final\n"

    report += f"\n---\n*Gerado automaticamente por bootcamp-tracker.py*"

    return report

def save_to_neo4j_format(candidate: str, week: int, metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Formata dados para salvar no Neo4j"""
    return {
        "query": "CREATE (p:Progress {candidate: $candidate, week: $week, score: $score, velocity: $velocity, timestamp: $timestamp})",
        "params": {
            "candidate": candidate,
            "week": week,
            "score": metrics["score"],
            "velocity": metrics["velocity"],
            "timestamp": datetime.now().isoformat(),
            "conceitos": json.dumps(metrics["conceitos"]),
            "projetos": json.dumps(metrics["projetos"]),
            "horas_estudo": metrics["horas_estudo"],
            "horas_mentoria": metrics["horas_mentoria"],
            "codigo_loc": metrics["codigo_loc"]
        }
    }

def main():
    """Hook principal executado após ações relevantes"""

    # Detecta contexto do hook
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        action = "weekly_check"

    # Candidato padrão para o exemplo
    candidate = "Diego Fornalha"
    current_week = 4  # Simulando semana 4

    # Gera métricas
    metrics = generate_weekly_metrics(candidate, current_week)

    # Gera relatório
    report = format_progress_report(candidate, current_week, metrics)

    # Output para o usuário
    print(report)

    # Prepara dados para Neo4j (seria executado em produção)
    neo4j_data = save_to_neo4j_format(candidate, current_week, metrics)

    # Log para audit
    with open(".claude/logs/bootcamp-progress.jsonl", "a") as f:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "candidate": candidate,
            "week": current_week,
            "metrics": metrics,
            "neo4j_query": neo4j_data
        }
        f.write(json.dumps(log_entry) + "\n")

    # Notificações baseadas em velocity
    if metrics["velocity"] == "BEHIND":
        print("\n⚠️ ALERTA: Candidato está BEHIND - ação necessária!")
        print("Sugestão: Agendar sessão extra de mentoria esta semana")
    elif metrics["velocity"] == "AHEAD":
        print("\n🎉 EXCELENTE: Candidato está AHEAD of schedule!")
        print("Sugestão: Considerar acelerar o programa")

    return 0

if __name__ == "__main__":
    sys.exit(main())