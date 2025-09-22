
# Evaluations com Promptfoo

### A Nota on este Evaluation Suite

1) Be sure para follow the instructions abaixo - specifically the pre-requisites sobre obrigatório packages.

2) Running the full eval suite may require higher than normal rate limits. Consider only running a subset of testes in promptfoo.

3) não every teste will pass out of the box - we've designed the evaluation para be moderately challenging.

### Pré-requisitos 
para use Promptfoo you will need para have node.js & npm installed on your system. Para mais informações follow [este Guia](https://docs.npmjs.com/downloading-e-installing-node-js-e-npm)  

You can instalar promptfoo using npm ou executar it directly using npx. In este Guia we will use npx.  

*Nota: For Este exemplo you will não need para executar `npx promptfoo@latest init` ali is already an initialized `promptfooconfig.yaml` arquivo in este diretório*  

Veja o official docs [aqui](https://www.promptfoo.dev/docs/getting-started)  

#### Nota - Additional Deps
For Este exemplo you will need para instalar O seguinte dependencies in order for our custom_evals para executar properly.

`pip install nltk rouge-score`

### Começando

Para começar, set your ANTHROPIC_API_KEY environment variável, ou other obrigatório keys for the providers you selected. You can do `export ANTHROPIC_API_KEY=YOUR_API_KEY`.

então, `cd` into the `evaluation` diretório e escrever `npx promptfoo@latest eval -c promptfooconfig.yaml --output ../data/results.csv`

Afterwards, you can view the results by running `npx promptfoo@latest view`.

### como it Works

The promptfooconfig.yaml arquivo is the heart of our evaluation Configuração. It defines several crucial sections:

Prompts:
- Prompts are imported de the prompts.py arquivo.
- estes prompts are designed para teste various aspects of LM desempenho.


Providers:
- We configurar different Claude versions e their configurações aqui.
- este allows us para teste across multiple models ou com varying parâmetros (e.g., different temperature configurações).


testes:
- teste cases are defined either in Este arquivo, ou in este case imported de testes.yaml.
- estes testes specify the inputs e expected outputs for our evaluations.
- Promptfoo offers various built-in teste types (see docs), ou you can define your own. We have 3 personalizado evaluations e 1 out of the box (contains método):
    - `bleu_eval.py`: Implements the BLEU (Bilingual Evaluation Understudy) score, qual measures the similarity entre machine-generated texto e reference texts.
    - `rouge_eval.py`: Implements the ROUGE (Recall-Oriented Understudy for Gisting Evaluation) score, qual assesses the quality of summarization by comparing it para reference summaries.
    - `llm_eval.py`: Contains personalizado evaluation métricas aquele leverage Language Models para assess various aspects of generated texto, such as coherence, relevance, ou factual accuracy.

saída:
- Specifies the format e location of evaluation results.
- Promptfoo supports various saída formats demais!

### Overriding the Python binary

By padrão, promptfoo will executar python in your shell. Certifique-se python points para the appropriate executable.

se a python binary is não present, you will see a "python: comando não found" erro.

para override the Python binary, set the PROMPTFOO_PYTHON environment variável. You may set it para a path (such as /path/para/python3.11) ou just an executable in your PATH (such as python3.11).