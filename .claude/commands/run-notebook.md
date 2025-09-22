---
name: run-notebook
description: Executa um notebook do Cookbook com adaptações automáticas
---

Use o agente notebook-runner para executar o notebook: {{args}}

Passos:
1. Verificar e instalar dependências
2. Adaptar autenticação (remover API keys, usar SDK)
3. Ajustar paths relativos
4. Executar célula por célula
5. Aplicar correções automáticas para erros comuns
6. Gerar relatório de execução

Importante:
- Migrar ANTHROPIC_API_KEY para ClaudeSDKClient
- Adicionar retry logic se necessário
- Criar dados de exemplo se não existirem