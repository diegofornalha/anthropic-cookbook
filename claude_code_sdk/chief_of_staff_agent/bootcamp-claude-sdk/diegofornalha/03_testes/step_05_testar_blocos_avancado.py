#!/usr/bin/env python3
"""
Script avançado para testar todos os tipos de blocos
Criado para: Diego Fornalha
Objetivo: Verificar se conseguimos ver ToolUseBlock e outros tipos
"""

import asyncio
import sys
import os

# Adicionar o diretório do SDK ao path
sys.path.insert(0, '/Users/2a/.claude/anthropic-cookbook/claude_code_sdk/chief_of_staff_agent/claude-code-sdk-python/src')

from claude_code_sdk import query, ClaudeCodeOptions

async def testar_todos_tipos_blocos():
    """Testa todos os tipos de blocos possíveis"""
    
    print("=" * 70)
    print("🧪 TESTE AVANÇADO - TODOS OS TIPOS DE BLOCOS")
    print("=" * 70)
    
    # Teste 1: Forçar uso de ferramentas
    print("\n📝 Teste 1: Forçar uso de ferramentas")
    print("-" * 50)
    
    try:
        # Configurar opções para permitir ferramentas
        opcoes = ClaudeCodeOptions(
            system_prompt="Você deve usar ferramentas quando necessário. Se precisar de informações atuais, use WebSearch."
        )
        
        pergunta = "Qual é a cotação do dólar hoje? Use uma ferramenta se necessário."
        
        print(f"Pergunta: {pergunta}")
        print("Resposta:")
        
        async for mensagem in query(prompt=pergunta, options=opcoes):
            print(f"\nTipo da mensagem: {type(mensagem).__name__}")
            
            if hasattr(mensagem, 'content'):
                print(f"Content é uma lista: {isinstance(mensagem.content, list)}")
                print(f"Número de blocos: {len(mensagem.content)}")
                
                for i, bloco in enumerate(mensagem.content):
                    print(f"\n--- Bloco {i+1} ---")
                    print(f"Tipo do bloco: {type(bloco).__name__}")
                    
                    # Verificar cada tipo de bloco
                    if hasattr(bloco, 'text'):
                        print(f"📝 TextBlock: {bloco.text[:100]}...")
                    elif hasattr(bloco, 'thinking'):
                        print(f"🤔 ThinkingBlock: {bloco.thinking[:100]}...")
                    elif hasattr(bloco, 'name'):
                        print(f"🛠️ ToolUseBlock:")
                        print(f"   Nome: {bloco.name}")
                        print(f"   ID: {bloco.id}")
                        print(f"   Input: {bloco.input}")
                    elif hasattr(bloco, 'tool_use_id'):
                        print(f"✅ ToolResultBlock:")
                        print(f"   Tool Use ID: {bloco.tool_use_id}")
                        print(f"   Conteúdo: {bloco.content}")
                        print(f"   É erro: {bloco.is_error}")
                    else:
                        print(f"❓ Tipo desconhecido: {bloco}")
                        print(f"   Atributos: {[attr for attr in dir(bloco) if not attr.startswith('_')]}")
            else:
                print("❌ Mensagem não tem atributo 'content'")
                print(f"   Atributos disponíveis: {[attr for attr in dir(mensagem) if not attr.startswith('_')]}")
                
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
    
    # Teste 2: Verificar tipos de mensagens
    print("\n📝 Teste 2: Tipos de mensagens")
    print("-" * 50)
    
    try:
        pergunta = "Explique o que são tipos de blocos no Claude Code SDK"
        
        print(f"Pergunta: {pergunta}")
        print("Resposta:")
        
        tipos_mensagens = []
        
        async for mensagem in query(prompt=pergunta):
            tipo = type(mensagem).__name__
            tipos_mensagens.append(tipo)
            print(f"Tipo: {tipo}")
            
            if hasattr(mensagem, 'content'):
                print(f"  Tem content: Sim")
                print(f"  Número de blocos: {len(mensagem.content)}")
            else:
                print(f"  Tem content: Não")
                print(f"  Atributos: {[attr for attr in dir(mensagem) if not attr.startswith('_')]}")
        
        print(f"\nTipos de mensagens encontrados: {set(tipos_mensagens)}")
                        
    except Exception as e:
        print(f"❌ Erro no teste 2: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Função principal"""
    print("🚀 TESTE AVANÇADO DE BLOCOS")
    print("   Desenvolvido para: Diego Fornalha")
    print("   Objetivo: Verificar todos os tipos de blocos\n")
    
    await testar_todos_tipos_blocos()
    
    print("\n" + "=" * 70)
    print("🎯 TESTE AVANÇADO CONCLUÍDO")
    print("=" * 70)
    
    print("\n💡 CONCLUSÕES:")
    print("   - Verifique quais tipos de blocos aparecem")
    print("   - Observe a estrutura real das mensagens")
    print("   - Confirme se o código funciona na prática")

if __name__ == "__main__":
    asyncio.run(main())
