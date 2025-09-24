# 🧪 03 - Testes e Validações

## Objetivo
Validar conceitos e estruturas do Claude Code SDK

## Arquivos

### `step_04_testar_blocos.py`
- **Propósito**: Testar estrutura de tipos de blocos
- **Conceitos**: TextBlock, ThinkingBlock, ToolUseBlock, ToolResultBlock
- **Status**: ✅ Funcionando

### `step_05_testar_blocos_avancado.py`
- **Propósito**: Teste avançado de todos os tipos de blocos
- **Conceitos**: Forçar uso de ferramentas, tipos de mensagens
- **Status**: ✅ Funcionando

## Como Executar

```bash
# Teste básico de blocos
/opt/homebrew/bin/python3.10 step_04_testar_blocos.py

# Teste avançado de blocos
/opt/homebrew/bin/python3.10 step_05_testar_blocos_avancado.py
```

## Resultados dos Testes

### ✅ Tipos de Blocos Confirmados

1. **TextBlock** 📝
   - Acesso via `bloco.text`
   - Funcionando perfeitamente

2. **ToolUseBlock** 🛠️
   - Acesso via `bloco.name`, `bloco.id`, `bloco.input`
   - Funcionando perfeitamente

3. **ToolResultBlock** ✅
   - Acesso via `bloco.tool_use_id`, `bloco.content`, `bloco.is_error`
   - Funcionando perfeitamente

### ✅ Tipos de Mensagens Confirmados

1. **SystemMessage** - Mensagens do sistema
2. **AssistantMessage** - Respostas do Claude
3. **UserMessage** - Entradas do usuário
4. **ResultMessage** - Metadados da sessão

## Estrutura Real Confirmada

```
Message
├── SystemMessage (sem content)
├── AssistantMessage
│   └── content: list[ContentBlock]
│       ├── TextBlock.text
│       └── ToolUseBlock (name, id, input)
├── UserMessage
│   └── content: list[ContentBlock]
│       └── ToolResultBlock (tool_use_id, content, is_error)
└── ResultMessage (sem content, com metadados)
```

## Conclusões

- ✅ **Código Funciona**: A estrutura de blocos está correta
- ✅ **Acesso Funciona**: `hasattr()` e atributos funcionam perfeitamente
- ✅ **Tipos Confirmados**: Todos os tipos de blocos funcionam
- ✅ **Estrutura Real**: Mensagens têm `content` como lista de blocos
- ✅ **Permissões**: Ferramentas precisam de permissão (comportamento esperado)

## Próximos Passos

1. **Exercício 1**: Implementar processamento de blocos
2. **Exercício 2**: Criar funções para cada tipo de bloco
3. **Exercício 3**: Implementar tratamento de erros robusto
