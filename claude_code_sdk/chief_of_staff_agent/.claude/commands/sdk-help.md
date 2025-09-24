---
type: command
name: sdk-help
description: Ajuda específica sobre módulos e funções do Claude Code SDK
---

# SDK Help - Assistência Claude Code SDK

Comando para obter ajuda detalhada sobre qualquer parte do Claude Code SDK.

## Uso

```bash
/sdk-help "query"           # Ajuda sobre query()
/sdk-help "ClaudeCodeOptions"  # Configurações
/sdk-help "MCP Tools"       # Ferramentas MCP
/sdk-help "Hooks"          # Sistema de hooks
/sdk-help                  # Menu geral
```

## Módulos Disponíveis

### Core Functions
- **query()** - Consultas one-shot assíncronas
- **ClaudeSDKClient** - Sessões interativas com contexto
- **ClaudeCodeOptions** - Todas configurações disponíveis

### MCP Tools (Gap Crítico!)
- **@tool decorator** - Como criar ferramentas
- **create_sdk_mcp_server()** - Servidor MCP local
- **SdkMcpTool** - Interface de ferramentas

### Hooks System (Gap Crítico!)
- **HookMatcher** - Padrões de matching
- **PreToolUse** - Validação antes de executar
- **PostToolUse** - Processamento após execução

### Error Handling
- **ClaudeSDKError** - Erro base
- **CLIConnectionError** - Problemas de conexão
- **ProcessError** - Erros de processo

## Exemplos Práticos

### Query Básica
```python
from claude_code_sdk import query

async for msg in query("Olá Claude!"):
    print(msg)
```

### Configurações Personalizadas
```python
from claude_code_sdk import ClaudeCodeOptions

options = ClaudeCodeOptions(
    temperature=0.7,
    allowed_tools=["Read", "Write"],
    max_turns=3
)
```

### MCP Tool Customizada
```python
from claude_code_sdk import tool, create_sdk_mcp_server

@tool(name="calc", description="Calculadora")
async def calc_tool(args):
    return {"result": eval(args["expr"])}

server = create_sdk_mcp_server(tools=[calc_tool])
```

## Arquivos de Referência

```
📁 claude-code-sdk-python/src/claude_code_sdk/
├── query.py         # START HERE
├── client.py        # Sessões interativas
├── types.py         # Todas as configurações
└── _errors.py       # Tratamento de erros
```

## Exercício Relacionado

Para praticar este conceito:
```bash
python examples/exercicios_praticos_pt_br.py [número]
```

- Query → Exercício 1
- Options → Exercício 2
- Tools → Exercício 3
- MCP → Exercício 4 🔴
- Hooks → Exercício 5 🔴

## Neo4j Tracking

Salva automaticamente suas consultas para aprendizado:
```cypher
CREATE (h:Learning {
    type: 'sdk_help_query',
    topic: $topic,
    timestamp: datetime()
})
```

---

*Use /sdk-help sempre que tiver dúvidas sobre o SDK!*