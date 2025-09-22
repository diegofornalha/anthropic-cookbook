---
name: migrate-to-sdk
description: Migra código do Cookbook para usar Claude Code SDK sem API key
---

Migre o código de: {{args}}

Transformações necessárias:

1. **Autenticação:**
   - DE: `anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))`
   - PARA: `ClaudeSDKClient(options=ClaudeCodeOptions(...))`

2. **Imports:**
   - DE: `import anthropic`
   - PARA: `from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query`

3. **Chamadas:**
   - DE: `client.messages.create(...)`
   - PARA: `async for msg in query(...)` ou `await agent.query(...)`

4. **Async:**
   - Adicionar `async/await` onde necessário
   - Usar `asyncio.run()` para executar

Gere código completo migrado e testável.