#!/usr/bin/env python3
"""
Script para testar o Assistente Pessoal de IA do Diego Fornalha
Criado para: Diego Fornalha
Objetivo: Demonstrar o agente personalizado para o bootcamp
"""

import asyncio
import sys
import os

# Adicionar o diretório pai ao path para importar o módulo agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import send_query

async def testar_agente_personalizado():
    """Função para testar o assistente personalizado do Diego"""
    
    print("=" * 70)
    print("🤖 ASSISTENTE PESSOAL DE IA - DIEGO FORNALHA")
    print("=" * 70)
    print("🎯 Bootcamp: Score 45 → 100 em 12 semanas")
    print("📅 Fase atual: Fundamentos (Semana 1)")
    print()
    
    # Teste 1: Consulta sobre progresso
    print("📝 Teste 1: Consulta sobre progresso do bootcamp")
    print("-" * 50)
    
    try:
        result, messages = await send_query(
            prompt="Qual é o meu progresso atual no bootcamp? Dê um resumo do que já aprendi e próximos passos.",
            permission_mode="plan"
        )
        
        print("✅ Consulta sobre progresso executada com sucesso!")
        print(f"📊 Resultado: {result[:300]}..." if result and len(result) > 300 else f"📊 Resultado: {result}")
        print(f"💬 Total de mensagens: {len(messages)}")
        
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")
    
    # Teste 2: Consulta sobre Claude Code SDK
    print("\n📝 Teste 2: Consulta sobre Claude Code SDK")
    print("-" * 50)
    
    try:
        result, messages = await send_query(
            prompt="Explique os conceitos fundamentais do Claude Code SDK que preciso dominar. Foque nos gaps críticos identificados.",
            permission_mode="plan"
        )
        
        print("✅ Consulta sobre SDK executada com sucesso!")
        print(f"📊 Resultado: {result[:300]}..." if result and len(result) > 300 else f"📊 Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")
    
    # Teste 3: Relatório executivo
    print("\n📝 Teste 3: Relatório executivo do bootcamp")
    print("-" * 50)
    
    try:
        result, messages = await send_query(
            prompt="Gere um relatório executivo sobre meu progresso no bootcamp, incluindo métricas e recomendações.",
            permission_mode="plan",
            output_style="executive"
        )
        
        print("✅ Relatório executivo gerado com sucesso!")
        print(f"📊 Resultado: {result[:300]}..." if result and len(result) > 300 else f"📊 Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Erro no relatório: {e}")

async def main():
    """Função principal"""
    print("🚀 ASSISTENTE PESSOAL DE IA - DIEGO FORNALHA")
    print("   Desenvolvido para: Diego Fornalha")
    print("   Meta: Score 45 → 100 em 12 semanas")
    print("   Objetivo: Dominar Claude Code SDK completamente\n")
    
    await testar_agente_personalizado()
    
    print("\n" + "=" * 70)
    print("🎯 TESTE CONCLUÍDO")
    print("=" * 70)
    
    print("\n💡 FUNCIONALIDADES PERSONALIZADAS:")
    print("   ✅ Contexto específico do Diego Fornalha")
    print("   ✅ Acesso ao progresso no Neo4j Memory")
    print("   ✅ Foco no bootcamp Claude Code SDK")
    print("   ✅ Subagentes CTO e Recrutador")
    print("   ✅ Scripts customizados para avaliação")
    print("   ✅ Comandos slash personalizados")
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("   1. Testar com permission_mode='default' para execução real")
    print("   2. Explorar comandos slash específicos do bootcamp")
    print("   3. Usar subagentes para questões técnicas e de carreira")
    print("   4. Integrar com scripts de avaliação de progresso")

if __name__ == "__main__":
    asyncio.run(main())
