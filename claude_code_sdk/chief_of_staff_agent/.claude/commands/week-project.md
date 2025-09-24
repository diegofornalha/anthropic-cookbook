---
name: week-project
description: Gerencie e desenvolva seus projetos semanais do bootcamp com orientação passo a passo
---

# 🚀 Week Project - Projetos Semanais do Bootcamp

Cada semana tem um projeto prático que consolida o aprendizado. Este comando guia você do início ao deploy!

## Uso

```bash
/week-project                  # Ver projeto da semana atual
/week-project --week 1         # Projeto específico
/week-project --start          # Iniciar projeto
/week-project --submit         # Submeter para review
/week-project --help "erro X"  # Ajuda com problema específico
```

## Projetos por Semana

### 📅 Semana 1: CLI Summarizer
**Objetivo**: Construir ferramenta CLI que resume textos usando Claude SDK

### 📅 Semana 2: Smart Contract RAG
**Objetivo**: Sistema RAG para responder perguntas sobre contratos Solidity

### 📅 Semana 3: Personal Knowledge Base
**Objetivo**: Base de conhecimento pessoal com busca semântica

### 📅 Semana 4: Multi-Document Q&A
**Objetivo**: Sistema que responde perguntas sobre múltiplos documentos

## Projeto Semana 1: CLI Summarizer

### 📋 Especificações
```markdown
Nome: claude-summarizer
Tipo: CLI Tool
Linguagem: Python
Dependências: claude-code-sdk, click, rich

Funcionalidades:
1. Resumir arquivo texto
2. Resumir URL (web page)
3. Resumir múltiplos arquivos
4. Diferentes níveis de resumo (curto/médio/longo)
5. Salvar resumos em markdown
```

### 🏗️ Estrutura do Projeto
```
claude-summarizer/
├── summarizer.py       # Código principal
├── requirements.txt    # Dependências
├── README.md          # Documentação
├── tests/             # Testes
│   └── test_summarizer.py
└── examples/          # Exemplos de uso
    ├── sample.txt
    └── output.md
```

### 📝 Starter Code
```python
# summarizer.py
import click
import asyncio
from pathlib import Path
from claude_code_sdk import ClaudeCodeClient, ClaudeCodeOptions

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--length', default='medium',
              type=click.Choice(['short', 'medium', 'long']))
@click.option('--output', '-o', help='Output file')
async def summarize(input_file, length, output):
    """
    Summarize text files using Claude AI

    Example:
    python summarizer.py document.txt --length short -o summary.md
    """
    # TODO: Ler arquivo
    with open(input_file, 'r') as f:
        content = f.read()

    # TODO: Definir prompts por tamanho
    prompts = {
        'short': 'Resuma em 2-3 frases:',
        'medium': 'Resuma em 1 parágrafo:',
        'long': 'Faça um resumo detalhado com bullets:'
    }

    # TODO: Configurar Claude
    options = ClaudeCodeOptions(
        model="claude-3-5-sonnet-20241022",
        temperature=0.3  # Mais determinístico para resumos
    )

    # TODO: Fazer request
    async with ClaudeCodeClient(options=options) as client:
        prompt = f"{prompts[length]}\n\n{content}"
        response = await client.query(prompt)
        summary = response.result

    # TODO: Salvar ou printar resultado
    if output:
        with open(output, 'w') as f:
            f.write(f"# Resumo\n\n{summary}\n")
            f.write(f"\n---\n*Resumido com Claude AI*")
        click.echo(f"✅ Resumo salvo em {output}")
    else:
        click.echo(summary)

if __name__ == '__main__':
    asyncio.run(summarize())
```

### 🎯 Milestones

#### Milestone 1: Setup Básico ✅
- [ ] Criar estrutura de pastas
- [ ] Instalar dependências
- [ ] Hello World com Claude SDK
- [ ] Commit inicial

#### Milestone 2: Funcionalidade Core
- [ ] Ler arquivos texto
- [ ] Enviar para Claude
- [ ] Receber e exibir resumo
- [ ] Testar com 3 arquivos diferentes

#### Milestone 3: Features Avançadas
- [ ] Adicionar níveis de resumo
- [ ] Suportar múltiplos arquivos
- [ ] Progress bar com `rich`
- [ ] Tratamento de erros

