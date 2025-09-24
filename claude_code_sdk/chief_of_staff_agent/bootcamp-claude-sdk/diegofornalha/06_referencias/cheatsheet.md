# 🎯 Claude Code SDK - Cheatsheet

## 📦 Imports Essenciais

```python
from claude_code_sdk import query, ClaudeCodeOptions, ClaudeSDKClient
```

## 🔵 Query (Stateless)

### Básico
```python
async for msg in query("Sua pergunta"):
    if hasattr(msg, 'content'):
        for bloco in msg.content:
            if hasattr(bloco, 'text'):
                print(bloco.text)
```

### Com Opções
```python
options = ClaudeCodeOptions(
    system_prompt="Seja conciso",
    allowed_tools=["Read", "Write"]
)
async for msg in query("pergunta", options):
    # processar
```

## 🔴 Client (Stateful)

### Setup
```python
client = ClaudeSDKClient(options=ClaudeCodeOptions(...))
```

### Conversa
```python
await client.query("primeira pergunta")
response1 = await client.receive_response()

await client.query("segunda pergunta")  # Lembra da primeira!
response2 = await client.receive_response()
```

## ⚙️ ClaudeCodeOptions

### ✅ Parâmetros VÁLIDOS
```python
ClaudeCodeOptions(
    system_prompt="...",           # Instruções base
    allowed_tools=["Read"],        # Ferramentas permitidas
    disallowed_tools=["Bash"],    # Ferramentas bloqueadas
    model="claude-3-5-sonnet-20241022",
    max_turns=5,                  # Máximo de interações
    permission_mode="default",
    cwd="/path/to/dir",           # Diretório de trabalho
    env={"VAR": "value"},         # Variáveis de ambiente
    append_system_prompt="..."    # Adicional ao system_prompt
)
```

### ❌ NÃO EXISTE
```python
# ERRADO - Estes parâmetros NÃO existem:
# temperature=0.7  ❌
# max_tokens=4096  ❌
# stream=True      ❌
```

## 🛠️ Ferramentas Nativas

```python
allowed_tools=[
    "Read",       # Ler arquivos
    "Write",      # Criar/editar arquivos
    "Edit",       # Editar arquivos
    "MultiEdit",  # Múltiplas edições
    "Bash",       # Comandos shell
    "Grep",       # Buscar com regex
    "Glob",       # Buscar arquivos
    "WebSearch",  # Pesquisar web
    "WebFetch",   # Buscar URL
    "TodoWrite",  # Lista de tarefas
    "Task"        # Delegar para subagentes
]
```

## 🔧 MCP Tools (Básico)

```python
from claude_code_sdk import tool

@tool("nome", "descrição", {"param": str})
async def minha_tool(args):
    resultado = args["param"].upper()
    return {
        "content": [{
            "type": "text",
            "text": f"Resultado: {resultado}"
        }]
    }
```

## 🪝 Hooks (Básico)

```python
from claude_code_sdk.types import HookMatcher

async def validar(input_data, tool_id, context):
    if "danger" in input_data.get("command", ""):
        return {"behavior": "deny"}  # Bloqueia
    return {}  # Permite

hooks = [HookMatcher("PreToolUse", validar)]
options = ClaudeCodeOptions(hooks=hooks)
```

## 🐛 Tratamento de Erros

```python
try:
    async for msg in query("pergunta"):
        # processar
except Exception as e:
    print(f"Erro: {e}")
```

## 🔍 Verificação de Tipos

```python
from claude_code_sdk.types import (
    TextBlock,
    ToolUseBlock,
    ThinkingBlock
)

if isinstance(bloco, TextBlock):
    print(bloco.text)
elif isinstance(bloco, ToolUseBlock):
    print(f"Usando: {bloco.name}")
elif isinstance(bloco, ThinkingBlock):
    print("Claude está pensando...")
```

## 📝 Padrão Completo

```python
#!/usr/bin/env python3
import asyncio
from claude_code_sdk import query, ClaudeCodeOptions

async def main():
    options = ClaudeCodeOptions(
        system_prompt="Seja direto e conciso",
        allowed_tools=["Read", "Write"]
    )

    async for msg in query("Sua pergunta", options):
        if hasattr(msg, 'content'):
            for bloco in msg.content:
                if hasattr(bloco, 'text'):
                    print(bloco.text)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🚀 Comandos Úteis

```bash
# Verificar instalação
pip list | grep claude-code-sdk

# Autenticar
claude login

# Executar exemplo
python exemplo.py

# Debug
python -m asyncio exemplo.py
```

## ⚠️ Lembre-se

1. **SEMPRE** use async/await
2. **NUNCA** use ANTHROPIC_API_KEY
3. **SEMPRE** verifique com hasattr()
4. **temperature** não existe - use system_prompt
5. MCP tools **SEMPRE** retornam dict com 'content'

---

*Mantenha este cheatsheet aberto enquanto programa!*