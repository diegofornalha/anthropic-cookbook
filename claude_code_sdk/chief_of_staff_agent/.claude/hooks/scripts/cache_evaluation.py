#!/usr/bin/env python3
"""
Avaliador de código Python - Cache Distribuído
Análise técnica detalhada para avaliação de candidatos
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class Nivel(Enum):
    JUNIOR = "Junior"
    MID = "Mid-level"
    SENIOR = "Senior"
    EXPERT = "Expert"

@dataclass
class AvaliacaoItem:
    criterio: str
    pontos: int
    pontos_max: int
    observacoes: List[str]
    sugestoes: List[str]

@dataclass
class AvaliacaoFinal:
    nota_total: int
    nivel: Nivel
    pontos_fortes: List[str]
    melhorias: List[str]
    avaliacoes: List[AvaliacaoItem]

def avaliar_cache_distribuido() -> AvaliacaoFinal:
    """Avalia o código do cache distribuído fornecido pelo candidato."""

    # 1. Qualidade do código Python (idiomático, PEP 8) - 20 pontos
    codigo_qualidade = AvaliacaoItem(
        criterio="Qualidade do Código Python",
        pontos=16,
        pontos_max=20,
        observacoes=[
            "✅ Type hints corretos e consistentes",
            "✅ Nomes de variáveis descritivos",
            "✅ Uso adequado de dataclasses implícitas (tuple)",
            "⚠️ Algumas linhas poderiam ser mais concisas",
            "⚠️ Docstrings ausentes nas classes e métodos"
        ],
        sugestoes=[
            "Adicionar docstrings para documentação",
            "Considerar use de dataclasses para cache entries",
            "Implementar __repr__ e __str__ para debugging"
        ]
    )

    # 2. Funcionalidades avançadas Python - 20 pontos
    funcionalidades_avancadas = AvaliacaoItem(
        criterio="Funcionalidades Avançadas",
        pontos=17,
        pontos_max=20,
        observacoes=[
            "✅ Decorators bem implementados com functools.wraps",
            "✅ Context managers implícitos com 'with' statement",
            "✅ Uso correto de *args, **kwargs",
            "✅ Compreensão de closures nos decorators",
            "⚠️ Falta implementação de __enter__/__exit__ personalizada",
            "⚠️ Poderia usar property decorators para métricas"
        ],
        sugestoes=[
            "Implementar context manager personalizado",
            "Usar property para expor métricas do cache",
            "Considerar metaclasses para configuração avançada"
        ]
    )

    # 3. Thread safety e async implementation - 25 pontos
    concorrencia = AvaliacaoItem(
        criterio="Thread Safety e Async",
        pontos=18,
        pontos_max=25,
        observacoes=[
            "✅ Uso correto de threading.Lock",
            "✅ Async methods com asyncio.to_thread",
            "⚠️ Lock muito granular - pode causar bottlenecks",
            "❌ Race condition no LRU eviction",
            "❌ Não é verdadeiramente 'distribuído'",
            "⚠️ asyncio.to_thread pode não ser eficiente"
        ],
        sugestoes=[
            "Implementar RWLock para melhor performance",
            "Usar asyncio.Lock para versões async nativas",
            "Corrigir race condition no min() do LRU",
            "Considerar threading.RLock para reentrância",
            "Implementar pool de connections para distribuição real"
        ]
    )

    # 4. Type hints - 10 pontos
    type_hints = AvaliacaoItem(
        criterio="Type Hints",
        pontos=9,
        pontos_max=10,
        observacoes=[
            "✅ Imports corretos do typing",
            "✅ Generics bem utilizados",
            "✅ Optional usado apropriadamente",
            "⚠️ Poderia usar TypeVar para maior flexibilidade"
        ],
        sugestoes=[
            "Usar TypeVar para cache genérico",
            "Adicionar Protocol para interface",
            "Considerar Literal types para constantes"
        ]
    )

    # 5. Design dos decorators - 15 pontos
    decorators = AvaliacaoItem(
        criterio="Design dos Decorators",
        pontos=13,
        pontos_max=15,
        observacoes=[
            "✅ Estrutura correta com factory pattern",
            "✅ Preservação de metadata com wraps",
            "✅ Parametrização adequada",
            "⚠️ Cache instance não é reutilizada entre decoradores",
            "⚠️ Key generation pode colidir para objetos complexos"
        ],
        sugestoes=[
            "Implementar cache singleton ou registry",
            "Melhorar algoritmo de key generation",
            "Adicionar suporte para exclusão de parâmetros"
        ]
    )

    # 6. Arquitetura e padrões - 10 pontos
    arquitetura = AvaliacaoItem(
        criterio="Arquitetura e Padrões",
        pontos=7,
        pontos_max=10,
        observacoes=[
            "✅ Separação clara de responsabilidades",
            "⚠️ Nome 'DistributedCache' enganoso",
            "⚠️ Falta interface/protocol definition",
            "❌ Não implementa padrões de cache distribuído real"
        ],
        sugestoes=[
            "Renomear para InMemoryCache ou LocalCache",
            "Implementar interface CacheProtocol",
            "Adicionar estratégias de eviction plugáveis",
            "Implementar observability (metrics, logging)"
        ]
    )

    avaliacoes = [
        codigo_qualidade,
        funcionalidades_avancadas,
        concorrencia,
        type_hints,
        decorators,
        arquitetura
    ]

    nota_total = sum(av.pontos for av in avaliacoes)

    # Determinar nível baseado na nota
    if nota_total >= 85:
        nivel = Nivel.EXPERT
    elif nota_total >= 70:
        nivel = Nivel.SENIOR
    elif nota_total >= 55:
        nivel = Nivel.MID
    else:
        nivel = Nivel.JUNIOR

    pontos_fortes = [
        "Sólido conhecimento de threading e locks",
        "Boa implementação de decorators com factory pattern",
        "Type hints consistentes e corretos",
        "Compreensão de conceitos async/await",
        "Código limpo e legível",
        "Uso apropriado de functools.wraps"
    ]

    melhorias = [
        "Corrigir race condition no algoritmo LRU",
        "Implementar verdadeiro cache distribuído",
        "Adicionar documentação (docstrings)",
        "Melhorar estratégia de key generation",
        "Implementar observability e métricas",
        "Considerar uso de AsyncContextManager",
        "Adicionar tratamento de exceções específicas",
        "Implementar configuração de logging"
    ]

    return AvaliacaoFinal(
        nota_total=nota_total,
        nivel=nivel,
        pontos_fortes=pontos_fortes,
        melhorias=melhorias,
        avaliacoes=avaliacoes
    )

def imprimir_avaliacao(avaliacao: AvaliacaoFinal) -> None:
    """Imprime a avaliação formatada."""

    print("=" * 80)
    print("🎯 AVALIAÇÃO TÉCNICA - CACHE DISTRIBUÍDO")
    print("=" * 80)

    print(f"\n📊 RESULTADO FINAL")
    print(f"Nota: {avaliacao.nota_total}/100")
    print(f"Nível: {avaliacao.nivel.value}")

    print(f"\n📈 DETALHAMENTO POR CRITÉRIO")
    for av in avaliacao.avaliacoes:
        print(f"\n{av.criterio}: {av.pontos}/{av.pontos_max}")
        for obs in av.observacoes:
            print(f"  {obs}")

    print(f"\n✅ PONTOS FORTES")
    for pf in avaliacao.pontos_fortes:
        print(f"  • {pf}")

    print(f"\n🔧 MELHORIAS RECOMENDADAS")
    for mel in avaliacao.melhorias:
        print(f"  • {mel}")

    print(f"\n💭 ANÁLISE DETALHADA")
    print("O candidato demonstra sólido conhecimento de Python e conceitos")
    print("de programação concorrente. O código é limpo e bem estruturado,")
    print("mas há algumas questões importantes de thread safety e o nome")
    print("'distribuído' é enganoso para um cache local.")

    print(f"\n🎓 RECOMENDAÇÃO")
    if avaliacao.nivel == Nivel.EXPERT:
        print("Candidato excepcional - recomendo contratação imediata")
    elif avaliacao.nivel == Nivel.SENIOR:
        print("Candidato muito bom - adequado para posições sênior")
    elif avaliacao.nivel == Nivel.MID:
        print("Candidato promissor - adequado para posições mid-level")
    else:
        print("Candidato precisaria de mentoria para posições mais sênior")

if __name__ == "__main__":
    avaliacao = avaliar_cache_distribuido()
    imprimir_avaliacao(avaliacao)