# Conceito 3: Tool Permissions

## 🧠 O que são Tool Permissions?

### Conceito Central
Claude pode executar ações no seu sistema através de "ferramentas" (tools).
Permissions controlam QUAIS ferramentas Claude pode usar.

### Analogia do Mundo Real
```
Estagiário → Só pode LER documentos
Funcionário → Pode LER e EDITAR
Gerente → Pode LER, EDITAR e DELETAR
Admin → Acesso total
```

## 🔧 Ferramentas Universais do SDK

### Ferramentas de Leitura (Read-Only)
- **Read** - Ler arquivos
- **Glob** - Buscar arquivos por padrão
- **Grep** - Buscar conteúdo em arquivos
- **WebFetch** - Buscar informações da web

### Ferramentas de Escrita (Modificação)
- **Write** - Criar/sobrescrever arquivos
- **Edit** - Modificar arquivos existentes
- **MultiEdit** - Múltiplas edições

### Ferramentas de Sistema
- **Bash** - Executar comandos
- **Task** - Delegar para sub-agentes

## 📊 Níveis de Permissão

| Nível | Permite | Use Case |
|-------|---------|----------|
| Read-Only | Apenas leitura | Análise, revisão |
| Edit | Leitura + Edição | Desenvolvimento |
| Full | Todas ferramentas | Automação completa |
| Custom | Seleção específica | Controle granular |

## 🎯 Padrões de Controle

### Padrão 1: Whitelist (Permitir específicas)
```
PERMITIR apenas [Read, Grep]
// Só essas duas funcionam
```

### Padrão 2: Blacklist (Negar específicas)
```
NEGAR [Bash, Write]
// Todas exceto essas
```

### Padrão 3: Modo Permissivo (Skip)
```
PULAR_PERMISSÕES
// Confia totalmente (desenvolvimento)
```

## 💡 Conceitos que Conectam com TypeScript

### Fluent API (TS) - Permissões Encadeadas
```
No TypeScript:
.allowTools('Read', 'Write')
.denyTools('Bash')
.skipPermissions()

Conceito: Configuração progressiva de permissões
```

### Permission Manager (TS) - Controle Granular
```
No TypeScript existe PermissionManager
Conceito: Objeto dedicado para gerenciar permissões
Benefício: Reutilização e consistência
```

## 🔗 Conexão com Email Agent

### Email Agent usa permissões para:
1. **Read** - Ler emails via IMAP
2. **Write** - Salvar drafts
3. **SQLite** - Cache local (tool customizada)
4. **WebSocket** - Comunicação real-time

### Insight do Email Agent:
```
Ferramentas CUSTOMIZADAS também precisam permissões!
MCP Tools = Suas próprias ferramentas
Mesmo sistema de permissões aplica
```

## 🚀 Evolução do Conceito

### Nível Iniciante (Python)
```python
allowed_tools=["Read"]  # Básico
```

### Nível Intermediário (TypeScript)
```typescript
.allowTools('Read', 'Write')  # Fluent
.withPermissions('acceptEdits')  # Modos
```

### Nível Avançado (Email Agent)
```typescript
// Permissões contextuais
if (user.role === 'admin') {
  allowTools.push('DeleteEmail');
}
```

## ✅ Teste de Compreensão

1. Por que limitar ferramentas?
2. Quando usar read-only?
3. Como Email Agent usa permissões custom?
4. O que é modo permissivo e quando usar?

## 🎮 Cenários Práticos

### Cenário 1: Code Review
```
Ferramentas: [Read, Grep]
Por quê: Só precisa analisar, não modificar
```

### Cenário 2: Desenvolvimento
```
Ferramentas: [Read, Write, Edit, Bash]
Por quê: Precisa criar e testar código
```

### Cenário 3: Email Assistant
```
Ferramentas: [IMAP_Read, Draft_Write, Search]
Por quê: Ferramentas específicas do domínio
```

## 🏗️ Preparação para o Futuro

### O que você verá em TypeScript:
- PermissionManager class
- Per-call permissions
- Dynamic permission switching

### O que você verá em Email Agent:
- Custom MCP tools
- Domain-specific permissions
- Real-time permission updates

## 🎓 Você entendeu quando...

- Sabe escolher ferramentas para cada tarefa
- Entende segurança vs funcionalidade
- Consegue criar estratégia de permissões
- Vê como Email Agent estende este conceito

---

**Próximo conceito**: [04_mcp_protocol.md](./04_mcp_protocol.md)