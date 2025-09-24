# 🚀 04 - Conceitos Avançados

## Objetivo
Dominar conceitos avançados do Claude Code SDK

## Arquivos

### `step_06_exemplos_avancados.py`
- **Propósito**: Exemplos de conceitos avançados
- **Conceitos**: Type hints, tratamento de erros, configurações
- **Status**: ✅ Funcionando

### `step_07_configuracoes_corretas.py`
- **Propósito**: Mostrar o que funciona vs o que não funciona
- **Conceitos**: Configurações válidas, alternativas para temperature
- **Status**: ✅ Funcionando

## Como Executar

```bash
# Exemplos avançados
/opt/homebrew/bin/python3.10 step_06_exemplos_avancados.py

# Configurações corretas
/opt/homebrew/bin/python3.10 step_07_configuracoes_corretas.py
```

## Conceitos Avançados

### ✅ Type Hints
```python
from typing import AsyncIterator, Optional
from claude_code_sdk import Message

async def consultar(prompt: str) -> AsyncIterator[Message]:
    async for mensagem in query(prompt=prompt):
        yield mensagem
```

### ✅ Tratamento de Erros
```python
try:
    async for msg in query(prompt):
        # processar
except ConnectionError as e:
    print(f"Erro de conexão: {e}")
except Exception as e:
    print(f"Erro geral: {e}")
```

### ✅ Configurações que FUNCIONAM
```python
opcoes = ClaudeCodeOptions(
    system_prompt="Você é um especialista",
    permission_mode="plan",
    cwd="/tmp",
    model="claude-sonnet-4-20250514"
)
```

### ❌ Configurações que NÃO FUNCIONAM
```python
# ❌ Estes parâmetros não existem
opcoes = ClaudeCodeOptions(
    temperature=0.9,    # ❌ Não existe
    max_tokens=1000,    # ❌ Não existe
    top_p=0.9          # ❌ Não existe
)
```

### 🎨 Alternativas para Temperature
```python
# ✅ Use system_prompt para controlar criatividade
opcoes_criativo = ClaudeCodeOptions(
    system_prompt="Você é um escritor criativo e poético"
)

opcoes_preciso = ClaudeCodeOptions(
    system_prompt="Você é um técnico preciso. Seja direto e objetivo"
)
```

## Funcionalidades Demonstradas

- ✅ **Type Hints**: `AsyncIterator`, `Optional`, `Message`
- ✅ **Tratamento de Erros**: `try/except` com tipos específicos
- ✅ **Configurações Válidas**: `system_prompt`, `permission_mode`, `cwd`
- ✅ **Configurações Inválidas**: `temperature`, `max_tokens`, `top_p`
- ✅ **Alternativas**: System prompt para controlar criatividade
- ✅ **AsyncIterator**: Funções personalizadas com type safety
- ✅ **Configuração Completa**: Todas as opções válidas

## Próximos Passos

1. **Exercício 4**: Implementar MCP Tools
2. **Exercício 5**: Dominar Hooks System
3. **Exercício 6**: Streaming e Client
4. **Exercício 7**: Multi-Agent

## Resumo

- ✅ **FUNCIONA**: `system_prompt`, `permission_mode`, `cwd`, `model`
- ❌ **NÃO FUNCIONA**: `temperature`, `max_tokens`, `top_p`
- 🎨 **ALTERNATIVA**: Use `system_prompt` para controlar criatividade
- 🛡️ **TRATAMENTO**: Use `try/except` com tipos específicos
- 🔍 **TYPE HINTS**: Use `AsyncIterator`, `Optional`, etc.
