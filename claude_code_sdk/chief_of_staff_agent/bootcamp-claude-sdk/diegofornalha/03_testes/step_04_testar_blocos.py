#!/usr/bin/env python3
"""
Script para testar a estrutura de tipos de blocos
Criado para: Diego Fornalha
Objetivo: Verificar se o código de blocos funciona na prática
"""

import asyncio
import sys
import os

# Adicionar o diretório do SDK ao path
sys.path.insert(0, '/Users/2a/.claude/anthropic-cookbook/claude_code_sdk/chief_of_staff_agent/claude-code-sdk-python/src')

from claude_code_sdk import query, ClaudeCodeOptions

async def testar_estrutura_blocos():
    """Testa a estrutura de tipos de blocos na prática"""
    
    print("=" * 60)
    print("🧪 TESTANDO ESTRUTURA DE TIPOS DE BLOCOS")
    print("=" * 60)
    
    # Teste 1: Consulta simples para ver TextBlock
    print("\n📝 Teste 1: TextBlock (resposta simples)")
    print("-" * 40)
    
    try:
        pergunta = "O que é Python em uma frase?"
        
        print(f"Pergunta: {pergunta}")
        print("Resposta:")
        
        async for mensagem in query(prompt=pergunta):
            print(f"Tipo da mensagem: {type(mensagem).__name__}")
            
            if hasattr(mensagem, 'content'):
                print(f"Content é uma lista: {isinstance(mensagem.content, list)}")
                print(f"Número de blocos: {len(mensagem.content)}")
                
                for i, bloco in enumerate(mensagem.content):
                    print(f"\n--- Bloco {i+1} ---")
                    print(f"Tipo do bloco: {type(bloco).__name__}")
                    print(f"Atributos disponíveis: {dir(bloco)}")
                    
                    # Verificar cada tipo de bloco
                    if hasattr(bloco, 'text'):
                        print(f"📝 TextBlock: {bloco.text}")
                    elif hasattr(bloco, 'thinking'):
                        print(f"🤔 ThinkingBlock: {bloco.thinking}")
                    elif hasattr(bloco, 'name'):
                        print(f"🛠️ ToolUseBlock: {bloco.name}")
                    elif hasattr(bloco, 'tool_use_id'):
                        print(f"✅ ToolResultBlock: {bloco.tool_use_id}")
                    else:
                        print(f"❓ Tipo desconhecido: {bloco}")
            else:
                print("❌ Mensagem não tem atributo 'content'")
                
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
    
    # Teste 2: Consulta que pode usar ferramentas
    print("\n📝 Teste 2: Possível ToolUseBlock")
    print("-" * 40)
    
    try:
        pergunta = "Qual é a data de hoje?"
        
        print(f"Pergunta: {pergunta}")
        print("Resposta:")
        
        async for mensagem in query(prompt=pergunta):
            if hasattr(mensagem, 'content'):
                for i, bloco in enumerate(mensagem.content):
                    print(f"\n--- Bloco {i+1} ---")
                    print(f"Tipo: {type(bloco).__name__}")
                    
                    if hasattr(bloco, 'text'):
                        print(f"📝 Texto: {bloco.text}")
                    elif hasattr(bloco, 'name'):
                        print(f"🛠️ Ferramenta: {bloco.name}")
                        print(f"Input: {bloco.input}")
                    elif hasattr(bloco, 'tool_use_id'):
                        print(f"✅ Resultado ID: {bloco.tool_use_id}")
                        print(f"Conteúdo: {bloco.content}")
                        print(f"É erro: {bloco.is_error}")
                        
    except Exception as e:
        print(f"❌ Erro no teste 2: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Função principal"""
    print("🚀 TESTE DE ESTRUTURA DE BLOCOS")
    print("   Desenvolvido para: Diego Fornalha")
    print("   Objetivo: Verificar se o código funciona na prática\n")
    
    await testar_estrutura_blocos()
    
    print("\n" + "=" * 60)
    print("🎯 TESTE CONCLUÍDO")
    print("=" * 60)
    
    print("\n💡 OBSERVAÇÕES:")
    print("   - Verifique se os tipos de blocos aparecem corretamente")
    print("   - Observe a estrutura real das mensagens")
    print("   - Confirme se o código de acesso funciona")

if __name__ == "__main__":
    asyncio.run(main())
