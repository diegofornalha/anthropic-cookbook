# ⚠️ CORREÇÕES IMPORTANTES - Claude Code SDK

## 🔴 O QUE NÃO FUNCIONA (e foi corrigido)

### 1. **Temperature NÃO existe em ClaudeCodeOptions**
❌ **ERRADO:**
```python
ClaudeCodeOptions(temperature=0.7)  # NÃO FUNCIONA!
```

✅ **CORRETO:**
```python
ClaudeCodeOptions(
    system_prompt="Use temperatura alta/baixa/balanceada"  # Instrução no prompt
)
```

### 2. **Parâmetros REAIS do ClaudeCodeOptions**
```python
# ESTES SÃO OS ÚNICOS PARÂMETROS QUE FUNCIONAM:
ClaudeCodeOptions(
    allowed_tools=["Read", "Write"],      # ✅ Funciona
    system_prompt="instruções",           # ✅ Funciona
    append_system_prompt="adicional",     # ✅ Funciona
    model="claude-3-5-sonnet-20241022",   # ✅ Funciona
    permission_mode="default",            # ✅ Funciona
    max_turns=5,                          # ✅ Funciona
    disallowed_tools=["Bash"],           # ✅ Funciona
    cwd="/path/to/dir",                   # ✅ Funciona
    env={"VAR": "value"},                 # ✅ Funciona

    # ESTES NÃO EXISTEM:
    # temperature=0.7,                    # ❌ NÃO EXISTE
    # max_tokens=4096,                    # ❌ NÃO EXISTE
    # stream=True,                        # ❌ NÃO EXISTE
)
```

### 3. **Import correto do SDK**
```python
# ✅ CORRETO:
from claude_code_sdk import query, ClaudeCodeOptions
from claude_code_sdk import ClaudeSDKClient

# ❌ ERRADO:
from claude_code_sdk import ClaudeSDKError  # Não exportado diretamente
# ✅ CORRETO:
from claude_code_sdk._errors import ClaudeSDKError  # Se precisar
```

### 4. **Ferramentas MCP - Nome correto**
```python
# ❌ ERRADO:
allowed_tools=["mcp_neo4j-memory_search_memories"]

# ✅ CORRETO:
allowed_tools=["mcp__neo4j-memory__search_memories"]  # Dois underscores!
```

### 5. **Async SEMPRE necessário**
```python
# ❌ ERRADO:
for msg in query("pergunta"):  # Não funciona!
    print(msg)

# ✅ CORRETO:
import asyncio

async def main():
    async for msg in query("pergunta"):
        print(msg.content[0].text)

asyncio.run(main())
```

## ✅ O QUE FUNCIONA PERFEITAMENTE

### 1. **query() para consultas simples**
```python
async for msg in query("Explique Python"):
    if hasattr(msg, 'content'):
        for bloco in msg.content:
            if hasattr(bloco, 'text'):
                print(bloco.text)
```

### 2. **ClaudeSDKClient para conversas**
```python
from claude_code_sdk import ClaudeSDKClient

client = ClaudeSDKClient(options=ClaudeCodeOptions(...))
# Use client.query() e client.receive_response()
```

### 3. **Ferramentas nativas**
```python
options = ClaudeCodeOptions(
    allowed_tools=[
        "Read",      # ✅ Ler arquivos
        "Write",     # ✅ Criar arquivos
        "Edit",      # ✅ Editar arquivos
        "MultiEdit", # ✅ Múltiplas edições
        "Bash",      # ✅ Comandos shell
        "Grep",      # ✅ Buscar com regex
        "Glob",      # ✅ Buscar arquivos
        "WebSearch", # ✅ Pesquisar web
        "WebFetch",  # ✅ Buscar URL
        "TodoWrite", # ✅ Lista de tarefas
        "Task"       # ✅ Delegar para subagentes
    ]
)
```

### 4. **Detecção de tipos de blocos**
```python
async for msg in query(prompt, options):
    if hasattr(msg, 'content'):
        for bloco in msg.content:
            block_type = type(bloco).__name__

            if 'Text' in block_type:
                print(f"Texto: {bloco.text}")
            elif 'ToolUse' in block_type:
                print(f"Ferramenta: {bloco.name}")
            elif 'Thinking' in block_type:
                print("Claude está pensando...")
```

## 📝 RESUMO DAS CORREÇÕES

| Conceito | Status | Solução |
|----------|--------|---------|
| temperature parameter | ❌ Não existe | Use system_prompt |
| max_tokens parameter | ❌ Não existe | SDK gerencia automaticamente |
| stream parameter | ❌ Não existe | Use include_partial_messages |
| ClaudeSDKError import | ⚠️ Não direto | Import de _errors |
| MCP tool names | ⚠️ Sintaxe específica | Use __ duplo underscore |
| Sync iteration | ❌ Não funciona | Sempre use async/await |

## 🎯 CHECKLIST DE VERIFICAÇÃO

Antes de executar qualquer código Claude CODE SDK:

- [ ] Usando async/await?
- [ ] ClaudeCodeOptions tem apenas parâmetros válidos?
- [ ] Imports estão corretos?
- [ ] Ferramentas MCP com __ duplo underscore?
- [ ] Sem temperature, max_tokens ou stream?
- [ ] Error handling com try/except genérico?

---

*Documento criado em 2025-09-23 após identificar e corrigir problemas reais*
*Mantido por: Diego Fornalha*