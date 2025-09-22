# CLAUDE.md

Este arquivo fornece orientação ao Claude Code (claude.ai/code) ao trabalhar com código neste repositório.

## Arquitetura Central do Repositório

Este é o Anthropic Cookbook oficial - uma coleção de exemplos práticos de código e padrões para trabalhar com Claude. O repositório demonstra implementações do mundo real em diferentes níveis de complexidade.

### Regra Crítica de Autenticação

**NUNCA use ANTHROPIC_API_KEY** - Todos os exemplos devem usar Claude Code SDK com autenticação `claude login`:
- ❌ `anthropic.Anthropic(api_key=...)`
- ✅ `ClaudeSDKClient(options=ClaudeCodeOptions(...))`

Hooks ativamente previnem uso de API key e migram código legado automaticamente.

## Comandos de Desenvolvimento

```bash
# Instalar dependências
pip install -e ".[dev]"

# Executar linting
ruff check .
ruff format .

# Validar notebooks
python scripts/validate_notebooks.py <caminho_notebook>
python scripts/validate_all_notebooks.py

# Testar notebooks com pytest
pytest --nbval <notebook.ipynb>

# Executar notebook
jupyter nbconvert --execute --to notebook --inplace <notebook.ipynb>
```

## Arquitetura de Alto Nível

### Organização do Conteúdo
- **skills/** - Capacidades centrais do Claude (RAG, classificação, sumarização)
  - Cada skill tem exemplos progressivos: básico → intermediário → avançado
  - Exemplos RAG devem preferir Neo4j GraphRAG sobre busca vetorial tradicional

- **tool_use/** - Padrões de integração de ferramentas
  - Sistemas de memória, agentes de atendimento, extração estruturada
  - Todos exemplos usam parâmetro `allowed_tools` em ClaudeCodeOptions

- **multimodal/** - Processamento de visão e documentos
  - Análise de imagem, extração PDF, interpretação de gráficos
  - Padrões de sub-agente com Haiku para eficiência

- **third_party/** - Integrações com serviços externos
  - Bancos vetoriais (Pinecone), busca (Brave), embeddings (Voyage AI)
  - Integração via servidores MCP quando disponível

- **claude_code_sdk/** - Exemplos específicos do SDK (prioridade)
  - 00_The_one_liner_research_agent.ipynb - Uso básico de query()
  - 01_The_chief_of_staff_agent.ipynb - Hooks, CLAUDE.md, subagentes
  - 02_The_observability_agent.ipynb - Servidores MCP, sistemas multi-agente

### Camada de Configuração (.claude/)
- **agents/** - Subagentes definidos em markdown com frontmatter + system prompt
- **commands/** - Comandos slash para atalhos do usuário
- **hooks/** - Automação e governança
  - api-key-guard.py - Bloqueia API keys, migra código automaticamente
  - dependency-installer.py - Mapeia imports para pacotes pip (50+ mapeamentos)
  - notebook-tracker.py - Rastreia uso, extrai padrões, gera insights

## Padrões Arquiteturais Chave

### Caminho de Aprendizado Progressivo
1. **Iniciante** (🌱): `query()` básico, ferramentas simples
2. **Intermediário** (🌿): Subagentes, hooks, CLAUDE.md
3. **Avançado** (🌳): Servidores MCP, orquestração multi-agente
4. **Expert** (🏆): Sistemas em produção com Neo4j GraphRAG

### Padrão de Migração SDK
Código API legado é automaticamente convertido:
```python
# Antes (bloqueado pelos hooks)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
response = client.messages.create(...)

# Depois (auto-migrado)
async for msg in query(
    prompt="...",
    options=ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
):
    result = msg.result
```

### Arquitetura de Subagentes
Agentes definidos via markdown habilitam delegação:
```python
options = ClaudeCodeOptions(
    allowed_tools=["Task"],  # Habilita delegação para subagentes
    system_prompt="Delegar análise para agente pattern-analyzer"
)
```

### Integração Neo4j GraphRAG
Preferido sobre RAG tradicional - fornece 20%+ melhores métricas:
- Relacionamentos contextuais entre documentos
- Capacidades de raciocínio multi-hop
- Persistência de memória de aprendizado

## Trabalhando com Exemplos

### Encontrando Código Relevante
Use `/find-example <tópico>` ou padrões de busca:
- Exemplos RAG: `skills/retrieval_augmented_generation/`
- Padrões SDK: `claude_code_sdk/*.ipynb`
- Uso de ferramentas: `tool_use/*_tool.ipynb`

### Adaptando Exemplos
1. Exemplos usando API keys disparam auto-migração
2. Dependências auto-detectadas dos imports
3. Modificações rastreadas em `.claude/logs/`
4. Padrões extraídos para aprendizado contínuo

### Testando Mudanças
- Notebooks validados via plugin pytest `nbval`
- Ruff configurado para linting de notebooks (ignora E402, F401 em .ipynb)
- Scripts em `scripts/` para validação em lote

## Pontos de Integração

### Servidores MCP Disponíveis
- neo4j-memory: Persistência em grafo de conhecimento
- jira-mcp: Integração com gerenciamento de projeto
- exa: Busca web avançada e pesquisa

### Sistema de Hooks
Hooks Pre/Post uso de ferramentas fornecem:
- Aplicação de segurança (sem API keys)
- Gerenciamento de dependências (auto-instalação)
- Analytics de uso (extração de padrões)
- Persistência de aprendizado (integração Neo4j)

## Contexto Importante

- Repositório foca em **padrões práticos** não apenas amostras de código
- Cada exemplo ensina conceitos aplicáveis à produção
- Hooks ativamente guiam usuários para melhores práticas
- Todo uso de notebook gera insights de aprendizado
- Neo4j Memory rastreia padrões bem-sucedidos para reuso