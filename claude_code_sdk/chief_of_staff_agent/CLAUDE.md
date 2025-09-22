# CLAUDE.md - Chief of Staff Context

## Visão Geral da Empresa
- **Empresa**: TechStart Inc
- **Estágio**: Series A (Fechou $10M em Janeiro 2024)
- **Indústria**: B2B SaaS - Plataforma de desenvolvimento de agentes de IA
- **Fundada**: 2022
- **Sede**: San Francisco, CA

## Financial Snapshot
- **Monthly Burn Rate**: $500,000
- **Current Runway**: 20 months (until September 2025)
- **ARR**: $2.4M (growing 15% MoM)
- **Cash in Bank**: $10M
- **Revenue per Employee**: $48K

## Team Structure
- **Total Headcount**: 50
- **Engineering**: 25 (50%)
  - Backend: 12
  - Frontend: 8
  - DevOps/SRE: 5
- **Sales & Marketing**: 12 (24%)
- **Product**: 5 (10%)
- **Operations**: 5 (10%)
- **Executive**: 3 (6%)

## Key Metrics
- **Customer Count**: 120 enterprise customers
- **NPS Score**: 72
- **Monthly Churn**: 2.5%
- **CAC**: $15,000
- **LTV**: $85,000
- **CAC Payback Period**: 10 months

## Prioridades Atuais (Q2 2024)
1. **Contratação**: Adicionar 10 engenheiros especialistas em IA para acelerar desenvolvimento
2. **Produto**: Lançar plataforma de agentes autônomos até fim do Q2
3. **Vendas**: Expandir para mercado europeu
4. **Fundraising**: Iniciar conversas Series B (meta: $30M)

## Benchmarks de Compensação (Brasil Remote - CLT/PJ)
- **Engenheiro IA Sênior**: R$ 17.500/mês (R$ 210K/ano)
- **Engenheiro IA Júnior**: R$ 12.000/mês (R$ 144K/ano)
- **ML Engineer**: R$ 15.000/mês (R$ 180K/ano)
- **Arquiteto de Agentes**: R$ 20.000/mês (R$ 240K/ano)
- **VP Engineering**: R$ 25.000/mês (R$ 300K/ano)

*Valores líquidos para PJ ou brutos para CLT*
*Benefícios: VR/VA, plano de saúde, home office*

## Board Composition
- **CEO**: Sarah Chen (Founder)
- **Investor 1**: Mark Williams (Sequoia Capital)
- **Investor 2**: Jennifer Park (Andreessen Horowitz)
- **Independent**: Michael Torres (Former CTO of GitHub)

## Panorama Competitivo
- **Principais Concorrentes**: LangChain Inc, AutoGPT Corp, CrewAI Systems
- **Nossa Diferenciação**: Melhor orquestração multi-agente, integração nativa com Claude
- **Tamanho do Mercado**: $8B em desenvolvimento de agentes de IA (crescendo 40% anualmente)

## Recent Decisions
- Approved hiring 3 senior backend engineers (March 2024)
- Launched freemium tier (February 2024)
- Opened European entity (January 2024)
- Closed Series A funding (January 2024)

## Upcoming Decisions
- Whether to acquire competitor SmartDev Inc ($8M asking price)
- Hiring plan for Q3 (engineering vs. sales focus)
- Office expansion vs. remote-first strategy
- Stock option refresh for early employees

## Risk Factors
- High dependency on AWS (70% of COGS)
- Key engineer retention (3 critical team members)
- Increasing competition from Big Tech
- Potential economic downturn impact on enterprise sales

## Scripts Disponíveis

### ai_expertise_evaluator.py
Avaliador de expertise técnica em desenvolvimento de agentes de IA.
Script localizado em `./scripts/ai_expertise_evaluator.py`

**Uso:**
```bash
python scripts/ai_expertise_evaluator.py --candidate-json '{"name":"João","llm_apis":["openai"]}'
```

### talent_scorer.py
Algoritmo de pontuação de candidatos.
Script localizado em `./scripts/talent_scorer.py`

**Uso:**
```bash
python scripts/talent_scorer.py --evaluate <candidate_data>
```

### simple_calculation.py
Calculadora rápida de métricas financeiras.
Script localizado em `./scripts/simple_calculation.py`

**Uso:**
```bash
python scripts/simple_calculation.py <total_runway> <monthly_burn>
```

Lembre-se: Como Chief of Staff, você tem acesso aos dados da empresa no diretório financial_data/ e pode delegar análises especializadas para seus subagentes (cto e recrutador).