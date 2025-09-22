"""
Neo4j GraphRAG Implementation - Substituindo RAG Tradicional
Migração de Voyage AI + Vector DB in-memory para Neo4j com busca híbrida
"""

import os
import json
import numpy as np
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from neo4j import GraphDatabase
import anthropic
import voyageai

@dataclass
class RAGConfig:
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "password")
    voyage_api_key: str = os.getenv("VOYAGE_API_KEY")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY")
    vector_index_name: str = "doc_embeddings"
    embedding_dimension: int = 1024
    similarity_metric: str = "cosine"

class Neo4jGraphRAG:
    """
    Sistema RAG aprimorado usando Neo4j para armazenamento vetorial e
    navegação em grafo, substituindo a abordagem tradicional de vector DB in-memory
    """

    def __init__(self, config: RAGConfig):
        self.config = config
        self.driver = GraphDatabase.driver(
            config.neo4j_uri,
            auth=(config.neo4j_user, config.neo4j_password)
        )
        self.voyage_client = voyageai.Client(api_key=config.voyage_api_key)
        self.anthropic_client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        self._ensure_indexes()

    def _ensure_indexes(self):
        """Criar índices vetoriais e constraints no Neo4j"""
        with self.driver.session() as session:
            # Criar constraint para URLs únicas
            session.run("""
                CREATE CONSTRAINT doc_url IF NOT EXISTS
                FOR (d:Document) REQUIRE d.url IS UNIQUE
            """)

            # Criar índice vetorial
            session.run(f"""
                CREATE VECTOR INDEX {self.config.vector_index_name} IF NOT EXISTS
                FOR (d:Document) ON (d.embedding)
                OPTIONS {{
                    dimensions: {self.config.embedding_dimension},
                    similarity: '{self.config.similarity_metric}'
                }}
            """)

            # Criar índice full-text para busca híbrida
            session.run("""
                CREATE FULLTEXT INDEX doc_text_index IF NOT EXISTS
                FOR (d:Document) ON EACH [d.text, d.heading, d.summary]
            """)

    def migrate_from_traditional_rag(self, json_file_path: str):
        """
        Migrar dados do formato tradicional (JSON) para Neo4j
        Mantém compatibilidade com estrutura existente do Anthropic Cookbook
        """
        with open(json_file_path, 'r') as f:
            docs = json.load(f)

        batch_size = 128
        processed = 0

        for i in range(0, len(docs), batch_size):
            batch = docs[i:i+batch_size]

            # Gerar embeddings usando Voyage AI (mantém a mesma biblioteca)
            texts = [f"Heading: {doc['chunk_heading']}\n\nText: {doc['text']}"
                    for doc in batch]
            embeddings = self.voyage_client.embed(texts, model="voyage-2").embeddings

            # Inserir no Neo4j com transação
            with self.driver.session() as session:
                session.execute_write(self._insert_documents_tx, batch, embeddings)

            processed += len(batch)
            print(f"Migrados {processed}/{len(docs)} documentos")

        # Criar relacionamentos entre documentos
        self._create_document_relationships()

        print(f"Migração completa! {len(docs)} documentos no grafo.")

    def _insert_documents_tx(self, tx, documents, embeddings):
        """Transação para inserir documentos com embeddings"""
        query = """
        UNWIND $data AS doc
        MERGE (d:Document {url: doc.url})
        SET d.chunk_heading = doc.heading,
            d.text = doc.text,
            d.summary = doc.summary,
            d.embedding = doc.embedding,
            d.created_at = datetime()
        RETURN d
        """

        data = []
        for doc, emb in zip(documents, embeddings):
            data.append({
                'url': doc['chunk_link'],
                'heading': doc['chunk_heading'],
                'text': doc['text'],
                'summary': doc.get('summary', ''),
                'embedding': emb
            })

        return tx.run(query, data=data)

    def _create_document_relationships(self):
        """Criar relacionamentos entre documentos baseado em similaridade e tópicos"""
        with self.driver.session() as session:
            # Conectar documentos do mesmo tópico
            session.run("""
                MATCH (d1:Document), (d2:Document)
                WHERE d1 <> d2
                AND d1.url STARTS WITH substring(d2.url, 0, 50)
                MERGE (d1)-[:SAME_TOPIC]->(d2)
            """)

            # Conectar documentos similares (top-3 mais similares para cada doc)
            session.run("""
                MATCH (d:Document)
                WHERE d.embedding IS NOT NULL
                CALL db.index.vector.query($index_name, 4, d.embedding)
                YIELD node, score
                WHERE node <> d AND score > 0.8
                MERGE (d)-[:SIMILAR_TO {score: score}]->(node)
            """, index_name=self.config.vector_index_name)

    def retrieve_hybrid(self, query: str, k: int = 5) -> Tuple[List[Dict], str]:
        """
        Busca híbrida: combina busca vetorial com travessia de grafo
        Substitui retrieve_base() e retrieve_advanced() do cookbook original
        """
        # Gerar embedding da query
        query_embedding = self.voyage_client.embed(
            [query],
            model="voyage-2"
        ).embeddings[0]

        with self.driver.session() as session:
            # Busca híbrida: vetorial + grafo + full-text
            result = session.run("""
                // 1. Busca vetorial inicial
                CALL db.index.vector.query($index_name, $k * 2, $query_vec)
                YIELD node AS doc, score AS vector_score

                // 2. Expandir contexto via relacionamentos
                OPTIONAL MATCH (doc)-[:SIMILAR_TO]-(similar:Document)
                OPTIONAL MATCH (doc)-[:SAME_TOPIC]-(related:Document)

                // 3. Busca full-text complementar
                CALL db.index.fulltext.query('doc_text_index', $query_text)
                YIELD node AS text_match, score AS text_score
                WHERE text_match = doc

                // 4. Calcular score combinado
                WITH doc,
                     vector_score,
                     COALESCE(text_score, 0) AS text_score,
                     collect(DISTINCT similar) AS similar_docs,
                     collect(DISTINCT related) AS related_docs

                WITH doc,
                     (vector_score * 0.7 + text_score * 0.3) AS combined_score,
                     similar_docs,
                     related_docs

                ORDER BY combined_score DESC
                LIMIT $k

                // 5. Retornar contexto enriquecido
                RETURN doc.url AS url,
                       doc.chunk_heading AS heading,
                       doc.text AS text,
                       doc.summary AS summary,
                       combined_score AS score,
                       [s IN similar_docs | {heading: s.chunk_heading, summary: s.summary}][:2] AS similar_context,
                       [r IN related_docs | {heading: r.chunk_heading}][:2] AS related_context
            """,
            index_name=self.config.vector_index_name,
            query_vec=query_embedding,
            query_text=query,
            k=k)

            documents = []
            context_parts = []

            for record in result:
                # Documento principal
                doc = {
                    'metadata': {
                        'chunk_link': record['url'],
                        'chunk_heading': record['heading'],
                        'text': record['text'],
                        'summary': record['summary']
                    },
                    'similarity': record['score']
                }
                documents.append(doc)

                # Contexto enriquecido com documentos relacionados
                context_part = f"""
                <document>
                Heading: {record['heading']}

                Content:
                {record['text']}

                Summary: {record['summary']}
                """

                # Adicionar contexto de documentos similares
                if record['similar_context']:
                    context_part += "\n\nRelated Context:\n"
                    for similar in record['similar_context']:
                        context_part += f"- {similar['heading']}: {similar['summary']}\n"

                context_part += "</document>"
                context_parts.append(context_part)

            context = "\n".join(context_parts)

        return documents, context

    def rerank_with_claude(self, query: str, documents: List[Dict], k: int = 3) -> List[Dict]:
        """
        Re-ranking usando Claude (substitui rerank_results do cookbook)
        Agora com contexto de grafo para melhor ranking
        """
        summaries = []
        for i, doc in enumerate(documents):
            metadata = doc['metadata']
            summary = f"[{i}] {metadata['chunk_heading']}\n"
            summary += f"Summary: {metadata['summary']}\n"
            summary += f"Relevance Score: {doc['similarity']:.2f}"
            summaries.append(summary)

        prompt = f"""
        Query: {query}

        You have documents retrieved from a knowledge graph. Each has a relevance score from our hybrid search.
        Select the {k} most relevant documents considering both the content AND the graph-based relevance scores.

        <documents>
        {chr(10).join(summaries)}
        </documents>

        Return only the indices of the {k} most relevant documents, separated by commas:
        """

        response = self.anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        try:
            indices = [int(idx.strip()) for idx in response.content[0].text.split(',')]
            reranked = [documents[idx] for idx in indices[:k] if idx < len(documents)]
            return reranked
        except:
            return documents[:k]

    def answer_query(self, query: str, use_reranking: bool = True) -> str:
        """
        Responder query usando RAG aprimorado com Neo4j
        Substitui answer_query_base e answer_query_advanced
        """
        # Recuperação híbrida
        documents, context = self.retrieve_hybrid(query, k=10 if use_reranking else 3)

        # Re-ranking opcional
        if use_reranking and len(documents) > 3:
            documents = self.rerank_with_claude(query, documents, k=3)
            # Reconstruir contexto com documentos re-rankeados
            context_parts = []
            for doc in documents:
                metadata = doc['metadata']
                context_parts.append(f"""
                <document>
                {metadata['chunk_heading']}

                {metadata['text']}
                </document>
                """)
            context = "\n".join(context_parts)

        # Gerar resposta com Claude
        prompt = f"""
        You have been tasked with answering the following query using a knowledge graph enhanced RAG system:

        <query>
        {query}
        </query>

        You have access to the following documents and their relationships from the knowledge graph:

        <context>
        {context}
        </context>

        Please provide a comprehensive answer based on the context.
        The documents include both primary content and related information from the graph.
        Be faithful to the context and leverage the relationships between documents when relevant.

        Answer:
        """

        response = self.anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.content[0].text

    def add_user_feedback(self, query: str, answer: str, feedback: str, score: int):
        """
        Adicionar feedback do usuário ao grafo para aprendizado contínuo
        Funcionalidade não disponível no RAG tradicional
        """
        with self.driver.session() as session:
            session.run("""
                CREATE (f:Feedback {
                    query: $query,
                    answer: $answer,
                    feedback: $feedback,
                    score: $score,
                    timestamp: datetime()
                })

                // Conectar com documentos usados na resposta
                WITH f
                MATCH (d:Document)
                WHERE d.text CONTAINS substring($answer, 0, 100)
                MERGE (f)-[:ABOUT]->(d)

                RETURN f
            """, query=query, answer=answer, feedback=feedback, score=score)

    def get_analytics(self) -> Dict[str, Any]:
        """
        Analytics do sistema RAG usando capacidades do grafo
        """
        with self.driver.session() as session:
            stats = session.run("""
                MATCH (d:Document)
                WITH count(d) AS total_docs

                MATCH ()-[r:SIMILAR_TO]->()
                WITH total_docs, count(r) AS similarity_links

                MATCH ()-[t:SAME_TOPIC]->()
                WITH total_docs, similarity_links, count(t) AS topic_links

                OPTIONAL MATCH (f:Feedback)
                WITH total_docs, similarity_links, topic_links,
                     count(f) AS feedbacks,
                     avg(f.score) AS avg_feedback_score

                RETURN {
                    documents: total_docs,
                    similarity_connections: similarity_links,
                    topic_connections: topic_links,
                    total_connections: similarity_links + topic_links,
                    user_feedbacks: feedbacks,
                    average_feedback_score: avg_feedback_score
                } AS stats
            """).single()['stats']

        return stats

    def close(self):
        """Fechar conexão com Neo4j"""
        self.driver.close()


