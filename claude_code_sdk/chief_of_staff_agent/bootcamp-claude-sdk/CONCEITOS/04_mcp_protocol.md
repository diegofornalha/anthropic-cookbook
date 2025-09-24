# Conceito 4: MCP Protocol (Model Context Protocol)

## 🧠 O que é MCP?

### Definição Universal
MCP permite criar suas PRÓPRIAS ferramentas que Claude pode usar.
É um protocolo, não uma implementação - funciona em qualquer linguagem.

### Analogia
```
Ferramentas Nativas = Apps pré-instalados no celular
MCP Tools = Apps que você instala da loja
Mesmo sistema, ferramentas customizadas
```

## 🎯 Estrutura Universal MCP

### Todo MCP Tool tem:
1. **Nome** - Identificador único
2. **Descrição** - O que faz (Claude lê isso!)
3. **Schema** - Parâmetros esperados
4. **Handler** - Função que executa

### Formato de Resposta UNIVERSAL:
```json
{
  "content": [
    {
      "type": "text",
      "text": "resultado aqui"
    }
  ]
}
```
**SEMPRE este formato, em QUALQUER linguagem!**

## 🔗 Como conecta com TypeScript e Email Agent

### No TypeScript SDK:
```typescript
// Viu no fluent.ts
.allowTools('MCPTool')  // Permite tools MCP
```

### No Email Agent:
```typescript
// Tools customizadas para email
@tool({
  name: "search_emails",
  description: "Busca emails por termo"
})
async function searchEmails(args) {
  // Busca no IMAP
  return {
    content: [{
      type: "text",
      text: JSON.stringify(emails)
    }]
  };
}
```

## 📊 MCP vs Native Tools

| Aspecto | Native Tools | MCP Tools |
|---------|--------------|-----------|
| Criador | Anthropic | Você |
| Customização | Não | Total |
| Instalação | Já vem | Você adiciona |
| Uso | Universal | Específico |

## 💡 Insights do Email Agent

### Email Agent tem MCP tools para:
1. **IMAP operations** - Ler/buscar emails
2. **SQLite queries** - Cache local
3. **Draft management** - Criar/editar rascunhos
4. **Contact extraction** - Análise de contatos

### Padrão importante:
```
Email Agent não usa Bash ou Write genéricos
Usa MCP tools ESPECÍFICAS para email
Mais seguro e preciso!
```

## 🚀 Evolução do Conceito

### Básico (Entender protocolo)
```
MCP = criar suas ferramentas
Retorno = {"content": [...]}
```

### Intermediário (Python)
```python
@tool(name="calculator")
async def calc(args: Dict) -> Dict:
    result = args["a"] + args["b"]
    return {
        "content": [{
            "type": "text",
            "text": str(result)
        }]
    }
```

### Avançado (TypeScript Email)
```typescript
// Tool com side effects e database
@tool({
  name: "save_draft",
  schema: draftSchema
})
async function saveDraft(args) {
  const id = await db.insert(args.draft);
  await syncWithIMAP(id);
  return formatMCPResponse(id);
}
```

## 🎮 Casos de Uso Reais

### Python Automation
```
MCP Tool: backup_database
Ação: Fazer backup do PostgreSQL
Retorno: Status e localização
```

### TypeScript Web App
```
MCP Tool: analytics_query
Ação: Buscar métricas do Google Analytics
Retorno: JSON com dados
```

### Email Agent
```
MCP Tool: smart_reply
Ação: Gerar resposta contextual
Retorno: Draft do email
```

## ⚠️ Erros Comuns (que você verá no Email Agent)

### ❌ Erro 1: Formato errado
```javascript
return "resultado";  // ERRADO!
```

### ✅ Correto:
```javascript
return {
  content: [{
    type: "text",
    text: "resultado"
  }]
};
```

### ❌ Erro 2: Pensar que é API REST
```
MCP tools são LOCAIS, não endpoints!
Email Agent roda na SUA máquina
```

## 🏗️ Preparação para o Futuro

### O que verá em TypeScript:
- Decorators para MCP tools
- Schema validation automático
- Type safety total

### O que verá em Email Agent:
- 10+ MCP tools específicas
- Composição de tools
- Tools que chamam outras tools

## ✅ Teste de Compreensão

1. Qual a diferença entre tool nativa e MCP?
2. Qual formato de retorno é OBRIGATÓRIO?
3. Como Email Agent usa MCP para emails?
4. Por que MCP é "protocol" não "implementation"?

## 🎓 Você entendeu quando...

- Sabe criar uma MCP tool mental
- Entende o formato de retorno universal
- Vê como Email Agent é só MCP tools
- Consegue imaginar suas próprias tools

---

**Próximo conceito**: [05_hook_system.md](./05_hook_system.md)