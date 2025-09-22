"""
Script de Integração Completa: Cookbook + Neo4j + Claude SDK
Centraliza todo conhecimento dos exemplos no grafo para consultas inteligentes
"""

from neo4j import GraphDatabase
import os
from typing import Dict, List, Optional
from datetime import datetime


class CookbookNeo4jIntegration:
    """
    Integra os exemplos do Anthropic Cookbook com Neo4j
    Permite consultas inteligentes sobre como usar o SDK
    """

    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = None):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password or os.getenv("NEO4J_PASSWORD", "password"))
        )

    def setup_cookbook_knowledge(self):
        """
        Adiciona todo conhecimento do Cookbook ao Neo4j
        """
        with self.driver.session() as session:
            # 1. Criar estrutura principal
            session.run("""
                // Nó principal do Cookbook
                MERGE (cookbook:CookbookKnowledge {name: 'Anthropic Cookbook Claude SDK'})
                SET cookbook.description = '3 notebooks progressivos demonstrando Claude Code SDK',
                    cookbook.path = '/Users/2a/.claude/anthropic-cookbook/claude_code_sdk',
                    cookbook.no_api_key = true,
                    cookbook.authentication = 'claude login',
                    cookbook.updated_at = datetime()

                // Regra importante sobre autenticação
                MERGE (auth_rule:Learning {name: 'SDK Authentication Rule'})
                SET auth_rule.type = 'critical_rule',
                    auth_rule.rule = 'NUNCA usar ANTHROPIC_API_KEY com Claude Code SDK',
                    auth_rule.correct_method = 'Usar apenas: claude login',
                    auth_rule.priority = 'CRITICAL',
                    auth_rule.applies_to = ['ClaudeSDKClient', 'query', 'Claude Code CLI']

                MERGE (auth_rule)-[:GOVERNS]->(cookbook)

                RETURN cookbook, auth_rule
            """)

            # 2. Adicionar exemplos com detalhes
            examples = [
                {
                    "name": "Research Agent",
                    "notebook": "00_The_one_liner_research_agent.ipynb",
                    "level": "beginner",
                    "hours": "1-2",
                    "concepts": [
                        "query() function básica",
                        "WebSearch tool",
                        "Read tool para imagens",
                        "ClaudeSDKClient para contexto",
                        "Activity handlers"
                    ],
                    "code_snippet": """
async for msg in query(
    prompt="Research AI trends",
    options=ClaudeCodeOptions(
        model="claude-3-5-sonnet-20241022",
        allowed_tools=["WebSearch"]
    )
):
    print(msg)""",
                    "key_takeaway": "Agente funcional em 5 linhas de código"
                },
                {
                    "name": "Chief of Staff Agent",
                    "notebook": "01_The_chief_of_staff_agent.ipynb",
                    "level": "intermediate",
                    "hours": "8-16",
                    "concepts": [
                        "CLAUDE.md para memória persistente",
                        "Bash tool para scripts Python",
                        "Output Styles (executive, technical)",
                        "Plan Mode para estratégia",
                        "Slash Commands customizados",
                        "Hooks para compliance",
                        "Subagentes especializados com Task tool"
                    ],
                    "code_snippet": """
# Delegar para subagente financeiro
options = ClaudeCodeOptions(
    allowed_tools=["Task"],
    system_prompt="Delegate to financial-analyst",
    cwd="chief_of_staff_agent"
)""",
                    "key_takeaway": "Sistema multi-agente empresarial completo"
                },
                {
                    "name": "Observability Agent",
                    "notebook": "02_The_observability_agent.ipynb",
                    "level": "advanced",
                    "hours": "16-24",
                    "concepts": [
                        "MCP servers externos",
                        "Git MCP (13+ tools)",
                        "GitHub MCP (100+ tools)",
                        "CI/CD monitoring",
                        "DevOps automation"
                    ],
                    "code_snippet": """
mcp_servers={
    "github": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_TOKEN": token}
    }
}""",
                    "key_takeaway": "Integração com sistemas externos via MCP"
                }
            ]

            for ex in examples:
                session.run("""
                    MATCH (cookbook:CookbookKnowledge {name: 'Anthropic Cookbook Claude SDK'})

                    MERGE (example:Example {name: $name})
                    SET example.notebook = $notebook,
                        example.level = $level,
                        example.time_estimate = $hours + ' hours',
                        example.concepts = $concepts,
                        example.code_snippet = $code_snippet,
                        example.key_takeaway = $key_takeaway,
                        example.no_api_key = true,
                        example.updated_at = datetime()

                    MERGE (example)-[:PART_OF]->(cookbook)

                    // Conectar com nível de conhecimento
                    MERGE (level:KnowledgeLevel {name: $level})
                    MERGE (example)-[:HAS_LEVEL]->(level)

                    RETURN example
                """, **ex)

            # 3. Adicionar features específicas
            features = [
                ("CLAUDE.md", "intermediate", "Arquivo markdown com contexto persistente e instruções"),
                ("Bash Tool", "intermediate", "Executa scripts Python para cálculos e modelos"),
                ("Output Styles", "intermediate", "Diferentes estilos de saída por audiência"),
                ("Plan Mode", "intermediate", "Cria plano sem executar (permission_mode='plan')"),
                ("Slash Commands", "intermediate", "Atalhos de usuário que expandem para prompts"),
                ("Hooks", "advanced", "Scripts Python executados em eventos (pre/post tool use)"),
                ("Subagents", "advanced", "Agentes especializados via Task tool"),
                ("MCP Servers", "expert", "Integração com serviços externos via Model Context Protocol")
            ]

            for feature_name, level, description in features:
                session.run("""
                    MERGE (feature:Feature {name: $name})
                    SET feature.description = $description,
                        feature.level = $level,
                        feature.cookbook_example = true

                    WITH feature
                    MATCH (level:KnowledgeLevel {name: $level})
                    MERGE (feature)-[:REQUIRES_LEVEL]->(level)

                    WITH feature
                    MATCH (cookbook:CookbookKnowledge {name: 'Anthropic Cookbook Claude SDK'})
                    MERGE (feature)-[:DEMONSTRATED_IN]->(cookbook)

                    RETURN feature
                """, name=feature_name, level=level, description=description)

            print("✅ Conhecimento do Cookbook adicionado ao Neo4j!")

    def query_cookbook_examples(self, topic: str) -> List[Dict]:
        """
        Busca exemplos relevantes do Cookbook
        """
        with self.driver.session() as session:
            result = session.run("""
                // Buscar por tópico
                MATCH (example:Example)-[:PART_OF]->(cookbook:CookbookKnowledge)
                WHERE example.name CONTAINS $topic
                   OR ANY(concept IN example.concepts WHERE concept CONTAINS $topic)
                   OR example.code_snippet CONTAINS $topic

                OPTIONAL MATCH (example)-[:HAS_LEVEL]->(level:KnowledgeLevel)

                RETURN example.name AS name,
                       example.notebook AS notebook,
                       example.level AS level,
                       example.time_estimate AS time,
                       example.concepts AS concepts,
                       example.code_snippet AS code,
                       example.key_takeaway AS takeaway
                ORDER BY
                    CASE level.name
                        WHEN 'beginner' THEN 1
                        WHEN 'intermediate' THEN 2
                        WHEN 'advanced' THEN 3
                        ELSE 4
                    END
            """, topic=topic)

            return [dict(record) for record in result]

    def get_learning_path(self, current_level: str = "beginner") -> Dict:
        """
        Retorna caminho de aprendizado baseado no nível atual
        """
        with self.driver.session() as session:
            result = session.run("""
                // Buscar exemplos do nível atual e próximo
                MATCH (current:KnowledgeLevel {name: $level})
                OPTIONAL MATCH (current)-[:NEXT_LEVEL]->(next:KnowledgeLevel)

                // Exemplos do nível atual
                MATCH (example:Example)-[:HAS_LEVEL]->(current)
                WHERE example.no_api_key = true

                // Features do nível
                OPTIONAL MATCH (feature:Feature)-[:REQUIRES_LEVEL]->(current)

                WITH current, next,
                     collect(DISTINCT example) AS current_examples,
                     collect(DISTINCT feature) AS current_features

                // Exemplos do próximo nível
                OPTIONAL MATCH (next_example:Example)-[:HAS_LEVEL]->(next)
                WHERE next_example.no_api_key = true

                RETURN current.name AS current_level,
                       next.name AS next_level,
                       [e IN current_examples | {
                           name: e.name,
                           notebook: e.notebook,
                           time: e.time_estimate,
                           takeaway: e.key_takeaway
                       }] AS examples,
                       [f IN current_features | f.name] AS features,
                       [e IN collect(next_example) | e.name] AS next_examples
            """, level=current_level)

            return dict(result.single())

    def get_feature_usage(self, feature_name: str) -> Dict:
        """
        Mostra como usar uma feature específica
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (feature:Feature {name: $feature})

                // Buscar exemplos que demonstram a feature
                OPTIONAL MATCH (example:Example)-[:PART_OF]->(cookbook)
                WHERE ANY(concept IN example.concepts WHERE concept CONTAINS $feature)

                // Buscar código relacionado
                WITH feature, collect(example) AS examples

                RETURN feature.name AS name,
                       feature.description AS description,
                       feature.level AS level,
                       [e IN examples | {
                           example: e.name,
                           notebook: e.notebook,
                           code: e.code_snippet
                       }] AS demonstrated_in
            """, feature=feature_name)

            record = result.single()
            return dict(record) if record else {}

    def compare_authentication_methods(self):
        """
        Compara métodos de autenticação (para educação)
        """
        with self.driver.session() as session:
            result = session.run("""
                CREATE (comparison:AuthComparison {
                    title: 'Claude SDK Authentication Methods',
                    created_at: datetime()
                })

                WITH comparison

                // Método INCORRETO (API Key)
                CREATE (wrong:Method {
                    name: 'API Key (INCORRETO para SDK)',
                    code: 'os.getenv("ANTHROPIC_API_KEY")',
                    when_to_use: 'NUNCA com Claude Code SDK',
                    works_with: 'anthropic library apenas',
                    status: 'deprecated_for_sdk'
                })

                // Método CORRETO (claude login)
                CREATE (right:Method {
                    name: 'Claude Login (CORRETO)',
                    code: 'claude login (no terminal)',
                    when_to_use: 'SEMPRE com Claude Code SDK',
                    works_with: 'ClaudeSDKClient, query(), CLI',
                    status: 'recommended'
                })

                MERGE (wrong)-[:COMPARED_TO]->(comparison)
                MERGE (right)-[:COMPARED_TO]->(comparison)

                RETURN comparison, wrong, right
            """)

            return "✅ Comparação de autenticação adicionada ao grafo"

    def generate_example_code(self, use_case: str) -> str:
        """
        Gera código exemplo baseado no caso de uso
        """
        examples = {
            "research": """
# Research Agent - SEM API KEY!
from claude_code_sdk import query, ClaudeCodeOptions

async for msg in query(
    prompt="Research the latest AI developments",
    options=ClaudeCodeOptions(
        model="claude-3-5-sonnet-20241022",
        allowed_tools=["WebSearch", "Read"]
    )
):
    if hasattr(msg, 'result'):
        print(msg.result)
""",
            "multiagent": """
# Chief of Staff com Subagentes - SEM API KEY!
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

options = ClaudeCodeOptions(
    model="claude-3-5-sonnet-20241022",
    allowed_tools=["Task"],
    cwd="chief_of_staff_agent",  # Dir com CLAUDE.md e .claude/agents/
    system_prompt="Delegate financial tasks to financial-analyst"
)

async with ClaudeSDKClient(options=options) as agent:
    await agent.query("Analyze our burn rate impact")
    async for msg in agent.receive_response():
        print(msg)
""",
            "hooks": """
# Hooks para Compliance - SEM API KEY!
# Em .claude/settings.local.json:
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

# Depois use normalmente:
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

options = ClaudeCodeOptions(
    cwd="my_project",  # Dir com .claude/settings.local.json
    allowed_tools=["Write", "Edit"]
)
""",
            "mcp": """
# MCP Server Integration - SEM API KEY para Claude!
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

options = ClaudeCodeOptions(
    mcp_servers={
        "github": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": "ghp_xxx"}  # Apenas GitHub token
        }
    },
    allowed_tools=["mcp__github__*"]
)

# Claude usa 'claude login', não API key!
async with ClaudeSDKClient(options=options) as agent:
    await agent.query("Check CI/CD status")
"""
        }

        return examples.get(use_case, "Caso de uso não encontrado. Tente: research, multiagent, hooks, mcp")

    def close(self):
        """Fecha conexão com Neo4j"""
        self.driver.close()


