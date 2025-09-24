# 🛠️ Ecossistema de Ferramentas - Claude Code SDK

## Visão Geral
Todas as ferramentas nativas disponíveis no SDK e como se relacionam.

## Diagrama do Ecossistema

```mermaid
graph TB
    subgraph "🔧 Ferramentas de Arquivo"
        Read[Read<br/>📖 Ler arquivos]
        Write[Write<br/>✏️ Criar/Sobrescrever]
        Edit[Edit<br/>✂️ Editar linha]
        MultiEdit[MultiEdit<br/>📝 Múltiplas edições]
    end

    subgraph "🔍 Ferramentas de Busca"
        Grep[Grep<br/>🔎 Busca com regex]
        Glob[Glob<br/>📁 Busca arquivos]
        WebSearch[WebSearch<br/>🌐 Pesquisa web]
        WebFetch[WebFetch<br/>🔗 Buscar URL]
    end

    subgraph "⚡ Ferramentas de Sistema"
        Bash[Bash<br/>💻 Comandos shell]
        Execute[Execute<br/>▶️ Executar código]
        TodoWrite[TodoWrite<br/>✅ Lista tarefas]
    end

    subgraph "🤖 Ferramentas de Delegação"
        Task[Task<br/>👥 Subagentes]
    end

    Read --> Edit
    Edit --> MultiEdit
    Write --> MultiEdit

    Grep --> Glob
    WebSearch --> WebFetch

    Bash --> Execute

    Task --> Read
    Task --> Write
    Task --> Bash

    style Read fill:#9cf
    style Write fill:#9cf
    style Edit fill:#9cf
    style MultiEdit fill:#9cf

    style Grep fill:#fc9
    style Glob fill:#fc9
    style WebSearch fill:#fc9
    style WebFetch fill:#fc9

    style Bash fill:#f99
    style Execute fill:#f99
    style TodoWrite fill:#f99

    style Task fill:#9f9
```

## 📊 Matriz de Uso

| Ferramenta | Quando Usar | Exemplo | Permissão Necessária |
|------------|-------------|---------|---------------------|
| **Read** | Ler qualquer arquivo | Análise de código | `allowed_tools=["Read"]` |
| **Write** | Criar arquivo novo | Gerar relatório | `allowed_tools=["Write"]` |
| **Edit** | Modificar linha específica | Corrigir bug | `allowed_tools=["Edit"]` |
| **MultiEdit** | Várias mudanças | Refatoração | `allowed_tools=["MultiEdit"]` |
| **Grep** | Buscar em conteúdo | Achar função | `allowed_tools=["Grep"]` |
| **Glob** | Buscar arquivos | Listar *.py | `allowed_tools=["Glob"]` |
| **WebSearch** | Pesquisar online | Docs atuais | `allowed_tools=["WebSearch"]` |
| **WebFetch** | Baixar página | API docs | `allowed_tools=["WebFetch"]` |
| **Bash** | Comandos shell | git status | `allowed_tools=["Bash"]` |
| **TodoWrite** | Gerenciar tarefas | Tracking | `allowed_tools=["TodoWrite"]` |
| **Task** | Delegar trabalho | Subagentes | `allowed_tools=["Task"]` |

## 🎯 Combinações Comuns

### 📝 Para Desenvolvimento
```python
allowed_tools=["Read", "Write", "Edit", "Bash"]
```

### 🔍 Para Análise
```python
allowed_tools=["Read", "Grep", "Glob"]
```

### 🌐 Para Pesquisa
```python
allowed_tools=["WebSearch", "WebFetch", "Read"]
```

### 🤖 Para Automação
```python
allowed_tools=["Task", "TodoWrite", "Bash"]
```

## ⚠️ Restrições Importantes

```mermaid
graph LR
    subgraph "✅ Sempre Permitidas"
        A[Read]
        B[TodoWrite]
    end

    subgraph "⚠️ Cuidado"
        C[Bash]
        D[Execute]
        E[Write]
    end

    subgraph "🔒 Restringir em Produção"
        F[WebSearch]
        G[WebFetch]
    end

    style A fill:#9f9
    style B fill:#9f9
    style C fill:#ff9
    style D fill:#ff9
    style E fill:#ff9
    style F fill:#f99
    style G fill:#f99
```

## 📈 Frequência de Uso (Diego)

```mermaid
pie title Ferramentas Mais Usadas no Bootcamp
    "Read" : 30
    "Write" : 20
    "Bash" : 15
    "Edit" : 10
    "Grep" : 8
    "Task" : 7
    "WebSearch" : 5
    "Outros" : 5
```

---

*Dica: Comece com poucas ferramentas e vá adicionando conforme necessário*