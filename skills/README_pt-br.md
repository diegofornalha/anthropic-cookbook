# Habilidades do Claude

Bem-vindo à seção de Habilidades do Anthropic Cookbook! Este diretório contém uma coleção de guias que demonstram habilidades e capacidades específicas onde o Claude se destaca. Cada guia oferece uma exploração aprofundada de uma habilidade particular, discutindo possíveis casos de uso, técnicas de engenharia de prompt para otimizar resultados e abordagens para avaliar o desempenho do Claude.

## Guias

- **[Classificação com Claude](./classification/guide.ipynb)**: Descubra como o Claude pode revolucionar tarefas de classificação, especialmente em cenários com regras de negócio complexas e dados de treinamento limitados. Este guia orienta você através da preparação de dados, engenharia de prompt com geração aumentada por recuperação (RAG), testes e avaliação.

- **[Geração Aumentada por Recuperação com Claude](./retrieval_augmented_generation/guide.ipynb)**: Aprenda como aprimorar as capacidades do Claude com conhecimento específico de domínio usando RAG. Este guia demonstra como construir um sistema RAG do zero, otimizar seu desempenho e criar uma suíte de avaliação. Você aprenderá como técnicas como indexação de resumo e re-ranqueamento podem melhorar significativamente a precisão, recall e acurácia geral em tarefas de perguntas e respostas.

- **[Geração Aumentada por Recuperação com Embeddings Contextuais](./contextual-embeddings/guide.ipynb)**: Aprenda a usar uma nova técnica para melhorar o desempenho do seu sistema RAG. No RAG tradicional, documentos são tipicamente divididos em pedaços menores para recuperação eficiente. Embora essa abordagem funcione bem para muitas aplicações, ela pode levar a problemas quando pedaços individuais carecem de contexto suficiente. Embeddings Contextuais resolvem esse problema adicionando contexto relevante a cada pedaço antes do embedding. Você aprenderá como usar embeddings contextuais com busca semântica, busca BM25 e re-ranqueamento para melhorar o desempenho.

- **[Sumarização com Claude](./summarization/guide.ipynb)**: Explore a capacidade do Claude de sumarizar e sintetizar informações de múltiplas fontes. Este guia abrange uma variedade de técnicas de sumarização, incluindo métodos multi-shot, baseados em domínio e de fragmentação, bem como estratégias para lidar com conteúdo extenso e múltiplos documentos. Também exploramos a avaliação de resumos, que pode ser um equilíbrio entre arte, subjetividade e a abordagem correta!

- **[Text-to-SQL com Claude](./text_to_sql/guide.ipynb)**: Este guia aborda como gerar consultas SQL complexas a partir de linguagem natural usando técnicas de prompt, autoaperfeiçoamento e RAG. Também exploraremos como avaliar e melhorar a precisão das consultas SQL geradas, com avaliações que testam sintaxe, correção de dados, contagem de linhas e muito mais.

## Começando

Para começar com os guias de Habilidades, simplesmente navegue até o diretório do guia desejado e siga as instruções fornecidas no arquivo `guide.ipynb`. Cada guia é autocontido e inclui todo o código, dados e scripts de avaliação necessários para reproduzir os exemplos e experimentos.