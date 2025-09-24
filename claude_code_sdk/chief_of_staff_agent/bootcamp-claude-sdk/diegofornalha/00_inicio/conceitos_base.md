# 📚 Conceitos Base - Claude Code SDK

cd /Users/2a/.claude/anthropic-cookbook/claude_code_sdk/chief_of_staff_agent/diegofornalha/00_inicio && source ../00_inicio/venv/bin/activate && python teste_ambiente.py





## 🎯 O que você precisa entender ANTES de codar

### 1. O que é Claude Code SDK?

É uma biblioteca Python que permite conversar com Claude diretamente do seu código, **sem precisar de API keys**.

**Analogia**: É como ter Claude como seu pair programmer, mas dentro do Python.

### 2. Stateless vs Stateful

#### 🔵 **Stateless (query)**
- Cada pergunta é independente
- Claude não lembra da anterior
- Como fazer perguntas para um professor novo a cada vez

**Quando usar**: Perguntas isoladas, traduções, análises únicas

#### 🔴 **Stateful (ClaudeSDKClient)**
- Claude mantém contexto
- Lembra de tudo que foi dito
- Como ter uma conversa contínua

**Quando usar**: Debug iterativo, desenvolvimento progressivo, tutoriais

### 3. Por que Async/Await?

Claude pode demorar para responder. Async permite que seu programa faça outras coisas enquanto espera.

**Analogia**: Como pedir pizza por app - você não fica parado na porta esperando, faz outras coisas e recebe quando chegar.

### 4. Estrutura de uma Resposta

```python
Mensagem
├── content[]          # Lista de blocos
│   ├── TextBlock     # Texto normal
│   ├── ToolUseBlock  # Claude usando ferramenta
│   └── ThinkingBlock # Claude pensando
```

### 5. ClaudeCodeOptions - O que realmente existe

✅ **EXISTE**:
- `system_prompt`: Personalidade do Claude
- `allowed_tools`: Ferramentas permitidas
- `model`: Modelo a usar
- `max_turns`: Máximo de interações

❌ **NÃO EXISTE** (erro comum!):
- `temperature`
- `max_tokens`
- `stream`

### 6. Ferramentas Nativas

Claude pode usar ferramentas para:
- **Read**: Ler arquivos
- **Write**: Criar arquivos
- **Bash**: Executar comandos
- **Search**: Buscar na web

### 7. O que são MCP Tools?

Ferramentas customizadas que você cria para estender as capacidades do Claude.

**Analogia**: Como adicionar plugins no VSCode - você adiciona funcionalidades específicas.

### 8. O que são Hooks?

Interceptadores que controlam o que Claude pode ou não fazer.

**Analogia**: Como um segurança na porta - decide quem entra e quem não entra.

## 🎮 Resumo Visual

```
Você → query("pergunta") → Claude → Resposta
         ↓
    [Stateless]

Você ↔ ClaudeSDKClient ↔ Claude
    [Mantém conversa]
```

## ✅ Checklist de Compreensão

Antes de continuar, você entende:

- [ ] Diferença entre query() e ClaudeSDKClient?
- [ ] Por que usamos async/await?
- [ ] Que temperature NÃO existe em ClaudeCodeOptions?
- [ ] Para que servem as ferramentas?
- [ ] Conceito básico de MCP Tools?
- [ ] Conceito básico de Hooks?

Se marcou todos, está pronto para codar! 🚀

## 🚦 Próximo Passo

```bash
cd ../01_fundamentos
python hello_claude.py
```

---

*"Entender o conceito antes do código economiza horas de debug"*