# 📅 Timeline Visual do Bootcamp - Diego Fornalha

## Jornada de 12 Semanas: Score 45 → 100

## Timeline Completa

```mermaid
gantt
    title Bootcamp Claude Code SDK - 12 Semanas
    dateFormat YYYY-MM-DD
    section Fase 1 - Fundamentos
    Semana 1 - query() básico           :done, w1, 2025-09-23, 7d
    Semana 2 - ClaudeSDKClient          :active, w2, after w1, 7d
    Semana 3 - ClaudeCodeOptions        :w3, after w2, 7d

    section Fase 2 - Ferramentas
    Semana 4 - Read/Write               :w4, after w3, 7d
    Semana 5 - Bash/Search              :w5, after w4, 7d
    Semana 6 - Integração               :w6, after w5, 7d

    section Fase 3 - Gaps Críticos
    Semana 7 - MCP Tools 🔴             :crit, w7, after w6, 7d
    Semana 8 - Hooks System 🔴          :crit, w8, after w7, 7d
    Semana 9 - Debug/Otimização         :w9, after w8, 7d
    Semana 10 - Padrões Avançados       :w10, after w9, 7d

    section Fase 4 - Expert
    Semana 11 - Streaming/Async         :w11, after w10, 7d
    Semana 12 - Projeto Final           :milestone, w12, after w11, 7d
```

## 📊 Evolução do Score

```mermaid
graph LR
    subgraph "Mês 1"
        W1[45] --> W2[48]
        W2 --> W3[52]
        W3 --> W4[60]
    end

    subgraph "Mês 2"
        W4 --> W5[63]
        W5 --> W6[66]
        W6 --> W7[70]
        W7 --> W8[75]
    end

    subgraph "Mês 3"
        W8 --> W9[80]
        W9 --> W10[85]
        W10 --> W11[90]
        W11 --> W12[100]
    end

    style W1 fill:#fcc
    style W12 fill:#9f9
    style W7 fill:#ff9
    style W8 fill:#ff9
```

## 🎯 Marcos Importantes

```mermaid
timeline
    title Marcos do Bootcamp

    section Início
        23/09 : Score 45
              : Primeiro hello_claude
              : Setup completo

    section Semana 2
        30/09 : Score 48
              : Domínio de query()
              : Primeiro ClaudeSDKClient

    section Semana 4
        14/10 : Score 60
              : Fase 1 completa
              : Início Ferramentas

    section Semana 7
        04/11 : Score 70
              : GAP MCP Tools
              : Crítico!

    section Semana 8
        11/11 : Score 75
              : GAP Hooks
              : Crítico!

    section Semana 12
        16/12 : Score 100
              : Projeto Final
              : FORMATURA! 🎓
```

## 📈 Detalhamento Semanal

### 🟢 Fase 1: Fundamentos (Score 45→60)

| Semana | Data | Foco | Entregável | Score |
|--------|------|------|------------|-------|
| 1 | 23-29 Set | query() e async | 3 exercícios básicos | 45→48 |
| 2 | 30 Set-06 Out | ClaudeSDKClient | Chat simples | 48→52 |
| 3 | 07-13 Out | ClaudeCodeOptions | Configurações | 52→60 |

### 🟡 Fase 2: Ferramentas (Score 60→70)

| Semana | Data | Foco | Entregável | Score |
|--------|------|------|------------|-------|
| 4 | 14-20 Out | Read/Write/Edit | Editor de texto | 60→63 |
| 5 | 21-27 Out | Bash/Grep/Search | CLI tool | 63→66 |
| 6 | 28 Out-03 Nov | Integração | Projeto integrado | 66→70 |

### 🔴 Fase 3: Gaps Críticos (Score 70→85)

| Semana | Data | Foco | Entregável | Score |
|--------|------|------|------------|-------|
| 7 | 04-10 Nov | **MCP Tools** 🚨 | Tool customizada | 70→75 |
| 8 | 11-17 Nov | **Hooks** 🚨 | Sistema segurança | 75→80 |
| 9 | 18-24 Nov | Debug/Otimização | Performance | 80→85 |

### 🏆 Fase 4: Expert (Score 85→100)

| Semana | Data | Foco | Entregável | Score |
|--------|------|------|------------|-------|
| 10 | 25 Nov-01 Dez | Padrões | Best practices | 85→90 |
| 11 | 02-08 Dez | Streaming | Real-time app | 90→95 |
| 12 | 09-16 Dez | **Projeto Final** | App completo | 95→100 |

## 🎮 Gamificação - Conquistas por Semana

```mermaid
graph TD
    subgraph "Badges por Fase"
        F1[🌱 Iniciante<br/>Semanas 1-3]
        F2[⚡ Ferramenteiro<br/>Semanas 4-6]
        F3[🔧 Problem Solver<br/>Semanas 7-9]
        F4[🏆 SDK Master<br/>Semanas 10-12]
    end

    F1 --> Badge1[query Master]
    F1 --> Badge2[Client Expert]

    F2 --> Badge3[Tool User]
    F2 --> Badge4[Bash Ninja]

    F3 --> Badge5[MCP Creator]
    F3 --> Badge6[Hook Master]

    F4 --> Badge7[Async Pro]
    F4 --> Badge8[SDK Expert]

    style F1 fill:#9f9
    style F2 fill:#ff9
    style F3 fill:#f99
    style F4 fill:#9cf
```

## 📊 Carga Horária Sugerida

```mermaid
pie title Distribuição de Tempo Semanal
    "Teoria/Leitura" : 2
    "Prática/Código" : 5
    "Exercícios" : 3
    "Quiz/Revisão" : 1
    "Projeto" : 4
```

**Total**: 15 horas/semana (2-3h/dia útil)

## 🚨 Pontos de Atenção

```mermaid
graph LR
    subgraph "Riscos"
        R1[Semana 7<br/>MCP Tools]
        R2[Semana 8<br/>Hooks]
        R3[Semana 12<br/>Projeto Final]
    end

    R1 --> M1[Dedicar tempo extra]
    R2 --> M2[Pedir mentoria]
    R3 --> M3[Começar cedo]

    style R1 fill:#f99
    style R2 fill:#f99
    style R3 fill:#ff9
```

## ✅ Checklist Semanal

### Esta Semana (Semana 1)
- [x] Setup ambiente
- [x] Primeiro programa
- [x] Entender query vs Client
- [ ] 3 exercícios práticos
- [ ] Quiz semanal

### Próxima Semana (Semana 2)
- [ ] Estudar ClaudeSDKClient
- [ ] Implementar chat
- [ ] 5 exercícios
- [ ] Projeto mini-chat
- [ ] Score 48+

---

*"12 semanas para dominar o SDK. Você está na semana 1. Keep going!" 🚀*