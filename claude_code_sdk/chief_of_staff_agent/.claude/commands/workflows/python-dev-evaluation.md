---
name: python-dev-evaluation
description: Avaliação completa de desenvolvedor Python usando múltiplos agentes especializados
---

# 🐍 Workflow de Avaliação - Desenvolvedor Python

Workflow completo para avaliar candidato Python usando nossa suite de agentes especializados.

## 📊 Visão Geral do Processo

**Posição**: Desenvolvedor Python Sênior
**Agentes Envolvidos**:
- python-pro (avaliação técnica Python)
- code-judge (orquestrador de análise)
- code-judge-quality (qualidade de código)
- code-judge-performance (otimização)
- code-judge-security (segurança)
- code-judge-patterns (design patterns)
- semantic-reasoner (análise profunda)

## 🔄 Etapas de Avaliação

### Step 1: Teste Prático Python (python-pro)
**Duração**: 2 horas
**Desafio**: Implementar sistema de cache distribuído em Python

```python
# Requisitos do desafio:
1. Criar classe CacheDistribuido com:
   - Suporte a TTL (time to live)
   - LRU eviction policy
   - Thread-safe operations
   - Async/await support
   - Type hints completos

2. Implementar decorators:
   - @cached com parametrização
   - @retry com backoff exponencial

3. Testes com pytest:
   - Cobertura > 90%
   - Fixtures e mocks
   - Testes de concorrência
```

**Avaliação pelo python-pro**:
- Código idiomático Python
- Uso de funcionalidades avançadas
- Performance e otimizações
- Qualidade dos testes

### Step 2: Análise de Código Existente (code-judge + sub-agentes)
**Duração**: 1 hora
**Tarefa**: Candidato recebe código legacy para analisar

O **code-judge** orquestra análise completa:
1. **code-judge-requirements**: Verifica se código atende especificações
2. **code-judge-quality**: Avalia clean code e manutenibilidade
3. **code-judge-security**: Identifica vulnerabilidades
4. **code-judge-performance**: Sugere otimizações
5. **code-judge-patterns**: Avalia uso de design patterns

**Candidato deve**:
- Identificar problemas
- Sugerir refatorações
- Propor melhorias de arquitetura

### Step 3: Desafio de Otimização (code-judge-performance)
**Duração**: 45 minutos
**Cenário**: Código Python com problemas de performance

```python
# Código lento fornecido:
def process_large_dataset(data):
    results = []
    for item in data:
        if item % 2 == 0:
            results.append(item ** 2)
    return results

# Candidato deve otimizar para:
# - Usar generators
# - Implementar multiprocessing
# - Adicionar caching
# - Usar NumPy quando apropriado
```

### Step 4: Security Review (code-judge-security)
**Duração**: 30 minutos
**Tarefa**: Identificar vulnerabilidades em código web

```python
# Código com vulnerabilidades:
@app.route('/user/<id>')
def get_user(id):
    query = f"SELECT * FROM users WHERE id = {id}"
    return db.execute(query)
```

**Candidato deve identificar**:
- SQL Injection
- XSS vulnerabilities
- Insecure dependencies
- Secrets hardcoded

### Step 5: Design Patterns Challenge (code-judge-patterns)
**Duração**: 1 hora
**Tarefa**: Refatorar código usando patterns apropriados

```python
# Código para refatorar:
class PaymentProcessor:
    def process(self, type, amount):
        if type == "credit":
            # 100 linhas de código
        elif type == "debit":
            # 100 linhas de código
        elif type == "pix":
            # 100 linhas de código
```

**Candidato deve aplicar**:
- Strategy Pattern
- Factory Pattern
- Dependency Injection
- SOLID principles

### Step 6: Análise Semântica Profunda (semantic-reasoner)
**Duração**: 30 minutos
**Discussão técnica sobre**:
- Trade-offs arquiteturais
- Decisões de design
- Escalabilidade
- Manutenibilidade

## 🎯 Critérios de Avaliação por Agente

### python-pro (40% do peso)
- [ ] Código idiomático (PEP 8, zen of Python)
- [ ] Funcionalidades avançadas (decorators, generators, async)
- [ ] Type hints completos e corretos
- [ ] Testes abrangentes com pytest
- [ ] Performance otimizada

