---
name: start-ai-bootcamp
description: Iniciar programa intensivo de desenvolvimento em IA para candidato em transição
---

# 🚀 Comando de Inicialização do Bootcamp IA

Inicia o programa de mentoria intensiva de 12 semanas para transformar desenvolvedores em engenheiros de IA.

## Uso

```bash
/start-ai-bootcamp "Diego Fornalha" --score-atual 45 --meta 95 --mentor "ai-mentor"
```

## Fluxo de Execução

### 1. Avaliação Inicial
Delega para o agente `ai-mentor` fazer diagnóstico completo:
- Análise de gaps de conhecimento
- Identificação de forças transferíveis
- Estimativa de velocidade de aprendizado
- Personalização do curriculum

### 2. Criação do Plano Personalizado
```python
# Plano específico para Diego Fornalha
bootcamp_plan = {
    "candidato": "{{args}}",
    "duracao": "12 semanas",
    "score_inicial": 45,
    "score_meta": 95,
    "mentor_principal": "ai-mentor",
    "suporte": "CTO",

    "fase_1": {
        "semanas": "1-4",
        "foco": "Fundamentos LLM + RAG",
        "meta_score": 60,
        "projeto": "RAG para Smart Contracts"
    },

    "fase_2": {
        "semanas": "5-8",
        "foco": "Frameworks (LangChain, Claude CODE SDK)",
        "meta_score": 75,
        "projeto": "Agente de auditoria Solidity"
    },

    "fase_3": {
        "semanas": "9-12",
        "foco": "Produção e otimização",
        "meta_score": 90,
        "projeto": "Plataforma Web3 + IA"
    },

    "fase_4": {
        "semanas": "13-16",
        "foco": "Especialização e inovação",
        "meta_score": 95+,
        "projeto": "Contribuição open source"
    }
}
```

### 3. Setup do Ambiente

#### Recursos Automaticamente Provisionados:
- **Contas e APIs**:
  - Claude Code SDK configurado
  - Acesso Claude via SDK empresarial

- **Infraestrutura**:
  - Workspace no Slack #ai-bootcamp-diego
  - Repo GitHub privado para projetos
  - Ambiente local de desenvolvimento
  - ChromaDB local para RAG
  - Neo4j para tracking

- **Materiais de Estudo**:
  - FastAI Course access
  - DeepLearning.AI subscription
  - O'Reilly Learning (livros IA/ML)
  - Papers importantes em PDF

### 4. Cronograma Detalhado

#### Semana 1: Kickoff e Fundamentos
```markdown
Segunda:
- 09:00 - Welcome call com CTO
- 10:00 - Setup ambiente de desenvolvimento
- 14:00 - Introdução a LLMs (vídeo curso)
- 16:00 - Primeiro código: Hello World com OpenAI

Terça:
- 09:00 - Conceitos: Tokens e Embeddings
- 11:00 - Hands-on: API OpenAI
- 14:00 - Pair programming com mentor
- 16:00 - Projeto do dia: Text classifier

Quarta:
- 09:00 - Prompt Engineering basics
- 11:00 - Workshop: Chain-of-thought
- 14:00 - Exercícios práticos
- 16:00 - Code review com mentor

Quinta:
- 09:00 - Introdução a RAG
- 11:00 - Vector databases overview
- 14:00 - Implementar primeiro RAG
- 16:00 - Debug session com mentor

Sexta:
- 09:00 - Projeto semanal: CLI Summarizer
- 14:00 - Apresentação do projeto
- 15:00 - Feedback e planning próxima semana
- 16:00 - Friday Tech Talk: "IA no Mundo Real"
```

### 5. Sistema de Tracking

#### Dashboard Neo4j
```cypher
// Inicializar jornada de bootcamp
CREATE (b:Bootcamp {
    candidato: 'Diego Fornalha',
    inicio: date(),
    score_inicial: 45,
    score_atual: 45,
    score_meta: 95,
    semana_atual: 0,
    status: 'INICIANDO',
    mentor: 'ai-mentor',
    velocity: 'NOT_MEASURED'
})

// Criar milestones
CREATE (m1:Milestone {semana: 4, meta: 60, conceitos: ['LLM', 'RAG', 'APIs']})
CREATE (m2:Milestone {semana: 8, meta: 75, conceitos: ['LangChain', 'Agents']})
CREATE (m3:Milestone {semana: 12, meta: 90, conceitos: ['Production', 'Scale']})
CREATE (m4:Milestone {semana: 16, meta: 95, conceitos: ['Innovation', 'Leadership']})

// Conectar milestones ao bootcamp
MATCH (b:Bootcamp {candidato: 'Diego Fornalha'})
MATCH (m:Milestone)
CREATE (b)-[:HAS_MILESTONE]->(m)
```

