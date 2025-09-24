# Conceito 1: Stateless vs Stateful

## 🧠 Entendimento Conceitual (Agnóstico)

### O que é STATELESS?
- **Definição**: Cada interação é independente
- **Analogia**: Como perguntar para um estranho na rua - sem contexto prévio
- **Característica**: Não lembra de conversas anteriores
- **Uso ideal**: Perguntas únicas, tarefas isoladas

### O que é STATEFUL?
- **Definição**: Mantém contexto entre interações
- **Analogia**: Como conversar com um amigo - lembra do histórico
- **Característica**: Acumula conhecimento da sessão
- **Uso ideal**: Conversas longas, tarefas sequenciais

## 📊 Comparação Conceitual

| Aspecto | Stateless | Stateful |
|---------|-----------|----------|
| Memória | Nenhuma | Mantém histórico |
| Performance | Mais rápido | Usa mais recursos |
| Complexidade | Simples | Mais complexo |
| Casos de uso | Perguntas únicas | Diálogos |

## 🎯 Quando usar cada um?

### Use STATELESS quando:
- ✅ Tarefa única e completa
- ✅ Não precisa contexto anterior
- ✅ Performance é crítica
- ✅ Múltiplas requisições paralelas

### Use STATEFUL quando:
- ✅ Conversa multi-turno
- ✅ Contexto é importante
- ✅ Refinamento iterativo
- ✅ Sessão de trabalho longa

## 🔄 Implementação Universal

### Padrão Stateless (qualquer linguagem)
```
FUNÇÃO consulta_simples(pergunta):
    resposta = enviar_para_claude(pergunta)
    RETORNAR resposta
    // Fim - sem memória
```

### Padrão Stateful (qualquer linguagem)
```
CLASSE conversa:
    histórico = []

    FUNÇÃO enviar_mensagem(mensagem):
        histórico.adicionar(mensagem)
        resposta = enviar_para_claude(histórico)
        histórico.adicionar(resposta)
        RETORNAR resposta
```

## 💡 Insight Principal

> "Stateless = Uma pergunta, uma resposta, fim."
> "Stateful = Conversa contínua com memória."

## ✅ Teste de Compreensão

Responda SEM código:

1. Quando você usaria stateless?
2. Quando stateful é essencial?
3. Qual é mais eficiente para 1000 perguntas independentes?
4. Qual é melhor para debugar código iterativamente?

## 🎓 Você entendeu quando...

- Consegue explicar para alguém sem usar código
- Sabe escolher o certo para cada situação
- Entende trade-offs de performance vs funcionalidade
- Pode implementar em QUALQUER linguagem

---

**Próximo conceito**: [02_async_patterns.md](./02_async_patterns.md)