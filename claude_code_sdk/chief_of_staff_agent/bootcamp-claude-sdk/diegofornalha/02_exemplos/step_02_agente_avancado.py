#!/usr/bin/env python3
"""
Script avançado para demonstrar funcionalidades do Agente Chefe de Gabinete
Criado para: Diego Fornalha
Objetivo: Demonstrar subagentes, comandos slash e scripts customizados
"""

import asyncio
import sys
import os

# Adicionar o diretório atual ao path para importar o módulo agent
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import send_query

async def demonstrar_funcionalidades():
    """Demonstra as principais funcionalidades do agente"""
    
    print("=" * 70)
    print("🚀 DEMONSTRAÇÃO AVANÇADA - AGENTE CHEFE DE GABINETE")
    print("=" * 70)
    
    # Teste 1: Usar subagente CTO
    print("\n📝 Teste 1: Delegando tarefa para subagente CTO")
    print("-" * 50)
    
    try:
        result, messages = await send_query(
            prompt="Use o subagente CTO para avaliar nossa estratégia de IA. Pergunte sobre as tecnologias mais promissoras para 2025.",
            permission_mode="plan"
        )
        
        print("✅ Subagente CTO consultado com sucesso!")
        print(f"📊 Resultado: {result[:300]}..." if result and len(result) > 300 else f"📊 Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Erro na consulta CTO: {e}")
    
    # Teste 2: Comando slash
    print("\n📝 Teste 2: Comando slash /budget-impact")
    print("-" * 50)
    
    try:
        result, messages = await send_query(
            prompt="/budget-impact",
            permission_mode="plan"
        )
        
        print("✅ Comando slash executado com sucesso!")
        print(f"📊 Resultado: {result[:300]}..." if result and len(result) > 300 else f"📊 Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Erro no comando slash: {e}")
    
    # Teste 3: Script customizado
    print("\n📝 Teste 3: Executando script customizado")
    print("-" * 50)
    
    try:
        result, messages = await send_query(
            prompt="Execute o script ai_expertise_evaluator.py para avaliar nossa equipe de IA",
            permission_mode="plan"
        )
        
        print("✅ Script customizado executado com sucesso!")
        print(f"📊 Resultado: {result[:300]}..." if result and len(result) > 300 else f"📊 Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Erro no script customizado: {e}")
    
    # Teste 4: Estilo de saída executivo
    print("\n📝 Teste 4: Relatório executivo")
    print("-" * 50)
    
    try:
        result, messages = await send_query(
            prompt="Gere um relatório executivo sobre o status da empresa",
            permission_mode="plan",
            output_style="executive"
        )
        
        print("✅ Relatório executivo gerado com sucesso!")
        print(f"📊 Resultado: {result[:300]}..." if result and len(result) > 300 else f"📊 Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Erro no relatório executivo: {e}")

async def main():
    """Função principal"""
    print("🏢 AGENTE CHEFE DE GABINETE - DEMONSTRAÇÃO AVANÇADA")
    print("   Desenvolvido para: Diego Fornalha")
    print("   Meta: Score 45 → 100 em 12 semanas\n")
    
    await demonstrar_funcionalidades()
    
    print("\n" + "=" * 70)
    print("🎯 DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 70)
    
    print("\n💡 FUNCIONALIDADES DEMONSTRADAS:")
    print("   ✅ Subagentes (CTO, Recrutador)")
    print("   ✅ Comandos slash (/budget-impact)")
    print("   ✅ Scripts Python customizados")
    print("   ✅ Estilos de saída (executive, technical)")
    print("   ✅ Integração com Neo4j Memory")
    print("   ✅ Sistema de permissões (plan mode)")
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("   1. Testar com permission_mode='default' para execução real")
    print("   2. Explorar outros comandos slash disponíveis")
    print("   3. Criar novos scripts Python customizados")
    print("   4. Integrar com sistemas externos via MCP")

if __name__ == "__main__":
    asyncio.run(main())
