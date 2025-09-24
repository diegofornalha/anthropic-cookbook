---
type: command
name: sdk-basics
description: Fundamentos essenciais do Claude Code SDK - início perfeito para o bootcamp
---

# 🚀 SDK Basics - Fundamentos do Claude Code SDK

Comando focado 100% em Claude Code SDK - seu ponto de partida oficial!

## Uso

```bash
/sdk-basics                    # Visão geral do SDK
/sdk-basics "query"           # Função query() explicada
/sdk-basics "options"         # ClaudeCodeOptions detalhado
/sdk-basics "tools"           # Ferramentas disponíveis
/sdk-basics "async"           # Por que async/await
```

## 📌 O QUE É O CLAUDE CODE SDK?

Uma biblioteca Python para usar Claude SEM API key! Autenticação via `claude login`.

### Diferença Fundamental:
```python
# ❌ NÃO USE (método antigo com API key)
import anthropic
client = anthropic.Anthropic(api_key="sk-ant-...")

# ✅ USE SEMPRE (Claude Code SDK)
from claude_code_sdk import query
async for msg in query("Olá Claude!"):
    print(msg)
```

## 🎯 3 CONCEITOS ESSENCIAIS

### 1. query() - Sua Função Principal
```python
from claude_code_sdk import query

# Uso básico - SEMPRE assíncrono!
async def meu_primeiro_claude():
    async for mensagem in query("O que é Python?"):
        if hasattr(mensagem, 'content'):
            for bloco in mensagem.content:
                if hasattr(bloco, 'text'):
                    print(bloco.text)

# Rode com: asyncio.run(meu_primeiro_claude())
```

**📚 Pratique**: `python examples/exercicios_praticos_pt_br.py 1`

### 2. ClaudeCodeOptions - Configurações
```python
from claude_code_sdk import ClaudeCodeOptions

opcoes = ClaudeCodeOptions(
    # Controles básicos
    temperature=0.7,           # Criatividade (0=preciso, 1=criativo)
    max_turns=3,              # Turnos de conversa

    # Ferramentas permitidas
    allowed_tools=["Read", "Write", "Edit"],

    # System prompt customizado
    system_prompt="Você é um expert em Python"
)

# Usar com query
async for msg in query("Crie uma função", options=opcoes):
    print(msg)
```

**📚 Pratique**: `python examples/exercicios_praticos_pt_br.py 2`

### 3. Ferramentas (Tools) - Superpoderes
```python
# Claude pode usar ferramentas para:
ferramentas_disponiveis = {
    "Read": "Ler arquivos",
    "Write": "Criar arquivos",
    "Edit": "Editar arquivos",
    "Bash": "Executar comandos",
    "Grep": "Buscar em código",
    "WebSearch": "Pesquisar na web"
}

# Exemplo prático
opcoes = ClaudeCodeOptions(
    allowed_tools=["Read", "Write"]
)

prompt = "Leia o README.md e crie um resumo.txt"
async for msg in query(prompt, options=opcoes):
    # Claude vai ler e escrever automaticamente!
    pass
```

**📚 Pratique**: `python examples/exercicios_praticos_pt_br.py 3`

## 🔴 GAPS CRÍTICOS - FOQUE AQUI!

### Gap 1: MCP Tools (Exercício 4)
```python
# Criar ferramentas customizadas
from claude_code_sdk import tool, create_sdk_mcp_server

@tool(name="calc", description="Calculadora")
async def calc_tool(args):
    return {"result": eval(args["expr"])}

# VOCÊ PRECISA DOMINAR ISSO!
```
**⚠️ CRÍTICO**: Dedique 3 semanas ao exercício 4

### Gap 2: Hooks System (Exercício 5)
```python
# Interceptar e modificar comportamento
from claude_code_sdk import HookMatcher

hooks = [
    HookMatcher(
        matcher="PreToolUse",
        hooks=[validar_antes]
    )
]

# VOCÊ PRECISA DOMINAR ISSO!
```
**⚠️ CRÍTICO**: Dedique 3 semanas ao exercício 5

## 📁 ESTRUTURA DO SDK

```
src/claude_code_sdk/
├── query.py          # ← COMECE AQUI
├── client.py         # Sessões interativas
├── types.py          # ClaudeCodeOptions
├── _errors.py        # Tratamento de erros
└── _internal/
    └── transport/    # Comunicação com CLI
```

## 🎮 SEU PRIMEIRO PROGRAMA

```bash
# Execute AGORA:
python examples/01_hello_claude.py

# Depois siga a sequência:
python examples/exercicios_praticos_pt_br.py 1  # query()
python examples/exercicios_praticos_pt_br.py 2  # options
python examples/exercicios_praticos_pt_br.py 3  # tools
```

## 📊 STATUS ATUAL - DIEGO FORNALHA

```python
seu_progresso = {
    "score": 45,
    "semana": 1,
    "proximo": "python examples/01_hello_claude.py",
    "gaps": ["MCP Tools", "Hooks"],
    "meta": "Score 95 em 12 semanas"
}
```

## 🚨 REGRAS DE OURO

1. **SEMPRE use async/await** - O SDK é assíncrono
2. **NUNCA use API keys** - Use `claude login`
3. **FOQUE nos gaps** - Exercícios 4 e 5 são críticos
4. **PRATIQUE diariamente** - Use `/daily-progress`

## 📈 Neo4j Tracking

```cypher
CREATE (p:Learning {
    type: 'sdk_basics_completed',
    learner: 'Diego Fornalha',
    concepts: ['query', 'options', 'tools'],
    timestamp: datetime()
})
```

## 🎯 PRÓXIMOS PASSOS IMEDIATOS

1. **AGORA**: Feche este help
2. **EXECUTE**: `python examples/01_hello_claude.py`
3. **PRATIQUE**: Exercícios 1, 2, 3 hoje
4. **AMANHÃ**: Continue com exercício 4 (MCP)

---

**Claude Code SDK: Zero to Expert em 12 semanas! 🚀**
*Criado por Diego Fornalha*