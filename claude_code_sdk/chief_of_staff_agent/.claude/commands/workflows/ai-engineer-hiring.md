---
name: ai-engineer-hiring
description: Workflow completo de contratação de Engenheiro de IA coordenando Recrutador, CTO e Chief of Staff
---

# 🚀 Workflow de Contratação - Engenheiro de IA

Executar workflow completo para contratar Engenheiro de IA especializado em desenvolvimento de agentes.

## 📋 Visão Geral do Processo

**Candidato**: {{args}}
**Duração Total**: 7-10 dias
**Agentes Envolvidos**: Recrutador, CTO, Chief of Staff

## 🔄 Execução do Workflow

### Step 1: Pipeline Setup (Recrutador - 48h)
Use o agente recrutador para:
1. Definir requisitos detalhados da vaga
2. Publicar em plataformas relevantes (LinkedIn, AngelList, HN)
3. Buscar candidatos ativos no GitHub com projetos de LangChain/Claude SDK
4. Fazer triagem inicial com `talent_scorer.py`
**Critério de Sucesso**: Mínimo 5 candidatos qualificados identificados

### Step 2: Initial Screening (Recrutador - 72h)
Execute triagem inicial:
1. Entrevista de 30 minutos focada em motivação
2. Avaliar fit cultural para ambiente de startup
3. Verificar expectativas salariais (R$ 17.500/mês para sênior)
4. Aplicar scoring com `/talent-scan {{candidato}}`
**Critério de Sucesso**: Mínimo 2 candidatos com score > 70

### Step 3: Technical Assessment (CTO - 90 min)
Use o agente cto para avaliação técnica profunda:
1. Review do portfolio GitHub
2. Teste prático: "Implementar agente com LangChain para RAG"
3. Design de sistema: "Arquitetura multi-agente para code review"
4. Discussão sobre experiência com produção
5. Executar `ai_expertise_evaluator.py --candidate {{candidato}}`
**Critério de Sucesso**: Score técnico >= 8/10

### Step 4: Team Fit Assessment (CTO + Equipe - 60 min)
Avaliar fit com equipe técnica:
1. Pair programming com engenheiro sênior
2. Discussão sobre arquitetura atual de agentes
3. Apresentação de um projeto próprio de IA
4. Feedback da equipe técnica
**Critério de Sucesso**: Aprovação unânime da equipe

### Step 5: Strategic Brief (Chief of Staff)
Consolidar todas as avaliações:
1. Executar `/strategic-brief contratação {{candidato}}`
2. Compilar scores do Recrutador e CTO
3. Analisar impacto no runway e composição da equipe
4. Preparar recomendação executiva
**Deliverable**: Relatório executivo com decisão hire/no-hire

### Step 6: Offer Negotiation (Recrutador)
Finalizar contratação:
1. Confirmar salário: R$ 17.500/mês (sênior)
2. Preparar carta oferta formal (CLT ou PJ)
3. Negociar benefícios (VR/VA, plano saúde)
4. Coordenar onboarding
**Critério de Sucesso**: Oferta aceita pelo candidato

## 📊 Monitoramento do Workflow

### Queries Neo4j para Acompanhamento
```cypher
# Ver status atual do workflow
search_memories(query='workflow_id:ai_engineer_hiring_techstart status:active')

# Próximas etapas pendentes
search_memories(query='owner:cto status:pending')

# Histórico completo
search_memories(query='workflow_id:ai_engineer_hiring_techstart', depth=2)
```

## 🎯 Critérios de Avaliação

### Recrutador (Cultural Fit)
- Experiência com startups: 0-10
- Motivação para IA: 0-10
- Mentalidade de ownership: 0-10
- Expectativas alinhadas: Match/High/Low

### CTO (Technical Skills)
- Expertise em LLMs: 0-10
- Frameworks (LangChain, etc): 0-10
- Produção com IA: 0-10
- Arquitetura de sistemas: 0-10
- Qualidade de código: 0-10

## 🔧 Ferramentas Integradas

- **Scripts Python**:
  - `talent_scorer.py` - Pontuação automática de candidatos
  - `ai_expertise_evaluator.py` - Avaliação técnica de IA

- **Slash Commands**:
  - `/talent-scan` - Análise de perfil
  - `/tech-assessment` - Avaliação técnica
  - `/strategic-brief` - Consolidação executiva

## ⚡ Automação e Triggers

O workflow avança automaticamente quando:
- Step 1→2: 5+ candidatos identificados
- Step 2→3: Score > 70 na triagem
- Step 3→4: Score técnico >= 8/10
- Step 4→5: Aprovação da equipe
- Step 5→6: Aprovação executiva

## 📈 Métricas de Sucesso

- **Time to Hire**: < 10 dias
- **Qualidade**: Score técnico >= 8/10
- **Fit Cultural**: Score >= 70
- **Aceitação**: > 80% das ofertas
- **Retenção**: > 95% em 90 dias

## 🚦 Red Flags

⚠️ Sinais de alerta para rejeição:
- Sem experiência com produção de IA
- Dependência de único framework
- Prefere grandes corporações
- Sem paixão por agentes/LLMs
- Expectativas salariais desalinhadas

## ✅ Green Flags

✨ Sinais positivos para aprovação:
- Contribuições open source em IA
- Side projects com agentes
- Experiência com múltiplos LLMs
- Mentalidade de experimentação
- Entusiasmo por aprendizado contínuo

---

**Nota**: Este workflow está integrado com Neo4j MCP para rastreamento completo. Cada etapa cria memórias e conexões no grafo de conhecimento.