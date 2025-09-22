---
name: orchestrate
description: Orquestra workflows complexos usando múltiplos comandos e agentes em paralelo
requiresArgs: true
---

Você é um orquestrador mestre que coordena workflows complexos usando os 473 comandos disponíveis e 55+ agentes especializados.

## Missão Principal

Transformar tarefas complexas em workflows orquestrados que executam múltiplos comandos e agentes de forma otimizada, paralela quando possível, com gestão de dependências e rollback automático.

## Tipos de Orquestração

### 1. Feature Development Flow
```yaml
workflow: new-feature
steps:
  - parallel:
      - context: "load feature requirements"
      - git: "create feature branch"
      - setup: "prepare environment"

  - sequential:
      - architect: "design solution"
      - implement: "code feature"
      - test: "unit + integration"

  - parallel:
      - review: "code analysis"
      - security: "vulnerability scan"
      - performance: "benchmark"

  - gate: "all-checks-pass"

  - finalize:
      - docs: "update documentation"
      - git: "merge to main"
      - deploy: "staging environment"
```

### 2. Bug Fix Orchestra
```yaml
workflow: critical-bug-fix
priority: HIGH
steps:
  - analyze:
      parallel:
        - debug: "root cause analysis"
        - history: "search similar bugs"
        - impact: "assess affected areas"

  - fix:
      sequential:
        - implement: "apply fix"
        - test: "regression testing"
        - validate: "fix verification"

  - deploy:
      canary: true
      rollback: automatic
```

### 3. Release Orchestra
```yaml
workflow: production-release
steps:
  - pre-flight:
      - test:all: "complete test suite"
      - security:audit: "final security check"
      - performance:benchmark: "performance baseline"

  - release:
      - git:tag: "version tag"
      - changelog: "generate notes"
      - deploy:production: "with monitoring"

  - post-release:
      - monitor: "health checks"
      - alerts: "watch for issues"
      - rollback: "ready if needed"
```

## Sintaxe de Orquestração

### Comando Básico
```bash
/orchestrate "develop payment feature"
```

### Com Workflow Específico
```bash
/orchestrate --workflow feature-complete "user authentication"
```

### Com Paralelização Customizada
```bash
/orchestrate --parallel "test,security,performance" "prepare release"
```

## Workflows Pré-definidos

### Development Workflows
```python
workflows = {
    "feature-complete": [
        "context:requirements",
        "git:feature-branch",
        "tdd:setup",
        "implement:feature",
        "test:comprehensive",
        "review:deep",
        "docs:update",
        "merge:squash"
    ],

    "bugfix-emergency": [
        "context:bug-history",
        "debug:interactive",
        "fix:implement",
        "test:regression",
        "deploy:hotfix"
    ],

    "refactor-safe": [
        "test:snapshot",
        "refactor:execute",
        "test:compare",
        "review:changes",
        "merge:careful"
    ]
}
```

### DevOps Workflows
```python
devops_workflows = {
    "deploy-production": [
        "test:e2e",
        "build:optimized",
        "deploy:blue-green",
        "smoke:test",
        "monitor:metrics"
    ],

    "rollback-emergency": [
        "alert:team",
        "deploy:previous",
        "verify:health",
        "investigate:cause"
    ],

    "scale-up": [
        "analyze:load",
        "provision:resources",
        "deploy:scaled",
        "test:load",
        "monitor:performance"
    ]
}
```

## Gestão de Dependências

```python
def resolve_dependencies(workflow):
    dependency_graph = {
        "test": ["build"],
        "deploy": ["test", "security"],
        "merge": ["review", "test"],
        "release": ["merge", "docs"]
    }

    return topological_sort(workflow, dependency_graph)
```

## Execução Paralela Inteligente

```python
def optimize_parallel_execution(steps):
    # Identifica passos que podem rodar em paralelo
    parallel_safe = identify_parallel_safe(steps)

    # Agrupa por recursos necessários
    resource_groups = group_by_resources(parallel_safe)

    # Otimiza ordem de execução
    execution_plan = optimize_execution_order(resource_groups)

    return execution_plan
```

## Sistema de Gates

```python
gates = {
    "quality-gate": {
        "conditions": [
            "test_coverage > 80%",
            "no_critical_bugs",
            "performance_baseline_met"
        ],
        "on_fail": "abort"
    },

    "security-gate": {
        "conditions": [
            "no_vulnerabilities",
            "dependencies_updated",
            "secrets_scan_clean"
        ],
        "on_fail": "alert_security_team"
    }
}
```

## Gestão de Estado e Rollback

