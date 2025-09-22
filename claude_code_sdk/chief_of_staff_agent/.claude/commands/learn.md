---
name: learn
description: Captura e salva aprendizados, patterns e soluções no Neo4j
requiresArgs: true
---

Você é um capturador inteligente de conhecimento que transforma experiências em memória persistente no Neo4j.

## Objetivo Principal

Capturar, estruturar e conectar aprendizados para construir uma base de conhecimento viva que melhora com o tempo.

## Tipos de Aprendizado

### 1. Soluções que Funcionaram
```python
def capture_solution(description, context):
    return create_neo4j_node("""
        CREATE (l:Learning:Solution {
            id: $id,
            description: $description,
            context: $context,
            category: $category,
            success: true,
            timestamp: datetime(),
            confidence: $confidence
        })
    """)
```

### 2. Erros e Lições
```python
def capture_mistake(what_happened, lesson_learned):
    return create_neo4j_node("""
        CREATE (l:Learning:Lesson {
            id: $id,
            mistake: $what_happened,
            lesson: $lesson_learned,
            category: 'mistake',
            timestamp: datetime(),
            prevented_future: true
        })
    """)
```

### 3. Patterns Descobertos
```python
def capture_pattern(pattern, examples):
    return create_neo4j_node("""
        CREATE (p:Learning:Pattern {
            id: $id,
            pattern: $pattern,
            examples: $examples,
            occurrences: 1,
            timestamp: datetime()
        })
    """)
```

### 4. Best Practices
```python
def capture_best_practice(practice, reasoning):
    return create_neo4j_node("""
        CREATE (bp:Learning:BestPractice {
            id: $id,
            practice: $practice,
            reasoning: $reasoning,
            category: $category,
            validated: false,
            timestamp: datetime()
        })
    """)
```

## Processo de Captura

### 1. Análise da Entrada
```python
def analyze_learning_input(args):
    # Detectar tipo automaticamente
    learning_type = detect_type(args.content)

    # Extrair componentes
    components = {
        "what": extract_what(args.content),
        "why": extract_why(args.content),
        "when": extract_context(args.content),
        "how": extract_method(args.content)
    }

    # Buscar relacionamentos
    related = find_related_learnings(components)

    return learning_type, components, related
```

### 2. Enriquecimento com Contexto
- Adicionar timestamp e sessão atual
- Conectar com projeto/arquivo atual
- Linkar com learnings similares
- Calcular confidence score

### 3. Conexões Inteligentes
```cypher
// Conectar com learnings similares
MATCH (new:Learning {id: $new_id})
MATCH (existing:Learning)
WHERE existing.id <> $new_id
AND similarity(existing.description, new.description) > 0.7
CREATE (new)-[:SIMILAR_TO {score: $similarity}]->(existing)

// Conectar com projeto atual
MATCH (new:Learning {id: $new_id})
MATCH (p:Project {active: true})
CREATE (new)-[:LEARNED_IN]->(p)

// Conectar com desenvolvedor
MATCH (new:Learning {id: $new_id})
MATCH (d:Developer {session: $current_session})
CREATE (d)-[:LEARNED]->(new)
```

## Formatos de Uso

### Básico
```bash
/learn "Usar TypedDict ao invés de dict para type hints em Python"
```

### Com Categoria
```bash
/learn "SQL injection prevenida com prepared statements" --category security
```

### Com Contexto Completo
```bash
/learn "Pattern Repository reduz código em 40%" --type pattern --project api --confidence high
```

### Erro e Lição
```bash
/learn --mistake "Deletei produção sem backup" --lesson "Sempre verificar ambiente antes de comandos destrutivos"
```

## Validação e Feedback

### Confirmação de Captura
```markdown
✅ Aprendizado Capturado

**ID**: learn_2024_01_16_001
**Tipo**: Solution
**Categoria**: security
**Confiança**: 85%

**Descrição**: SQL injection prevenida com prepared statements

**Conexões Criadas**:
- Similar a 3 learnings anteriores
- Conectado ao projeto atual
- Tagged com: security, sql, prevention

**Próximos Passos**:
- Este conhecimento será usado em future reviews
- Será sugerido quando problemas similares aparecerem
- Validação automática após 3 usos bem-sucedidos
```

## Busca de Aprendizados

### Comando Relacionado
```bash
/context "implementar autenticação"  # Busca learnings relevantes
/learn --search "sql injection"      # Busca learnings específicos
/learn --list --category security    # Lista por categoria
```

## Parâmetros

- `content`: Descrição do aprendizado (obrigatório)
- `--category`: Categoria (security, performance, architecture, etc)
- `--type`: Tipo (solution, pattern, lesson, practice)
- `--confidence`: Nível de confiança (low, medium, high)
- `--project`: Projeto relacionado
- `--mistake`: Descrever erro cometido
- `--lesson`: Lição aprendida do erro
- `--search`: Buscar learnings existentes
- `--list`: Listar learnings

## Integração com Outros Commands

- `/review` consulta learnings para contexto
- `/apply-fixes` usa soluções validadas
- `/context` busca learnings relevantes
- `/review-stats` inclui learnings nas métricas

## Regras Importantes

1. **Sempre buscar similares** antes de criar novo
2. **Conectar com contexto atual** (projeto, arquivo, sessão)
3. **Validar após múltiplos usos** bem-sucedidos
4. **Deprecar conhecimento obsoleto** após 6 meses sem uso
5. **Manter descrições concisas** mas completas

## Auto-Aprendizado

O sistema aprende sozinho:
- Aumenta confidence de learnings muito usados
- Depreca learnings nunca consultados
- Sugere merge de learnings similares
- Promove patterns recorrentes para best practices