# 🎓 Aprendizados Completos do Claude Code SDK - Anthropic Cookbook

## 📚 Visão Geral
O Anthropic Cookbook contém **3 notebooks progressivos** que ensinam desde o básico até implementações enterprise do Claude Code SDK.

**🔑 Insight Principal:** Todos os exemplos funcionam **SEM ANTHROPIC_API_KEY** - usam apenas `claude login`

---

## 🌱 NÍVEL 1: Research Agent (Beginner)
**Tempo:** 1-2 horas | **Notebook:** `00_The_one_liner_research_agent.ipynb`

### Aprendizados Fundamentais

#### 1. **One-Liner Agent**
```python
# Agente funcional em literalmente 1 linha!
async for msg in query(prompt="Research AI", options=ClaudeCodeOptions(allowed_tools=["WebSearch"])): print(msg)
```
**Aprendizado:** A simplicidade do SDK permite criar agentes funcionais instantaneamente.

#### 2. **Padrão Async Iterator**
```python
async for msg in query(prompt="...", options=options):
    if hasattr(msg, 'result'):
        result = msg.result  # Captura resultado final
    elif isinstance(msg, AssistantMessage):
        # Processa mensagem intermediária
```
**Aprendizado:** O SDK usa async iterators para streaming natural de respostas.

#### 3. **Contexto com ClaudeSDKClient**
```python
async with ClaudeSDKClient(options=options) as agent:
    await agent.query("First question")
    # ... processa resposta ...
    await agent.query("Follow-up question")  # Mantém contexto!
```
**Aprendizado:** `ClaudeSDKClient` mantém conversação sem repassar contexto manualmente.

#### 4. **Multimodal com Read Tool**
```python
options = ClaudeCodeOptions(
    allowed_tools=["WebSearch", "Read"],  # Read analisa imagens!
    cwd="research_agent"  # Diretório com imagens
)
```
**Aprendizado:** Tool `Read` é multimodal - analisa charts, diagramas, PDFs.

#### 5. **Activity Handlers Flexíveis**
```python
async def activity_handler(msg):
    # Pode ser sync ou async
    if asyncio.iscoroutinefunction(handler):
        await handler(msg)
    else:
        handler(msg)
```
**Aprendizado:** SDK aceita handlers síncronos e assíncronos para máxima flexibilidade.

---

## 🌿 NÍVEL 2: Chief of Staff Agent (Intermediate)
**Tempo:** 1 dia | **Notebook:** `01_The_chief_of_staff_agent.ipynb`

### Aprendizados Avançados

#### 1. **CLAUDE.md como Memória Persistente**
```markdown
# CLAUDE.md
## Company Context
- Monthly Burn: $500K
- Runway: 20 months
- ARR: $2.4M
```
**Aprendizado:** `CLAUDE.md` no `cwd` é automaticamente lido como contexto persistente.

#### 2. **Bash Tool para Scripts Python**
```python
# Em CLAUDE.md ou prompt:
"Use scripts/hiring_impact.py to calculate..."

# Agent executa automaticamente:
# python scripts/hiring_impact.py 3 200000
```
**Aprendizado:** Bash tool executa scripts Python para cálculos complexos e modelos.

#### 3. **Output Styles Customizados**
```python
# Em .claude/output-styles/executive.md
options = ClaudeCodeOptions(
    settings='{"outputStyle": "executive"}'  # JSON string!
)
```
**Aprendizado:** Output styles modificam completamente o tom e formato das respostas.

#### 4. **Plan Mode para Estratégia**
```python
options = ClaudeCodeOptions(
    permission_mode="plan"  # Cria plano sem executar
)
# Agent para após ExitPlanMode()
# Continue com continue_conversation=True
```
**Aprendizado:** Plan mode força planejamento antes da execução - ideal para tarefas críticas.

#### 5. **Slash Commands como Macros**
```markdown
# Em .claude/commands/budget-impact.md
---
name: budget-impact
---
Analyze budget impact of: {{args}}
```
**Uso:** `/budget-impact hiring 5 engineers`
**Aprendizado:** Slash commands são expansões client-side, não capacidades do agente.

#### 6. **Hooks para Governança**
```json
// Em .claude/settings.local.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/audit.py"
      }]
    }]
  }
}
```
**Aprendizado:** Hooks executam deterministicamente em eventos - perfeito para compliance.

#### 7. **Subagentes via Task Tool**
```markdown
# Em .claude/agents/financial-analyst.md
---
name: financial-analyst
tools: Read, Bash, WebSearch
---
You are a financial analyst...
```
```python
options = ClaudeCodeOptions(allowed_tools=["Task"])
# Agent delega automaticamente baseado na descrição
```
**Aprendizado:** Subagentes têm contexto isolado e podem trabalhar em paralelo.

---