# Exemplo de uso e migração
def exemplo_migracao():
    """
    Demonstra como migrar do sistema RAG tradicional para Neo4j GraphRAG
    """

    # Configurar Neo4j GraphRAG
    config = RAGConfig()
    graph_rag = Neo4jGraphRAG(config)

    # 1. Migrar dados existentes
    print("Migrando dados do formato tradicional...")
    graph_rag.migrate_from_traditional_rag('data/anthropic_summary_indexed_docs.json')

    # 2. Testar recuperação híbrida
    query = "How can I implement caching in Claude?"
    print(f"\nTestando query: {query}")

    documents, context = graph_rag.retrieve_hybrid(query)
    print(f"Recuperados {len(documents)} documentos com contexto enriquecido")

    # 3. Gerar resposta
    answer = graph_rag.answer_query(query, use_reranking=True)
    print(f"\nResposta: {answer[:500]}...")

    # 4. Adicionar feedback (nova funcionalidade)
    graph_rag.add_user_feedback(
        query=query,
        answer=answer,
        feedback="Resposta precisa e útil",
        score=5
    )

    # 5. Ver analytics
    stats = graph_rag.get_analytics()
    print(f"\nEstatísticas do GraphRAG:")
    print(f"- Documentos: {stats['documents']}")
    print(f"- Conexões de similaridade: {stats['similarity_connections']}")
    print(f"- Conexões de tópico: {stats['topic_connections']}")
    print(f"- Feedbacks: {stats['user_feedbacks']}")

    graph_rag.close()


if __name__ == "__main__":
    exemplo_migracao()