#!/usr/bin/env python3
"""
Configurações Corretas - Claude Code SDK
Criado para: Diego Fornalha
Objetivo: Mostrar configurações que FUNCIONAM vs que NÃO funcionam
"""

import asyncio
import sys
import os

# Adicionar o diretório do SDK ao path
sys.path.insert(0, '/Users/2a/.claude/anthropic-cookbook/claude_code_sdk/chief_of_staff_agent/claude-code-sdk-python/src')

from claude_code_sdk import query, ClaudeCodeOptions

async def exemplo_configuracoes_que_funcionam():
    """
    Exemplo de configurações que FUNCIONAM no ClaudeCodeOptions
    """
    print("✅ CONFIGURAÇÕES QUE FUNCIONAM")
    print("=" * 50)
    
    # ✅ FUNCIONA: System prompt
    print("\n1️⃣ System Prompt (FUNCIONA)")
    opcoes1 = ClaudeCodeOptions(
        system_prompt="Você é um professor de Python que usa analogias simples"
    )
    
    try:
        async for mensagem in query(prompt="Explique o que são variáveis", options=opcoes1):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"✅ System prompt funcionando: {bloco.text[:100]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # ✅ FUNCIONA: Permission mode
    print("\n2️⃣ Permission Mode (FUNCIONA)")
    opcoes2 = ClaudeCodeOptions(
        permission_mode="plan"
    )
    
    try:
        async for mensagem in query(prompt="Crie um arquivo Python", options=opcoes2):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"✅ Permission mode funcionando: {bloco.text[:100]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # ✅ FUNCIONA: CWD (Current Working Directory)
    print("\n3️⃣ CWD (FUNCIONA)")
    opcoes3 = ClaudeCodeOptions(
        cwd="/tmp"
    )
    
    try:
        async for mensagem in query(prompt="Qual é o diretório atual?", options=opcoes3):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"✅ CWD funcionando: {bloco.text[:100]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # ✅ FUNCIONA: Model
    print("\n4️⃣ Model (FUNCIONA)")
    opcoes4 = ClaudeCodeOptions(
        model="claude-sonnet-4-20250514"
    )
    
    try:
        async for mensagem in query(prompt="Qual modelo você está usando?", options=opcoes4):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"✅ Model funcionando: {bloco.text[:100]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")

async def exemplo_configuracoes_que_nao_funcionam():
    """
    Exemplo de configurações que NÃO FUNCIONAM no ClaudeCodeOptions
    """
    print("\n❌ CONFIGURAÇÕES QUE NÃO FUNCIONAM")
    print("=" * 50)
    
    # ❌ NÃO FUNCIONA: Temperature
    print("\n1️⃣ Temperature (NÃO FUNCIONA)")
    try:
        opcoes_erro = ClaudeCodeOptions(
            temperature=0.9  # ❌ Este parâmetro não existe
        )
        print("❌ Erro: temperature não é um parâmetro válido")
    except TypeError as e:
        print(f"✅ Erro capturado corretamente: {e}")
    
    # ❌ NÃO FUNCIONA: Max tokens
    print("\n2️⃣ Max Tokens (NÃO FUNCIONA)")
    try:
        opcoes_erro = ClaudeCodeOptions(
            max_tokens=1000  # ❌ Este parâmetro não existe
        )
        print("❌ Erro: max_tokens não é um parâmetro válido")
    except TypeError as e:
        print(f"✅ Erro capturado corretamente: {e}")
    
    # ❌ NÃO FUNCIONA: Top P
    print("\n3️⃣ Top P (NÃO FUNCIONA)")
    try:
        opcoes_erro = ClaudeCodeOptions(
            top_p=0.9  # ❌ Este parâmetro não existe
        )
        print("❌ Erro: top_p não é um parâmetro válido")
    except TypeError as e:
        print(f"✅ Erro capturado corretamente: {e}")

