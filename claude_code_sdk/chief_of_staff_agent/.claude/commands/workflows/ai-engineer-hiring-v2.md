---
name: ai-engineer-hiring-v2
description: Workflow OTIMIZADO de contratação de Engenheiro de IA com foco em 2025
---

# 🚀 Workflow de Contratação v2 - Engenheiro de IA

Workflow otimizado para contratar Engenheiro de IA especializado em desenvolvimento de agentes.

## 📋 Visão Geral do Processo

**Candidato**: {{args}}
**Duração Total**: 5-7 dias (ACELERADO)
**Agentes Envolvidos**: Recrutador, CTO, Chief of Staff, Python-Pro

## 🆕 NOVAS VALIDAÇÕES PARA 2025

### 🤖 Checklist Específico de IA/Agentes

#### Experiência Obrigatória:
- [ ] **LLMs**: OpenAI GPT-4, Claude 3, Gemini
- [ ] **Frameworks**: LangChain, AutoGen, CrewAI, Claude SDK
- [ ] **Vector DBs**: Pinecone, Weaviate, ChromaDB
- [ ] **RAG**: Implementação em produção
- [ ] **Prompt Engineering**: Chain-of-thought, few-shot
- [ ] **Fine-tuning**: LoRA, QLoRA, PEFT
- [ ] **Embeddings**: OpenAI, Cohere, Sentence Transformers

#### Nice to Have:
- [ ] **Open Source LLMs**: Llama 3, Mistral, Mixtral
- [ ] **MLOps**: Weights & Biases, MLflow
- [ ] **Deployment**: Replicate, HuggingFace, Modal

## 🔄 Workflow Otimizado

### Step 0: Pre-Screening Automático (NOVO - 1h)
**Hook Automático ao receber CV:**
```python
# Executa automaticamente:
1. Parse CV com AI
2. Extrai keywords de IA/ML
3. Score inicial com ai_expertise_evaluator.py
4. Rejeita se score < 50
```

### Step 1: Fast Track Assessment (Recrutador + IA - 24h)
**Triagem acelerada com IA:**
1. Video screening assíncrono (5 perguntas, 2min cada)
2. Análise automática do GitHub:
   - Repos com "langchain", "agent", "llm"
   - Commits recentes em projetos IA
   - Stars em projetos relevantes
3. Background check automático:
   - LinkedIn scraping
   - Publicações/artigos sobre IA
   - Participação em comunidades

**Output**: Relatório automático com score 0-100

### Step 2: Live Coding Challenge (CTO + Python-Pro - 2h)
**Desafio ao vivo específico de IA:**

```python
# DESAFIO: Implementar mini-agente com memória
Requisitos:
1. Usar Claude SDK ou LangChain
2. Implementar memória conversacional
3. Adicionar RAG com documents
4. Tool calling para web search
5. Stream responses

# Avaliação em tempo real:
- python-quality-synergy.py (durante coding)
- code-judge orquestra análise
- CTO observa approach e decisões
```

### Step 3: System Design Interview (CTO - 1h)
**Cases específicos de IA:**

1. **Case 1**: "Projete sistema multi-agente para customer support"
2. **Case 2**: "Arquitetura RAG para 10M documentos"
3. **Case 3**: "Pipeline de fine-tuning com feedback loop"

**Avaliar:**
- Conhecimento de patterns de agentes
- Considerações de custo (tokens, latência)
- Escalabilidade e cache strategies
- Error handling e fallbacks

### Step 4: Cultural + Vision Fit (Chief of Staff - 45min)
**Foco em mindset IA:**
1. "Como você vê AGI evoluindo?"
2. "Ética em IA - seus princípios"
3. "Contribuições open source em IA"
4. "Como se mantém atualizado?" (papers, blogs)

### Step 5: Offer Decision Matrix (Automático - 30min)
**Matriz automática de decisão:**

```python
# decision_matrix.py com pesos específicos IA:
weights = {
    'llm_experience': 0.25,      # Crítico
    'agent_frameworks': 0.20,     # Crítico
    'production_exp': 0.20,       # Importante
    'system_design': 0.15,        # Importante
    'culture_fit': 0.10,          # Relevante
    'communication': 0.10         # Relevante
}

# Auto-gera oferta baseado em score:
90-100: R$ 22.000/mês + 0.3% equity
75-89:  R$ 19.000/mês + 0.2% equity
60-74:  R$ 17.500/mês + 0.15% equity
< 60:   Rejection com feedback
```

## 🎯 KPIs do Processo

### Métricas de Sucesso:
- **Time to Hire**: < 7 dias (vs 10 anterior)
- **Acceptance Rate**: > 85%
- **Quality Score**: >= 80/100
- **Cost per Hire**: < R$ 5.000
- **Retention 90d**: > 95%

### Automação Level:
- **70% automático** (vs 40% anterior)
- **30% human-in-the-loop** para decisões críticas

## 🔧 Ferramentas Integradas

### Scripts Automáticos:
```bash
.claude/hooks/scripts/
├── ai_expertise_evaluator.py    # Score IA/ML
├── python-quality-synergy.py    # Qualidade código
├── talent_scorer.py              # Score geral
├── decision_matrix.py            # Decisão final
└── offer_generator.py            # NOVO - Gera proposta
```

### Neo4j Tracking:
```cypher
// Salva todo histórico
CREATE (h:Hiring {
  candidate: $name,
  position: 'AI Engineer',
  scores: $scores,
  decision: $decision,
  timestamp: datetime()
})

// Aprende com padrões de sucesso
MATCH (h:Hiring)-[:RESULTED_IN]->(s:Success)
RETURN h.scores, count(*) as success_rate
```

## 📊 Dashboard de Acompanhamento

### Queries para Monitoramento:
```python
# Status em tempo real
mcp__neo4j-memory__search_memories(
  query='hiring status:active position:ai_engineer',
  limit=20
)

# Taxa de conversão por etapa
mcp__neo4j-memory__search_memories(
  query='hiring funnel_stage:* conversion_rate:*'
)

# Candidatos em pipeline
mcp__neo4j-memory__search_memories(
  query='candidate stage:in_progress',
  depth=2
)
```

## 🚀 Comando Quick Start

```bash
# Iniciar avaliação completa
/ai-engineer-hiring-v2 "João Silva" --fast-track --auto-score

# Batch processing
/ai-engineer-hiring-v2 --batch candidates.csv --parallel

# Re-avaliar com novos critérios
/ai-engineer-hiring-v2 --reevaluate "Maria Costa" --focus "llm_experience"
```

## ⚡ Modo Emergencial

Para contratação urgente (< 3 dias):
```bash
/ai-engineer-hiring-v2 --emergency --skip-cultural --auto-approve-if-score > 85
```

---

**NOTA**: Este workflow v2 é 40% mais rápido e 70% mais automatizado que a versão anterior, mantendo a qualidade da avaliação através de validações específicas de IA.