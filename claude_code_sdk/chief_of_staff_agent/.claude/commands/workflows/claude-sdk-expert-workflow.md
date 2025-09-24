---
type: workflow
name: claude-sdk-expert-workflow
description: Workflow completo para transformar qualquer desenvolvedor em expert Claude Code SDK em 12 semanas
---

# Workflow: Expert em Claude Code SDK

Processo estruturado para domínio completo do Claude Code SDK, com avaliações práticas e tracking via Neo4j.

## Uso

```bash
/claude-sdk-expert-workflow "Diego Fornalha" --score-inicial 45
/claude-sdk-expert-workflow --avaliar "Diego Fornalha" --semana 4
/claude-sdk-expert-workflow --certificar "Diego Fornalha"
```

## Fases do Workflow

### FASE 1: Onboarding (Semana 1)
```python
fase_1 = {
    "objetivo": "Setup completo e fundamentos",
    "score_meta": "45→55",
    "ações": [
        "1. Clone repositório: github.com/diegofornalha/claude-code-sdk-python",
        "2. Checkout branch: feature/portuguese-translations",
        "3. Execute: python examples/01_hello_claude.py",
        "4. Complete: exercicios_praticos_pt_br.py 1",
        "5. Complete: exercicios_praticos_pt_br.py 2"
    ],
    "validação": {
        "teste": "sdk_practical_tests.py test_1 test_2",
        "neo4j": "CREATE (p:Progress {week:1, score:55})"
    },
    "entregável": "CLI simples usando query()"
}
```

### FASE 2: Ferramentas Básicas (Semana 2)
```python
fase_2 = {
    "objetivo": "Dominar ferramentas do SDK",
    "score_meta": "55→60",
    "ações": [
        "1. Complete: exercicios_praticos_pt_br.py 3",
        "2. Criar pipeline Read→Process→Write",
        "3. Experimentar com todas ferramentas permitidas",
        "4. Debugar erros comuns"
    ],
    "ferramentas": ["Read", "Write", "Edit", "Bash", "Grep"],
    "validação": {
        "teste": "sdk_practical_tests.py test_3",
        "projeto": "Automatizador de tarefas com SDK"
    }
}
```

### FASE 3: MCP Tools 🔴 CRÍTICA (Semanas 3-5)
```python
fase_3_mcp = {
    "objetivo": "DOMINAR MCP Tools completamente",
    "score_meta": "60→75",
    "duração": "3 SEMANAS INTENSIVAS",
    "semana_3": {
        "foco": "Entender @tool decorator",
        "exercícios": [
            "exercicios_praticos_pt_br.py 4",
            "Criar 3 ferramentas simples",
            "Debugar retorno content"
        ],
        "código": """
@tool(name='calc', description='Calculadora')
async def calc(args):
    return {'content': [{'type': 'text', 'text': result}]}
        """
    },
    "semana_4": {
        "foco": "create_sdk_mcp_server()",
        "exercícios": [
            "Criar servidor com 5 ferramentas",
            "Integrar com ClaudeCodeOptions",
            "Testar todas ferramentas"
        ]
    },
    "semana_5": {
        "foco": "Sistema MCP completo",
        "projeto": "Suite de 10 ferramentas customizadas",
        "validação": "sdk_practical_tests.py test_4"
    },
    "erro_comum": "Esquecer 'content' no retorno",
    "neo4j": "CREATE (g:GapResolved {type:'MCP_Tools', weeks:3})"
}
```

### FASE 4: Hooks System 🔴 CRÍTICA (Semanas 6-8)
```python
fase_4_hooks = {
    "objetivo": "DOMINAR Hooks completamente",
    "score_meta": "75→85",
    "duração": "3 SEMANAS INTENSIVAS",
    "semana_6": {
        "foco": "PreToolUse hooks",
        "exercícios": [
            "exercicios_praticos_pt_br.py 5",
            "Criar 5 hooks de validação",
            "Bloquear comandos perigosos"
        ],
        "código": """
HookMatcher(
    matcher='PreToolUse',
    hooks=[validar_seguranca]
)
        """
    },
    "semana_7": {
        "foco": "PostToolUse hooks",
        "exercícios": [
            "Hooks de logging",
            "Modificação de resultados",
            "Chain de hooks"
        ]
    },
    "semana_8": {
        "foco": "Sistema completo",
        "projeto": "Pipeline com validação e auditoria completa",
        "validação": "sdk_practical_tests.py test_5"
    },
    "erro_comum": "Não retornar None para permitir",
    "neo4j": "CREATE (g:GapResolved {type:'Hooks', weeks:3})"
}
```

### FASE 5: Avançado (Semanas 9-11)
```python
fase_5_avancado = {
    "objetivo": "Features avançadas",
    "score_meta": "85→92",
    "semana_9": {
        "foco": "ClaudeSDKClient e streaming",
        "exercícios": [
            "exercicios_praticos_pt_br.py 6",
            "Chat interativo",
            "Interrupt handling"
        ]
    },
    "semana_10": {
        "foco": "Multi-agente",
        "exercícios": [
            "exercicios_praticos_pt_br.py 7",
            "Orquestração com Task",
            "Delegação complexa"
        ]
    },
    "semana_11": {
        "projeto_final": "Sistema completo com todos recursos",
        "requisitos": [
            "MCP Tools customizadas",
            "Hooks de segurança",
            "Streaming",
            "Multi-agente"
        ]
    }
}
```

