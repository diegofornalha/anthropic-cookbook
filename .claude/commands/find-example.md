---
name: find-example
description: Busca exemplos relevantes no Cookbook baseado em um tópico ou técnica
---

Use o agente cookbook-explorer para encontrar exemplos sobre: {{args}}

Procure em todas as categorias:
- skills/ (classification, RAG, summarization)
- tool_use/ (memory, customer service, structured JSON)
- multimodal/ (vision, charts, PDFs)
- third_party/ (integrações)
- claude_code_sdk/ (SDK examples)
- misc/ (diversos)

Retorne:
1. Lista de exemplos relevantes com paths
2. Breve descrição de cada um
3. Recomendação de qual começar
4. Como adaptar para o caso específico