# Avaliações com Promptfoo

### Pré-requisitos
Para usar o Promptfoo você precisará ter o node.js e npm instalados em seu sistema. Para mais informações, siga [este guia](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

Você pode instalar o promptfoo usando npm ou executá-lo diretamente usando npx. Neste guia, usaremos npx.

*Observação: Para este exemplo, você não precisará executar `npx promptfoo@latest init`, já existe um arquivo `promptfooconfig.yaml` inicializado neste diretório*

Veja a documentação oficial [aqui](https://www.promptfoo.dev/docs/getting-started)

### Começando
A avaliação é orquestrada pelo arquivo `promptfooconfig.yaml`. Neste arquivo, definimos as seguintes seções:

- Prompts
    - O Promptfoo permite que você importe prompts em muitos formatos diferentes. Você pode ler mais sobre isso [aqui](https://www.promptfoo.dev/docs/configuration/parameters).
    - Neste exemplo, carregaremos 3 prompts - os mesmos usados em `guide.ipynb` do arquivo `prompts.py`:
        - As funções são idênticas às usadas em `guide.ipynb`, exceto que, em vez de chamar a API Anthropic, elas apenas retornam o prompt. O Promptfoo então gerencia a orquestração de chamar a API e armazenar os resultados.
        - Você pode ler mais sobre funções de prompt [aqui](https://www.promptfoo.dev/docs/configuration/parameters#prompt-functions). Usar python nos permite reutilizar a classe VectorDB que é necessária para RAG, isso está definido em `vectordb.py`.
- Provedores
    - Com o Promptfoo você pode se conectar a muitos LLMs diferentes de diferentes plataformas, veja [aqui para mais](https://www.promptfoo.dev/docs/providers). Em `guide.ipynb` usamos Haiku com temperatura padrão 0.0. Usaremos o Promptfoo para experimentar com uma variedade de configurações de temperatura diferentes para identificar a escolha ideal para nosso caso de uso.
- Testes
    - Usaremos os mesmos dados que foram usados em `guide.ipynb`, que podem ser encontrados nesta [Planilha Google](https://docs.google.com/spreadsheets/d/1UwbrWCWsTFGVshyOfY2ywtf5BEt7pUcJEGYZDkfkufU/edit#gid=0).
    - O Promptfoo tem uma ampla variedade de testes integrados que podem ser encontrados [aqui](https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic).
    - Neste exemplo, definiremos um teste em nosso `dataset.csv` já que as condições de nossa avaliação mudam com cada linha e um teste no `promptfooconfig.yaml` para condições que são consistentes em todos os casos de teste. Leia mais sobre isso [aqui](https://www.promptfoo.dev/docs/configuration/parameters/#import-from-csv)
- Transform
    - Na seção `defaultTest` definimos uma função de transformação. Esta é uma função python que extrai a saída específica que queremos testar da resposta do LLM.
- Output
    - Definimos o caminho para o arquivo de saída. O Promptfoo pode gerar resultados em muitos formatos, [veja aqui](https://www.promptfoo.dev/docs/configuration/parameters/#output-file). Alternativamente, você pode usar a interface web do Promptfoo, [veja aqui](https://www.promptfoo.dev/docs/usage/web-ui).

### Executar a avaliação

Para começar com o Promptfoo, abra seu terminal e navegue até este diretório (`./evaluation`).

Antes de executar sua avaliação, você deve definir as seguintes variáveis de ambiente:

`export ANTHROPIC_API_KEY=YOUR_API_KEY`
`export VOYAGE_API_KEY=YOUR_API_KEY`

Do diretório `evaluation`, execute o seguinte comando:

`npx promptfoo@latest eval`

Se você quiser aumentar a concorrência das requisições (padrão = 4), execute o seguinte comando:

`npx promptfoo@latest eval -j 25`

Quando a avaliação estiver completa, o terminal imprimirá os resultados para cada linha no conjunto de dados.

Agora você pode voltar para `guide.ipynb` para analisar os resultados!