#### Métricas Semanais
```python
def track_weekly_progress(candidate: str, week: int):
    metrics = {
        "conceitos_aprendidos": [],
        "projetos_completados": [],
        "horas_estudo": 0,
        "horas_mentoria": 0,
        "codigo_produzido_loc": 0,
        "score_atual": 0,
        "velocity": "ON_TRACK/BEHIND/AHEAD",
        "bloqueios": [],
        "highlights": []
    }

    # Salvar no Neo4j
    save_to_neo4j(candidate, week, metrics)

    # Gerar relatório
    generate_weekly_report(candidate, metrics)

    # Ajustar plano se necessário
    if metrics["velocity"] == "BEHIND":
        add_extra_support(candidate)
    elif metrics["velocity"] == "AHEAD":
        accelerate_curriculum(candidate)
```

### 6. Suporte e Comunicação

#### Canais de Suporte
- **Slack #ai-bootcamp-diego**: Comunicação diária
- **Office Hours**: 16:00-17:00 todos os dias
- **Pair Programming**: 3x por semana
- **Code Review**: Toda sexta-feira
- **1:1 com CTO**: Quinzenal

#### SLA de Resposta
- Dúvidas críticas: 30 minutos
- Dúvidas normais: 2 horas
- Code review: 24 horas
- Feedback projetos: 48 horas

### 7. Projetos por Fase

#### Fase 1 (Semanas 1-4): Fundamentos
1. **CLI Text Summarizer**: Ferramenta de resumo usando OpenAI
2. **Embedding Explorer**: Visualizador de embeddings
3. **Smart Contract RAG**: Q&A sobre contratos Solidity
4. **Prompt Library**: Sistema de templates reutilizáveis

#### Fase 2 (Semanas 5-8): Frameworks
1. **LangChain Agent**: Agente com ferramentas customizadas
2. **Conversation Bot**: Sistema com memória persistente
3. **Code Auditor**: Agente que analisa código Solidity
4. **Multi-Chain System**: Workflow com múltiplos agentes

#### Fase 3 (Semanas 9-12): Produção
1. **Production API**: Deploy de agente em produção
2. **Cost Optimizer**: Sistema de cache e otimização
3. **A/B Testing**: Framework para testar prompts
4. **Full Platform**: Web3 + IA integrado

#### Fase 4 (Semanas 13-16): Especialização
1. **Open Source**: Contribuição para LangChain/outros
2. **Research Project**: Implementar paper recente
3. **Innovation**: Criar algo novo no espaço
4. **Teaching**: Mentorar outro desenvolvedor

### 8. Avaliações e Certificação

#### Checkpoints Formais
- **Semana 4**: Exame de Fundamentos (target: 60/100)
- **Semana 8**: Projeto de Frameworks (target: 75/100)
- **Semana 12**: Deploy em Produção (target: 90/100)
- **Semana 16**: Apresentação Final (target: 95/100)

#### Certificação
Ao atingir score 90+:
- Certificado interno "AI Engineer - TechStart"
- Promoção de L3 Trainee para L4 Engineer
- Ajuste salarial automático
- Entrada no time de IA como membro pleno

### 9. Comandos de Acompanhamento

```bash
# Verificar progresso atual
/check-bootcamp-progress "Diego Fornalha"

# Agendar mentoria extra
/schedule-mentoring "Diego Fornalha" --topic "RAG optimization"

# Solicitar recursos adicionais
/request-resources "Diego Fornalha" --type "gpu-credits"

# Avaliar projeto
/evaluate-project "Diego Fornalha" --project "smart-contract-rag"

# Ajustar plano
/adjust-bootcamp-plan "Diego Fornalha" --accelerate
```

### 10. Integração com Agentes

O comando automaticamente:
1. Aciona o `ai-mentor` para conduzir o programa
2. Notifica o `cto` sobre início do bootcamp
3. Configura o `chief-of-staff` para acompanhar ROI
4. Registra tudo no Neo4j para aprendizado contínuo

---

**Resultado Esperado**: Diego Fornalha sairá do score 45 para 95+ em 12-16 semanas, tornando-se um AI Engineer produtivo e inovador.