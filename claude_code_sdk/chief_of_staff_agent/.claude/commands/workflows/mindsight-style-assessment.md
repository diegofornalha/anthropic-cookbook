---
name: mindsight-style-assessment
description: Processo de avaliação estilo Mindsight adaptado para TechStart - Desenvolvedor IA Pleno
---

# 🎯 Avaliação Estilo Mindsight - Desenvolvedor IA Pleno

Processo profissional de avaliação adaptado do modelo Mindsight para nossa empresa.

## 📋 Informações do Processo

**Posição**: Desenvolvedor de IA Pleno | Serviços de IA
**Código da Vaga**: IA-{{vaga_id}}
**Candidato**: {{candidate_name}}
**Status**: {{status}}

## 🔒 Termos e Condições

### Aviso de Integridade
```
ATENÇÃO: Nosso sistema possui mecanismos de segurança que detectam:
- Uso de IA para responder testes (GPT, Claude, etc)
- Cópia de código de internet durante avaliação
- Múltiplas abas/janelas abertas
- Tentativas de burlar condições dos testes
- Comportamentos suspeitos de navegação

Caso detectado, os resultados serão INVALIDADOS.
```

### Compromisso Ético
Ao prosseguir, o candidato confirma que:
- [ ] Leu e compreendeu este aviso
- [ ] Realizará testes de forma ética e honesta
- [ ] Não utilizará recursos externos não permitidos
- [ ] Entende que violações resultam em desclassificação

## 📊 Painel de Testes

### Status dos Testes
| Teste | Tempo Estimado | Limite | Status | Ações |
|-------|----------------|--------|--------|-------|
| **1. Teste de Estilos de Trabalho** | 7 min | Sem limite | {{status_1}} | [Iniciar] |
| **2. Avaliação Técnica Python** | 45 min | 60 min | {{status_2}} | [Iniciar] |
| **3. Desafio de IA/Agentes** | 90 min | 120 min | {{status_3}} | [Iniciar] |
| **4. System Design IA** | 30 min | 45 min | {{status_4}} | [Iniciar] |
| **5. Fit Cultural** | 20 min | Sem limite | {{status_5}} | [Iniciar] |

### Legenda de Status
- 🔴 **Pendente**: Ainda não iniciado
- 🟡 **Iniciado**: Em andamento (retomar de onde parou)
- 🟢 **Finalizado**: Concluído com sucesso
- 🔄 **Pode Refazer**: Disponível após 120 dias
- ♿ **Acessibilidade**: Recursos especiais habilitados

## 🎯 Detalhamento dos Testes

### 1️⃣ Teste de Estilos de Trabalho (7 min)
**Objetivo**: Mapear perfil comportamental e fit cultural

**Avalia**:
- Trabalho em equipe vs autonomia
- Abordagem analítica vs criativa
- Orientação a processos vs resultados
- Comunicação e colaboração
- Adaptabilidade e resiliência

**Formato**: 30 perguntas situacionais
**Sem código**: Apenas questões comportamentais

### 2️⃣ Avaliação Técnica Python (45 min)
**Objetivo**: Validar competências Python para IA

**Desafios**:
```python
# Exemplo de questão:
"""
Implemente uma função que:
1. Processe stream de dados em tempo real
2. Use generators para eficiência de memória
3. Implemente cache LRU
4. Adicione type hints completos
5. Trate exceções apropriadamente
"""

def process_data_stream(
    stream: Iterator[Dict[str, Any]],
    cache_size: int = 100
) -> Generator[ProcessedData, None, None]:
    # Sua implementação aqui
    pass
```

**Avaliação Automática**:
- python-quality-synergy.py analisa em tempo real
- Score instantâneo de qualidade
- Feedback sobre melhorias

### 3️⃣ Desafio de IA/Agentes (90 min)
**Objetivo**: Construir mini-agente funcional

**Requisitos**:
```python
"""
Construa um agente que:
1. Use LangChain ou Claude CODE SDK
2. Implemente memória conversacional
3. Integre com ferramenta de busca
4. Processe documentos com RAG
5. Responda perguntas sobre o conteúdo
"""
```

**Recursos Permitidos**:
- Documentação oficial (LangChain, OpenAI, Claude)
- IDE de sua preferência
- Ambiente Python local

**NÃO Permitido**:
- Copiar código pronto da internet
- Usar ChatGPT/Claude para gerar código
- Consultar outros desenvolvedores

### 4️⃣ System Design IA (30 min)
**Objetivo**: Arquitetura de sistema com IA

**Case**: "Projete sistema de atendimento com múltiplos agentes"

**Entregar**:
- Diagrama de arquitetura
- Escolha de tecnologias
- Estimativa de custos (tokens, infra)
- Estratégia de scaling
- Plano de fallback

### 5️⃣ Fit Cultural (20 min)
**Objetivo**: Alinhamento com valores da empresa

