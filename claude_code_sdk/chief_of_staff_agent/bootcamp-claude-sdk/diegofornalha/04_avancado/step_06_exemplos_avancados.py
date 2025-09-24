#!/usr/bin/env python3
"""
Exemplos Avançados - Claude Code SDK
Criado para: Diego Fornalha
Objetivo: Demonstrar conceitos avançados como type hints, tratamento de erros e configurações
"""

import asyncio
import sys
import os
from typing import AsyncIterator, Optional

# Adicionar o diretório do SDK ao path
sys.path.insert(0, '/Users/2a/.claude/anthropic-cookbook/claude_code_sdk/chief_of_staff_agent/claude-code-sdk-python/src')

from claude_code_sdk import query, ClaudeCodeOptions, Message

async def exemplo_type_hints(prompt: str) -> AsyncIterator[Message]:
    """
    Exemplo de função com type hints completos
    
    Args:
        prompt: A pergunta para o Claude
        
    Yields:
        Message: Mensagens do Claude com type safety
    """
    print(f"🔍 Type Hints - Processando: {prompt}")
    
    async for mensagem in query(prompt=prompt):
        yield mensagem

async def exemplo_tratamento_erros(prompt: str) -> Optional[str]:
    """
    Exemplo de tratamento robusto de erros
    
    Args:
        prompt: A pergunta para o Claude
        
    Returns:
        Optional[str]: Resultado ou None se houver erro
    """
    print(f"🛡️ Tratamento de Erros - Processando: {prompt}")
    
    try:
        resultado = ""
        async for mensagem in query(prompt=prompt):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        resultado += bloco.text + "\n"
        
        return resultado.strip()
        
    except Exception as e:
        print(f"❌ Erro capturado: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        return None

async def exemplo_configuracoes_avancadas():
    """
    Exemplo de configurações avançadas do ClaudeCodeOptions
    """
    print("⚙️ Configurações Avançadas")
    print("-" * 40)
    
    # Configuração 1: System prompt personalizado
    print("\n📝 Configuração 1: System Prompt Personalizado")
    opcoes1 = ClaudeCodeOptions(
        system_prompt="Você é um professor de Python que sempre usa analogias com comida brasileira"
    )
    
    try:
        async for mensagem in query(prompt="Explique o que são listas em Python", options=opcoes1):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"🍽️ Resposta: {bloco.text[:200]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Configuração 2: Diretório de trabalho
    print("\n📁 Configuração 2: Diretório de Trabalho")
    opcoes2 = ClaudeCodeOptions(
        cwd="/tmp",  # Diretório temporário
        system_prompt="Você é um assistente de arquivos"
    )
    
    try:
        async for mensagem in query(prompt="Liste os arquivos no diretório atual", options=opcoes2):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"📂 Resposta: {bloco.text[:200]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")

async def exemplo_permission_modes():
    """
    Exemplo de diferentes modos de permissão
    """
    print("\n🔐 Modos de Permissão")
    print("-" * 40)
    
    # Modo Plan (apenas planejar)
    print("\n📋 Modo Plan - Apenas Planejar")
    opcoes_plan = ClaudeCodeOptions(
        permission_mode="plan",
        system_prompt="Você deve apenas planejar, não executar"
    )
    
    try:
        async for mensagem in query(prompt="Crie um arquivo Python com uma função que calcula fatorial", options=opcoes_plan):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"📋 Plano: {bloco.text[:200]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")

async def exemplo_async_iterator():
    """
    Exemplo de uso de AsyncIterator com type hints
    """
    print("\n🔄 AsyncIterator com Type Hints")
    print("-" * 40)
    
    async def processar_mensagens(prompt: str) -> AsyncIterator[str]:
        """
        Processa mensagens e retorna apenas o texto
        
        Args:
            prompt: A pergunta para o Claude
            
        Yields:
            str: Texto das respostas
        """
        async for mensagem in query(prompt=prompt):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        yield bloco.text
    
    try:
        print("📝 Processando mensagens...")
        async for texto in processar_mensagens("Explique o que é async/await em Python"):
            print(f"💬 Texto: {texto[:150]}...")
            break  # Apenas o primeiro bloco para o exemplo
    except Exception as e:
        print(f"❌ Erro: {e}")