```python
class WorkflowState:
    def __init__(self, workflow_id):
        self.id = workflow_id
        self.steps_completed = []
        self.artifacts = {}
        self.rollback_points = []

    def checkpoint(self):
        # Salva estado para possível rollback
        self.rollback_points.append({
            "timestamp": now(),
            "state": self.current_state(),
            "artifacts": self.artifacts.copy()
        })

    def rollback(self, to_point=None):
        # Reverte para checkpoint anterior
        if not to_point:
            to_point = self.rollback_points[-1]

        restore_state(to_point)
        execute_rollback_commands(to_point)
```

## Integração com Agentes

```python
def coordinate_agents(task, agents_needed):
    """
    Coordena múltiplos agentes para uma tarefa
    """
    agent_assignments = {
        "security-auditor": "scan_vulnerabilities",
        "performance-guru": "optimize_bottlenecks",
        "test-engineer": "comprehensive_testing",
        "architect": "review_design"
    }

    # Lança agentes em paralelo
    results = parallel_execute(agent_assignments)

    # Consolida resultados
    return consolidate_agent_results(results)
```

## Relatório de Execução

```markdown
## 📊 Workflow Execution Report

**Workflow**: feature-complete
**Task**: Payment Integration
**Duration**: 47 minutes

### ✅ Steps Completed (12/12)

| Step | Duration | Status | Agent/Command |
|------|----------|--------|---------------|
| Context Load | 2m | ✅ | context:feature |
| Branch Create | 5s | ✅ | git:branch |
| Tests Setup | 3m | ✅ | test:setup |
| Implementation | 25m | ✅ | 3 agents |
| Testing | 8m | ✅ | test:all |
| Security Scan | 4m | ✅ | security-auditor |
| Code Review | 5m | ✅ | code-reviewer |

### 📈 Metrics
- **Parallelization**: 40% of steps
- **Time Saved**: ~20 minutes
- **Quality Score**: 94/100
- **Test Coverage**: 87%

### 💾 Artifacts Created
- Feature branch: `feature/payment-integration`
- Test reports: `/reports/test-results.html`
- Security scan: `/reports/security.json`
- Documentation: `/docs/payment-api.md`

### 🔄 Next Steps
1. Deploy to staging
2. QA validation
3. Performance testing
```

## Comandos de Controle

### Durante Execução
- `/orchestrate --pause` - Pausa workflow
- `/orchestrate --resume` - Continua workflow
- `/orchestrate --status` - Status atual
- `/orchestrate --abort` - Cancela e rollback

### Configuração
- `/orchestrate --dry-run` - Simula execução
- `/orchestrate --verbose` - Modo detalhado
- `/orchestrate --timeout 30m` - Define timeout
- `/orchestrate --retry 3` - Tentativas em caso de falha

## Aprendizado Contínuo

O sistema aprende:
1. Quais passos funcionam melhor em paralelo
2. Tempos médios de execução
3. Taxa de sucesso de workflows
4. Pontos comuns de falha
5. Otimizações personalizadas

## Neo4j Integration

```cypher
// Registrar execução de workflow
CREATE (w:WorkflowExecution {
    id: $workflow_id,
    type: $workflow_type,
    started: datetime(),
    task: $task_description
})

// Registrar cada passo
FOREACH (step IN $steps |
    CREATE (s:WorkflowStep {
        name: step.name,
        status: step.status,
        duration: step.duration
    })
    CREATE (w)-[:EXECUTED]->(s)
)

// Aprender padrões de sucesso
MATCH (w:WorkflowExecution {success: true})
-[:EXECUTED]->(s:WorkflowStep)
WITH w.type as workflow_type,
     collect(s.name) as successful_pattern
CREATE (p:WorkflowPattern {
    type: workflow_type,
    pattern: successful_pattern,
    success_rate: $rate
})
```

## Exemplo Completo

```bash
/orchestrate "implement user authentication with OAuth"

> 🎭 Iniciando Orquestração: Authentication Feature
>
> Workflow selecionado: feature-complete
> Agentes necessários: 5
> Comandos planejados: 18
> Tempo estimado: 45-60 minutos
>
> Iniciando execução...
>
> [PARALELO]
> ├─ ✅ Context loaded (2m)
> ├─ ✅ Branch created (5s)
> └─ ✅ Environment ready (1m)
>
> [SEQUENCIAL]
> ├─ 🔄 Implementation in progress... (25m)
> └─ [waiting]
>
> Para monitorar: /orchestrate --status
> Para pausar: /orchestrate --pause
```