"""
Integração do Claude Code SDK Python com Neo4j GraphRAG
Enriquece o grafo de conhecimento com informações completas do SDK
"""

import os
import json
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import anthropic
import voyageai

@dataclass
class SDKKnowledge:
    """Estrutura para conhecimento do SDK"""
    file_path: str
    module_name: str
    content_type: str  # 'code', 'example', 'test', 'doc'
    description: str
    code_snippet: str
    imports: List[str]
    functions: List[str]
    classes: List[str]
    decorators: List[str]
    metadata: Dict[str, Any]

class ClaudeSDKNeo4jIntegration:
    """
    Integra o conhecimento do Claude Code SDK Python ao Neo4j
    para criar um sistema RAG especializado no SDK
    """

    def __init__(self, neo4j_driver, voyage_client=None, anthropic_client=None):
        self.driver = neo4j_driver
        self.voyage_client = voyage_client or voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
        self.anthropic_client = anthropic_client or anthropic.Anthropic()
        self.sdk_path = Path("/Users/2a/.claude/claude-code-sdk-python")

    def extract_sdk_knowledge(self) -> List[SDKKnowledge]:
        """Extrai conhecimento estruturado do SDK"""
        knowledge_items = []

        # 1. Processar código fonte principal
        src_path = self.sdk_path / "src" / "claude_code_sdk"
        for py_file in src_path.rglob("*.py"):
            knowledge = self._analyze_python_file(py_file, "source")
            if knowledge:
                knowledge_items.append(knowledge)

        # 2. Processar exemplos
        examples_path = self.sdk_path / "examples"
        for py_file in examples_path.glob("*.py"):
            knowledge = self._analyze_python_file(py_file, "example")
            if knowledge:
                knowledge_items.append(knowledge)

        # 3. Processar testes
        tests_path = self.sdk_path / "tests"
        for py_file in tests_path.glob("test_*.py"):
            knowledge = self._analyze_python_file(py_file, "test")
            if knowledge:
                knowledge_items.append(knowledge)

        # 4. Processar documentação
        for doc_file in [self.sdk_path / "README.md", self.sdk_path / "CHANGELOG.md"]:
            if doc_file.exists():
                knowledge = self._analyze_doc_file(doc_file)
                if knowledge:
                    knowledge_items.append(knowledge)

        return knowledge_items

    def _analyze_python_file(self, file_path: Path, content_type: str) -> Optional[SDKKnowledge]:
        """Analisa arquivo Python e extrai informações estruturadas"""
        try:
            content = file_path.read_text()
            tree = ast.parse(content)

            # Extrair componentes
            imports = []
            functions = []
            classes = []
            decorators = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    # Verificar decoradores
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            decorators.append(decorator.id)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

            # Extrair docstring do módulo
            docstring = ast.get_docstring(tree) or ""

            # Criar snippet relevante (primeiras 50 linhas)
            lines = content.split('\n')[:50]
            snippet = '\n'.join(lines)

            return SDKKnowledge(
                file_path=str(file_path),
                module_name=file_path.stem,
                content_type=content_type,
                description=docstring[:500] if docstring else f"{content_type.title()} file: {file_path.name}",
                code_snippet=snippet,
                imports=list(set(imports))[:20],  # Limitar para não poluir
                functions=functions[:20],
                classes=classes[:10],
                decorators=list(set(decorators))[:10],
                metadata={
                    "file_size": len(content),
                    "line_count": len(lines),
                    "has_async": "async " in content,
                    "has_types": "typing" in content or "Type" in content,
                    "relative_path": str(file_path.relative_to(self.sdk_path))
                }
            )
        except Exception as e:
            print(f"Erro ao analisar {file_path}: {e}")
            return None

    def _analyze_doc_file(self, file_path: Path) -> Optional[SDKKnowledge]:
        """Analisa arquivo de documentação"""
        try:
            content = file_path.read_text()

            # Extrair seções principais
            sections = []
            current_section = ""
            for line in content.split('\n'):
                if line.startswith('#'):
                    if current_section:
                        sections.append(current_section)
                    current_section = line
                elif current_section:
                    current_section += "\n" + line

            return SDKKnowledge(
                file_path=str(file_path),
                module_name=file_path.stem,
                content_type="documentation",
                description=f"Documentation: {file_path.name}",
                code_snippet=content[:1000],  # Primeiros 1000 chars
                imports=[],
                functions=[],
                classes=[],
                decorators=[],
                metadata={
                    "sections_count": len(sections),
                    "file_size": len(content),
                    "has_examples": "```python" in content,
                    "has_installation": "pip install" in content or "Installation" in content
                }
            )
        except Exception as e:
            print(f"Erro ao analisar doc {file_path}: {e}")
            return None

    def load_to_neo4j(self, knowledge_items: List[SDKKnowledge]):
        """Carrega conhecimento estruturado no Neo4j"""

        with self.driver.session() as session:
            # 1. Criar nós principais do SDK
            session.run("""
                MERGE (sdk:SDK {name: 'Claude Code SDK Python'})
                SET sdk.version = '0.0.22',
                    sdk.path = $path,
                    sdk.updated_at = datetime(),
                    sdk.description = 'Python SDK for Claude Code with MCP support'
                RETURN sdk
            """, path=str(self.sdk_path))

            for item in knowledge_items:
                # Gerar embedding para o conhecimento
                text_for_embedding = f"""
                Module: {item.module_name}
                Type: {item.content_type}
                Description: {item.description}
                Functions: {', '.join(item.functions[:5])}
                Classes: {', '.join(item.classes[:5])}
                Code Preview: {item.code_snippet[:200]}
                """

                embedding = self.voyage_client.embed([text_for_embedding], model="voyage-2").embeddings[0]

                # Criar nó de conhecimento
                result = session.run("""
                    MERGE (k:SDKKnowledge {file_path: $file_path})
                    SET k.module_name = $module_name,
                        k.content_type = $content_type,
                        k.description = $description,
                        k.code_snippet = $code_snippet,
                        k.imports = $imports,
                        k.functions = $functions,
                        k.classes = $classes,
                        k.decorators = $decorators,
                        k.metadata = $metadata,
                        k.embedding = $embedding,
                        k.updated_at = datetime()

                    WITH k
                    MATCH (sdk:SDK {name: 'Claude Code SDK Python'})
                    MERGE (k)-[:PART_OF]->(sdk)

                    RETURN k
                """,
                file_path=item.file_path,
                module_name=item.module_name,
                content_type=item.content_type,
                description=item.description,
                code_snippet=item.code_snippet,
                imports=item.imports,
                functions=item.functions,
                classes=item.classes,
                decorators=item.decorators,
                metadata=json.dumps(item.metadata),
                embedding=embedding)

                # Criar relacionamentos entre módulos
                if item.imports:
                    for import_name in item.imports[:10]:  # Limitar imports
                        if "claude_code_sdk" in import_name:
                            session.run("""
                                MATCH (k:SDKKnowledge {file_path: $file_path})
                                MERGE (m:Module {name: $import_name})
                                MERGE (k)-[:IMPORTS]->(m)
                            """, file_path=item.file_path, import_name=import_name)

            # 2. Criar relacionamentos especiais
            self._create_sdk_relationships(session)

            # 3. Criar índices para busca otimizada
            self._create_sdk_indexes(session)

    def _create_sdk_relationships(self, session):
        """Cria relacionamentos especiais entre componentes do SDK"""

        # Conectar exemplos com código fonte relacionado
        session.run("""
            MATCH (example:SDKKnowledge {content_type: 'example'})
            MATCH (source:SDKKnowledge {content_type: 'source'})
            WHERE ANY(func IN example.functions WHERE func IN source.functions)
               OR ANY(cls IN example.classes WHERE cls IN source.classes)
            MERGE (example)-[:DEMONSTRATES]->(source)
        """)

        # Conectar testes com código testado
        session.run("""
            MATCH (test:SDKKnowledge {content_type: 'test'})
            MATCH (source:SDKKnowledge {content_type: 'source'})
            WHERE test.module_name CONTAINS replace(source.module_name, '.py', '')
            MERGE (test)-[:TESTS]->(source)
        """)

        # Criar hierarquia de módulos
        session.run("""
            MATCH (k:SDKKnowledge)
            WHERE k.content_type = 'source'
            WITH k, split(k.file_path, '/') AS path_parts
            WITH k, path_parts[-2] AS parent_module
            WHERE parent_module IS NOT NULL
            MERGE (pm:Module {name: parent_module})
            MERGE (k)-[:BELONGS_TO]->(pm)
        """)

        # Conectar componentes relacionados por funcionalidade
        session.run("""
            MATCH (k1:SDKKnowledge), (k2:SDKKnowledge)
            WHERE k1 <> k2
              AND (
                ANY(dec IN k1.decorators WHERE dec IN k2.decorators)
                OR (k1.module_name CONTAINS 'mcp' AND k2.module_name CONTAINS 'mcp')
                OR (k1.module_name CONTAINS 'hook' AND k2.module_name CONTAINS 'hook')
              )
            MERGE (k1)-[:RELATED_FUNCTIONALITY]->(k2)
        """)

    def _create_sdk_indexes(self, session):
        """Cria índices específicos para busca no SDK"""

        # Índice vetorial para SDKKnowledge
        session.run("""
            CREATE VECTOR INDEX sdk_knowledge_embedding IF NOT EXISTS
            FOR (k:SDKKnowledge) ON (k.embedding)
            OPTIONS {dimensions: 1024, similarity: 'cosine'}
        """)

        # Índice full-text para busca em código
        session.run("""
            CREATE FULLTEXT INDEX sdk_code_search IF NOT EXISTS
            FOR (k:SDKKnowledge)
            ON EACH [k.description, k.module_name, k.code_snippet]
        """)

        # Índice para funções e classes
        session.run("""
            CREATE INDEX sdk_functions IF NOT EXISTS FOR (k:SDKKnowledge) ON (k.functions)
        """)

        session.run("""
            CREATE INDEX sdk_classes IF NOT EXISTS FOR (k:SDKKnowledge) ON (k.classes)
        """)

    def query_sdk_knowledge(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Busca conhecimento sobre o SDK usando RAG híbrido
        """
        # Gerar embedding da query
        query_embedding = self.voyage_client.embed([query], model="voyage-2").embeddings[0]

        with self.driver.session() as session:
            result = session.run("""
                // 1. Busca vetorial
                CALL db.index.vector.query('sdk_knowledge_embedding', $k * 2, $query_vec)
                YIELD node AS sdk_node, score AS vec_score

                // 2. Busca full-text
                CALL db.index.fulltext.query('sdk_code_search', $query_text)
                YIELD node AS text_node, score AS text_score
                WHERE text_node = sdk_node

                // 3. Expandir contexto
                OPTIONAL MATCH (sdk_node)-[:DEMONSTRATES]->(demo:SDKKnowledge)
                OPTIONAL MATCH (sdk_node)-[:TESTS]->(test:SDKKnowledge)
                OPTIONAL MATCH (sdk_node)-[:RELATED_FUNCTIONALITY]->(related:SDKKnowledge)

                // 4. Coletar memórias relacionadas do Learning
                OPTIONAL MATCH (learning:Learning)
                WHERE learning.name CONTAINS 'claude'
                  AND learning.name CONTAINS 'sdk'

                // 5. Combinar e ranquear
                WITH sdk_node,
                     COALESCE(vec_score, 0) * 0.6 + COALESCE(text_score, 0) * 0.4 AS combined_score,
                     collect(DISTINCT demo) AS examples,
                     collect(DISTINCT test) AS tests,
                     collect(DISTINCT related) AS related_nodes,
                     collect(DISTINCT learning) AS learning_memories

                ORDER BY combined_score DESC
                LIMIT $k

                RETURN sdk_node.module_name AS module,
                       sdk_node.content_type AS type,
                       sdk_node.description AS description,
                       sdk_node.code_snippet AS code,
                       sdk_node.functions AS functions,
                       sdk_node.classes AS classes,
                       combined_score AS score,
                       [e IN examples | {name: e.module_name, snippet: substring(e.code_snippet, 0, 200)}] AS example_code,
                       [t IN tests | t.module_name] AS test_files,
                       [r IN related_nodes | r.module_name][:3] AS related_modules,
                       [l IN learning_memories | {name: l.name, desc: l.description}][:2] AS prior_knowledge
            """,
            query_vec=query_embedding,
            query_text=query,
            k=k)

            knowledge_results = []
            for record in result:
                knowledge_results.append({
                    'module': record['module'],
                    'type': record['type'],
                    'description': record['description'],
                    'code': record['code'],
                    'functions': record['functions'],
                    'classes': record['classes'],
                    'score': record['score'],
                    'examples': record['example_code'],
                    'tests': record['test_files'],
                    'related': record['related_modules'],
                    'prior_knowledge': record['prior_knowledge']
                })

            return {
                'query': query,
                'results': knowledge_results,
                'timestamp': datetime.now().isoformat()
            }

    def generate_sdk_answer(self, query: str) -> str:
        """
        Gera resposta sobre o SDK usando conhecimento do Neo4j
        """
        # Buscar conhecimento relevante
        knowledge = self.query_sdk_knowledge(query, k=5)

        # Construir contexto
        context_parts = []
        for result in knowledge['results']:
            context_part = f"""
            Module: {result['module']} (Type: {result['type']})
            Description: {result['description']}

            Key Components:
            - Functions: {', '.join(result['functions'][:5]) if result['functions'] else 'None'}
            - Classes: {', '.join(result['classes'][:3]) if result['classes'] else 'None'}
            """

            if result['code']:
                context_part += f"\nCode Snippet:\n```python\n{result['code'][:500]}\n```"

            if result['examples']:
                context_part += "\nExamples Available:"
                for ex in result['examples'][:2]:
                    context_part += f"\n- {ex['name']}: {ex['snippet'][:100]}..."

            context_parts.append(context_part)

        full_context = "\n---\n".join(context_parts)

        # Gerar resposta com Claude
        prompt = f"""
        You are an expert on the Claude Code SDK Python. Answer the following question using the knowledge from our graph database.

        Question: {query}

        Available Knowledge from Neo4j:
        {full_context}

        Please provide a comprehensive, practical answer with code examples when relevant.
        Focus on being accurate and helpful based on the actual SDK implementation.
        """

        response = self.anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.content[0].text

    def create_sdk_learning_paths(self):
        """
        Cria caminhos de aprendizado no grafo para diferentes níveis
        """
        with self.driver.session() as session:
            # Caminho para iniciantes
            session.run("""
                CREATE (path:LearningPath {
                    name: 'Claude SDK Beginner',
                    level: 'beginner',
                    description: 'Start with basic query() function and simple examples'
                })

                WITH path
                MATCH (k:SDKKnowledge)
                WHERE k.module_name IN ['quick_start', 'query', 'types']
                  AND k.content_type IN ['example', 'source']
                CREATE (path)-[:INCLUDES {order: 1}]->(k)
            """)

            # Caminho intermediário
            session.run("""
                CREATE (path:LearningPath {
                    name: 'Claude SDK Intermediate',
                    level: 'intermediate',
                    description: 'Learn ClaudeSDKClient, streaming, and error handling'
                })

                WITH path
                MATCH (k:SDKKnowledge)
                WHERE k.module_name IN ['client', 'streaming_mode', '_errors']
                  OR (k.content_type = 'example' AND k.module_name CONTAINS 'streaming')
                CREATE (path)-[:INCLUDES {order: 2}]->(k)
            """)

            # Caminho avançado
            session.run("""
                CREATE (path:LearningPath {
                    name: 'Claude SDK Advanced',
                    level: 'advanced',
                    description: 'Master hooks, MCP servers, and custom tools'
                })

                WITH path
                MATCH (k:SDKKnowledge)
                WHERE k.module_name IN ['hooks', 'mcp_calculator', 'tool_permission_callback']
                  OR k.module_name CONTAINS 'mcp'
                  OR 'tool' IN k.decorators
                CREATE (path)-[:INCLUDES {order: 3}]->(k)
            """)


# Script de execução
def main():
    """
    Executa a integração completa do Claude Code SDK com Neo4j
    """
    from neo4j import GraphDatabase

    # Configurar conexão
    driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", os.getenv("NEO4J_PASSWORD", "password"))
    )

    try:
        # Criar integração
        integration = ClaudeSDKNeo4jIntegration(driver)

        print("1. Extraindo conhecimento do SDK...")
        knowledge_items = integration.extract_sdk_knowledge()
        print(f"   Extraídos {len(knowledge_items)} itens de conhecimento")

        print("2. Carregando no Neo4j...")
        integration.load_to_neo4j(knowledge_items)
        print("   Conhecimento carregado com sucesso")

        print("3. Criando caminhos de aprendizado...")
        integration.create_sdk_learning_paths()
        print("   Caminhos criados")

        print("4. Testando busca...")
        test_query = "How to use hooks in Claude SDK?"
        result = integration.query_sdk_knowledge(test_query)
        print(f"   Query: {test_query}")
        print(f"   Resultados: {len(result['results'])} documentos encontrados")

        print("5. Gerando resposta de exemplo...")
        answer = integration.generate_sdk_answer(test_query)
        print(f"   Resposta: {answer[:200]}...")

        print("\n✅ Integração completa! O Neo4j agora tem conhecimento completo do Claude Code SDK Python")

    finally:
        driver.close()


if __name__ == "__main__":
    main()