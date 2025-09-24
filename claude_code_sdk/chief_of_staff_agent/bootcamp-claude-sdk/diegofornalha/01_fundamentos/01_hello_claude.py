#!/usr/bin/env python3
"""
🎓 Seu primeiro programa com Claude Code SDK!
Criado para: Diego Fornalha
Objetivo: Aprender o básico do SDK
"""

import asyncio
from claude_code_sdk import query, ClaudeCodeOptions

async def meu_primeiro_claude():
    """Função básica para conversar com Claude"""

    print("=" * 50)
    print("🤖 MEU PRIMEIRO PROGRAMA COM CLAUDE")
    print("=" * 50)

    # Pergunta simples
    pergunta = "Explique em 2 linhas o que é Python"

    print(f"\n📝 Pergunta: {pergunta}")
    print("\n💬 Resposta do Claude:")

    # Conversar com Claude
    async for mensagem in query(prompt=pergunta):
        # Processar resposta
        if hasattr(mensagem, 'content'):
            for bloco in mensagem.content:
                if hasattr(bloco, 'text'):
                    print(f"   {bloco.text}")

    print("\n✅ Parabéns! Você executou seu primeiro programa com Claude!")

async def exemplo_com_opcoes():
    """Exemplo usando ClaudeCodeOptions"""

    print("\n" + "=" * 50)
    print("🔧 USANDO OPÇÕES PERSONALIZADAS")
    print("=" * 50)

    # Configurar opções
    opcoes = ClaudeCodeOptions(
        system_prompt="Você é um professor de Python que usa analogias simples"
    )

    pergunta = "O que são variáveis em Python?"

    print(f"\n📝 Pergunta: {pergunta}")
    print("⚙️ System Prompt: Professor de Python com analogias simples")
    print("\n💬 Resposta:")

    async for mensagem in query(prompt=pergunta, options=opcoes):
        if hasattr(mensagem, 'content'):
            for bloco in mensagem.content:
                if hasattr(bloco, 'text'):
                    print(f"   {bloco.text}")

async def main():
    """Função principal"""

    print("\n🚀 BEM-VINDO AO CLAUDE CODE SDK!")
    print("   Desenvolvido por: Diego Fornalha")
    print("   Meta: Score 45 → 95 em 12 semanas\n")

    # Executar exemplo 1
    await meu_primeiro_claude()

    # Pausa dramática
    await asyncio.sleep(2)

    # Executar exemplo 2
    await exemplo_com_opcoes()

    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("   1. Rode: python examples/exercicios_praticos_pt_br.py 1")
    print("   2. Use: /daily-progress para registrar seu avanço")
    print("   3. Experimente mudar a temperatura e o system_prompt")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())