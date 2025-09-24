#!/usr/bin/env python3
"""
🔍 Teste de Ambiente - Claude Code SDK
Verifica se tudo está configurado corretamente
"""

import sys
import asyncio
from pathlib import Path

print("="*50)
print("🔧 VERIFICANDO AMBIENTE CLAUDE CODE SDK")
print("="*50)

# 1. Verificar Python
print(f"\n✅ Python: {sys.version}")
if sys.version_info < (3, 10):
    print("❌ ERRO: Python 3.10+ é necessário")
    sys.exit(1)

# 2. Verificar imports
try:
    from claude_code_sdk import query, ClaudeCodeOptions, ClaudeSDKClient
    print("✅ Claude Code SDK importado com sucesso")
except ImportError as e:
    print(f"❌ ERRO ao importar SDK: {e}")
    print("\nTente: pip install claude-code-sdk")
    sys.exit(1)

# 3. Verificar autenticação
async def testar_query():
    """Testa uma query simples"""
    try:
        print("\n🔍 Testando query()...")
        contador = 0
        async for msg in query(prompt="Responda apenas 'OK'"):
            contador += 1
            if contador == 1:
                print("✅ Query funcionando!")
                return True
    except Exception as e:
        print(f"❌ Erro na query: {e}")
        print("\nVerifique:")
        print("1. Execute: claude login")
        print("2. Certifique-se de estar autenticado")
        return False

# 4. Verificar diretório de logs
logs_dir = Path.home() / '.claude' / 'logs'
if logs_dir.exists():
    print(f"✅ Diretório de logs existe: {logs_dir}")
else:
    print(f"⚠️ Criando diretório de logs: {logs_dir}")
    logs_dir.mkdir(parents=True, exist_ok=True)

# 5. Executar teste
async def main():
    print("\n" + "="*50)
    print("🚀 EXECUTANDO TESTE COMPLETO")
    print("="*50)

    sucesso = await testar_query()

    if sucesso:
        print("\n" + "="*50)
        print("🎉 AMBIENTE CONFIGURADO COM SUCESSO!")
        print("="*50)
        print("\n✅ Você está pronto para começar o bootcamp!")
        print("\nPróximo passo:")
        print("cd ../01_fundamentos")
        print("python hello_claude.py")
    else:
        print("\n" + "="*50)
        print("❌ PROBLEMAS ENCONTRADOS")
        print("="*50)
        print("\nResolva os erros acima antes de continuar")

if __name__ == "__main__":
    asyncio.run(main())