async def exemplo_configuracoes_completas():
    """
    Exemplo de configuração completa com todas as opções
    """
    print("\n🎛️ Configuração Completa")
    print("-" * 40)
    
    opcoes_completas = ClaudeCodeOptions(
        system_prompt="Você é um especialista em Claude Code SDK",
        cwd=os.getcwd(),
        permission_mode="default",
        continue_conversation=False,
        max_turns=5,
        model="claude-sonnet-4-20250514"
    )
    
    try:
        async for mensagem in query(prompt="Dê um resumo sobre Claude Code SDK", options=opcoes_completas):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"🎯 Resposta: {bloco.text[:200]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")

async def exemplo_erro_especifico():
    """
    Exemplo de tratamento de erros específicos
    """
    print("\n🚨 Tratamento de Erros Específicos")
    print("-" * 40)
    
    try:
        # Tentar uma operação que pode falhar
        async for mensagem in query(prompt="Execute um comando que não existe"):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"✅ Sucesso: {bloco.text[:100]}...")
                        break
    except ConnectionError as e:
        print(f"🔌 Erro de conexão: {e}")
    except TimeoutError as e:
        print(f"⏰ Timeout: {e}")
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        print(f"Tipo: {type(e).__name__}")

async def main():
    """Função principal com todos os exemplos"""
    print("🚀 EXEMPLOS AVANÇADOS - CLAUDE CODE SDK")
    print("   Desenvolvido para: Diego Fornalha")
    print("   Objetivo: Demonstrar conceitos avançados\n")
    
    # Exemplo 1: Type Hints
    print("=" * 60)
    print("1️⃣ TYPE HINTS")
    print("=" * 60)
    try:
        async for msg in exemplo_type_hints("O que é Python?"):
            if hasattr(msg, 'content'):
                for bloco in msg.content:
                    if hasattr(bloco, 'text'):
                        print(f"✅ Type hints funcionando: {bloco.text[:100]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Exemplo 2: Tratamento de Erros
    print("\n" + "=" * 60)
    print("2️⃣ TRATAMENTO DE ERROS")
    print("=" * 60)
    resultado = await exemplo_tratamento_erros("Explique o que são funções em Python")
    if resultado:
        print(f"✅ Tratamento de erros funcionando: {resultado[:100]}...")
    else:
        print("❌ Erro capturado e tratado")
    
    # Exemplo 3: Configurações Avançadas
    print("\n" + "=" * 60)
    print("3️⃣ CONFIGURAÇÕES AVANÇADAS")
    print("=" * 60)
    await exemplo_configuracoes_avancadas()
    
    # Exemplo 4: Modos de Permissão
    print("\n" + "=" * 60)
    print("4️⃣ MODOS DE PERMISSÃO")
    print("=" * 60)
    await exemplo_permission_modes()
    
    # Exemplo 5: AsyncIterator
    print("\n" + "=" * 60)
    print("5️⃣ ASYNC ITERATOR")
    print("=" * 60)
    await exemplo_async_iterator()
    
    # Exemplo 6: Configuração Completa
    print("\n" + "=" * 60)
    print("6️⃣ CONFIGURAÇÃO COMPLETA")
    print("=" * 60)
    await exemplo_configuracoes_completas()
    
    # Exemplo 7: Erro Específico
    print("\n" + "=" * 60)
    print("7️⃣ ERRO ESPECÍFICO")
    print("=" * 60)
    await exemplo_erro_especifico()
    
    print("\n" + "=" * 60)
    print("🎯 EXEMPLOS CONCLUÍDOS")
    print("=" * 60)
    
    print("\n💡 CONCEITOS DEMONSTRADOS:")
    print("   ✅ Type Hints (AsyncIterator, Optional)")
    print("   ✅ Tratamento de Erros (try/except)")
    print("   ✅ Configurações Avançadas (ClaudeCodeOptions)")
    print("   ✅ Modos de Permissão (plan, default)")
    print("   ✅ AsyncIterator personalizado")
    print("   ✅ Configuração completa")
    print("   ✅ Tratamento de erros específicos")

if __name__ == "__main__":
    asyncio.run(main())