async def exemplo_alternativas_para_temperature():
    """
    Alternativas para controlar criatividade (já que temperature não existe)
    """
    print("\n🎨 ALTERNATIVAS PARA CONTROLAR CRIATIVIDADE")
    print("=" * 50)
    
    # Alternativa 1: System prompt para criatividade
    print("\n1️⃣ System Prompt para Criatividade")
    opcoes_criativo = ClaudeCodeOptions(
        system_prompt="Você é um escritor criativo e poético. Use metáforas e linguagem rica."
    )
    
    try:
        async for mensagem in query(prompt="Descreva o que é programação", options=opcoes_criativo):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"🎨 Resposta criativa: {bloco.text[:150]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Alternativa 2: System prompt para precisão
    print("\n2️⃣ System Prompt para Precisão")
    opcoes_preciso = ClaudeCodeOptions(
        system_prompt="Você é um técnico preciso. Seja direto e objetivo. Use apenas fatos."
    )
    
    try:
        async for mensagem in query(prompt="Descreva o que é programação", options=opcoes_preciso):
            if hasattr(mensagem, 'content'):
                for bloco in mensagem.content:
                    if hasattr(bloco, 'text'):
                        print(f"🎯 Resposta precisa: {bloco.text[:150]}...")
                        break
    except Exception as e:
        print(f"❌ Erro: {e}")

async def exemplo_tratamento_erros_completo():
    """
    Exemplo completo de tratamento de erros
    """
    print("\n🛡️ TRATAMENTO DE ERROS COMPLETO")
    print("=" * 50)
    
    async def consultar_seguro(prompt: str) -> str:
        """
        Função segura para consultar o Claude
        
        Args:
            prompt: A pergunta para o Claude
            
        Returns:
            str: Resposta ou mensagem de erro
        """
        try:
            resultado = ""
            async for mensagem in query(prompt=prompt):
                if hasattr(mensagem, 'content'):
                    for bloco in mensagem.content:
                        if hasattr(bloco, 'text'):
                            resultado += bloco.text + "\n"
            
            return resultado.strip() if resultado else "Nenhuma resposta recebida"
            
        except ConnectionError as e:
            return f"Erro de conexão: {e}"
        except TimeoutError as e:
            return f"Timeout: {e}"
        except Exception as e:
            return f"Erro inesperado: {e} (Tipo: {type(e).__name__})"
    
    # Teste da função segura
    print("📝 Testando função segura...")
    resposta = await consultar_seguro("Explique o que é Python")
    print(f"✅ Resposta segura: {resposta[:100]}...")

async def exemplo_type_hints_completo():
    """
    Exemplo completo de type hints
    """
    print("\n🔍 TYPE HINTS COMPLETO")
    print("=" * 50)
    
    from typing import AsyncIterator, Optional, List, Dict, Any
    from claude_code_sdk import Message
    
    async def processar_mensagens(prompt: str) -> AsyncIterator[str]:
        """
        Processa mensagens e retorna apenas texto
        
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
    
    async def obter_resposta(prompt: str) -> Optional[str]:
        """
        Obtém uma resposta do Claude
        
        Args:
            prompt: A pergunta para o Claude
            
        Returns:
            Optional[str]: Resposta ou None se houver erro
        """
        try:
            async for texto in processar_mensagens(prompt):
                return texto
        except Exception:
            return None
    
    # Teste das funções com type hints
    print("📝 Testando type hints...")
    resposta = await obter_resposta("O que é type hints em Python?")
    if resposta:
        print(f"✅ Type hints funcionando: {resposta[:100]}...")
    else:
        print("❌ Erro na função com type hints")

async def main():
    """Função principal"""
    print("🚀 CONFIGURAÇÕES CORRETAS - CLAUDE CODE SDK")
    print("   Desenvolvido para: Diego Fornalha")
    print("   Objetivo: Mostrar o que funciona vs o que não funciona\n")
    
    # Exemplo 1: Configurações que funcionam
    await exemplo_configuracoes_que_funcionam()
    
    # Exemplo 2: Configurações que não funcionam
    await exemplo_configuracoes_que_nao_funcionam()
    
    # Exemplo 3: Alternativas para temperature
    await exemplo_alternativas_para_temperature()
    
    # Exemplo 4: Tratamento de erros completo
    await exemplo_tratamento_erros_completo()
    
    # Exemplo 5: Type hints completo
    await exemplo_type_hints_completo()
    
    print("\n" + "=" * 60)
    print("🎯 EXEMPLOS CONCLUÍDOS")
    print("=" * 60)
    
    print("\n💡 RESUMO:")
    print("   ✅ FUNCIONA: system_prompt, permission_mode, cwd, model")
    print("   ❌ NÃO FUNCIONA: temperature, max_tokens, top_p")
    print("   🎨 ALTERNATIVA: Use system_prompt para controlar criatividade")
    print("   🛡️ TRATAMENTO: Use try/except com tipos específicos")
    print("   🔍 TYPE HINTS: Use AsyncIterator, Optional, etc.")

if __name__ == "__main__":
    asyncio.run(main())