# Funções auxiliares para consultas rápidas
def quick_search(topic: str):
    """Busca rápida sobre um tópico"""
    integration = CookbookNeo4jIntegration()
    results = integration.query_cookbook_examples(topic)
    integration.close()

    if results:
        print(f"\n📚 Exemplos do Cookbook sobre '{topic}':\n")
        for r in results:
            print(f"📖 {r['name']} ({r['level']})")
            print(f"   Notebook: {r['notebook']}")
            print(f"   Tempo: {r['time']}")
            print(f"   Takeaway: {r['takeaway']}")
            if r['code']:
                print(f"   Código:\n```python\n{r['code'][:200]}...\n```")
            print()
    else:
        print(f"Nenhum exemplo encontrado sobre '{topic}'")

    return results


def show_learning_path(level: str = "beginner"):
    """Mostra caminho de aprendizado"""
    integration = CookbookNeo4jIntegration()
    path = integration.get_learning_path(level)
    integration.close()

    print(f"\n🎯 Caminho de Aprendizado - Nível {path['current_level'].upper()}\n")
    print("Exemplos deste nível:")
    for ex in path['examples']:
        print(f"  • {ex['name']} - {ex['time']}")
        print(f"    → {ex['takeaway']}")

    if path['features']:
        print(f"\nFeatures para aprender:")
        for f in path['features']:
            print(f"  • {f}")

    if path['next_level']:
        print(f"\nPróximo nível: {path['next_level'].upper()}")
        print(f"Próximos exemplos: {', '.join(path['next_examples'])}")

    return path


