# Arquitetura Claude Code SDK - Bootcamp Diego Fornalha

## 📦 Core Modules - Estrutura Principal do SDK

```mermaid
graph LR
    subgraph "Claude Code SDK Core"
        Query[query.py<br/>📝 Consultas Stateless]
        Client[client.py<br/>💬 Sessões Stateful]
        Types[types.py<br/>⚙️ ClaudeCodeOptions]
        Errors[_errors.py<br/>🚨 Tratamento Erros]
        Transport[_internal/transport<br/>🔌 Comunicação CLI]
    end

    Query --> Transport
    Client --> Transport
    Types --> Query
    Types --> Client
    Errors --> Query
    Errors --> Client

    style Query fill:#9cf,stroke:#333,stroke-width:2px
    style Client fill:#9fc,stroke:#333,stroke-width:2px
    style Types fill:#fc9,stroke:#333,stroke-width:2px
    style Transport fill:#f99,stroke:#333,stroke-width:2px
```

## 🗺️ Fluxo de Aprendizado - Diego Fornalha

```mermaid
graph TD
    Dev[👨‍💻 Diego Fornalha<br/>Score: 45/100] --> SDK[Claude Code SDK]

    SDK --> Learning[📚 Learning Path]
    SDK --> Tools[🛠️ Advanced Tools]
    SDK --> Neo4j[🧠 Neo4j Memory]

    %% Caminho de Aprendizado
    Learning --> Week1[Semana 1-2: Fundamentos<br/>✅ 01_hello_claude.py]
    Learning --> Week3[Semana 3-5: Ferramentas<br/>🔄 Exercícios 1-3]
    Learning --> Week6[Semana 6-8: MCP Tools<br/>🔴 GAP CRÍTICO]
    Learning --> Week9[Semana 9-11: Hooks<br/>🔴 GAP CRÍTICO]
    Learning --> Week12[Semana 12: Expert<br/>🎯 Meta: Score 95]

    %% Ferramentas Avançadas
    Tools --> MCP[MCP Tools<br/>@tool decorator<br/>create_sdk_mcp_server]
    Tools --> Hooks[Hooks System<br/>PreToolUse<br/>PostToolUse]
    Tools --> Agents[Multi-Agents<br/>Task delegation]

    %% Neo4j Tracking
    Neo4j --> Progress[📈 Progresso<br/>45→60→75→95]
    Neo4j --> Gaps[🔴 Gaps<br/>MCP & Hooks]
    Neo4j --> Learning_Records[📝 Aprendizados<br/>456 registros]

    style Dev fill:#ffd,stroke:#333,stroke-width:3px
    style Week6 fill:#fbb,stroke:#f00,stroke-width:3px
    style Week9 fill:#fbb,stroke:#f00,stroke-width:3px
    style Week12 fill:#bfb,stroke:#0f0,stroke-width:3px
```

## Status Atual do Projeto

### 📊 Progresso Diego Fornalha
- **Score Atual**: 45/100
- **Meta**: 95/100 em 12 semanas
- **Semana**: 1 (Fundamentos)
- **Último Comando**: `/ai-basics` ✅

### ✅ Arquivos Criados
```
claude-code-sdk-python/
├── examples/
│   ├── 01_hello_claude.py              # Primeiro programa ✅
│   ├── exercicios_praticos.py          # Original em inglês
│   └── exercicios_praticos_pt_br.py    # Tradução PT-BR ✅
├── src/claude_code_sdk/
│   ├── query.py                        # Função principal
│   ├── client.py                       # Cliente interativo
│   ├── types.py                        # Configurações
│   └── *_pt-br.py                      # Traduções
└── COMECE_AQUI.md                      # Guia inicial ✅
```


```mermaid
sequenceDiagram
    participant Diego as Diego Fornalha
    participant SDK as Claude Code SDK
    participant Neo4j as Neo4j Memory
    participant Bot as Bootcamp Tracker

    Diego->>SDK: python 01_hello_claude.py
    SDK-->>Diego: Primeiro sucesso ✅
    Diego->>Neo4j: Salva progresso
    Neo4j-->>Diego: Score: 45/100

    Diego->>SDK: exercicios_praticos_pt_br.py 1-3
    SDK-->>Diego: Fundamentos dominados ✅
    Diego->>Neo4j: Atualiza aprendizado
    Neo4j-->>Diego: Score: 60/100

    Diego->>SDK: exercicio 4 - MCP Tools 🔴
    SDK->>SDK: @tool decorator
    SDK->>SDK: create_sdk_mcp_server()
    SDK-->>Diego: Gap crítico resolvido!
    Diego->>Neo4j: Registra conquista
    Neo4j-->>Diego: Score: 75/100

    Diego->>SDK: exercicio 5 - Hooks 🔴
    SDK->>SDK: HookMatcher implementation
    SDK-->>Diego: Sistema avançado dominado!
    Diego->>Neo4j: Novo milestone
    Neo4j-->>Diego: Score: 85/100

    Diego->>SDK: exercicios 6-7
    SDK-->>Diego: Expert total!
    Diego->>Neo4j: Bootcamp completo
    Neo4j-->>Diego: Score: 95/100 🏆
```

## Comandos Essenciais

### Início Rápido
```bash
# Dia 1 - Hello World
python examples/01_hello_claude.py

# Ver todos exercícios
python examples/exercicios_praticos_pt_br.py

# Exercício específico
python examples/exercicios_praticos_pt_br.py 4

# Check-in diário
/daily-progress
```

### Neo4j Memory - Aprendizados Salvos
- ✅ Estrutura SDK documentada (ID: 428)
- ✅ Módulos principais mapeados (ID: 441)
- ✅ Conceitos básicos dominados (ID: 427)
- ✅ Gaps críticos identificados (IDs: 417, 419)
- ✅ Framework universal criado (ID: 456)

## Próximos Passos Imediatos

1. **AGORA**: `python examples/01_hello_claude.py`
2. **HOJE**: Exercícios 1-2 (query e configurações)
3. **SEMANA**: Exercícios 3-4 (pipeline e MCP Tools)
4. **CRÍTICO**: Dominar exercício 4 (MCP) e 5 (Hooks)

---

*Branch atual: feature/portuguese-translations*
*Criador: Diego Fornalha (diegofornalha@gmail.com)*