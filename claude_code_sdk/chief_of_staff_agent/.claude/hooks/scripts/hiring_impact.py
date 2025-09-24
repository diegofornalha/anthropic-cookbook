#!/usr/bin/env python3
"""
Calculadora de Impacto de Contratação para Diego Fornalha
Calcula o impacto financeiro da contratação de engenheiros
"""

import json
import sys


def calculate_hiring_impact(num_engineers, salary_per_engineer=200000):
    """
    Calcula o impacto financeiro da contratação de engenheiros.

    Args:
        num_engineers: Número de engenheiros para contratar
        salary_per_engineer: Salário anual por engenheiro (padrão: $200K)

    Returns:
        Dicionário com métricas de impacto financeiro
    """
    # Financeiro atual (do CLAUDE.md)
    CURRENT_BURN_MONTHLY = 500000  # $500K/month
    CURRENT_RUNWAY_MONTHS = 20  # 20 months
    CASH_IN_BANK = 10000000  # $10M

    # Calcula custo total (salário + benefícios + impostos = salário * 1.3)
    annual_loaded_cost_per_engineer = salary_per_engineer * 1.3
    monthly_cost_per_engineer = annual_loaded_cost_per_engineer / 12

    # Aumento total de custo mensal
    total_monthly_increase = monthly_cost_per_engineer * num_engineers

    # Nova taxa de burn
    new_burn_monthly = CURRENT_BURN_MONTHLY + total_monthly_increase

    # Novo runway
    new_runway_months = CASH_IN_BANK / new_burn_monthly
    runway_reduction_months = CURRENT_RUNWAY_MONTHS - new_runway_months

    # Calcula impacto potencial na receita (suposição: engenheiros aumentam velocidade em 15%)
    velocity_increase = 0.15 * num_engineers / 5  # Assumindo 5 engenheiros = 15% de aumento

    # Recomendação
    if runway_reduction_months > 3:
        recommendation = "ALTO RISCO: Redução significativa do runway. Considerar contratação em fases."
    elif runway_reduction_months > 1.5:
        recommendation = "RISCO MODERADO: Gerenciável se o crescimento da receita acelerar."
    else:
        recommendation = "BAIXO RISCO: Impacto mínimo no runway. Prosseguir se talento estiver disponível."

    return {
        "num_engineers": num_engineers,
        "salary_per_engineer": salary_per_engineer,
        "monthly_cost_per_engineer": round(monthly_cost_per_engineer, 2),
        "total_monthly_increase": round(total_monthly_increase, 2),
        "current_burn_monthly": CURRENT_BURN_MONTHLY,
        "new_burn_monthly": round(new_burn_monthly, 2),
        "current_runway_months": CURRENT_RUNWAY_MONTHS,
        "new_runway_months": round(new_runway_months, 2),
        "runway_reduction_months": round(runway_reduction_months, 2),
        "velocity_increase_percent": round(velocity_increase * 100, 1),
        "recommendation": recommendation,
    }


def main():
    # Analisa argumentos da linha de comando
    if len(sys.argv) < 2:
        print("Uso: python hiring_impact.py <num_engenheiros> [salario_por_engenheiro]")
        sys.exit(1)

    num_engineers = int(sys.argv[1])
    salary = int(sys.argv[2]) if len(sys.argv) > 2 else 200000

    # Calcula impacto
    impact = calculate_hiring_impact(num_engineers, salary)

    # Saída em JSON para fácil análise
    print(json.dumps(impact, indent=2))

    # Também imprime resumo
    print("\n=== RESUMO DO IMPACTO DE CONTRATAÇÃO ===")
    print(f"Contratando {impact['num_engineers']} engenheiros a ${impact['salary_per_engineer']:,}/ano")
    print(f"Aumento do burn mensal: ${impact['total_monthly_increase']:,.0f}")
    print(f"Nova taxa de burn: ${impact['new_burn_monthly']:,.0f}/mês")
    print(
        f"Mudança no runway: {impact['current_runway_months']:.1f} → {impact['new_runway_months']:.1f} meses"
    )
    print(f"Aumento de velocidade: +{impact['velocity_increase_percent']}%")
    print(f"\n{impact['recommendation']}")


if __name__ == "__main__":
    main()
