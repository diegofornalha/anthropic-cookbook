# Conceito 5: Hook System

## 🧠 O que são Hooks?

### Definição Universal
Hooks são "ganchos" que interceptam execução ANTES ou DEPOIS de algo acontecer.
Permitem modificar, validar ou bloquear ações.

### Analogia do Aeroporto
```
Check-in → [HOOK: Verificar documentos] → Embarque
         ↓
    Se inválido: BLOQUEIA
    Se válido: CONTINUA
```

## 🎯 Tipos de Hooks no Claude SDK

### PreToolUse (ANTES)
```
Claude quer usar ferramenta Write
↓
[HOOK PRE: Validar se pode escrever]
↓
Se permitido → Executa Write
Se negado → Bloqueia
```

### PostToolUse (DEPOIS)
```
Claude usou ferramenta Bash
↓
Comando executado
↓
[HOOK POST: Logar comando usado]
↓
Continua normalmente
```

## 🔗 Como TypeScript e Email Agent usam

### TypeScript SDK - Hook Management
```typescript
// Visto em TypeScript
HookManager.register({
  type: 'PreToolUse',
  matcher: (tool) => tool.name === 'Bash',
  handler: validateBashCommand
});
```

### Email Agent - Hooks Práticos
```typescript
// Hook para sanitizar emails
PreToolUse: {
  tool: 'send_email',
  validate: (args) => {
    // Remove dados sensíveis
    // Valida destinatários
    // Check rate limits
  }
}
```

## 📊 Casos de Uso por Hook

| Hook Type | Quando Usar | Exemplo Real |
|-----------|-------------|--------------|
| Pre-Tool | Validação/Segurança | Bloquear rm -rf |
| Post-Tool | Logging/Analytics | Registrar uso |
| Pre-Message | Filtrar entrada | Remover PII |
| Post-Message | Processar saída | Adicionar metadata |

## 💡 Padrões que Você Verá

### Padrão 1: Validation Hook (Email Agent)
```
ANTES de enviar email:
- Validar destinatário existe
- Check limites de envio
- Sanitizar conteúdo
- Se tudo OK → envia
```

### Padrão 2: Logging Hook (TypeScript)
```
DEPOIS de qualquer tool:
- Log timestamp
- Log usuário
- Log parâmetros
- Log resultado
→ Audit trail completo!
```

### Padrão 3: Transform Hook
```
ANTES de Write:
- Adicionar header copyright
- Formatar código
- Adicionar timestamp
→ Arquivo sempre padronizado
```

## 🚀 Evolução do Conceito

### Básico (Entender conceito)
```
Hook = interceptar execução
Pre = antes
Post = depois
Return None = permite
Return {deny} = bloqueia
```

### Intermediário (Python)
```python
def pre_bash_hook(command):
    if "rm -rf /" in command:
        return {"behavior": "deny"}
    return None  # permite
```

### Avançado (Email Agent)
```typescript
// Hook com async e database
async function preEmailHook(args) {
  const user = await db.getUser(args.from);
  if (!user.canSend) {
    return {
      behavior: "deny",
      message: "User over quota"
    };
  }

  // Transform args
  args.signature = user.signature;
  return {
    behavior: "allow",
    args: args  // modificado!
  };
}
```

## 🎮 Cenários do Mundo Real

### Segurança (Você já tem!)
```python
# Seu hook atual
api-key-guard.py
→ Bloqueia uso de API keys
→ Força uso de claude login
```

### Automação (Email Agent)
```typescript
// Auto-categorização
postEmailReceived → categorizaEmail()
→ Email automaticamente organizado
```

### Compliance
```
preWrite → checkCopyright()
preCommit → checkSecrets()
→ Nunca vaza informação sensível
```

## ⚠️ Insights Importantes

### Do TypeScript SDK:
```
Hooks podem ser CHAINADOS
Multiple hooks no mesmo evento
Executam em ordem
```

### Do Email Agent:
```
Hooks podem ser ASYNC
Podem fazer I/O (database, API)
Podem transformar argumentos
```

## 🏗️ Preparação para o Futuro

### O que verá em TypeScript:
- HookManager class
- Hook composition
- Async hooks
- Hook middleware pattern

### O que verá em Email Agent:
- 15+ hooks diferentes
- Hooks que chamam MCP tools
- Hooks com side effects
- Rate limiting via hooks

## ✅ Teste de Compreensão

1. Diferença entre Pre e Post hooks?
2. Como bloquear uma ação?
3. Como Email Agent usa hooks para segurança?
4. Hooks podem modificar argumentos?

## 🎓 Você entendeu quando...

- Sabe quando usar Pre vs Post
- Entende return None vs return {deny}
- Vê hooks como middleware
- Consegue imaginar hooks para seu projeto

---

## 🔄 Conexão com Seus Arquivos

Você JÁ está usando hooks!
```
.claude/hooks/
├── api-key-guard.py       # PreToolUse - segurança
├── bootcamp-tracker.py    # PostToolUse - tracking
└── sdk-auto-helper.py     # PreMessage - ajuda
```

Quando chegar no Email Agent, verá os MESMOS conceitos, só que mais avançados!

---

**Próximo**: Voltar para implementação Python com estes conceitos em mente!