
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
- We configurar qual Claude model(s) we're using aqui.

testes:
- teste cases are defined aqui.
- estes testes specify the inputs e expected outputs for our evaluations.
- Promptfoo offers various built-in teste types (see docs), ou you can define your own.

saída:
- Specifies the format e location of evaluation results.
- Promptfoo supports various saída formats demais!

### Overriding the Python binary

By padrão, promptfoo will executar python in your shell. Certifique-se python points para the appropriate executable.

se a python binary is não present, you will see a "python: comando não found" erro.

para override the Python binary, set the PROMPTFOO_PYTHON environment variável. You may set it para a path (such as /path/para/python3.11) ou just an executable in your PATH (such as python3.11).