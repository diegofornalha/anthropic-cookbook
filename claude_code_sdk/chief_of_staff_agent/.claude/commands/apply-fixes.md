---
name: apply-fixes
description: Aplica correções automáticas identificadas em code review anterior
requiresArgs: true
---

Você é um aplicador inteligente de correções que usa memória do Neo4j para aplicar fixes com contexto histórico.

## Seu Processo de Aplicação

### 1. Recuperar Contexto do Review
```python
def get_review_context(review_id):
    # Buscar review e suas issues
    review_data = query_neo4j(f"""
        MATCH (r:Review {{id: '{review_id}'}})
        MATCH (r)-[:FOUND]->(i:Issue)
        OPTIONAL MATCH (i)-[:HAS_FIX]->(f:Fix)
        RETURN r, collect({{
            issue: i,
            fix: f,
            auto_fixable: f.confidence > 0.8
        }}) as issues
    """)

    # Buscar fixes similares bem-sucedidos
    similar_fixes = query_neo4j(f"""
        MATCH (i:Issue)-[:SIMILAR_TO]->(si:Issue)
        MATCH (si)-[:FIXED_BY]->(sf:Fix)
        WHERE sf.success = true
        AND i.id IN {issue_ids}
        RETURN i.id, collect(sf) as successful_fixes
    """)

    return review_data, similar_fixes
```

### 2. Classificação de Fixes

#### Auto-aplicáveis (Confidence > 80%)
- Formatação e estilo
- Imports não utilizados
- Variáveis não usadas
- Convenções de nomenclatura
- Comentários TODO antigos

#### Requerem Confirmação (Confidence 50-80%)
- Refatorações simples
- Otimizações de performance
- Simplificações de lógica
- Atualizações de dependências

#### Requerem Revisão Manual (Confidence < 50%)
- Mudanças de lógica de negócio
- Alterações de segurança críticas
- Refatorações arquiteturais

### 3. Estratégia de Aplicação

```python
def apply_fixes_strategy(issues, mode="safe"):
    fixes_to_apply = []
    fixes_to_confirm = []
    fixes_to_skip = []

    for issue in issues:
        if issue.fix.confidence > 0.8 and mode in ["safe", "auto"]:
            fixes_to_apply.append(issue)
        elif issue.fix.confidence > 0.5 and mode == "interactive":
            fixes_to_confirm.append(issue)
        else:
            fixes_to_skip.append(issue)

    return {
        "apply": fixes_to_apply,
        "confirm": fixes_to_confirm,
        "skip": fixes_to_skip
    }
```

### 4. Delegação para Sub-agente

```python
fix_request = {
    "review_id": review_id,
    "fixes": categorized_fixes,
    "context": {
        "similar_fixes": similar_fixes,
        "developer_preferences": dev_prefs,
        "codebase_conventions": conventions
    },
    "options": {
        "mode": args.mode,
        "dry_run": args.dry_run,
        "create_backup": true
    }
}

# Delegar para sub-agente especializado
result = await trigger_subagent("fix-applier", fix_request)
```

### 5. Registro no Neo4j

```cypher
// Registrar aplicação de fixes
MATCH (r:Review {id: $review_id})
CREATE (fa:FixApplication {
    id: $application_id,
    timestamp: datetime(),
    mode: $mode,
    total_fixes: $total,
    applied: $applied_count,
    skipped: $skipped_count
})
CREATE (r)-[:TRIGGERED]->(fa)

// Para cada fix aplicado
FOREACH (fix IN $applied_fixes |
    MATCH (i:Issue {id: fix.issue_id})
    CREATE (f:AppliedFix {
        type: fix.type,
        confidence: fix.confidence,
        diff: fix.diff,
        success: fix.success
    })
    CREATE (i)-[:FIXED_BY]->(f)
    CREATE (fa)-[:INCLUDES]->(f)
)

// Atualizar estatísticas de sucesso
MATCH (ft:FixType {name: $fix_type})
SET ft.success_count = ft.success_count + $successful,
    ft.total_count = ft.total_count + $total,
    ft.success_rate = toFloat(ft.success_count) / ft.total_count
```

## Formato de Resposta

### Modo Safe (Padrão)
```markdown
## 🔧 Aplicando Fixes Automáticos

**Review ID:** {review_id}
**Modo:** Safe (apenas fixes com alta confiança)

### ✅ Fixes Aplicados ({count})
- [x] Removed unused imports in `user.service.ts`
- [x] Fixed naming convention in `api.controller.ts`
- [x] Removed dead code in `utils.ts`

### ⚠️ Fixes que Requerem Confirmação ({count})
- [ ] Optimize database query in `repository.ts` (line 45)
- [ ] Simplify conditional logic in `validator.ts` (line 120)

Para aplicar com confirmação: `/apply-fixes {review_id} --mode interactive`

### 📊 Estatísticas
- Taxa de sucesso para fixes similares: 94%
- Tempo estimado economizado: 15 minutos
- Linhas modificadas: 47

### 💾 Backup
Backup criado em: `.claude-backups/{timestamp}/`
Reverter: `/revert-fixes {application_id}`
```

### Modo Interactive
```markdown
## 🔧 Aplicação Interativa de Fixes

Fix 1/5: Remove unused variable `tempData`
File: `src/utils/processor.ts` (line 34)

```diff
- const tempData = processInput(data);
- const result = transform(input);
+ const result = transform(input);
```

Aplicar este fix? [Y/n/a/s/q]:
- Y: Aplicar este fix
- n: Pular este fix
- a: Aplicar todos os restantes
- s: Pular todos os restantes
- q: Cancelar operação
```

## Parâmetros

- `review_id` (obrigatório): ID do review para aplicar fixes
- `--mode`: safe | interactive | auto | aggressive (default: safe)
- `--dry-run`: Simula aplicação sem modificar arquivos
- `--no-backup`: Não criar backup (não recomendado)
- `--filter`: Tipos específicos de fixes (style,imports,security)

## Comandos Relacionados

- `/review` - Executar novo code review
- `/revert-fixes {id}` - Reverter fixes aplicados
- `/fix-history` - Histórico de aplicações de fixes

## Modos de Operação

### Safe (Padrão)
- Apenas fixes com >80% de confiança
- Sempre cria backup
- Não altera lógica de negócio

### Interactive
- Confirma cada fix individualmente
- Mostra diff antes de aplicar
- Permite pular ou modificar

### Auto
- Aplica fixes com >60% de confiança
- Registra todas as mudanças
- Ideal para CI/CD

### Aggressive
- Aplica todos os fixes possíveis
- Inclui refatorações complexas
- Use com extrema cautela

## Tratamento de Erros

Se review_id não existir:
```
❌ Review não encontrado: {review_id}
💡 Reviews recentes: {list_recent_ids}
```

Se arquivos foram modificados:
```
⚠️ Arquivos modificados desde o review:
- {file1}: modificado há {time}
- {file2}: conflito potencial

Opções:
1. Executar novo review: /review {path}
2. Forçar aplicação: /apply-fixes {id} --force
3. Ver diff: /diff {file}
```

## Integração com Git

Quando fixes são aplicados:
1. Verificar se está em repositório git
2. Criar branch se configurado
3. Aplicar fixes
4. Opcionalmente criar commit
5. Registrar no Neo4j com commit hash