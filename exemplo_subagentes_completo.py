"""
Exemplo Completo: Sistema Multi-Agente com Markdown
Demonstra como criar e usar subagentes apenas com arquivos .md
"""

import asyncio
from pathlib import Path
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions


# ============================================================
# PASSO 1: Criar estrutura de diretórios e arquivos
# ============================================================

def setup_agent_structure():
    """
    Cria a estrutura completa para um sistema multi-agente
    """
    base_dir = Path("my_company_agent")

    # Criar diretórios
    (base_dir / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
    (base_dir / ".claude" / "commands").mkdir(parents=True, exist_ok=True)
    (base_dir / ".claude" / "output-styles").mkdir(parents=True, exist_ok=True)
    (base_dir / "scripts").mkdir(parents=True, exist_ok=True)
    (base_dir / "data").mkdir(parents=True, exist_ok=True)

    # 1. CLAUDE.md - Contexto do agente principal
    claude_md = """# Company Context

## Overview
- Company: TechCorp
- Employees: 50
- Burn Rate: $500K/month
- Runway: 20 months
- ARR: $2.4M

## Team Structure
- Engineering: 25
- Sales: 12
- Product: 5
- Operations: 5
- Executive: 3

## Current Priorities
1. Hire 10 engineers
2. Launch new AI feature
3. Expand to Europe
4. Raise Series B ($30M)
"""
    (base_dir / "CLAUDE.md").write_text(claude_md)

    # 2. Subagente: Data Analyst
    data_analyst_md = """---
name: data-analyst
description: Data analysis expert for metrics, KPIs, dashboards, and data-driven insights. Use for any analytics, reporting, or data visualization needs.
tools: Read, Bash, Write
---

You are a senior data analyst specializing in SaaS metrics and business intelligence.

## Your Responsibilities

1. **Metrics Analysis**
   - Track and analyze KPIs (ARR, MRR, Churn, CAC, LTV)
   - Create performance dashboards
   - Identify trends and anomalies
   - Provide actionable insights

2. **Reporting**
   - Generate weekly/monthly reports
   - Create executive summaries
   - Visualize complex data
   - Track goal progress

3. **Predictive Analytics**
   - Forecast revenue growth
   - Predict churn risk
   - Model customer behavior
   - Scenario planning

## Available Tools

- Python scripts in `scripts/` for analysis:
  - `analyze_metrics.py` - KPI calculations
  - `generate_report.py` - Automated reporting
- Data files in `data/` directory
- Can write reports to `reports/` directory

## Output Format

Always provide:
1. Key finding (1 sentence)
2. Supporting data (3-5 metrics)
3. Visualization description
4. Recommended action
5. Confidence level (High/Medium/Low)

## Example Analysis

"Revenue growth is slowing. MRR growth dropped from 15% to 8% last month, primarily due to enterprise segment (-12%). Churn increased to 3.5%. Recommend immediate focus on enterprise retention. Confidence: High"
"""
    (base_dir / ".claude" / "agents" / "data-analyst.md").write_text(data_analyst_md)

    # 3. Subagente: DevOps Engineer
    devops_engineer_md = """---
name: devops-engineer
description: DevOps and infrastructure expert for deployment, monitoring, scaling, and reliability. Use for CI/CD, cloud infrastructure, or performance issues.
tools: Bash, Read, Write
---

You are a senior DevOps engineer responsible for infrastructure and reliability.

## Your Responsibilities

1. **Infrastructure Management**
   - AWS/Cloud resource optimization
   - Kubernetes cluster management
   - Database performance tuning
   - Cost optimization

2. **CI/CD Pipeline**
   - Build and deployment automation
   - Testing infrastructure
   - Release management
   - Rollback procedures

3. **Monitoring & Reliability**
   - System monitoring setup
   - Incident response
   - Performance optimization
   - SLA management

## Available Scripts

- `scripts/deploy.py` - Deployment automation
- `scripts/monitor.py` - System health checks
- `scripts/scale.py` - Auto-scaling logic

## Decision Framework

When analyzing infrastructure:
1. Current state assessment
2. Identify bottlenecks
3. Cost-benefit analysis
4. Risk assessment
5. Implementation plan

## Output Format

**For Incidents:**
"[SEVERITY] Issue with [COMPONENT]. Impact: [DESCRIPTION]. Root cause: [CAUSE]. Resolution: [FIX]. ETA: [TIME]"

**For Improvements:**
"Optimize [AREA] to achieve [BENEFIT]. Current: [METRIC]. Target: [GOAL]. Investment: [COST]. ROI: [VALUE]"
"""
    (base_dir / ".claude" / "agents" / "devops-engineer.md").write_text(devops_engineer_md)

    # 4. Subagente: Marketing Strategist
    marketing_strategist_md = """---
name: marketing-strategist
description: Marketing and growth expert for campaigns, content strategy, lead generation, and brand positioning. Use for marketing plans, growth hacking, or customer acquisition.
tools: WebSearch, Read, Write
---

You are a growth-focused marketing strategist for B2B SaaS.

## Your Responsibilities

1. **Growth Strategy**
   - Customer acquisition channels
   - Conversion optimization
   - Pricing strategy
   - Market positioning

2. **Content Marketing**
   - Content calendar planning
   - SEO strategy
   - Thought leadership
   - Case studies

3. **Campaign Management**
   - Campaign planning and execution
   - A/B testing strategies
   - Budget allocation
   - ROI tracking

4. **Market Research**
   - Competitive analysis
   - Customer segmentation
   - Market trends
   - Voice of customer

## Key Metrics

- CAC: $15,000
- LTV: $85,000
- LTV/CAC: 5.7x
- Conversion Rate: 2.5%
- MQL to SQL: 25%

## Output Guidelines

Always include:
1. Strategic recommendation
2. Expected impact (quantified)
3. Required resources
4. Timeline
5. Success metrics

## Campaign Framework

"Launch [CAMPAIGN] targeting [SEGMENT]. Expected: [X] leads, [Y]% conversion, $[Z] revenue. Budget: $[N]. Timeline: [WEEKS] weeks. KPIs: [METRICS]"
"""
    (base_dir / ".claude" / "agents" / "marketing-strategist.md").write_text(marketing_strategist_md)

    # 5. Script Python de exemplo
    analyze_script = """#!/usr/bin/env python3
import json
import sys

def analyze_metrics(metric_type="general"):
    metrics = {
        "general": {
            "arr": "$2.4M",
            "growth": "15% MoM",
            "churn": "2.5%",
            "nps": 72
        },
        "financial": {
            "burn_rate": "$500K/month",
            "runway": "20 months",
            "cash": "$10M"
        },
        "team": {
            "headcount": 50,
            "engineers": 25,
            "productivity": "high"
        }
    }

    return json.dumps(metrics.get(metric_type, metrics["general"]), indent=2)

if __name__ == "__main__":
    metric_type = sys.argv[1] if len(sys.argv) > 1 else "general"
    print(analyze_metrics(metric_type))
"""
    (base_dir / "scripts" / "analyze_metrics.py").write_text(analyze_script)
    (base_dir / "scripts" / "analyze_metrics.py").chmod(0o755)

    print(f"✅ Estrutura criada em {base_dir}/")
    return base_dir


# ============================================================
# PASSO 2: Classe do Sistema Multi-Agente
# ============================================================

class MultiAgentSystem:
    """
    Sistema multi-agente que orquestra subagentes via markdown
    """

    def __init__(self, base_dir: str = "my_company_agent"):
        self.base_dir = Path(base_dir)
        self.options = ClaudeCodeOptions(
            model="claude-3-5-sonnet-20241022",
            allowed_tools=["Task"],  # Permite delegação para subagentes
            cwd=str(self.base_dir),
            system_prompt="""
            You are the Chief of Staff orchestrating specialized agents.

            Delegate tasks based on expertise:
            - Data/metrics/KPIs → data-analyst
            - Infrastructure/DevOps → devops-engineer
            - Marketing/growth → marketing-strategist

            You can also handle general executive questions directly.
            Always explain which agent you're delegating to and why.
            """
        )

    async def process_query(self, query: str) -> str:
        """
        Processa uma query, delegando para subagentes quando apropriado
        """
        result = None
        delegation_info = []

        async with ClaudeSDKClient(options=self.options) as agent:
            await agent.query(query)

            async for msg in agent.receive_response():
                # Detectar delegações
                if hasattr(msg, 'content'):
                    for block in msg.content:
                        if hasattr(block, 'name') and block.name == 'Task':
                            delegation_info.append({
                                'subagent': block.input.get('subagent_type'),
                                'task': block.input.get('prompt')
                            })

                # Capturar resultado final
                if hasattr(msg, 'result'):
                    result = msg.result

        # Adicionar informação sobre delegação
        if delegation_info:
            delegation_summary = "\n\n📊 Delegação realizada:\n"
            for d in delegation_info:
                delegation_summary += f"  • {d['subagent']}: {d['task'][:50]}...\n"
            result = result + delegation_summary if result else delegation_summary

        return result


# ============================================================
# PASSO 3: Exemplos de Uso
# ============================================================

async def exemplo_uso_completo():
    """
    Demonstra o sistema multi-agente em ação
    """

    print("=" * 60)
    print("SISTEMA MULTI-AGENTE COM MARKDOWN")
    print("=" * 60)

    # Setup inicial (criar estrutura)
    print("\n1. Criando estrutura de agentes...")
    base_dir = setup_agent_structure()

    # Criar sistema
    system = MultiAgentSystem(base_dir)

    # Exemplo 1: Delegação para Data Analyst
    print("\n2. Testando delegação para Data Analyst...")
    result1 = await system.process_query(
        "What are our key metrics and are we on track for Series B?"
    )
    print(f"Resposta: {result1[:300]}...")

    # Exemplo 2: Delegação para DevOps
    print("\n3. Testando delegação para DevOps Engineer...")
    result2 = await system.process_query(
        "How can we reduce our AWS costs while maintaining performance?"
    )
    print(f"Resposta: {result2[:300]}...")

    # Exemplo 3: Delegação para Marketing
    print("\n4. Testando delegação para Marketing Strategist...")
    result3 = await system.process_query(
        "Design a campaign to increase enterprise sales by 30%"
    )
    print(f"Resposta: {result3[:300]}...")

    # Exemplo 4: Múltiplas delegações
    print("\n5. Testando múltiplas delegações...")
    result4 = await system.process_query(
        "I need a complete analysis: metrics performance, infrastructure costs, and marketing ROI"
    )
    print(f"Resposta: {result4[:400]}...")

    print("\n" + "=" * 60)
    print("✅ Sistema multi-agente funcionando!")
    print("=" * 60)


# ============================================================
# PASSO 4: Guia de Customização
# ============================================================

def print_customization_guide():
    """
    Imprime guia para customizar o sistema
    """
    guide = """

    🎨 COMO CUSTOMIZAR SEU SISTEMA MULTI-AGENTE
    ============================================

    1. ADICIONAR NOVO SUBAGENTE:
       • Crie arquivo .md em .claude/agents/
       • Defina: name, description, tools
       • Escreva system prompt especializado

    2. ESTRUTURA DO ARQUIVO .MD:
       ---
       name: seu-agente
       description: Quando delegar para este agente
       tools: Tool1, Tool2, Tool3
       ---

       System prompt aqui...

    3. TOOLS DISPONÍVEIS:
       • Read - Ler arquivos e imagens
       • Write - Criar/editar arquivos
       • Bash - Executar comandos e scripts
       • WebSearch - Pesquisar na web
       • Task - Delegar para outros agentes

    4. QUANDO O CLAUDE DELEGA:
       • Analisa descrição de cada subagente
       • Match semântico com a query
       • Delega automaticamente se há match
       • Retorna resultado consolidado

    5. MELHORES PRÁTICAS:
       • Descrições claras e específicas
       • Evitar sobreposição de responsabilidades
       • Incluir exemplos no system prompt
       • Definir formato de output
       • Listar recursos disponíveis (scripts, data)

    6. EXEMPLO DE NOVO SUBAGENTE:

       security-analyst.md:
       ---
       name: security-analyst
       description: Security audits, vulnerability assessments, compliance checks
       tools: Read, Bash, WebSearch
       ---

       You are a senior security analyst...
       Focus on: OWASP, SOC2, GDPR...

    """
    print(guide)


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

if __name__ == "__main__":
    # Executar exemplo
    asyncio.run(exemplo_uso_completo())

    # Mostrar guia de customização
    print_customization_guide()

    print("\n💡 Dica: Explore a pasta 'my_company_agent/' criada!")
    print("   Veja como os subagentes são simples arquivos .md")
    print("   Sem código Python complexo, sem configuração!")
    print("\n🚀 Agora você pode criar seus próprios subagentes!"