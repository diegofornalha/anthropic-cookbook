---
name: ai-transition-hiring
description: Workflow especializado para desenvolvedores em transição para IA/ML vindos de outras áreas
---

# 🔄 Workflow de Transição para IA - Desenvolvedores com Alto Potencial

Processo otimizado para identificar e contratar desenvolvedores talentosos de outras áreas (blockchain, backend, mobile) que demonstram potencial para transição para IA.

## 🎯 Filosofia do Processo

**Princípio Central**: Avaliar POTENCIAL + VELOCIDADE DE APRENDIZADO ao invés de experiência atual em IA.

**Candidatos-alvo**:
- Desenvolvedores sênior em outras áreas
- Forte base em Python/JavaScript/TypeScript
- Histórico de aprendizado de tecnologias complexas
- Mentalidade de crescimento e curiosidade técnica

## 📊 Matriz de Avaliação Adaptada

### Pesos Rebalanceados:
```python
transition_weights = {
    'programming_foundation': 0.25,    # Python, arquitetura, clean code
    'learning_velocity': 0.20,         # Velocidade para aprender novo
    'complexity_handling': 0.15,       # Experiência com sistemas complexos
    'open_source_contrib': 0.15,       # Indicador de autodidatismo
    'domain_expertise': 0.10,          # Expertise atual (blockchain, etc)
    'culture_fit': 0.10,               # Fit com startup
    'ai_potential': 0.05               # Conhecimento básico IA
}
```

## 🚀 Workflow Completo

### Step 0: Pre-Screening Inteligente (2h)
**Identificar Potencial ao invés de Rejeitar:**

```python
# transition_evaluator.py
def evaluate_transition_candidate(profile):
    signals = {
        'python_proficiency': check_python_repos(),
        'learning_curve': analyze_tech_evolution(),     # Como evoluiu
        'complexity_projects': count_complex_systems(),  # Projetos difíceis
        'contribution_volume': count_github_repos(),     # 466 repos = alto
        'innovation_mindset': check_first_mover(),      # Pioneiro em algo
    }

    # Threshold mais baixo para IA, mais alto para fundamentos
    if signals['python_proficiency'] > 70 and
       signals['learning_curve'] > 60:
        return "PROCEED_WITH_TRANSITION_TRACK"
```

### Step 1: Avaliação de Fundamentos (Recrutador + CTO - 3h)

#### Parte A: Fundamentos de Programação
- **Code Review**: Análise de código Python existente
- **Arquitetura**: Design de sistema escalável (genérico)
- **Problem Solving**: Algoritmos e estrutura de dados
- **Best Practices**: Clean code, testing, documentação

#### Parte B: Potencial para IA
- **Curiosidade**: "O que você sabe sobre LLMs?"
- **Visão**: "Como aplicaria IA no seu domínio atual?"
- **Aprendizado**: "Última tecnologia complexa que aprendeu?"
- **Recursos**: "Como aprenderia sobre agentes IA?"

### Step 2: Mini-Projeto de Aprendizado (48h em casa)

**Desafio Prático com Tutorial:**
```python
"""
Mini-Projeto: Construa seu primeiro agente IA

Fornecemos:
1. Tutorial passo-a-passo de LangChain
2. Acesso temporário a Claude/OpenAI API
3. Dataset de exemplo
4. Boilerplate inicial

Você deve:
1. Completar o tutorial (2h)
2. Implementar agente simples que:
   - Responde perguntas sobre documentos
   - Usa ferramentas básicas (calculator, search)
   - Mantém histórico de conversação
3. Adicionar uma feature criativa sua

Avaliamos:
- Capacidade de seguir documentação
- Velocidade de aprendizado
- Qualidade do código Python
- Criatividade na feature adicional
"""
```

### Step 3: Technical Discussion (CTO - 1.5h)

**Foco na Jornada, não no Destino:**

1. **Walk-through do projeto**: Explicar decisões e aprendizados
2. **Debugging ao vivo**: Adicionar feature simples juntos
3. **Conceitos IA**: Verificar absorção dos conceitos básicos
4. **Plano de desenvolvimento**: Como continuaria aprendendo?

### Step 4: Fit Cultural + Compromisso (Chief of Staff - 45min)

**Validar Compromisso com Transição:**

1. **Expectativas realistas**: "6 meses para proficiência - ok?"
2. **Investimento pessoal**: "Disposto a estudar fora do horário?"
3. **Mudança de identidade**: "De especialista para júnior - como lida?"
4. **Visão de carreira**: "Onde se vê em 2 anos?"

### Step 5: Oferta Estruturada com Desenvolvimento

**Pacote Transition-to-AI:**

