"""
Sistema de Níveis de Conhecimento para Neo4j
Organiza conhecimento em Básico, Intermediário e Avançado com progressão
"""

import os
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json

class KnowledgeLevel(Enum):
    """Níveis de conhecimento"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class LevelCriteria:
    """Critérios para classificação de nível"""
    level: KnowledgeLevel
    complexity_score: Tuple[float, float]  # (min, max)
    prerequisites: List[str]
    concepts: List[str]
    skills: List[str]
    time_estimate: str
    description: str

class Neo4jKnowledgeLevels:
    """
    Sistema de níveis de conhecimento para Neo4j
    Classifica e organiza conhecimento por complexidade e progressão
    """

    def __init__(self, driver):
        self.driver = driver
        self.level_criteria = self._define_level_criteria()

    def _define_level_criteria(self) -> Dict[KnowledgeLevel, LevelCriteria]:
        """Define critérios para cada nível de conhecimento"""
        return {
            KnowledgeLevel.BEGINNER: LevelCriteria(
                level=KnowledgeLevel.BEGINNER,
                complexity_score=(0.0, 0.3),
                prerequisites=[],
                concepts=[
                    "instalação", "setup", "configuração básica",
                    "hello world", "primeiro exemplo", "import",
                    "query simples", "tipos básicos", "print",
                    "async básico", "error handling básico"
                ],
                skills=[
                    "Instalar e configurar o ambiente",
                    "Executar queries simples",
                    "Entender tipos de mensagem",
                    "Usar a função query()",
                    "Tratamento básico de erros"
                ],
                time_estimate="1-3 horas",
                description="Fundamentos essenciais para começar a usar o SDK"
            ),

            KnowledgeLevel.INTERMEDIATE: LevelCriteria(
                level=KnowledgeLevel.INTERMEDIATE,
                complexity_score=(0.3, 0.6),
                prerequisites=["query básico", "tipos", "async/await"],
                concepts=[
                    "ClaudeSDKClient", "streaming", "context manager",
                    "options avançadas", "tools permitidas", "working directory",
                    "permission mode", "error handling completo",
                    "message parsing", "transport", "subprocess"
                ],
                skills=[
                    "Usar ClaudeSDKClient para conversas",
                    "Implementar streaming de respostas",
                    "Configurar permissões e ferramentas",
                    "Gerenciar contexto e sessões",
                    "Debug e troubleshooting"
                ],
                time_estimate="1-2 dias",
                description="Recursos intermediários para aplicações mais complexas"
            ),

            KnowledgeLevel.ADVANCED: LevelCriteria(
                level=KnowledgeLevel.ADVANCED,
                complexity_score=(0.6, 0.85),
                prerequisites=["ClaudeSDKClient", "streaming", "context manager"],
                concepts=[
                    "hooks system", "PreToolUse", "PostToolResult",
                    "HookMatcher", "permission callbacks", "tool callbacks",
                    "custom validation", "intercept events", "modify behavior",
                    "control flow", "bidirectional communication"
                ],
                skills=[
                    "Implementar hooks customizados",
                    "Interceptar e validar tool use",
                    "Criar callbacks de permissão",
                    "Modificar comportamento do SDK",
                    "Implementar lógica de negócio em hooks"
                ],
                time_estimate="2-3 dias",
                description="Hooks e callbacks para customização avançada"
            ),

            KnowledgeLevel.EXPERT: LevelCriteria(
                level=KnowledgeLevel.EXPERT,
                complexity_score=(0.85, 1.0),
                prerequisites=["hooks", "callbacks", "async patterns"],
                concepts=[
                    "MCP servers in-process", "SDK MCP", "@tool decorator",
                    "create_sdk_mcp_server", "mixed servers", "custom tools",
                    "tool implementation", "server lifecycle", "IPC optimization",
                    "production patterns", "scaling", "monitoring"
                ],
                skills=[
                    "Criar MCP servers in-process",
                    "Implementar ferramentas customizadas",
                    "Otimizar performance com SDK MCP",
                    "Integrar múltiplos servers",
                    "Deploy em produção"
                ],
                time_estimate="3-5 dias",
                description="MCP servers e ferramentas customizadas para soluções enterprise"
            )
        }

    def setup_knowledge_levels(self):
        """Configura estrutura de níveis no Neo4j"""
        with self.driver.session() as session:
            # 1. Criar nós de nível
            for level, criteria in self.level_criteria.items():
                session.run("""
                    MERGE (l:KnowledgeLevel {name: $level_name})
                    SET l.complexity_min = $complexity_min,
                        l.complexity_max = $complexity_max,
                        l.description = $description,
                        l.time_estimate = $time_estimate,
                        l.skills = $skills,
                        l.concepts = $concepts,
                        l.order = $order,
                        l.color = $color,
                        l.icon = $icon
                    RETURN l
                """,
                level_name=level.value,
                complexity_min=criteria.complexity_score[0],
                complexity_max=criteria.complexity_score[1],
                description=criteria.description,
                time_estimate=criteria.time_estimate,
                skills=criteria.skills,
                concepts=criteria.concepts,
                order=list(self.level_criteria.keys()).index(level),
                color=self._get_level_color(level),
                icon=self._get_level_icon(level))

            # 2. Criar relacionamentos de progressão
            session.run("""
                MATCH (b:KnowledgeLevel {name: 'beginner'})
                MATCH (i:KnowledgeLevel {name: 'intermediate'})
                MATCH (a:KnowledgeLevel {name: 'advanced'})
                MATCH (e:KnowledgeLevel {name: 'expert'})

                MERGE (b)-[:NEXT_LEVEL]->(i)
                MERGE (i)-[:NEXT_LEVEL]->(a)
                MERGE (a)-[:NEXT_LEVEL]->(e)

                MERGE (i)-[:REQUIRES]->(b)
                MERGE (a)-[:REQUIRES]->(i)
                MERGE (e)-[:REQUIRES]->(a)
            """)

    def _get_level_color(self, level: KnowledgeLevel) -> str:
        """Retorna cor para visualização do nível"""
        colors = {
            KnowledgeLevel.BEGINNER: "#4CAF50",     # Verde
            KnowledgeLevel.INTERMEDIATE: "#2196F3",  # Azul
            KnowledgeLevel.ADVANCED: "#FF9800",      # Laranja
            KnowledgeLevel.EXPERT: "#9C27B0"         # Roxo
        }
        return colors.get(level, "#757575")

    def _get_level_icon(self, level: KnowledgeLevel) -> str:
        """Retorna ícone/emoji para o nível"""
        icons = {
            KnowledgeLevel.BEGINNER: "🌱",
            KnowledgeLevel.INTERMEDIATE: "🌿",
            KnowledgeLevel.ADVANCED: "🌳",
            KnowledgeLevel.EXPERT: "🏆"
        }
        return icons.get(level, "📚")

    def classify_claude_sdk_knowledge(self):
        """
        Classifica conhecimento do Claude SDK por nível
        """
        classifications = {
            KnowledgeLevel.BEGINNER: {
                "modules": ["query", "types", "quick_start"],
                "examples": ["quick_start.py"],
                "topics": [
                    "Installation", "Basic Usage", "Simple Query",
                    "Message Types", "Text Blocks", "Error Handling Basics"
                ],
                "functions": ["query", "run"],
                "classes": ["ClaudeCodeOptions", "AssistantMessage", "TextBlock"]
            },

            KnowledgeLevel.INTERMEDIATE: {
                "modules": ["client", "_errors", "transport", "message_parser"],
                "examples": ["streaming_mode.py", "streaming_mode_ipython.py"],
                "topics": [
                    "ClaudeSDKClient", "Streaming", "Context Manager",
                    "Working Directory", "Permission Modes", "Tool Selection",
                    "Error Types", "Message Parsing"
                ],
                "functions": ["receive_response", "query_with_client"],
                "classes": [
                    "ClaudeSDKClient", "Transport", "CLIError",
                    "ProcessError", "CLIConnectionError"
                ]
            },

            KnowledgeLevel.ADVANCED: {
                "modules": ["hooks", "callbacks"],
                "examples": ["hooks.py", "tool_permission_callback.py"],
                "topics": [
                    "Hook System", "PreToolUse", "PostToolResult",
                    "Permission Callbacks", "Tool Validation",
                    "Event Interception", "Custom Logic"
                ],
                "functions": ["check_bash_command", "validate_permission"],
                "classes": ["HookMatcher", "HookEvent", "PermissionCallback"]
            },

            KnowledgeLevel.EXPERT: {
                "modules": ["sdk_mcp", "mcp_server", "tool_decorator"],
                "examples": ["mcp_calculator.py"],
                "topics": [
                    "MCP Servers", "In-Process Tools", "Custom Tools",
                    "@tool Decorator", "SDK MCP Server", "Mixed Servers",
                    "Production Patterns", "Performance Optimization"
                ],
                "functions": ["create_sdk_mcp_server", "tool"],
                "classes": ["SdkMcpServer", "SdkMcpTool", "McpServerConfig"]
            }
        }

        with self.driver.session() as session:
            for level, items in classifications.items():
                # Classificar módulos
                for module in items["modules"]:
                    session.run("""
                        MATCH (k:SDKKnowledge)
                        WHERE k.module_name CONTAINS $module
                        MATCH (l:KnowledgeLevel {name: $level})
                        MERGE (k)-[:HAS_LEVEL]->(l)
                    """, module=module, level=level.value)

                # Classificar exemplos
                for example in items["examples"]:
                    session.run("""
                        MATCH (k:SDKKnowledge {module_name: $example})
                        MATCH (l:KnowledgeLevel {name: $level})
                        MERGE (k)-[:HAS_LEVEL]->(l)
                    """, example=example.replace('.py', ''), level=level.value)

                # Classificar por funções e classes
                for func in items["functions"]:
                    session.run("""
                        MATCH (k:SDKKnowledge)
                        WHERE $func IN k.functions
                        MATCH (l:KnowledgeLevel {name: $level})
                        MERGE (k)-[:HAS_LEVEL]->(l)
                    """, func=func, level=level.value)

                for cls in items["classes"]:
                    session.run("""
                        MATCH (k:SDKKnowledge)
                        WHERE $cls IN k.classes
                        MATCH (l:KnowledgeLevel {name: $level})
                        MERGE (k)-[:HAS_LEVEL]->(l)
                    """, cls=cls, level=level.value)

    def create_learning_paths(self):
        """
        Cria caminhos de aprendizado estruturados
        """
        learning_paths = [
            {
                "name": "Claude SDK: Do Zero ao Expert",
                "description": "Caminho completo de aprendizado do Claude Code SDK Python",
                "duration": "2 semanas",
                "modules": [
                    {
                        "week": 1,
                        "level": "beginner",
                        "topics": [
                            {"day": 1, "topic": "Setup e Instalação", "practice": "Hello World com query()"},
                            {"day": 2, "topic": "Tipos e Mensagens", "practice": "Processar diferentes tipos de resposta"},
                            {"day": 3, "topic": "Ferramentas Básicas", "practice": "Usar Read, Write, Bash"},
                            {"day": 4, "topic": "Error Handling", "practice": "Tratar erros comuns"},
                            {"day": 5, "topic": "Projeto Básico", "practice": "CLI simples com query()"}
                        ]
                    },
                    {
                        "week": 1,
                        "level": "intermediate",
                        "topics": [
                            {"day": 6, "topic": "ClaudeSDKClient", "practice": "Conversas interativas"},
                            {"day": 7, "topic": "Streaming", "practice": "Processar respostas em tempo real"}
                        ]
                    },
                    {
                        "week": 2,
                        "level": "advanced",
                        "topics": [
                            {"day": 8, "topic": "Hooks Básicos", "practice": "Interceptar tool use"},
                            {"day": 9, "topic": "Permission Callbacks", "practice": "Validação customizada"},
                            {"day": 10, "topic": "Hooks Avançados", "practice": "Modificar comportamento"}
                        ]
                    },
                    {
                        "week": 2,
                        "level": "expert",
                        "topics": [
                            {"day": 11, "topic": "MCP Tools", "practice": "Criar ferramenta simples"},
                            {"day": 12, "topic": "SDK MCP Server", "practice": "Server in-process"},
                            {"day": 13, "topic": "Integração", "practice": "Mixed servers"},
                            {"day": 14, "topic": "Projeto Final", "practice": "Aplicação completa com MCP"}
                        ]
                    }
                ]
            },
            {
                "name": "Fast Track: Hooks e MCP",
                "description": "Caminho acelerado para features avançadas",
                "duration": "3 dias",
                "prerequisites": ["ClaudeSDKClient", "async/await"],
                "modules": [
                    {
                        "day": 1,
                        "level": "advanced",
                        "topics": [
                            {"hour": "1-4", "topic": "Hook System Overview", "practice": "PreToolUse hook"},
                            {"hour": "5-8", "topic": "PostToolResult", "practice": "Processar resultados"}
                        ]
                    },
                    {
                        "day": 2,
                        "level": "expert",
                        "topics": [
                            {"hour": "1-4", "topic": "@tool decorator", "practice": "Criar tool customizada"},
                            {"hour": "5-8", "topic": "SDK MCP Server", "practice": "Server completo"}
                        ]
                    },
                    {
                        "day": 3,
                        "level": "expert",
                        "topics": [
                            {"hour": "1-4", "topic": "Production Patterns", "practice": "Error handling robusto"},
                            {"hour": "5-8", "topic": "Deploy", "practice": "Aplicação production-ready"}
                        ]
                    }
                ]
            }
        ]

        with self.driver.session() as session:
            for path in learning_paths:
                # Criar nó do caminho
                session.run("""
                    CREATE (p:LearningPath {
                        name: $name,
                        description: $description,
                        duration: $duration,
                        created_at: datetime()
                    })
                    RETURN p
                """,
                name=path["name"],
                description=path["description"],
                duration=path["duration"])

                # Conectar com níveis
                for module in path["modules"]:
                    if "level" in module:
                        session.run("""
                            MATCH (p:LearningPath {name: $path_name})
                            MATCH (l:KnowledgeLevel {name: $level})
                            MERGE (p)-[:COVERS {week: $week}]->(l)
                        """,
                        path_name=path["name"],
                        level=module.get("level"),
                        week=module.get("week", 1))

    def query_by_level(self, level: str, query: str = None) -> List[Dict]:
        """
        Busca conhecimento filtrado por nível
        """
        with self.driver.session() as session:
            if query:
                # Busca com query específica no nível
                result = session.run("""
                    MATCH (k:SDKKnowledge)-[:HAS_LEVEL]->(l:KnowledgeLevel {name: $level})
                    WHERE k.description CONTAINS $query
                       OR k.module_name CONTAINS $query
                       OR ANY(f IN k.functions WHERE f CONTAINS $query)
                       OR ANY(c IN k.classes WHERE c CONTAINS $query)

                    OPTIONAL MATCH (k)-[:DEMONSTRATES]->(demo)
                    OPTIONAL MATCH (k)-[:TESTS]->(test)

                    RETURN k.module_name AS module,
                           k.description AS description,
                           k.content_type AS type,
                           substring(k.code_snippet, 0, 500) AS code,
                           k.functions[:5] AS functions,
                           k.classes[:3] AS classes,
                           collect(DISTINCT demo.module_name) AS examples,
                           l.name AS level,
                           l.description AS level_description
                    ORDER BY k.module_name
                    LIMIT 10
                """, level=level, query=query)
            else:
                # Busca todos do nível
                result = session.run("""
                    MATCH (k:SDKKnowledge)-[:HAS_LEVEL]->(l:KnowledgeLevel {name: $level})

                    OPTIONAL MATCH (k)-[:DEMONSTRATES]->(demo)

                    RETURN k.module_name AS module,
                           k.description AS description,
                           k.content_type AS type,
                           k.functions[:5] AS functions,
                           k.classes[:3] AS classes,
                           collect(DISTINCT demo.module_name) AS examples,
                           l.name AS level,
                           l.icon AS icon
                    ORDER BY k.content_type, k.module_name
                    LIMIT 20
                """, level=level)

            return [dict(record) for record in result]

    def get_user_progression(self, user_id: str) -> Dict:
        """
        Rastreia progressão do usuário pelos níveis
        """
        with self.driver.session() as session:
            # Criar/atualizar perfil do usuário
            session.run("""
                MERGE (u:User {id: $user_id})
                ON CREATE SET u.created_at = datetime(),
                              u.current_level = 'beginner'
                RETURN u
            """, user_id=user_id)

            # Buscar progressão
            result = session.run("""
                MATCH (u:User {id: $user_id})
                OPTIONAL MATCH (u)-[r:COMPLETED]->(k:SDKKnowledge)
                OPTIONAL MATCH (k)-[:HAS_LEVEL]->(l:KnowledgeLevel)

                WITH u, l.name AS level, count(DISTINCT k) AS completed_items

                RETURN u.current_level AS current_level,
                       collect({level: level, completed: completed_items}) AS progress
            """, user_id=user_id)

            record = result.single()
            return {
                "user_id": user_id,
                "current_level": record["current_level"],
                "progress": record["progress"]
            }

    def recommend_next_content(self, user_id: str) -> List[Dict]:
        """
        Recomenda próximo conteúdo baseado no nível do usuário
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User {id: $user_id})
                MATCH (l:KnowledgeLevel {name: u.current_level})

                // Buscar conteúdo não completado do nível atual
                MATCH (k:SDKKnowledge)-[:HAS_LEVEL]->(l)
                WHERE NOT (u)-[:COMPLETED]->(k)

                // Priorizar exemplos e conteúdo prático
                WITH k,
                     CASE k.content_type
                        WHEN 'example' THEN 3
                        WHEN 'source' THEN 2
                        WHEN 'test' THEN 1
                        ELSE 0
                     END AS priority

                RETURN k.module_name AS module,
                       k.description AS description,
                       k.content_type AS type,
                       l.name AS level,
                       l.icon AS icon,
                       priority
                ORDER BY priority DESC, k.module_name
                LIMIT 5
            """, user_id=user_id)

            return [dict(record) for record in result]

    def mark_as_completed(self, user_id: str, module_name: str):
        """
        Marca conteúdo como completado e atualiza progressão
        """
        with self.driver.session() as session:
            # Marcar como completado
            session.run("""
                MATCH (u:User {id: $user_id})
                MATCH (k:SDKKnowledge {module_name: $module_name})
                MERGE (u)-[r:COMPLETED]->(k)
                SET r.completed_at = datetime()
            """, user_id=user_id, module_name=module_name)

            # Verificar se deve avançar de nível
            result = session.run("""
                MATCH (u:User {id: $user_id})
                MATCH (current:KnowledgeLevel {name: u.current_level})

                // Contar items completados no nível atual
                MATCH (k:SDKKnowledge)-[:HAS_LEVEL]->(current)
                OPTIONAL MATCH (u)-[:COMPLETED]->(k)
                WITH u, current, count(k) AS total, count((u)-[:COMPLETED]->(k)) AS completed

                // Se completou 80% ou mais, sugerir próximo nível
                WHERE toFloat(completed) / toFloat(total) >= 0.8
                MATCH (current)-[:NEXT_LEVEL]->(next:KnowledgeLevel)

                RETURN next.name AS next_level,
                       completed,
                       total,
                       toFloat(completed) / toFloat(total) AS completion_rate
            """, user_id=user_id)

            record = result.single()
            if record:
                # Atualizar nível do usuário
                session.run("""
                    MATCH (u:User {id: $user_id})
                    SET u.current_level = $next_level,
                        u.level_updated_at = datetime()
                """, user_id=user_id, next_level=record["next_level"])

                return {
                    "level_up": True,
                    "new_level": record["next_level"],
                    "completion_rate": record["completion_rate"]
                }

            return {"level_up": False}


def create_dashboard_query():
    """
    Query para dashboard de níveis de conhecimento
    """
    return """
    // Dashboard de Conhecimento por Nível
    MATCH (l:KnowledgeLevel)
    OPTIONAL MATCH (k:SDKKnowledge)-[:HAS_LEVEL]->(l)

    WITH l, count(DISTINCT k) AS total_items,
         collect(DISTINCT k.content_type) AS content_types

    RETURN l.name AS level,
           l.icon AS icon,
           l.color AS color,
           l.description AS description,
           l.time_estimate AS time_estimate,
           total_items,
           content_types,
           l.order AS display_order
    ORDER BY l.order
    """


# Script de execução
def main():
    """
    Configura sistema de níveis no Neo4j
    """
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", os.getenv("NEO4J_PASSWORD", "password"))
    )

    try:
        system = Neo4jKnowledgeLevels(driver)

        print("🎯 Configurando Sistema de Níveis de Conhecimento\n")

        print("1. Criando estrutura de níveis...")
        system.setup_knowledge_levels()
        print("   ✅ Níveis criados: Beginner, Intermediate, Advanced, Expert")

        print("\n2. Classificando conhecimento do SDK...")
        system.classify_claude_sdk_knowledge()
        print("   ✅ Conhecimento classificado por nível")

        print("\n3. Criando caminhos de aprendizado...")
        system.create_learning_paths()
        print("   ✅ Caminhos criados: Completo (2 semanas) e Fast Track (3 dias)")

        print("\n4. Testando queries por nível...")

        # Exemplo Beginner
        beginner_content = system.query_by_level("beginner")
        print(f"\n   🌱 BEGINNER: {len(beginner_content)} items")
        for item in beginner_content[:3]:
            print(f"      - {item['module']} ({item['type']})")

        # Exemplo Intermediate
        intermediate_content = system.query_by_level("intermediate")
        print(f"\n   🌿 INTERMEDIATE: {len(intermediate_content)} items")
        for item in intermediate_content[:3]:
            print(f"      - {item['module']} ({item['type']})")

        # Exemplo Advanced
        advanced_content = system.query_by_level("advanced", "hooks")
        print(f"\n   🌳 ADVANCED (hooks): {len(advanced_content)} items")
        for item in advanced_content[:3]:
            print(f"      - {item['module']}: {item['description'][:50]}...")

        # Exemplo Expert
        expert_content = system.query_by_level("expert")
        print(f"\n   🏆 EXPERT: {len(expert_content)} items")
        for item in expert_content[:3]:
            print(f"      - {item['module']} ({item['type']})")

        print("\n5. Simulando progressão de usuário...")
        user_id = "test_user_123"

        # Progressão inicial
        progress = system.get_user_progression(user_id)
        print(f"\n   Usuário: {user_id}")
        print(f"   Nível atual: {progress['current_level']}")

        # Recomendações
        recommendations = system.recommend_next_content(user_id)
        print(f"\n   📚 Conteúdo recomendado:")
        for rec in recommendations[:3]:
            print(f"      {rec['icon']} [{rec['level']}] {rec['module']} - {rec['type']}")

        print("\n✅ Sistema de Níveis configurado com sucesso!")
        print("\n📊 Dashboard Query disponível em: create_dashboard_query()")

    finally:
        driver.close()


if __name__ == "__main__":
    main()