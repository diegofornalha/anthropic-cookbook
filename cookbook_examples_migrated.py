"""
Exemplos do Anthropic Cookbook migrados para ClaudeSDKClient
SEM necessidade de ANTHROPIC_API_KEY - usa autenticação via claude login
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query
from claude_code_sdk import AssistantMessage, TextBlock, ToolUseBlock


# ========================================================================
# EXEMPLO 1: Research Agent - Pesquisa Web Simples
# ========================================================================

class ResearchAgent:
    """
    Agente de pesquisa que usa WebSearch e Read tools
    Baseado em: anthropic-cookbook/claude_code_sdk/00_The_one_liner_research_agent.ipynb
    """

    def __init__(self, system_prompt: str = None):
        self.system_prompt = system_prompt or "You are a research agent specialized in AI"
        self.options = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",  # Modelo mais recente
            allowed_tools=["WebSearch", "Read"],
            system_prompt=self.system_prompt
        )

    async def research_simple(self, prompt: str) -> str:
        """
        Pesquisa simples com query() - one-liner
        NÃO USA API KEY - usa autenticação do claude login
        """
        result = None
        async for msg in query(prompt=prompt, options=self.options):
            if hasattr(msg, 'result'):
                result = msg.result
            elif isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(f"🤖 {block.text[:100]}...")
        return result

    async def research_with_context(self, prompts: List[str]) -> List[str]:
        """
        Pesquisa com contexto mantido entre queries
        Usa ClaudeSDKClient para manter conversação
        """
        results = []

        async with ClaudeSDKClient(options=self.options) as agent:
            for prompt in prompts:
                await agent.query(prompt)
                async for msg in agent.receive_response():
                    if hasattr(msg, 'result'):
                        results.append(msg.result)
                        print(f"✅ Resultado obtido para: {prompt[:50]}...")

        return results

    async def analyze_image_and_research(self, image_path: str, research_prompt: str):
        """
        Analisa imagem e faz pesquisa relacionada
        Demonstra capacidade multimodal
        """
        options_with_cwd = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",
            allowed_tools=["WebSearch", "Read"],
            system_prompt=self.system_prompt,
            cwd=str(Path(image_path).parent)
        )

        async with ClaudeSDKClient(options=options_with_cwd) as agent:
            # Primeiro: analisar imagem
            await agent.query(f"Analyze the image {Path(image_path).name}")
            image_analysis = ""
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    image_analysis = msg.result
                    print(f"📊 Análise da imagem concluída")

            # Segundo: pesquisar baseado na análise
            await agent.query(research_prompt)
            research_result = ""
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    research_result = msg.result
                    print(f"🔍 Pesquisa concluída")

            return {
                "image_analysis": image_analysis,
                "research": research_result
            }


# ========================================================================
# EXEMPLO 2: Chief of Staff Agent - Multi-agente Empresarial
# ========================================================================

class ChiefOfStaffAgent:
    """
    Agente executivo com subagentes, hooks, e output styles
    Baseado em: anthropic-cookbook/claude_code_sdk/01_The_chief_of_staff_agent.ipynb
    """

    def __init__(self, cwd: str = "chief_of_staff_agent"):
        self.cwd = cwd
        self.base_options = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",
            cwd=cwd  # Diretório com CLAUDE.md, hooks, agents, etc
        )

    async def query_with_memory(self, prompt: str) -> str:
        """
        Query que usa CLAUDE.md como memória persistente
        O arquivo CLAUDE.md deve estar em self.cwd
        """
        async with ClaudeSDKClient(options=self.base_options) as agent:
            await agent.query(prompt)
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    return msg.result

    async def execute_with_bash_tools(self, prompt: str) -> Dict[str, Any]:
        """
        Executa com acesso a scripts Python via Bash
        Scripts devem estar em self.cwd/scripts/
        """
        options = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",
            cwd=self.cwd,
            allowed_tools=["Bash", "Read", "Write"]
        )

        results = {
            "script_outputs": [],
            "final_result": None
        }

        async with ClaudeSDKClient(options=options) as agent:
            await agent.query(prompt)
            async for msg in agent.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, ToolUseBlock) and block.name == "Bash":
                            results["script_outputs"].append({
                                "tool": "Bash",
                                "input": block.input
                            })
                if hasattr(msg, 'result'):
                    results["final_result"] = msg.result

        return results

    async def query_with_output_style(self, prompt: str, style: str = "executive") -> str:
        """
        Query com diferentes estilos de output
        Styles devem estar definidos em self.cwd/.claude/output-styles/
        """
        options = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",
            cwd=self.cwd,
            settings=f'{{"outputStyle": "{style}"}}'
        )

        async with ClaudeSDKClient(options=options) as agent:
            await agent.query(prompt)
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    return msg.result

    async def plan_without_execution(self, prompt: str) -> str:
        """
        Cria plano detalhado sem executar (Plan Mode)
        """
        options = ClaudeCodeOptions(
            model="claude-3-opus-20240229",  # Opus é melhor para planejamento
            cwd=self.cwd,
            permission_mode="plan"
        )

        plan = None
        async with ClaudeSDKClient(options=options) as agent:
            await agent.query(prompt)
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    plan = msg.result

        return plan

    async def use_slash_command(self, command: str) -> str:
        """
        Usa slash commands customizados
        Commands devem estar em self.cwd/.claude/commands/
        """
        async with ClaudeSDKClient(options=self.base_options) as agent:
            await agent.query(command)  # ex: "/budget-impact hiring 3 engineers"
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    return msg.result

    async def delegate_to_subagent(self, task: str, subagent_type: str) -> str:
        """
        Delega tarefa para subagente especializado
        Subagents devem estar definidos em self.cwd/.claude/agents/
        """
        options = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",
            cwd=self.cwd,
            allowed_tools=["Task"],
            system_prompt=f"Delegate this task to the {subagent_type} subagent"
        )

        async with ClaudeSDKClient(options=options) as agent:
            await agent.query(task)
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    return msg.result


# ========================================================================
# EXEMPLO 3: Observability Agent - DevOps com MCP
# ========================================================================

class ObservabilityAgent:
    """
    Agente DevOps com integração MCP para GitHub/Git
    Baseado em: anthropic-cookbook/claude_code_sdk/02_The_observability_agent.ipynb
    """

    def __init__(self, github_token: str = None):
        self.github_token = github_token

    def get_mcp_servers_config(self) -> Dict:
        """
        Configuração de MCP servers para Git e GitHub
        """
        servers = {}

        # Git MCP Server (local)
        servers["git"] = {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-git"]
        }

        # GitHub MCP Server (precisa token)
        if self.github_token:
            servers["github"] = {
                "type": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_TOKEN": self.github_token}
            }

        return servers

    async def analyze_repository(self, repo_path: str) -> Dict[str, Any]:
        """
        Analisa repositório Git local
        """
        options = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",
            cwd=repo_path,
            mcp_servers=self.get_mcp_servers_config(),
            allowed_tools=["mcp__git__*"]  # Permite todas as tools do Git MCP
        )

        analysis = {
            "recent_commits": None,
            "branch_info": None,
            "status": None
        }

        async with ClaudeSDKClient(options=options) as agent:
            # Análise de commits recentes
            await agent.query("Show me the last 5 commits with their changes")
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    analysis["recent_commits"] = msg.result

            # Status do repositório
            await agent.query("What's the current status of the repository?")
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    analysis["status"] = msg.result

        return analysis

    async def monitor_ci_cd(self, github_repo: str) -> Dict[str, Any]:
        """
        Monitora CI/CD pipeline no GitHub
        Requer github_token
        """
        if not self.github_token:
            return {"error": "GitHub token required"}

        options = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",
            mcp_servers=self.get_mcp_servers_config(),
            allowed_tools=["mcp__github__*"],
            system_prompt=f"Monitor CI/CD for repository {github_repo}"
        )

        monitoring = {
            "workflow_runs": None,
            "failures": None,
            "pr_status": None
        }

        async with ClaudeSDKClient(options=options) as agent:
            # Check workflow runs
            await agent.query(f"Check recent workflow runs for {github_repo}")
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    monitoring["workflow_runs"] = msg.result

            # Identify failures
            await agent.query("Identify any failed workflows and their causes")
            async for msg in agent.receive_response():
                if hasattr(msg, 'result'):
                    monitoring["failures"] = msg.result

        return monitoring


# ========================================================================
# EXEMPLO 4: Sistema Integrado Neo4j + Claude SDK
# ========================================================================

class Neo4jCookbookIntegration:
    """
    Integra exemplos do Cookbook com Neo4j para memória persistente
    """

    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver
        self.research_agent = ResearchAgent()
        self.chief_agent = ChiefOfStaffAgent()

    async def research_and_save(self, topic: str) -> Dict[str, Any]:
        """
        Pesquisa um tópico e salva no Neo4j
        """
        # Pesquisar
        result = await self.research_agent.research_simple(f"Research about {topic}")

        # Salvar no Neo4j
        with self.driver.session() as session:
            session.run("""
                CREATE (r:Research {
                    topic: $topic,
                    result: $result,
                    timestamp: datetime(),
                    source: 'cookbook_example'
                })
                RETURN r
            """, topic=topic, result=result)

        return {"topic": topic, "result": result, "saved": True}

    async def execute_with_memory(self, task: str) -> str:
        """
        Executa tarefa usando memória do Neo4j como contexto
        """
        # Buscar contexto relevante do Neo4j
        with self.driver.session() as session:
            result = session.run("""
                MATCH (m:Learning)
                WHERE m.name CONTAINS 'claude' OR m.description CONTAINS $task
                RETURN m.name AS name, m.description AS description
                LIMIT 5
            """, task=task)

            context = []
            for record in result:
                context.append(f"- {record['name']}: {record['description']}")

        # Criar prompt com contexto
        enhanced_prompt = f"""
        Task: {task}

        Relevant context from knowledge base:
        {chr(10).join(context)}

        Please complete the task considering this context.
        """

        # Executar com chief agent
        return await self.chief_agent.query_with_memory(enhanced_prompt)


# ========================================================================
# FUNÇÕES AUXILIARES E EXEMPLOS DE USO
# ========================================================================

async def exemplo_completo():
    """
    Demonstra uso completo sem ANTHROPIC_API_KEY
    Usa apenas autenticação via `claude login`
    """

    print("=" * 60)
    print("EXEMPLOS DO COOKBOOK - SEM API KEY")
    print("Usando autenticação via 'claude login'")
    print("=" * 60)

    # 1. Research Agent Simples
    print("\n1. RESEARCH AGENT - Pesquisa Simples")
    print("-" * 40)

    research = ResearchAgent()
    result = await research.research_simple(
        "What are the latest developments in AI agents? Be brief."
    )
    print(f"Resultado: {result[:200]}...")

    # 2. Research com Contexto
    print("\n2. RESEARCH AGENT - Múltiplas Queries com Contexto")
    print("-" * 40)

    queries = [
        "What is Claude Code SDK?",
        "How does it differ from regular API usage?"
    ]
    results = await research.research_with_context(queries)
    for i, res in enumerate(results):
        print(f"Query {i+1}: {res[:100]}...")

    # 3. Chief of Staff com Output Styles
    print("\n3. CHIEF OF STAFF - Diferentes Estilos")
    print("-" * 40)

    chief = ChiefOfStaffAgent()

    # Estilo executivo
    exec_result = await chief.query_with_output_style(
        "Summarize our financial status",
        style="executive"
    )
    print(f"Executive Style: {exec_result[:150]}...")

    # Estilo técnico
    tech_result = await chief.query_with_output_style(
        "Explain our tech stack",
        style="technical"
    )
    print(f"Technical Style: {tech_result[:150]}...")

    # 4. Plan Mode
    print("\n4. CHIEF OF STAFF - Modo Planejamento")
    print("-" * 40)

    plan = await chief.plan_without_execution(
        "Plan the migration from API keys to SDK authentication"
    )
    print(f"Plano criado: {plan[:200]}...")

    print("\n" + "=" * 60)
    print("✅ Todos os exemplos funcionam SEM ANTHROPIC_API_KEY!")
    print("Usando apenas autenticação via 'claude login'")
    print("=" * 60)


# Script para adicionar conhecimento ao Neo4j
def setup_neo4j_knowledge(driver):
    """
    Adiciona conhecimento dos exemplos ao Neo4j
    """
    with driver.session() as session:
        # Criar nó principal do Cookbook
        session.run("""
            MERGE (cookbook:CookbookExample {name: 'Anthropic Cookbook Claude SDK'})
            SET cookbook.description = 'Exemplos oficiais do Claude Code SDK',
                cookbook.no_api_key = true,
                cookbook.uses_claude_login = true,
                cookbook.updated_at = datetime()

            WITH cookbook

            // Research Agent
            MERGE (research:Example {name: 'Research Agent'})
            SET research.notebook = '00_The_one_liner_research_agent.ipynb',
                research.level = 'beginner',
                research.features = ['WebSearch', 'Read', 'ClaudeSDKClient'],
                research.no_api_key = true
            MERGE (research)-[:PART_OF]->(cookbook)

            // Chief of Staff Agent
            MERGE (chief:Example {name: 'Chief of Staff Agent'})
            SET chief.notebook = '01_The_chief_of_staff_agent.ipynb',
                chief.level = 'intermediate',
                chief.features = ['CLAUDE.md', 'Bash', 'Hooks', 'Subagents', 'OutputStyles'],
                chief.no_api_key = true
            MERGE (chief)-[:PART_OF]->(cookbook)

            // Observability Agent
            MERGE (obs:Example {name: 'Observability Agent'})
            SET obs.notebook = '02_The_observability_agent.ipynb',
                obs.level = 'advanced',
                obs.features = ['MCP', 'GitHub', 'Git', 'DevOps'],
                obs.no_api_key = true
            MERGE (obs)-[:PART_OF]->(cookbook)

            // Criar regra importante
            MERGE (rule:Learning {name: 'Cookbook Examples - No API Key'})
            SET rule.type = 'important_rule',
                rule.description = 'Todos os exemplos do Cookbook funcionam SEM ANTHROPIC_API_KEY, usando apenas claude login',
                rule.priority = 'HIGH',
                rule.created_at = datetime()

            MERGE (rule)-[:APPLIES_TO]->(cookbook)

            RETURN cookbook, research, chief, obs, rule
        """)

        print("✅ Conhecimento dos exemplos adicionado ao Neo4j!")


if __name__ == "__main__":
    # Para executar os exemplos
    asyncio.run(exemplo_completo())

    # Para adicionar ao Neo4j (descomente e configure driver)
    # from neo4j import GraphDatabase
    # driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    # setup_neo4j_knowledge(driver)
    # driver.close()