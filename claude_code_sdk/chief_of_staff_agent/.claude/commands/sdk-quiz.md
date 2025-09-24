---
type: command
name: sdk-quiz
description: Quiz interativo sobre Claude Code SDK - teste seus conhecimentos e identifique gaps
---

# SDK Quiz - Teste Seus Conhecimentos do Claude Code SDK

Quiz gamificado para avaliar e reforçar conhecimento do Claude Code SDK com identificação automática de gaps.

## Uso

```bash
/sdk-quiz                    # Pergunta aleatória não respondida/errada
/sdk-quiz --completo         # Quiz completo (12 questões)
/sdk-quiz --gaps            # Apenas questões dos seus gaps
/sdk-quiz --historico       # Ver seus resultados anteriores
/sdk-quiz "query"           # Pergunta específica sobre o tema
```

## Modos de Jogo

### 🎮 Modo Completo
```bash
/sdk-quiz --completo
```
- 12 questões cobrindo todos os conceitos
- 30 segundos por questão
- Máximo de 230 pontos
- Ideal para avaliação completa

### 🎯 Questão Aleatória
```bash
/sdk-quiz
```
- 1 pergunta aleatória que você errou ou nunca respondeu
- Ideal para revisão rápida diária
- 1-2 minutos apenas
- Foca nos seus pontos fracos

### 🔴 Modo Gaps
```bash
/sdk-quiz --gaps
```
- Questões focadas nos seus gaps identificados
- Baseado em resultados anteriores
- Reforço direcionado
- Adaptativo ao seu progresso

### 🎯 Modo Desafio Pessoal
```bash
/sdk-quiz --desafio
```
- Desafie seus próprios recordes
- Supere sua melhor pontuação
- Melhore seu tempo médio
- Acompanhe sua evolução

### 📊 Histórico Pessoal
```bash
/sdk-quiz --historico
```
- Histórico de todos os seus quizzes
- Evolução do seu score ao longo do tempo
- Seus gaps resolvidos vs pendentes
- Suas estatísticas detalhadas

## Categorias de Questões

### 🟢 Básico (10 pts cada)
- Fundamentos do SDK
- query() vs ClaudeSDKClient
- Autenticação sem API key

### 🟡 Intermediário (15 pts cada)
- ClaudeCodeOptions
- Ferramentas disponíveis
- Quando usar cada abordagem

### 🔴 Avançado (25 pts cada) - GAPS CRÍTICOS!
- **MCP Tools** - Como criar e usar
- **Hooks System** - PreToolUse e PostToolUse
- Estrutura de retorno

### 🏆 Expert (20 pts cada)
- Streaming com ClaudeSDKClient
- Async/await patterns
- Otimizações avançadas

## Sistema de Pontuação

```python
pontuacao = {
    "resposta_correta": pontos_da_questao,
    "tempo_bonus": +(5) se responder em < 10 segundos,
    "streak_bonus": +(10) a cada 3 acertos seguidos,
    "perfeito": +(50) se acertar todas
}
```

## Níveis de Classificação

| Score | Nível | Badge | Significado |
|-------|-------|-------|-------------|
| 90-100% | 🏆 EXPERT | SDK Master | Pronto para contribuir com o SDK |
| 75-89% | 💎 AVANÇADO | SDK Pro | Poucos gaps restantes |
| 60-74% | ⭐ INTERMEDIÁRIO | SDK User | Bom progresso |
| 40-59% | 🌱 INICIANTE | SDK Learner | Continue praticando |
| 0-39% | 🔰 NOVATO | SDK Starter | Comece pelo básico |

## Questões Exemplo

### Questão Básica
```
Q: Qual a diferença entre query() e ClaudeSDKClient?
A) Não há diferença
B) query() é stateless, Client é stateful ✅
C) Client é mais lento
D) query() só funciona offline
```

### Questão Gap Crítico (MCP)
```
Q: Qual a estrutura de retorno CORRETA de uma MCP tool?
A) return resultado
B) return {"result": valor}
C) return {"content": [{"type": "text", "text": "resultado"}]} ✅
D) return None
```

## Feedback Personalizado

### Após cada questão:
- ✅ Correto: Explicação do conceito
- ❌ Incorreto: Resposta correta + explicação
- 📚 Link para exercício relacionado

### Relatório Final:
```
📊 SEUS RESULTADOS
═════════════════
Acertos: 8/12 (66.7%)
Pontuação: 140/230
Tempo: 5min 23s

✅ Pontos Fortes:
• query() usage
• ClaudeCodeOptions

🔴 Gaps Críticos:
• MCP Tools (exercício 4)
• Hooks System (exercício 5)

📈 Progresso:
Quiz 1: 45% → Quiz 2: 66% ↗️
```

## Integração com Neo4j

### Tracking Automático
```cypher
CREATE (q:QuizResult {
    player: 'Diego Fornalha',
    mode: 'completo',
    score: 140,
    percentage: 66.7,
    gaps: ['mcp_tools', 'hooks'],
    timestamp: datetime()
})-[:COMPLETED_BY]->(player)
```

### Análise de Evolução
```cypher
MATCH (q:QuizResult)-[:COMPLETED_BY]->(p:Player {name: 'Diego'})
RETURN q.score, q.timestamp
ORDER BY q.timestamp
// Mostra evolução do score ao longo do tempo
```

## Gamificação

### 🏅 Achievements
- **First Try**: Complete seu primeiro quiz
- **Perfect Score**: 100% de acertos
- **Speed Demon**: Responda todas em < 10s cada
- **Gap Killer**: Resolva todos os gaps críticos
- **SDK Master**: Score 95%+ três vezes seguidas

### 📈 Seu Histórico
```bash
/sdk-quiz --historico
```
```
🏆 SEU PROGRESSO - CLAUDE CODE SDK
════════════════════════════════
1. 2025-09-23 - 140 pts (66.7%)
2. 2025-09-22 - 125 pts (54.3%)
3. 2025-09-21 - 110 pts (47.8%)

Evolução: 📈 +19% em 3 dias!
```

## Comandos Relacionados

```bash
/sdk-help "MCP Tools"    # Ajuda específica sobre gaps
/sdk-basics              # Revisar conceitos
python examples/exercicios_praticos_pt_br.py 4  # Praticar MCP
python examples/exercicios_praticos_pt_br.py 5  # Praticar Hooks
```

## Dicas para Melhorar

1. **Foque nos Gaps**: Use modo `/sdk-quiz --gaps`
2. **Pratique Diariamente**: Modo rápido todo dia
3. **Revise Erros**: `/sdk-quiz --review` mostra onde errou
4. **Supere-se**: Modo desafio pessoal acelera aprendizado
5. **Complete Exercícios**: Gaps indicam qual exercício fazer

## Easter Eggs

- 🎉 Score 100% toca fanfarra
- 🔥 3 perfeitos seguidos = "On Fire!"
- 💀 0% = "Hora de estudar!"
- ⚡ < 3min no completo = "Lightning Fast!"

## Executar Direto

Além do comando, você pode executar diretamente:
```bash
python examples/quiz_claude_sdk.py
```

---

*Quiz criado por Diego Fornalha para o Bootcamp Claude Code SDK*
*Meta: Identificar e eliminar todos os gaps em 12 semanas*