---
name: ai-basics
description: Aprenda os fundamentos de IA e LLMs com explicações práticas e exemplos de código
---

# 🎓 AI Basics - Fundamentos de IA para Iniciantes

Este comando fornece explicações e exemplos práticos sobre conceitos fundamentais de IA.

## Uso

```bash
/ai-basics "tokens"           # Entenda o que são tokens
/ai-basics "embeddings"       # Aprenda sobre embeddings
/ai-basics "rag"              # Introdução ao RAG
/ai-basics "prompt-engineering" # Técnicas de prompt
/ai-basics "llm"              # Como funcionam LLMs
/ai-basics                    # Menu interativo
```

## Conceitos Disponíveis

### 1. Tokens
**O que são:** Unidades básicas que LLMs usam para processar texto
**Exemplo prático:**
```python
# Texto: "Hello World" pode virar:
# Tokens: ["Hello", " World"] ou ["Hel", "lo", " Wor", "ld"]

from claude_code_sdk import ClaudeCodeClient, ClaudeCodeOptions

async def contar_tokens(texto):
    # Claude processa ~3-4 caracteres por token em média
    estimativa = len(texto) / 4
    print(f"Texto: {texto}")
    print(f"Tokens estimados: {estimativa:.0f}")

# "Olá mundo" = ~2-3 tokens
# "Inteligência Artificial" = ~6-7 tokens
```

### 2. Embeddings
**O que são:** Representações numéricas de texto em vetores
**Exemplo prático:**
```python
# Embeddings transformam palavras em números
# "gato" → [0.2, -0.5, 0.8, ...]
# "cachorro" → [0.3, -0.4, 0.7, ...]
# Palavras similares têm vetores próximos!

# Uso prático: busca semântica
textos = ["Python é ótimo", "JavaScript é legal", "IA é o futuro"]
query = "programação"
# Embedding encontra "Python é ótimo" mesmo sem a palavra "programação"
```

### 3. RAG (Retrieval-Augmented Generation)
**O que é:** Técnica para dar contexto extra ao LLM
**Exemplo prático:**
```python
# RAG em 3 passos simples:

async def rag_simples(pergunta):
    # 1. BUSCAR - Encontra informações relevantes
    documentos = buscar_documentos_similares(pergunta)

    # 2. AUMENTAR - Adiciona contexto à pergunta
    contexto = f"""
    Contexto: {documentos}
    Pergunta: {pergunta}
    """

    # 3. GERAR - Claude responde com o contexto
    resposta = await claude.query(contexto)
    return resposta

# Exemplo: "Qual a capital do Brasil?"
# RAG busca: "Brasil é um país da América do Sul..."
# Claude responde com contexto completo!
```

### 4. Prompt Engineering
**O que é:** Arte de escrever instruções eficazes para IA
**Técnicas principais:**

```python
# ❌ Prompt ruim
"escreve codigo"

# ✅ Prompt bom
"""
Escreva uma função Python que:
1. Receba uma lista de números
2. Retorne apenas os pares
3. Use list comprehension
4. Adicione type hints
"""

# 🚀 Prompt profissional (Few-shot)
"""
Exemplos de análise de sentimento:
"Adorei!" → Positivo
"Péssimo" → Negativo

Analise: "Muito bom esse produto"
"""
```

### 5. Chain-of-Thought
**O que é:** Fazer a IA "pensar em voz alta"
```python
# Sem CoT
prompt = "Quanto é 245 * 38?"

# Com CoT
prompt = """
Quanto é 245 * 38?
Pense passo a passo:
1. Primeiro decomponha os números
2. Faça as multiplicações parciais
3. Some os resultados
"""
```

### 6. Temperature
**O que é:** Controla criatividade vs precisão
```python
# temperature = 0.0 → Respostas determinísticas
# temperature = 0.7 → Balanceado (padrão)
# temperature = 1.0 → Mais criativo/aleatório

options = ClaudeCodeOptions(
    temperature=0.1  # Para código: mais preciso
    # temperature=0.9  # Para escrita criativa
)
```

## Exercícios Práticos

### Semana 1 - Exercício Token
```python
# Complete o código:
async def analisar_custo_tokens(texto):
    # TODO: Calcule quantos tokens
    # TODO: Estime custo (Claude: $3/milhão tokens input)
    # TODO: Retorne análise
    pass
```

### Semana 1 - Exercício Prompt
```python
# Melhore este prompt:
prompt_ruim = "faz um site"

# Sua versão melhorada:
prompt_bom = """
TODO: Adicione:
- Especificações claras
- Tecnologias desejadas
- Estrutura esperada
- Exemplos se possível
"""
```

## Recursos de Aprendizado

### 📚 Leitura Essencial
1. "Attention is All You Need" - Paper fundamental
2. "What are Embeddings?" - OpenAI Guide
3. "RAG Survey 2024" - Estado da arte
4. "Prompt Engineering Guide" - Anthropic

### 🎥 Vídeos Recomendados
1. "LLMs Explained in 5 Minutes"
2. "Building Your First RAG System"
3. "Claude CODE SDK Tutorial"

### 🧪 Projetos para Praticar
1. **Dia 1**: Contador de tokens
2. **Dia 2**: Classificador com prompts
3. **Dia 3**: Mini RAG com 10 documentos
4. **Dia 4**: Comparador de embeddings
5. **Dia 5**: CLI com Claude CODE SDK

## Tracking Neo4j

Quando você usa este comando, salvamos seu progresso:
```cypher
CREATE (l:Learning {
    conceito: 'tokens',
    data: datetime(),
    compreensao: 'iniciante',
    exercicios_feitos: 0
})
```

## Dicas do Diego

> "Quando eu comecei, o conceito de tokens foi o mais confuso.
> Pense neles como sílabas que a IA usa para 'ler'.
> Uma vez que você entende tokens, embeddings fazem sentido,
> e RAG vira natural. Um conceito constrói sobre o outro!"

## Próximos Passos

Depois de dominar os basics:
1. Use `/week-project` para seu primeiro projeto
2. Use `/daily-progress` para registrar aprendizado
3. Use `/mentor-help` quando travar

---

**Lembre-se**: Todo expert já foi iniciante. A diferença é que eles continuaram praticando! 🚀