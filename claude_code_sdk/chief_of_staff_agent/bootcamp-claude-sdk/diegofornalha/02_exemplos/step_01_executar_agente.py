#!/usr/bin/env python3
"""
Script para executar o Agente Chefe de Gabinete
Criado para: Diego Fornalha
Objetivo: Testar e demonstrar o funcionamento do agente
"""

import asyncio
import sys
import os

# Adicionar o diretório atual ao path para importar o módulo agent
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import send_query

async def testar_agente():
    """Função para testar o agente Chefe de Gabinete"""
    
    print("=" * 60)
    print("🏢 AGENTE CHEFE DE GABINETE - Diego Fornalha")
    print("=" * 60)
    print("🤖 Iniciando agente...")
    print()
    
    # Teste 1: Consulta simples
    print("📝 Teste 1: Consulta sobre status da empresa")
    print("-" * 40)
    
    try:
        result, messages = await send_query(
            prompt="Qual é o status atual da Diego Fornalha? Dê um resumo executivo.",
            permission_mode="plan"  # Apenas planejar, não executar
        )
        
        print("✅ Consulta executada com sucesso!")
        print(f"📊 Resultado: {result[:200]}..." if result and len(result) > 200 else f"📊 Resultado: {result}")
        print(f"💬 Total de mensagens: {len(messages)}")
        
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 TESTE CONCLUÍDO")
    print("=" * 60)

async def main():
    """Função principal"""
    print("🚀 EXECUTANDO AGENTE CHEFE DE GABINETE")
    print("   Desenvolvido para: Diego Fornalha")
    print("   Meta: Score 45 → 100 em 12 semanas\n")
    
    await testar_agente()
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("   1. Testar com permission_mode='default' para execução real")
    print("   2. Experimentar comandos slash como /budget-impact")
    print("   3. Usar subagentes cto e recrutador via Task")
    print("   4. Executar scripts Python customizados")

if __name__ == "__main__":
    asyncio.run(main())
