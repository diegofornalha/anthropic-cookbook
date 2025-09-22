# Building Powerful Agents com the Claude Code SDK

A Tutorial series demonstrating como para construir sophisticated general-purpose agentic systems using the [Claude Code SDK](https://github.com/anthropics/claude-code-sdk-python), progressing de simples research agents para multi-agent orchestration com externo system integração.

## Começando

#### 1. instalar uv, [node](https://nodejs.org/en/baixar/), e the Claude Code CLI (se you haven't already)

```curl -LsSf https://astral.sh/uv/install.sh | sh ```

```npm install -g @anthropic-ai/claude-code```

#### 2. clonar e set up the projeto

```git clone https://github.com/anthropics/anthropic-cookbook.git ```

```cd anthropic-cookbook/claude_code_sdk```

```uv sync ```

#### 3. Register venv as Jupyter kernel so aquele you can use it in the notebooks

```uv run python -m ipykernel install --user --name="cc-sdk-tutorial" --display-name "Python (cc-sdk-tutorial)" ```

#### 4. Anthropic API Key
1. Visit [console.anthropic.com](https://console.anthropic.com/painel)
2. Sign up ou log in para your conta
3. Click on "Get API keys"
4. copiar the key e colar it into your `.env` arquivo as ```ANTHROPIC_API_KEY=```

#### 5. GitHub Token for Notebook 02
se you plan para work through the Observability Agent notebook:
1. Get a GitHub Personal Access Token [aqui](https://github.com/configurações/personal-access-tokens/novo)
2. Select "Fine-grained" token com padrão opções (público repos, no conta permissions)
3. adicionar it para your `.env` arquivo as `GITHUB_TOKEN="<token>"`
4. Ensure [Docker](https://www.docker.com/products/docker-desktop/) is running on your machine

## Tutorial Series Visão Geral

este Tutorial series takes you on a journey de basic agent implementation para sophisticated multi-agent systems capable of handling real-world complexity. Each notebook builds upon the anterior one, introducing novo concepts e capabilities while maintaining practical, produção-ready implementations.

### o que You'll Learn

Through este series, you'll be exposed para:
- **Core SDK fundamentals** com `query()` e the `ClaudeSDKClient` & `ClaudeCodeOptions` interfaces in the Python SDK
- **Tool Uso patterns** de basic WebSearch para complexo MCP servidor integração
- **Multi-agent orchestration** com specialized subagents e coordination
- **Enterprise Recursos** by leveraging hooks for compliance tracking e audit trails
- **externo system integração** via Model Context Protocol (MCP)

Nota: este Tutorial assumes you have alguns level of familiarity com Claude Code. Ideally, se you have been using Claude Code para supercharge your coding tasks e would like para leverage its raw agentic power for tasks beyond Software Engineering, este Tutorial will help you get started.

## Notebook Structure & Content

### [Notebook 00: The One-Liner Research Agent](00_The_one_liner_research_agent.ipynb)

iniciar your journey com a simples yet powerful research agent built in just a poucos lines of code. este notebook introduces core SDK concepts e demonstrates como the Claude Code SDK enables autonomous information gathering e synthesis.

**Key Concepts:**
- Basic agent loops com `query()` e async iteration
- WebSearch tool for autonomous research
- Multimodal capabilities com the ler tool
- Conversation context management com `ClaudeSDKClient`
- System prompts for agent specialization

### [Notebook 01: The Chief of Staff Agent](01_The_chief_of_staff_agent.ipynb)

construir a comprehensive AI Chief of Staff for a startup CEO, showcasing avançado SDK Recursos for produção environments. este notebook demonstrates como para criar sophisticated agent architectures com governance, compliance, e specialized expertise.

**Key Recursos Explored:**
- **memória & Context:** Persistent instructions com CLAUDE.md arquivos
- **saída Styles:** Tailored communication for different audiences
- **Plan Mode:** Strategic planning sem execution for complexo tasks
- **personalizado Slash comandos:** usuário-friendly shortcuts for common operations
- **Hooks:** Automated compliance tracking e audit trails
- **Subagent Orchestration:** Coordinating specialized agents for domain expertise
- **Bash Tool integração:** Python script execution for procedural knowledge e complexo computations

### [Notebook 02: The Observability Agent](02_The_observability_agent.ipynb)

Expand beyond local capabilities by connecting agents para externo systems through the Model Context Protocol. Transform your agent de a passivo observer into an ativo participant in DevOps workflows.

**avançado Capabilities:**
- **Git MCP servidor:** 13+ tools for repositório analysis e versão control
- **GitHub MCP servidor:** 100+ tools for completo GitHub platform integração
- **Real-tempo monitoramento:** CI/CD pipeline analysis e falha detection
- **Intelligent Incident resposta:** Automated root cause analysis
- **produção fluxo de trabalho automação:** de monitoramento para actionable insights

## completo Agent Implementations

Each notebook includes an agent implementation in its respective diretório:
- **`research_agent/`** - Autonomous research agent com web buscar e multimodal analysis
- **`chief_of_staff_agent/`** - Multi-agent executive assistant com financial modeling e compliance
- **`observability_agent/`** - DevOps monitoramento agent com GitHub integração

## Background
### The Evolution of Claude Code SDK

Claude Code has emerged as one of Anthropic's maioria successful products, but não just for its SOTA coding capabilities. Its true breakthrough lies in something mais fundamental: **Claude is exceptionally good at agentic work**.

o que makes Claude Code special isn't just code understanding; it's the ability para:
- Break down complexo tasks into manageable steps autonomously
- Use tools effectively e make intelligent decisions sobre qual tools para use e quando
- Maintain context e memória across long-running tasks
- Recover gracefully de erros e adapt approaches quando needed
- Know quando para ask for clarification versus quando para proceed com reasonable assumptions

estes capabilities have made Claude Code the closest thing para a "bare metal" harness for Claude's raw agentic power: a minimal yet completo e sophisticated interface aquele lets the model's capabilities shine com the mínimo possible overhead.

### Beyond Coding: The Agent Builder's Toolkit

Originally an interno tool built by Anthropic engineers para accelerate desenvolvimento workflows, the SDK's público lançamento revealed unexpected potential. depois the lançamento of the Claude Code SDK e its GitHub integração, developers began using it for tasks far beyond coding:

- **Research agents** aquele gather e synthesize information across multiple sources
- **Data analysis agents** aquele explore datasets e generate insights
- **fluxo de trabalho automação agents** aquele handle repetitive business processes
- **monitoramento e observability agents** aquele watch systems e respond para issues
- **Content generation agents** aquele criar e refine various types of content

The pattern was limpar: the SDK had inadvertently become an effective agent-building framework. Its Arquitetura, designed para handle software desenvolvimento complexity, proved remarkably well-suited for general-purpose agent creation.

este Tutorial series demonstrates como para leverage the Claude Code SDK para construir highly efficient agents for any domain ou use case, de simples automação para complexo enterprise systems. 

## Contribuindo

Found an problema ou have a suggestion? Please abrir an problema ou enviar a pull requisição!
