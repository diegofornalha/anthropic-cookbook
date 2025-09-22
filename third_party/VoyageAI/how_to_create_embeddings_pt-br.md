# Embeddings
texto embeddings are numerical representations of texto strings, represented as a vector of floating point numbers. We can use the distance entre two texto embeddings (popularly cosine similarity) para measure como related two pieces of texto are para one another, com smaller distances predicting higher relatedness.

Comparing the similarity of strings, ou clustering strings by their distance de one another, allows for a wide variety of applications including **buscar** (popular in RAG architectures), **recommendations**, e **anomaly detection**.

## como para get embeddings com Anthropic
While Anthropic does não offer its own embedding model, we have partnered com [Voyage AI](https://www.voyageai.com/?ref=anthropic) as our preferred provider for texto embeddings. Voyage makes [state of the art](https://blog.voyageai.com/2023/10/29/voyage-embeddings/?ref=anthropic) embedding models, e even offers models customized for specific industry domains such as finance e healthcare, e models aquele can be fine-tuned for your empresa.

para access Voyage embeddings, please primeiro sign up on [Voyage AI’s site](https://dash.voyageai.com/?ref=anthropic),  obtain an API key, e set the API key as an environment variável for convenience:

```bash
export VOYAGE_API_KEY="<your secret key>"
```

You can obtain the embeddings either using the official [`voyageai` Python pacote](https://github.com/voyage-ai/voyageai-python) ou HTTP requests, as described abaixo.

### Voyage Python pacote

The `voyageai` pacote can be installed using O seguinte comando:

```bash
pip install -U voyageai
```

então, you can criar a cliente object e iniciar using it para embed your texts:

```python
import voyageai

vo = voyageai.Client()
# This will automatically use the environment variable VOYAGE_API_KEY.
# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

texts = ["Sample text 1", "Sample text 2"]

result = vo.embed(texts, model="voyage-2", input_type="document")
print(result.embeddings[0])
print(result.embeddings[1])
```

`result.embeddings` will be a lista of two embedding vectors, each containing 1024 floating-point numbers. depois running the acima code, the two embeddings will be printed on the tela:

```
[0.02012746, 0.01957859, ...]  # embedding for "Sample text 1"
[0.01429677, 0.03077182, ...]  # embedding for "Sample text 2"
```

quando creating the embeddings, you may specify a poucos other argumentos para the `embed()` função. aqui is the specification:

> `voyageai.Client.embed(texts : List[str], model : str = "voyage-2", input_type : Optional[str] = None, truncation : Optional[bool] = None)`

- **texts** (lista[str]) - A lista of texts as a lista of strings, such as `["I like cats", "I also like dogs"]`. atualmente, the máximo comprimento of the lista is 128, e total número of tokens in the lista is at maioria 320K for `voyage-2` e 120K for `voyage-code-2`.
- **model** (str) - Name of the model. Recommended opções: `voyage-2` (padrão), `voyage-code-2`.
- **input_type** (str, opcional, defaults para `None`) - Type of the entrada texto. Defalut para `None`. Other opções:  `query`, `document`.
    - quando the input_type is set para `None`, e the entrada texto will be directly encoded by our embedding model. Alternatively, quando the inputs are documents ou queries, the usuários can specify input_type para be `query` ou `document`, respectively. In such cases, Voyage will prepend a special prompt para entrada texto e enviar the extended inputs para the embedding model.
    - For retrieval/buscar use cases, we recommend specifying este argumento quando encoding queries ou documents para aprimorar retrieval quality. Embeddings generated com e sem the input_type argumento are compatível.

- **truncation** (bool, opcional, defaults para `None`) - Whether para truncate the entrada texts para fit within the context comprimento.
    - se `True`, over-comprimento entrada texts will be truncated para fit within the context comprimento, antes vectorized by the embedding model.
    - se `False`, an erro will be raised se any given texto exceeds the context comprimento.
    - se não specified (defaults para `None`), Voyage will truncate the entrada texto antes sending it para the embedding model se it slightly exceeds the context janela comprimento. se it significantly exceeds the context janela comprimento, an erro will be raised.

### Voyage HTTP API

You can also get embeddings by requesting Voyage HTTP API. For example, you can enviar an HTTP requisição through the `curl` comando in a terminal:

```bash
curl https://api.voyageai.com/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VOYAGE_API_KEY" \
  -d '{
    "input": ["Sample text 1", "Sample text 2"],
    "model": "voyage-2"
  }'
```

The resposta you would get is a JSON object containing the embeddings e the token Uso:

```bash
{
  "object": "list",
  "data": [
    {
      "embedding": [0.02012746, 0.01957859, ...],
      "index": 0
    },
    {
      "embedding": [0.01429677, 0.03077182, ...],
      "index": 1
    }
  ],
  "model": "voyage-2",
  "usage": {
    "total_tokens": 10
  }
}
```

Voyage AI's embedding endpoint is `https://api.voyageai.com/v1/embeddings` (POST). The requisição header must contain the API key. The requisição body is a JSON object containing O seguinte argumentos:

- **entrada** (str, lista[str]) - A single texto string, ou a lista of texts as a lista of strings. atualmente, the máximo comprimento of the lista is 128, e total número of tokens in the lista is at maioria 320K for `voyage-2` e 120K for `voyage-code-2`.
- **model** (str) - Name of the model. Recommended opções: `voyage-2` (padrão), `voyage-code-2`.
- **input_type** (str, opcional, defaults para `None`) - Type of the entrada texto. Defalut para `None`. Other opções:  `query`, `document`.
- **truncation** (bool, opcional, defaults para `None`) - Whether para truncate the entrada texts para fit within the context comprimento.
    - se `True`, over-comprimento entrada texts will be truncated para fit within the context comprimento, antes vectorized by the embedding model.
    - se `False`, an erro will be raised se any given texto exceeds the context comprimento.
    - se não specified (defaults para `None`), Voyage will truncate the entrada texto antes sending it para the embedding model se it slightly exceeds the context janela comprimento. se it significantly exceeds the context janela comprimento, an erro will be raised.
- **encoding_format** (str, opcional, padrão para `None`) - Format in qual the embeddings are encoded. Voyage atualmente supports two opções:
    - se não specified (defaults para `None`): the embeddings are represented as lists of floating-point numbers;
    - `"base64"`: the embeddings are compressed para [Base64](https://docs.python.org/3/biblioteca/base64.html) encodings.


### AWS Marketplace

Voyage embeddings are available on [AWS Marketplace](https://aws.amazon.com/marketplace/seller-perfil?id=seller-snt4gb6fd7ljg). aqui is the instruction for accessing Voyage on AWS:

1. Subscribe para the model pacote

    1. Navigate para the [model pacote listing página](https://aws.amazon.com/marketplace/seller-perfil?id=seller-snt4gb6fd7ljg) e select the model para implantar.
    1. Click on the *Continue para subscribe* botão.
    1. On the *Subscribe para este software* página, please carefully review the details. se you e your organização agree com the standard End-usuário Licença Agreement (EULA), pricing, e support terms, click on "Accept Offer".
    1. depois selecting *Continue para Configuração* e choosing a region, you will be presented com a Product Arn. este is the model pacote ARN obrigatório for creating a deployable model using Boto3. copiar the ARN aquele corresponds para your selected region e use it in the subsequent cell.

2. implantar the model pacote

    de agora on, we recommend you para continue com our provided [notebook](https://github.com/voyage-ai/voyageai-aws/blob/principal/notebooks/deploy_voyage_code_2_sagemaker.ipynb) in [Sagemaker Studio](https://aws.amazon.com/sagemaker/studio/). Please criar a JupyterLab space, enviar our notebook, e continue de ali.


## Available Models

Voyage recommends using O seguinte embedding models:

|  Model | Context comprimento | Embedding Dimension | Description |
| --- | --- | --- | --- |
| `voyage-2` | 4000 | 1024 | mais recente base (generalist) embedding model com the best retrieval quality. See [blog post](https://blog.voyageai.com/2023/10/29/voyage-embeddings/?ref=anthropic) for details. |
| `voyage-code-2` | 16000 | 1536 | Optimized for code retrieval (17% better than alternatives), e also SoTA on general-purpose corpora. See [blog post](https://blog.voyageai.com/2024/01/23/voyage-code-2-elevate-your-code-retrieval/?ref=anthropic) for details. |

`voyage-2` is a generalist embedding model, qual achieves state-of-the-art desempenho across domains e retains high efficiency. `voyage-code-2` is optimized for code applications, offering 4x the context comprimento for mais flexível Uso, albeit at a slightly higher latency.

Voyage is actively developing mais avançado e specialized models, e can fine-tune embeddings for your empresa. Please email [contact@voyageai.com](mailto:contact@voyageai.com) for trial access ou finetuning on your own data!

- `voyage-finance-2`: coming em breve
- `voyage-law-2`: coming em breve
- `voyage-multilingual-2`: coming em breve
- `voyage-healthcare-2`: coming em breve

## Motivating Example
agora aquele we know como para get embeddings, let's see a brief motivating example.

Suppose we have a small corpus of six documents para retrieve de

```python
documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
    "Apple’s conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature."
]
```

We will primeiro use Voyage para convert each of them into an embedding vector

```python
import voyageai

vo = voyageai.Client()

# Embed the documents
doc_embds = vo.embed(
    documents, model="voyage-2", input_type="document"
).embeddings
```

The embeddings will allow us para do semantic buscar / retrieval in the vector space. Given an example query,

```python
query = "When is Apple's conference call scheduled?"
```

we convert it into an embedding, e conduct a nearest neighbor buscar para encontrar the maioria relevant document based on the distance in the embedding space.

```python
import numpy as np

# Embed the query
query_embd = vo.embed(
    [query], model="voyage-2", input_type="query"
).embeddings[0]

# Compute the similarity
# Voyage embeddings are normalized to length 1, therefore dot-product
# and cosine similarity are the same.
similarities = np.dot(doc_embds, query_embd)

retrieved_id = np.argmax(similarities)
print(documents[retrieved_id])
```

Nota aquele we use `input_type="document"` e `input_type="query"` for embedding the document e query, respectively. mais specification can be found [aqui](#voyage-python-pacote).

The saída would be the 5th document, qual is indeed the maioria relevant para the query:

```
Apple’s conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.
```

se you are looking for a detailed set of cookbooks on como para do RAG com embeddings, including vector databases, verificar out our [RAG cookbook](https://github.com/anthropics/anthropic-cookbook/blob/principal/third_party/Pinecone/rag_using_pinecone.ipynb).

## Frequently Asked Questions
### como do I calculate the distance entre two embedding vectors?
Cosine similarity is a popular choice, but maioria distance funções will do fine. Voyage embeddings are normalized para comprimento 1, therefore cosine similarity is essentially the same as the dot-product entre two vectors. aqui is a code snippet you can use for calculating cosine similarity entre two embedding vectors.

```python
import numpy

similarity = np.dot(embd1, embd2)
# Voyage embeddings are normalized to length 1, therefore cosine similarity
# is the same as dot-product.
```

se you want para encontrar the K nearest embedding vectors over a large corpus, we recommend using the capabilities built into maioria vector databases.

### Can I contagem the número of tokens in a string antes embedding it?
Yes! You can do so com O seguinte code.

```python
import voyageai

vo = voyageai.Client()
total_tokens = vo.count_tokens(["Sample text"])
```

## Pricing
Pricing information is available on the Voyage site's [pricing página](https://docs.voyageai.com/pricing/?ref=anthropic), e should be checked ali.