```python
def generate_transition_offer(scores):
    base_offer = {
        'position': 'AI Engineer Trainee',
        'level': 'L3' if scores['total'] > 70 else 'L2',
        'salary_initial': calculate_transition_salary(scores),
        'salary_after_6m': '+20% se atingir metas',
        'equity': '0.1-0.2%',
        'benefits': {
            'bootcamp': '3 meses com mentor dedicado',
            'courses': 'Budget R$ 5.000 para cursos',
            'conferences': '2 conferências IA/ano',
            'gpu_credits': 'R$ 500/mês para experiments'
        }
    }
    return base_offer

# Faixas salariais para transição:
L2_RANGE = "R$ 12.000 - 14.000/mês"
L3_RANGE = "R$ 14.000 - 16.500/mês"
L4_RANGE = "R$ 17.500/mês" # Após certificação 6 meses
```

## 📚 Programa de Desenvolvimento Incluído

### Mês 1-3: Fundamentos IA
- **Semana 1-2**: Curso FastAI + Certificação
- **Semana 3-4**: LangChain + Claude SDK
- **Semana 5-8**: Projeto interno supervisionado
- **Semana 9-12**: Contribuição em produção com pair programming

### Mês 4-6: Especialização
- Escolher trilha: Agentes / RAG / Fine-tuning
- Projeto próprio com impacto real
- Apresentação para o time

### Checkpoint 6 meses:
- Avaliação completa
- Promoção para AI Engineer (L4) se aprovado
- Ajuste salarial automático

## 🎯 Métricas de Sucesso do Programa

### Para o Candidato:
- **3 meses**: Primeiro PR em produção com IA
- **6 meses**: Liderando feature de IA
- **12 meses**: Referência em algum aspecto de IA

### Para a Empresa:
- **ROI**: Break-even em 8 meses (vs 12 meses hiring sênior)
- **Retenção**: 90% após 1 ano (loyalty por investimento)
- **Inovação**: Perspectivas únicas de outros domínios

## 🔧 Scripts Específicos para Transição

```bash
.claude/hooks/scripts/
├── transition_evaluator.py      # Avalia potencial de transição
├── learning_velocity_scorer.py  # Mede velocidade de aprendizado
├── bootcamp_tracker.py         # Acompanha progresso no bootcamp
└── milestone_validator.py      # Valida checkpoints de aprendizado
```

## 💡 Casos de Uso Específicos

### Exemplo 1: Diego Fornalha (Blockchain → IA)
```python
profile = {
    'current': 'Blockchain Expert, Flow Ambassador',
    'strengths': 'Python, 466 repos, pioneiro',
    'gaps': 'Zero LLMs, frameworks IA',
    'potential': 'Alto - histórico de inovação'
}

# Resultado esperado:
offer = {
    'position': 'AI Engineer Trainee L3',
    'salary': 'R$ 15.000/mês',
    'path': 'Fast-track com foco em Web3+AI',
    'mentor': 'CTO direto',
    'timeline': '4 meses para L4'
}
```

### Exemplo 2: Mobile Developer → IA
```python
profile = {
    'current': 'iOS Senior Developer',
    'strengths': 'Swift, arquitectura, UX',
    'gaps': 'Python básico, zero ML',
    'potential': 'Médio - precisa fundamentos'
}

# Resultado:
offer = {
    'position': 'AI Engineer Trainee L2',
    'salary': 'R$ 12.000/mês',
    'path': 'Bootcamp completo 3 meses',
    'mentor': 'Senior AI Engineer',
    'timeline': '6-8 meses para L3'
}
```

## 🚀 Comandos de Execução

```bash
# Avaliar candidato em transição
/ai-transition-hiring "Diego Fornalha" --from "blockchain" --to "ai"

# Gerar plano de desenvolvimento personalizado
/generate-transition-plan "Diego Fornalha" --fast-track

# Acompanhar progresso
/track-transition-progress "Diego Fornalha" --week 4
```

## 📈 Neo4j Learning Tracking

```cypher
// Criar nó de transição
CREATE (t:Transition {
  candidate: 'Diego Fornalha',
  from_domain: 'Blockchain',
  to_domain: 'AI',
  start_date: date(),
  initial_score: 45,
  potential_score: 85,
  status: 'IN_BOOTCAMP'
})

// Registrar progresso
MATCH (t:Transition {candidate: 'Diego Fornalha'})
CREATE (p:Progress {
  week: 4,
  milestone: 'First LangChain Agent',
  score: 65,
  velocity: 'ABOVE_EXPECTED'
})-[:BELONGS_TO]->(t)

// Aprender com sucessos
MATCH (t:Transition)-[:RESULTED_IN]->(s:Success)
WHERE s.reached_l4 < duration('P6M')
RETURN t.from_domain, avg(t.potential_score) as avg_potential
ORDER BY avg_potential DESC
```

## ✅ Vantagens do Processo

1. **Acesso a talentos ocultos**: Desenvolvedores excelentes sem experiência IA
2. **Custo reduzido**: 30-40% menos que sênior IA
3. **Loyalty maior**: Gratidão pelo investimento em desenvolvimento
4. **Diversidade de perspectivas**: Inovação vinda de outros domínios
5. **Pipeline sustentável**: Menos dependência de mercado aquecido IA

---

**NOTA**: Este workflow reconhece que grandes desenvolvedores podem se tornar grandes AI Engineers com o investimento correto. Foco em POTENCIAL + PROGRAMA ESTRUTURADO = SUCESSO.