### code-judge-quality (20% do peso)
- [ ] Clean code principles
- [ ] Complexidade ciclomática baixa
- [ ] DRY (Don't Repeat Yourself)
- [ ] Nomenclatura clara
- [ ] Documentação adequada

### code-judge-security (15% do peso)
- [ ] Sem vulnerabilidades críticas
- [ ] Validação de input
- [ ] Sanitização de dados
- [ ] Gestão segura de secrets
- [ ] Dependências atualizadas

### code-judge-performance (15% do peso)
- [ ] Complexidade algorítmica apropriada
- [ ] Uso eficiente de memória
- [ ] Paralelização quando necessário
- [ ] Caching estratégico
- [ ] Profiling e benchmarks

### code-judge-patterns (10% do peso)
- [ ] Design patterns apropriados
- [ ] SOLID principles
- [ ] Arquitetura escalável
- [ ] Separação de concerns
- [ ] Testabilidade

## 📈 Scoring Sistema

```python
def calculate_final_score(scores):
    weights = {
        'python_pro': 0.40,
        'code_quality': 0.20,
        'security': 0.15,
        'performance': 0.15,
        'patterns': 0.10
    }

    final_score = sum(
        scores[area] * weight
        for area, weight in weights.items()
    )

    level = {
        90: "Expert Python Developer",
        75: "Senior Python Developer",
        60: "Mid-level Python Developer",
        40: "Junior Python Developer",
        0: "Needs Improvement"
    }

    for threshold, title in sorted(level.items(), reverse=True):
        if final_score >= threshold:
            return final_score, title
```

## 🚀 Execução do Workflow

### Comando para iniciar avaliação completa:

```bash
# 1. Iniciar com python-pro
Task com python-pro: "Avaliar implementação de cache distribuído do candidato X"

# 2. Orquestrar análise completa
Task com code-judge: "Coordenar análise completa do código submetido"

# 3. Deep dive em áreas específicas
Task com code-judge-performance: "Analisar otimizações propostas"
Task com code-judge-security: "Verificar vulnerabilidades identificadas"
Task com code-judge-patterns: "Avaliar uso de design patterns"

# 4. Análise semântica final
Task com semantic-reasoner: "Consolidar insights e trade-offs das decisões"
```

## 📊 Template de Relatório Final

```markdown
# Avaliação Python Developer - [Nome Candidato]

## Resumo Executivo
- **Score Final**: XX/100
- **Classificação**: [Senior/Mid/Junior]
- **Recomendação**: [Aprovar/Reprovar/Condicional]

## Scores por Área
| Agente | Área | Score | Peso |
|--------|------|-------|------|
| python-pro | Expertise Python | XX/100 | 40% |
| code-judge-quality | Qualidade | XX/100 | 20% |
| code-judge-security | Segurança | XX/100 | 15% |
| code-judge-performance | Performance | XX/100 | 15% |
| code-judge-patterns | Patterns | XX/100 | 10% |

## Pontos Fortes
- [Lista de strengths identificados]

## Áreas de Melhoria
- [Lista de weaknesses]

## Recomendações
- [Próximos passos]
```

## 🎯 Red Flags Automáticos

⚠️ **Reprovar imediatamente se**:
- Não usa type hints em Python 3.7+
- Zero testes escritos
- SQL injection em código web
- Copia código sem entender
- Não consegue explicar Big O notation

## ✅ Green Flags Positivos

✨ **Sinais de excelência**:
- Usa dataclasses e pydantic
- Implementa async/await corretamente
- Escreve testes com fixtures complexas
- Conhece memory profiling
- Contribui para projetos open source

## 🔄 Integração com Neo4j

Cada avaliação cria memórias no grafo:
- Padrões de código identificados
- Soluções criativas
- Áreas de expertise
- Gaps de conhecimento

Isso permite melhorar futuras avaliações baseadas em aprendizados.

---

**Nota**: Este workflow usa 7+ agentes especializados para uma avaliação 360° de desenvolvedores Python.