---
name: daily-progress
description: Registre seu progresso diário no bootcamp e receba feedback personalizado
---

# 📈 Daily Progress - Check-in Diário do Bootcamp

Registre seu progresso diário e receba orientações personalizadas baseadas no seu avanço.

## Uso

```bash
/daily-progress                     # Check-in interativo
/daily-progress "completei RAG"     # Registro rápido
/daily-progress --week 1 --day 3    # Check-in específico
/daily-progress --stats             # Ver estatísticas
```

## Check-in Completo

O comando fará as seguintes perguntas:

### 1. O que você aprendeu hoje?
```markdown
Exemplos de respostas:
- "Aprendi sobre tokens e como LLMs processam texto"
- "Implementei meu primeiro RAG com ChromaDB"
- "Entendi a diferença entre few-shot e zero-shot"
```

### 2. Quanto tempo você estudou?
```markdown
- Manhã: ___ horas
- Tarde: ___ horas
- Noite: ___ horas
Total: ___ horas
```

### 3. O que você construiu/codou?
```python
# Cole seu código principal do dia
# Exemplo:
async def meu_primeiro_rag():
    docs = carregar_documentos()
    query = "Como funciona RAG?"
    resultado = buscar_similar(query, docs)
    return resultado
```

### 4. Quais foram seus bloqueios?
```markdown
Exemplos:
- [ ] Configuração do ambiente
- [ ] Entender conceito de embeddings
- [ ] Erro ao conectar com Claude CODE SDK
- [ ] Nenhum bloqueio hoje! 🎉
```

### 5. Como está seu nível de energia?
```markdown
🔋 Energia: [1-10]
😊 Motivação: [1-10]
🧠 Clareza mental: [1-10]
```

## Análise Automática

Com base no seu check-in, o sistema fornece:

### 📊 Métricas do Dia
```python
{
    "horas_estudo": 4.5,
    "conceitos_novos": 3,
    "codigo_escrito": 150,  # linhas
    "exercicios_completos": 2,
    "velocity": "ON_TRACK",
    "score_atual": 48  # subiu de 45!
}
```

### 🎯 Feedback Personalizado
```markdown
## Análise do seu progresso:

✅ **Pontos fortes hoje:**
- Ótimo tempo de estudo (4.5h)
- Código RAG funcionando
- Superou bloqueio com embeddings

⚠️ **Atenção para:**
- Temperature ainda confuso → revisar /ai-basics "temperature"
- Velocity um pouco abaixo → adicionar 30min amanhã

💡 **Recomendações:**
1. Amanhã foque em prompt engineering
2. Refaça o exercício de tokens com mais calma
3. Assista vídeo sobre Chain-of-Thought
```

### 🏆 Conquistas Desbloqueadas
```markdown
🎖️ "Primeiro RAG" - Implementou sistema RAG funcional!
⭐ "Maratonista" - Estudou 4+ horas em um dia!
🔥 "Streak 3 dias" - Check-in consistente!
```

## Tracking Semanal

### Visualização da Semana
```
Semana 1 - Fundamentos
Seg [✅] 3h - Tokens/LLMs
Ter [✅] 4h - Embeddings
Qua [✅] 4.5h - RAG ← VOCÊ ESTÁ AQUI
Qui [ ] - Prompt Engineering
Sex [ ] - Projeto CLI

Progress: ███████░░░ 60%
Score: 45 → 48 (+3)
```

## Integração Neo4j

Cada check-in é salvo para análise de padrões:

```cypher
CREATE (d:DailyProgress {
    data: date(),
    semana: 1,
    dia: 3,
    horas: 4.5,
    conceitos: ['RAG', 'embeddings', 'ChromaDB'],
    bloqueios: ['config ambiente'],
    energia: 8,
    motivacao: 9,
    score: 48,
    velocity: 'ON_TRACK'
})-[:BELONGS_TO]->(b:Bootcamp {nome: 'Diego'})

// Análise de padrões
MATCH (d:DailyProgress)-[:BELONGS_TO]->(b:Bootcamp {nome: 'Diego'})
RETURN
    AVG(d.horas) as media_horas,
    MAX(d.score) as score_maximo,
    COLLECT(d.bloqueios) as bloqueios_comuns
```

## Seu Progresso Individual

```markdown
📊 Suas métricas pessoais:

Horas de estudo hoje: {{horas}}h
Score atual: {{score}}
Velocity: {{velocity}}
Gaps resolvidos: {{gaps_count}}
```

## Templates de Respostas

### Check-in Rápido de Sucesso
```bash
/daily-progress "RAG completo! 4h estudo. Próximo: prompts. Energia 9/10"
```

### Check-in com Dificuldades
```bash
/daily-progress "Travado em embeddings. 2h estudo. Preciso ajuda. Energia 5/10"
# Sistema automaticamente sugere: /mentor-help "embeddings"
```

### Check-in de Projeto
```bash
/daily-progress "Projeto CLI 80% pronto. 5h coding. Deploy amanhã!"
```

## Gamificação

### Sistema de Pontos
- Check-in diário: +10 pts
- 4+ horas estudo: +20 pts
- Código funcional: +30 pts
- Compartilhar aprendizado: +15 pts
- Resolver bloqueio solo: +25 pts

### Seus Pontos Acumulados
```markdown
🏆 Seu Progresso:
Pontos totais: {{total_pontos}}
Pontos hoje: {{pontos_hoje}}

Próxima recompensa: {{proxima_meta}} pts = {{recompensa}}
```

## Alertas Inteligentes

O sistema detecta padrões e alerta:

```markdown
⚠️ **Alerta: Burnout Risk**
Detectamos 3 dias com energia < 6.
Sugestão: Tire tarde de folga amanhã.

⚠️ **Alerta: Conceito não absorvido**
"Embeddings" mencionado como bloqueio 2x.
Sugestão: /mentor-help "embeddings" hoje!

✅ **Parabéns: Velocity aumentando!**
Sua velocidade cresceu 20% esta semana.
Continue assim!
```

## Exportar Progresso

```bash
/daily-progress --export markdown  # Gera relatório
/daily-progress --export json      # Para análise
/daily-progress --export pdf       # Para portfolio
```

## Motivação Diária

A cada check-in, uma mensagem motivacional:

> "Dia 3 e você já está construindo RAG!
> Lembre-se: GitHub Copilot não existia há 5 anos.
> Em 3 meses, você estará criando o próximo.
> Keep going! 🚀"
>
> — Diego Fornalha

---

**Pro tip**: Consistência > Intensidade.
Melhor 2h todo dia do que 10h uma vez por semana!