**Perguntas Abertas**:
- Como você aprende novas tecnologias de IA?
- Descreva um projeto desafiador com LLMs
- Como lida com mudanças rápidas de requisitos?
- Sua visão sobre ética em IA

## 🔄 Sistema de Reaproveitamento

### Validade dos Resultados: 120 dias
```python
# Lógica de reaproveitamento
if candidate.last_test_date > (today - 120_days):
    if candidate.score >= 70:
        results = "REAPROVEITADO"
        skip_tests = True
    else:
        results = "REFAZER"
        reset_tests = True
```

### Critérios para Reaproveitamento:
- Score >= 70/100 em todos os testes
- Mesma senioridade (Pleno)
- Tecnologias similares (Python + IA)
- Sem flags de comportamento suspeito

## 🔐 Segurança e Monitoramento

### Sistema Anti-Fraude
```javascript
// Monitoramento em tempo real
const securityChecks = {
    tabSwitching: monitor_tab_focus(),
    copyPaste: detect_clipboard_usage(),
    aiDetection: analyze_typing_patterns(),
    codeOriginality: check_code_similarity(),
    browserTools: monitor_devtools()
};

if (any(securityChecks.triggered)) {
    flag_candidate();
    notify_recruiter();
    invalidate_results();
}
```

### Comportamentos Monitorados:
- ⚠️ Múltiplas mudanças de aba (> 5)
- ⚠️ Copy/paste de grandes blocos de código
- ⚠️ Padrões de digitação não-humanos
- ⚠️ Código idêntico a repositórios públicos
- ⚠️ Uso de ferramentas de automação

## ♿ Acessibilidade

### Recursos Disponíveis:
- 🔍 **Zoom**: Até 200% sem quebra de layout
- 🎨 **Alto Contraste**: Modo escuro/claro
- 🔊 **Leitor de Tela**: Compatível com NVDA/JAWS
- ⏱️ **Tempo Extra**: +50% para PcD
- 📝 **Fonte**: Ajustável (12-24px)

### Como Solicitar:
```python
# Antes de iniciar testes
accessibility_request = {
    "screen_reader": True,
    "high_contrast": True,
    "extra_time": True,
    "font_size": 18
}
```

## 📈 Scoring e Decisão

### Matriz de Avaliação:
```python
weights = {
    "work_styles": 0.15,      # Fit cultural
    "python_technical": 0.25,  # Competência Python
    "ai_challenge": 0.30,      # Habilidade com IA
    "system_design": 0.20,     # Arquitetura
    "cultural_fit": 0.10       # Alinhamento valores
}

final_score = sum(test_score * weight for test_score, weight in scores.items())

decision = {
    >= 85: "APROVADO_IMEDIATO",
    70-84: "APROVADO_ENTREVISTA",
    60-69: "SEGUNDA_CHANCE",
    < 60: "REPROVADO"
}
```

## 🚀 Comandos de Execução

### Iniciar Avaliação Completa:
```bash
/mindsight-style-assessment "Diego Alcantara" --position "IA Pleno"
```

### Reaproveitar Resultados:
```bash
/mindsight-style-assessment --reuse-results "Diego Alcantara"
```

### Modo Acessibilidade:
```bash
/mindsight-style-assessment "Diego Alcantara" --accessibility "screen-reader,extra-time"
```

### Verificar Status:
```bash
/mindsight-style-assessment --check-status "Diego Alcantara"
```

## 📊 Dashboard de Acompanhamento

### Para Recrutador:
```python
# Ver todos candidatos em avaliação
mcp__neo4j-memory__search_memories(
    query='assessment status:in_progress position:ia_pleno'
)

# Candidatos com flags de segurança
mcp__neo4j-memory__search_memories(
    query='security_flag:true assessment:mindsight'
)
```

### Para Candidato:
- Link único de acesso: `techstart.ai/assessment/{{unique_id}}`
- Painel com progresso em tempo real
- Feedback instantâneo após cada teste
- Certificado de conclusão (se aprovado)

## 📧 Comunicação Automática

### Templates de Email:
1. **Convite**: Instruções e link de acesso
2. **Lembrete**: 24h antes do prazo expirar
3. **Resultado**: Feedback detalhado e próximos passos
4. **Reaproveitamento**: Notificação de resultados válidos

## ⚙️ Integração com Sistema Atual

### Hooks Automáticos:
```python
# Quando candidato submete código
.claude/hooks/python-orchestrator.py -> Avalia automaticamente

# Salva no Neo4j
mcp__neo4j-memory__create_memory({
    "type": "assessment_result",
    "candidate": candidate_name,
    "scores": test_scores,
    "flags": security_flags
})
```

---

**NOTA**: Este workflow adapta as melhores práticas da Mindsight com nossa tecnologia de agentes e automação, mantendo a integridade e profissionalismo do processo.