### FASE 6: Expert (Semana 12)
```python
fase_6_expert = {
    "objetivo": "Certificação como Expert",
    "score_meta": "92→95+",
    "requisitos": [
        "Contribuir PR para repositório",
        "Documentar novo padrão",
        "Criar extensão para SDK",
        "Mentorar outro desenvolvedor"
    ],
    "certificação": {
        "teste_final": "Todos os 6 testes práticos",
        "projeto": "Ferramenta inovadora com SDK",
        "apresentação": "Demo de 15 minutos",
        "neo4j": "CREATE (c:Certification {level:'EXPERT', score:95})"
    }
}
```

## Sistema de Avaliação

### Avaliação Semanal
```python
async def avaliar_semana(candidato: str, semana: int):
    # 1. Executar teste de código
    resultado_codigo = run_script(
        "claude_sdk_evaluator.py",
        candidato=candidato
    )

    # 2. Executar testes práticos
    resultado_pratico = run_script(
        "sdk_practical_tests.py",
        candidato=candidato
    )

    # 3. Salvar no Neo4j
    save_to_neo4j(f"""
        MATCH (c:Candidate {{name: '{candidato}'}})
        CREATE (w:WeeklyEval {{
            week: {semana},
            score_codigo: {resultado_codigo['score']},
            score_pratico: {resultado_pratico['score']},
            gaps: {resultado_codigo['gaps']},
            timestamp: datetime()
        }})-[:EVALUATION_OF]->(c)
    """)

    # 4. Gerar feedback
    return {
        "score_atual": (resultado_codigo['score'] + resultado_pratico['score']) / 2,
        "progresso": calcular_progresso(semana),
        "próximos_passos": gerar_proximos_passos(resultado_codigo['gaps']),
        "on_track": score_atual >= score_esperado[semana]
    }
```

### Critérios de Progressão
```python
criterios = {
    "semana_1": {"min_score": 50, "exercicios": [1, 2]},
    "semana_2": {"min_score": 55, "exercicios": [3]},
    "semana_5": {"min_score": 70, "mcp_tools": True},  # CRÍTICO!
    "semana_8": {"min_score": 80, "hooks": True},      # CRÍTICO!
    "semana_11": {"min_score": 90, "projeto_final": True},
    "semana_12": {"min_score": 95, "certificacao": True}
}
```

## Tracking Neo4j

### Estrutura do Grafo
```cypher
// Criar jornada
CREATE (j:Journey {
    candidate: 'Diego Fornalha',
    start_date: date(),
    initial_score: 45,
    target_score: 95,
    workflow: 'claude-sdk-expert'
})

// Registrar progresso
CREATE (w:Week {number: 1, score: 55})
-[:PART_OF]->(j)

// Marcar gaps resolvidos
CREATE (g:GapResolved {
    type: 'MCP_Tools',
    resolved_week: 5,
    exercises_done: [4]
})-[:RESOLVED_BY]->(candidate)

// Certificação final
CREATE (cert:Certification {
    level: 'EXPERT',
    score: 95,
    date: date(),
    skills: ['query', 'options', 'tools', 'mcp', 'hooks', 'streaming']
})-[:EARNED_BY]->(candidate)
```

## Comandos de Execução

### Iniciar Workflow
```bash
/claude-sdk-expert-workflow "Diego Fornalha" --start
```

### Verificar Progresso
```bash
/claude-sdk-expert-workflow --check "Diego Fornalha"
```

### Executar Avaliação
```bash
/claude-sdk-expert-workflow --avaliar "Diego Fornalha" --semana 4
```

### Certificar Expert
```bash
/claude-sdk-expert-workflow --certificar "Diego Fornalha"
```

## Garantias do Workflow

```python
garantias = {
    "entrada": "Qualquer desenvolvedor com Python básico",
    "saída": "Expert em Claude Code SDK",
    "tempo": "12 semanas",
    "score_final": "95+/100",
    "gaps_resolvidos": ["MCP Tools", "Hooks", "Todos"],
    "certificação": "Expert verificado e rastreável",
    "empregabilidade": "100% pronto para projetos com SDK"
}
```

## Recursos de Suporte

- **Repositório**: claude-code-sdk-python (branch PT-BR)
- **Exercícios**: exercicios_praticos_pt_br.py (1-7)
- **Avaliador**: claude_sdk_evaluator.py
- **Testes**: sdk_practical_tests.py
- **Mentor**: /claude-sdk-expert (agente)
- **Tracking**: Neo4j Memory

## Casos de Sucesso

```python
casos = [
    {
        "nome": "Diego Fornalha",
        "inicio": "Score 45, blockchain dev",
        "fim": "Score 95, Claude CODE SDK Expert",
        "tempo": "12 semanas",
        "destaque": "Criador do bootcamp"
    }
]
```

---

*Workflow Claude CODE SDK Expert - 100% focado em domínio do SDK*
*Zero to Expert garantido em 12 semanas*