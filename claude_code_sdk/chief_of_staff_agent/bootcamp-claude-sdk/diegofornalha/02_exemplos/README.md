# 🚀 02 - Exemplos Práticos

## Objetivo
Demonstrar funcionalidades práticas do agente personalizado

## Arquivos

### `step_01_executar_agente.py`
- **Propósito**: Teste básico do agente Chefe de Gabinete
- **Funcionalidades**: `send_query()`, `permission_mode="plan"`
- **Status**: ✅ Funcionando

### `step_02_agente_avancado.py`
- **Propósito**: Demonstração avançada com subagentes
- **Funcionalidades**: Subagentes, comandos slash, scripts customizados
- **Status**: ✅ Funcionando

### `step_03_agente_personalizado.py`
- **Propósito**: Agente personalizado para Diego Fornalha
- **Funcionalidades**: Contexto específico, Neo4j Memory, bootcamp
- **Status**: ✅ Funcionando

## Como Executar

```bash
# Teste básico
/opt/homebrew/bin/python3.10 step_01_executar_agente.py

# Demonstração avançada
/opt/homebrew/bin/python3.10 step_02_agente_avancado.py

# Agente personalizado
/opt/homebrew/bin/python3.10 step_03_agente_personalizado.py
```

## Funcionalidades Demonstradas

- ✅ **Subagentes**: CTO e Recrutador via `Task`
- ✅ **Comandos Slash**: `/budget-impact` e outros
- ✅ **Scripts Customizados**: Python via `Bash`
- ✅ **Estilos de Saída**: `executive`, `technical`
- ✅ **Integração Neo4j**: Acesso ao progresso
- ✅ **Modos de Permissão**: `plan`, `default`, `acceptEdits`

## Casos de Uso

1. **Análise Executiva**: Relatórios de status
2. **Tomada de Decisão**: Scripts de decisão estratégica
3. **Gestão de Talentos**: Avaliação de candidatos
4. **Planejamento**: Modo "plan" para análise
5. **Automação**: Execução de scripts Python

## Próximos Passos

1. **Exercício 4**: Implementar MCP Tools
2. **Exercício 5**: Dominar Hooks System
3. **Exercício 6**: Streaming e Client
4. **Exercício 7**: Multi-Agent
