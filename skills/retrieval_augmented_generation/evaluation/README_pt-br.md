# Evaluations com Promptfoo

### Pré-requisitos 
para use Promptfoo you will need para have node.js & npm installed on your system. Para mais informações follow [este Guia](https://docs.npmjs.com/downloading-e-installing-node-js-e-npm)  

You can instalar promptfoo using npm ou executar it directly using npx. In este Guia we will use npx.  

*Nota: For Este exemplo you will não need para executar `npx promptfoo@latest init` ali is already an initialized `promptfooconfig.yaml` arquivo in este diretório*  

Veja o official docs [aqui](https://www.promptfoo.dev/docs/getting-started)  


### Começando
The evaluation is orchestrated by the `promptfooconfig...` `.yaml` arquivos. In our application we divide the evaluation logic entre `promptfooconfig_retrieval.yaml` for evaluating the retrieval system e `promptfooconfig_end_to_end.yaml` para evaluate the end para end desempenho. In each of estes arquivos we define O seguinte sections

### Retrieval Evaluations

- Prompts
    - Promptfoo enables you para importar prompts in muitos different formats. You can Leia mais sobre este [aqui](https://www.promptfoo.dev/docs/Configuração/parâmetros).
    - In our case, we skip providing a novo prompt each tempo, e merely pass through the `{{query}}` para each retrieval 'provider' for evaluation
- Providers
    - Instead of using a standard LLM provider, we wrote personalizado providers for each retrieval método found in `guide.ipynb`
- testes
    - We will use the same data aquele was used in `guide.ipynb`. We dividir it into `end_to_end_dataset.csv` e `retrieval_dataset.csv` e added an `__expected` column para each dataset qual allows us para automatically executar assertions for each row
    - You can encontrar our retrieval evaluation logic in `eval_end_to_end.py`

### End para End Evaluations

- Prompts
    - Promptfoo enables you para importar prompts in muitos different formats. You can Leia mais sobre este [aqui](https://www.promptfoo.dev/docs/Configuração/parâmetros).
    - We have 3 prompts in our end para end evaluation config: each of qual corresponds para a método use
        - The funções are identical para aqueles used in `guide.ipynb` except aquele instead of calling the Anthropic API they just retorna the prompt. Promptfoo então handles the orchestration of calling the API e storing the results.
        - You can Leia mais sobre prompt funções [aqui](https://www.promptfoo.dev/docs/Configuração/parâmetros#prompt-funções). Using python allows us para reuse the VectorDB classe qual is necessary for RAG, este is defined in `vectordb.py`.
- Providers
    - com Promptfoo you can conectar para muitos different LLMs de different platforms, see [aqui for mais](https://www.promptfoo.dev/docs/providers). In `guide.ipynb` we used Haiku com padrão temperature 0.0. We will use Promptfoo para experiment com different models.
- testes
    - We will use the same data aquele was used in `guide.ipynb`. We dividir it into `end_to_end_dataset.csv` e `retrieval_dataset.csv` e added an `__expected` column para each dataset qual allows us para automatically executar assertions for each row
    - Promptfoo has a wide array of built in testes qual can be found [aqui](https://www.promptfoo.dev/docs/Configuração/expected-outputs/deterministic).
    - You can encontrar the teste logic for the retrieval system in `eval_retrieval.py` e the teste logic for the end para end system in `eval_end_to_end.py`
- saída
    - We define the path for the saída arquivo. Promptfoo can saída results in muitos formats, [see aqui](https://www.promptfoo.dev/docs/Configuração/parâmetros/#saída-arquivo). Alternatively you can use Promptfoo's web UI, [see aqui](https://www.promptfoo.dev/docs/Uso/web-ui).


### executar the eval

Para começar com Promptfoo abrir your terminal e navigate para este diretório (`./evaluation`).

antes running your evaluation you must define O seguinte enviroment variáveis:

`export ANTHROPIC_API_KEY=YOUR_API_KEY`  
`export VOYAGE_API_KEY=YOUR_API_KEY`

de the `evaluation` diretório, executar one of O seguinte comandos.  

- para evaluate the end para end system desempenho: `npx promptfoo@latest eval -c promptfooconfig_end_to_end.yaml --output ../data/end_to_end_results.json`

- para evaluate the retrieval system desempenho in isolation: `npx promptfoo@latest eval -c promptfooconfig_retrieval.yaml --output ../data/retrieval_results.json`

quando the evaluation is completo the terminal will print the results for each row in the dataset. You can also executar `npx promptfoo@latest view` para view outputs in the promptfoo UI viewer.