#### Milestone 4: Polish
- [ ] Adicionar testes
- [ ] Escrever README completo
- [ ] Criar GIF demonstrativo
- [ ] Deploy no GitHub

### 🧪 Testes Requeridos
```python
# test_summarizer.py
import pytest
from summarizer import summarize_text

def test_short_summary():
    text = "Python é uma linguagem..." * 100
    summary = summarize_text(text, length='short')
    assert len(summary) < len(text) / 10

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        summarize_file("nao_existe.txt")

def test_empty_file():
    summary = summarize_text("")
    assert "vazio" in summary.lower()
```

### 📊 Critérios de Avaliação

```markdown
Funcionalidade (40%)
- [ ] Resume arquivos corretamente
- [ ] Diferentes níveis funcionam
- [ ] Tratamento de erros

Código (30%)
- [ ] Clean code
- [ ] Type hints
- [ ] Documentação

UX (20%)
- [ ] Interface CLI intuitiva
- [ ] Feedback claro
- [ ] Progress indicators

Extra (10%)
- [ ] Testes automatizados
- [ ] CI/CD configurado
- [ ] Features bonus
```

### 🆘 Problemas Comuns e Soluções

#### Erro: "Rate limit exceeded"
```python
# Solução: Adicionar retry com backoff
import time

async def query_with_retry(client, prompt, max_retries=3):
    for i in range(max_retries):
        try:
            return await client.query(prompt)
        except RateLimitError:
            wait_time = 2 ** i  # Exponential backoff
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

#### Erro: "Token limit exceeded"
```python
# Solução: Chunkar texto grande
def chunk_text(text, max_tokens=3000):
    # Aproximadamente 4 chars = 1 token
    max_chars = max_tokens * 4
    chunks = []
    for i in range(0, len(text), max_chars):
        chunks.append(text[i:i+max_chars])
    return chunks
```

### 🏆 Features Bonus (Opcional)

Se terminar cedo, adicione:

1. **Resumir URLs**
```python
import requests
from bs4 import BeautifulSoup

def fetch_url_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()
```

2. **Comparar documentos**
```python
@click.option('--compare', help='Compare dois arquivos')
def summarize(input_file, compare, ...):
    if compare:
        diff = compare_documents(input_file, compare)
        # Resumir diferenças
```

3. **Export para JSON**
```python
@click.option('--format', type=click.Choice(['md', 'json', 'txt']))
def export_summary(summary, format):
    if format == 'json':
        return json.dumps({
            'summary': summary,
            'metadata': {...}
        })
```

## Submit do Projeto

### Para submeter seu projeto:

```bash
/week-project --submit
```

Isso vai:
1. Rodar testes automatizados
2. Verificar estrutura do projeto
3. Calcular score (0-100)
4. Salvar no Neo4j
5. Gerar feedback

### Exemplo de Feedback:
```markdown
## Avaliação Projeto Semana 1

Score Total: 85/100 ✅

### Pontos Positivos:
- Código limpo e bem organizado
- Boa tratativa de erros
- Interface CLI intuitiva

### Melhorias Sugeridas:
- Adicionar mais testes unitários
- Melhorar documentação do README
- Considerar cache para textos repetidos

### Próximos Passos:
- Projeto aprovado!
- Pronto para Semana 2
- Considere adicionar features bonus
```

## Tracking Neo4j

```cypher
CREATE (p:Project {
    semana: 1,
    nome: 'CLI Summarizer',
    status: 'COMPLETO',
    score: 85,
    tempo_desenvolvimento: '12h',
    commits: 23,
    features_bonus: ['url_support']
})
```

## Showcase Gallery

Projetos destacados de outros alunos:

### 🌟 "Super Summarizer" - João
- Adicionou suporte para PDFs
- UI com Textual
- 95/100 score

### 🌟 "SmartSum" - Maria
- Resumo multilingual
- Integração com Notion
- 92/100 score

## Dica do Diego

> "Não tente fazer tudo perfeito de primeira.
> Faça funcionar, depois faça direito, depois faça rápido.
> Meu primeiro CLI Summarizer era 50 linhas bagunçadas.
> Hoje tenho um com 500 linhas e 10k downloads.
> Comece simples!"

---

**Lembre-se**: O projeto é para aprender, não para impressionar.
Foque em entender cada linha de código que você escreve! 🎯