# Script principal
if __name__ == "__main__":
    print("=" * 60)
    print("INTEGRAÇÃO NEO4J + COOKBOOK")
    print("Todos os exemplos funcionam SEM ANTHROPIC_API_KEY!")
    print("=" * 60)

    # Inicializar
    integration = CookbookNeo4jIntegration()

    # Setup inicial (rodar uma vez)
    print("\n1. Adicionando conhecimento ao Neo4j...")
    integration.setup_cookbook_knowledge()

    # Comparar autenticação
    print("\n2. Comparando métodos de autenticação...")
    print(integration.compare_authentication_methods())

    # Exemplos de consultas
    print("\n3. Buscando exemplos sobre 'hooks'...")
    hooks_examples = integration.query_cookbook_examples("hooks")
    for ex in hooks_examples[:2]:
        print(f"   - {ex['name']}: {ex['takeaway']}")

    # Caminho de aprendizado
    print("\n4. Caminho de aprendizado para iniciantes...")
    path = integration.get_learning_path("beginner")
    print(f"   Começar com: {path['examples'][0]['name'] if path['examples'] else 'N/A'}")

    # Gerar código
    print("\n5. Código exemplo para research:")
    print(integration.generate_example_code("research"))

    # Fechar
    integration.close()

    print("\n✅ Integração completa!")
    print("\nUse as funções auxiliares:")
    print("  • quick_search('topic') - Busca exemplos")
    print("  • show_learning_path('level') - Mostra caminho")
    print("  • integration.generate_example_code('use_case') - Gera código")