## 🌳 NÍVEL 3: Observability Agent (Advanced)
**Tempo:** 2 dias | **Notebook:** `02_The_observability_agent.ipynb`

### Aprendizados Expert

#### 1. **MCP Servers Externos**
```python
mcp_servers = {
    "github": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_TOKEN": github_token}  # Só GitHub precisa token!
    }
}
```
**Aprendizado:** MCP permite integração com qualquer sistema externo via protocolo padrão.

#### 2. **Namespace de Tools MCP**
```python
allowed_tools = [
    "mcp__github__*",  # Todas as tools do GitHub
    "mcp__git__commit",  # Tool específica do Git
]
```
**Aprendizado:** Tools MCP têm namespace `mcp__server__tool` para evitar conflitos.

#### 3. **Múltiplos MCP Servers**
```python
mcp_servers = {
    "git": {...},      # Git local
    "github": {...},   # GitHub API
    "custom": {...}    # Seu próprio server
}
```
**Aprendizado:** Pode rodar múltiplos MCP servers simultaneamente.

---

## 🏗️ Padrões Arquiteturais

### 1. **Estrutura de Diretório Padrão**
```
agent_project/
├── .claude/
│   ├── agents/           # Definições de subagentes
│   ├── commands/         # Slash commands
│   ├── hooks/           # Scripts de hooks
│   ├── output-styles/   # Estilos de output
│   └── settings.local.json
├── scripts/             # Python scripts (Bash tool)
├── data/               # Dados para análise
├── CLAUDE.md           # Contexto persistente
└── agent.py            # Implementação principal
```

### 2. **Padrão de Agent Wrapper**
```python
class AgentWrapper:
    def __init__(self, cwd):
        self.options = ClaudeCodeOptions(cwd=cwd)

    async def execute(self, prompt):
        async with ClaudeSDKClient(options=self.options) as agent:
            await agent.query(prompt)
            async for msg in agent.receive_response():
                # Processa resposta
```

### 3. **Padrão de Delegação**
```python
# Main agent delega baseado em expertise
system_prompt = """
Delegate:
- Financial tasks → financial-analyst
- Technical tasks → tech-lead
- HR tasks → recruiter
"""
```

---

## 💡 Insights Práticos

### 1. **Autenticação**
- ❌ NUNCA: `ANTHROPIC_API_KEY` com Claude Code SDK
- ✅ SEMPRE: `claude login` no terminal
- 📝 Exceção: GitHub token para MCP, não para Claude

### 2. **Performance**
- Use `continue_conversation=True` para manter contexto
- Subagentes podem rodar em paralelo via Task tool
- MCP servers rodam como processos separados

### 3. **Debugging**
```python
# Visualizar conversação completa
from utils.agent_visualizer import visualize_conversation
visualize_conversation(messages)
```

### 4. **Progressão de Aprendizado**
1. **Dia 1:** Research Agent - Domine query() e ClaudeSDKClient
2. **Dia 2-3:** Chief of Staff - Implemente todos os 7 features
3. **Dia 4-5:** Observability - Integre com sistemas externos

### 5. **Casos de Uso Validados**
- ✅ Research e síntese de informação
- ✅ Análise financeira e modelos
- ✅ Automação DevOps
- ✅ Monitoramento CI/CD
- ✅ Governança e compliance
- ✅ Multi-agent orchestration

---

## 🚀 Próximos Passos

1. **Clone o Cookbook:**
```bash
git clone https://github.com/anthropics/anthropic-cookbook.git
cd anthropic-cookbook/claude_code_sdk
```

2. **Setup Rápido:**
```bash
npm install -g @anthropic-ai/claude-code
claude login  # NÃO precisa API key!
uv sync
```

3. **Execute Exemplos:**
```python
from research_agent.agent import send_query
result = await send_query("Research quantum computing")
```

4. **Crie Seu Agent:**
- Copie estrutura do `chief_of_staff_agent/`
- Customize CLAUDE.md com seu contexto
- Adicione seus scripts e hooks
- Defina subagentes especializados

---

## 📊 Métricas de Sucesso

| Métrica | Research | Chief | Observability |
|---------|----------|-------|---------------|
| Linhas de código | ~50 | ~200 | ~300 |
| Tempo setup | 5 min | 30 min | 1 hora |
| Features | 2 | 7 | 3 |
| Complexidade | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| ROI | Alto | Muito Alto | Enterprise |

---

## 🎯 Conclusão

O Cookbook demonstra que o Claude Code SDK é muito mais que uma ferramenta de código - é um **framework completo para construção de agentes** que podem:

1. Começar simples (5 linhas)
2. Escalar para enterprise (multi-agent + MCP)
3. Manter governança (hooks + audit)
4. Integrar com qualquer sistema (MCP protocol)
5. Funcionar SEM API keys (claude login)

**Filosofia Central:** "Bare metal harness" - interface mínima que libera o máximo poder agêntico do Claude.